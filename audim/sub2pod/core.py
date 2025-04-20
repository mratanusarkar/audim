import concurrent.futures
import logging
import multiprocessing
import os
import shutil
import subprocess
import tempfile

import numpy as np
import pysrt
from PIL import Image
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s (%(levelname)s) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("VideoGenerator")


class VideoGenerator:
    """
    Core engine for generating videos from SRT files

    This class is responsible for generating video frames from an SRT or subtitle file.
    The subtitle file must follow our extended SRT format,
    which adds speaker identification:

    - Standard SRT format with sequential numbering, timestamps, and text content
    - Speaker identification in square brackets at the beginning of each subtitle text
      Example: "[Host] Welcome to our podcast!"

    Example of expected SRT format:
    ```srt
    1
    00:00:00,000 --> 00:00:04,500
    [Host] Welcome to our podcast!

    2
    00:00:04,600 --> 00:00:08,200
    [Guest] Thank you! Glad to be here.
    ```

    The speaker tag is used to visually distinguish different speakers in the
    generated video, and is mandatory for the core engine to work.

    It uses a layout object to define the visual arrangement of the video.
    """

    def __init__(self, layout, fps=30, batch_size=300):
        """
        Initialize the video generator

        Args:
            layout: Layout object that defines the visual arrangement
            fps (int): Frames per second for the output video
            batch_size (int): Number of frames to process in a batch
                              before writing to disk
        """

        self.layout = layout
        self.fps = fps
        self.batch_size = batch_size
        self.audio_path = None
        self.logo_path = None
        self.title = None
        self.temp_dir = None
        self.frame_files = []
        self.total_frames = 0

    def generate_from_srt(
        self,
        srt_path,
        audio_path=None,
        logo_path=None,
        title=None,
        cpu_core_utilization="most",
    ):
        """
        Generate video frames from an SRT file

        Args:
            srt_path (str): Path to the SRT file
            audio_path (str, optional): Path to the audio file
            logo_path (str, optional): Path to the logo image
            title (str, optional): Title for the video
            cpu_core_utilization (str, optional): `'single'`, `'half'`, `'most'`,
                `'max'`

                - `single`: Uses 1 CPU core
                - `half`: Uses half of available CPU cores
                - `most`: (default) Uses all available CPU cores except one
                - `max`: Uses all available CPU cores for maximum performance
        """

        # Store paths for later use
        self.audio_path = audio_path
        self.logo_path = logo_path
        self.title = title

        # Update layout with logo and title
        if hasattr(self.layout, "logo_path"):
            self.layout.logo_path = logo_path
        if hasattr(self.layout, "title"):
            self.layout.title = title

        # Load SRT file
        logger.info(f"Loading subtitles from {srt_path}")
        subs = pysrt.open(srt_path)
        
        # Determine if we need to normalize the timestamps
        # Find the minimum start time (ordinal) from all subtitles
        min_start_ordinal = min(sub.start.ordinal for sub in subs) if subs else 0
        logger.info(f"SRT starts at {min_start_ordinal} milliseconds")
        
        # Create temporary directory for frame storage
        self.temp_dir = tempfile.mkdtemp()
        self.frame_files = []
        self.total_frames = 0

        # Determine optimal number of workers
        if cpu_core_utilization == "single":
            num_workers = 1
        elif cpu_core_utilization == "half":
            num_workers = max(1, multiprocessing.cpu_count() // 2)
        elif cpu_core_utilization == "most":
            num_workers = max(1, multiprocessing.cpu_count() - 1)
        elif cpu_core_utilization == "max":
            num_workers = max(1, multiprocessing.cpu_count())
        else:
            raise ValueError(f"Invalid CPU core utilities: {cpu_core_utilization}")

        logger.info(f"Using {num_workers} CPU cores for parallel processing")

        # Process subtitles in parallel batches
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_workers
        ) as executor:
            # Prepare subtitle batches for parallel processing
            sub_batches = []
            current_batch = []
            current_batch_frames = 0

            for sub in subs:
                # Calculate the frame numbers normalized to start from frame 0
                # This ensures compatibility with SRTs that start at any timestamp
                start_frame = (sub.start.ordinal - min_start_ordinal) // (1000 // self.fps)
                end_frame = (sub.end.ordinal - min_start_ordinal) // (1000 // self.fps)
                
                num_frames = (end_frame - start_frame) + min(
                    15, end_frame - start_frame
                )  # Including fade frames

                if (
                    current_batch_frames + num_frames > self.batch_size
                    and current_batch
                ):
                    sub_batches.append((current_batch, min_start_ordinal))
                    current_batch = []
                    current_batch_frames = 0

                current_batch.append(sub)
                current_batch_frames += num_frames

            # Add the last batch if not empty
            if current_batch:
                sub_batches.append((current_batch, min_start_ordinal))

            logger.info(
                f"Processing subtitle to generate frames in {len(sub_batches)} batches"
            )

            # Process each batch in parallel
            batch_results = []
            for batch_idx, (batch, offset) in enumerate(sub_batches):
                batch_results.append(
                    executor.submit(
                        self._process_subtitle_batch,
                        batch,
                        batch_idx,
                        self.layout,
                        self.fps,
                        self.temp_dir,
                        offset,
                    )
                )

            # Collect results with progress bar
            with tqdm(
                total=len(batch_results), desc="Processing batch", unit="batch"
            ) as pbar:
                for future in concurrent.futures.as_completed(batch_results):
                    batch_frame_files, batch_frame_count = future.result()
                    self.frame_files.extend(batch_frame_files)
                    self.total_frames += batch_frame_count
                    pbar.update(1)
                    pbar.set_postfix({"frames processed": self.total_frames})

        # Sort frame files by frame number to ensure correct sequence
        self.frame_files.sort(
            key=lambda x: int(os.path.basename(x).split("_")[1].split(".")[0])
        )

        logger.info(
            f"Frame generation completed: Total {self.total_frames} frames created"
        )
        return self

    def _process_subtitle_batch(self, subs_batch, batch_index, layout, fps, temp_dir, time_offset=0):
        """
        Process a batch of subtitles in parallel

        Args:
            subs_batch (list): List of subtitles to process
            batch_index (int): Index of the current batch
            layout: Layout object to use for frame creation
            fps (int): Frames per second
            temp_dir (str): Directory to store temporary files
            time_offset (int): Time offset in milliseconds to normalize timestamps

        Returns:
            tuple: (list of frame files, number of frames processed)
        """

        # Create a batch directory
        batch_dir = os.path.join(temp_dir, f"batch_{batch_index}")
        os.makedirs(batch_dir, exist_ok=True)

        frame_files = []
        frame_count = 0

        # Process each subtitle in the batch
        for sub in subs_batch:
            # Normalize timestamps to start from time zero
            start_frame = (sub.start.ordinal - time_offset) // (1000 // fps)
            end_frame = (sub.end.ordinal - time_offset) // (1000 // fps)

            # Calculate subtitle duration (in seconds)
            subtitle_duration = (sub.end.ordinal - sub.start.ordinal) / 1000.0

            # Get transition frames count from layout's transition effect
            transition_frames = 15  # Default
            if hasattr(layout, "transition_effect") and layout.transition_effect:
                transition_frames = layout.transition_effect.frames

            # Add transition frames
            fade_frames = min(transition_frames, end_frame - start_frame)
            for i in range(fade_frames):
                # Calculate progress for transition effect
                progress = i / fade_frames
                # Convert progress to opacity for backward compatibility
                opacity = int(progress * 255)

                # Calculate subtitle position (in seconds)
                subtitle_position = i / fps

                # Create frame with transition effect passing position info as kwargs
                frame = layout.create_frame(
                    current_sub=sub,
                    opacity=opacity,
                    subtitle_position=subtitle_position,
                    subtitle_duration=subtitle_duration,
                )

                frame_path = os.path.join(batch_dir, f"frame_{start_frame + i:08d}.png")

                # Convert numpy array to PIL Image and save
                if isinstance(frame, np.ndarray):
                    Image.fromarray(frame).save(frame_path)
                else:
                    frame.save(frame_path)

                frame_files.append(frame_path)
                frame_count += 1

            # Add main frames
            for frame_idx in range(start_frame + fade_frames, end_frame):
                # Calculate subtitle position for current frame
                subtitle_position = (frame_idx - start_frame) / fps

                # Create frame passing position info as kwargs
                frame = layout.create_frame(
                    current_sub=sub,
                    subtitle_position=subtitle_position,
                    subtitle_duration=subtitle_duration,
                )

                frame_path = os.path.join(batch_dir, f"frame_{frame_idx:08d}.png")

                # Convert numpy array to PIL Image and save
                if isinstance(frame, np.ndarray):
                    Image.fromarray(frame).save(frame_path)
                else:
                    frame.save(frame_path)

                frame_files.append(frame_path)
                frame_count += 1

        return frame_files, frame_count

    def export_video(
        self,
        output_path,
        encoder="auto",
        video_codec=None,
        audio_codec=None,
        video_bitrate="8M",
        audio_bitrate="192k",
        preset="medium",
        crf=23,
        threads=None,
        gpu_acceleration=True,
        extra_ffmpeg_args=None,
    ):
        """
        Export the generated frames as a video

        Args:
            output_path (str): Path for the output video file
            encoder (str): Encoding method to use:
                `'ffmpeg'`, `'moviepy'`, or `'auto'` (default)
            video_codec (str, optional): Video codec to use
                (default: `'h264_nvenc'` for GPU, `'libx264'` for CPU)

                - See [FFmpeg H.264 Guide](https://trac.ffmpeg.org/wiki/Encode/H.264)
                  for CPU options
                - See [NVIDIA FFmpeg Guide](https://developer.nvidia.com/blog/nvidia-ffmpeg-transcoding-guide/)
                  for GPU options

            audio_codec (str, optional): Audio codec to use (default: `'aac'`)

                - See [FFmpeg AAC Guide](https://trac.ffmpeg.org/wiki/Encode/AAC)
                  for audio codec options

            video_bitrate (str, optional): Video bitrate (default: `'8M'`)
            audio_bitrate (str, optional): Audio bitrate (default: `'192k'`)
            preset (str, optional): Encoding preset (default: `'medium'`)
                
                For CPU encoding (libx264):
                    Options: `'ultrafast'`, `'superfast'`, `'veryfast'`, `'faster'`,
                             `'fast'`, `'medium'`, `'slow'`, `'slower'`, `'veryslow'`
                    Slower presets give better compression/quality at the cost of
                    encoding time.
                    
                - See [FFmpeg Preset Guide](https://trac.ffmpeg.org/wiki/Encode/H.264#a2.Chooseapresetandtune)

                For GPU encoding (NVENC):
                    Will be automatically converted to NVENC presets:
                    `'slow'`/`'slower'`/`'veryslow'` → `'p1'` (highest quality)
                    `'medium'` → `'p3'` (balanced)
                    `'fast'`/`'faster'` → `'p5'` (faster encoding)
                    `'veryfast'`/`'superfast'`/`'ultrafast'` → `'p7'` (fastest encoding)
                    
                - See [NVIDIA FFmpeg Integration](https://docs.nvidia.com/video-technologies/video-codec-sdk/12.0/ffmpeg-with-nvidia-gpu/index.html)

            crf (int, optional): Constant Rate Factor for quality
                (default: `23`, lower is better quality)

                - Range: `0-51`, where lower values mean better quality and larger
                  file size
                - Recommended range: `18-28`.
                - See [CRF Guide](https://trac.ffmpeg.org/wiki/Encode/H.264#crf)

            threads (int, optional): Number of encoding threads (default: CPU count - 1)
            gpu_acceleration (bool, optional): Whether to use GPU acceleration
                if available (default: `True`)
            extra_ffmpeg_args (list, optional): Additional FFmpeg arguments as a list

                - See [FFmpeg Documentation](https://ffmpeg.org/ffmpeg.html) for all
                  available options
        """

        logger.info(
            f"Starting video generation process with {self.total_frames} frames"
        )

        # Calculate video duration
        video_duration = self.total_frames / self.fps

        # Determine audio duration if provided
        audio_duration = None
        if self.audio_path:
            try:
                # Import locally since this is a heavier dependency
                from moviepy.editor import AudioFileClip

                audio = AudioFileClip(self.audio_path)
                audio_duration = audio.duration
                audio.close()
            except Exception as e:
                logger.warning(f"Could not determine audio duration: {e}")

        # Use the shorter duration to ensure sync
        final_duration = video_duration
        if audio_duration:
            final_duration = min(video_duration, audio_duration)
            logger.info(
                f"Video duration: {final_duration:.2f}s (adjusted to match audio)"
            )
        else:
            logger.info(f"Video duration: {final_duration:.2f}s")

        # Sort frames by number to ensure correct sequence
        self.frame_files.sort(
            key=lambda x: int(os.path.basename(x).split("_")[1].split(".")[0])
        )

        # Set default threads if not specified
        if threads is None:
            threads = max(4, os.cpu_count() - 1)

        # Determine which encoder to use
        if encoder == "auto":
            try:
                logger.info("Attempting video export with FFmpeg encoding")
                self._export_video_with_ffmpeg(
                    output_path,
                    final_duration,
                    video_codec,
                    audio_codec,
                    video_bitrate,
                    audio_bitrate,
                    preset,
                    crf,
                    threads,
                    gpu_acceleration,
                    extra_ffmpeg_args,
                )
            except Exception as e:
                logger.warning(f"FFmpeg export failed: {e}")
                logger.info("Falling back to MoviePy for video encoding")
                self._export_video_with_moviepy(
                    output_path,
                    final_duration,
                    video_codec,
                    audio_codec,
                    video_bitrate,
                    audio_bitrate,
                    preset,
                    threads,
                )
        elif encoder == "ffmpeg":
            logger.info("Starting video export using native FFmpeg")
            self._export_video_with_ffmpeg(
                output_path,
                final_duration,
                video_codec,
                audio_codec,
                video_bitrate,
                audio_bitrate,
                preset,
                crf,
                threads,
                gpu_acceleration,
                extra_ffmpeg_args,
            )
        elif encoder == "moviepy":
            logger.info("Starting video export using module MoviePy")
            self._export_video_with_moviepy(
                output_path,
                final_duration,
                video_codec,
                audio_codec,
                video_bitrate,
                audio_bitrate,
                preset,
                threads,
            )
        else:
            logger.error(
                f"Invalid encoder: {encoder}. Choose 'ffmpeg', 'moviepy', or 'auto'"
            )
            raise ValueError(
                f"Invalid encoder: {encoder}. Choose 'ffmpeg', 'moviepy', or 'auto'"
            )

        # Clean up temporary files
        try:
            shutil.rmtree(self.temp_dir)
            logger.info(f"Cleaned up temporary files in {self.temp_dir}")
        except Exception as e:
            logger.warning(f"Could not clean up temporary files: {e}")

        logger.info(f"Video generation completed! Exported to: {output_path}")
        return output_path

    def _export_video_with_ffmpeg(
        self,
        output_path,
        duration,
        video_codec=None,
        audio_codec=None,
        video_bitrate="8M",
        audio_bitrate="192k",
        preset="medium",
        crf=23,
        threads=None,
        gpu_acceleration=True,
        extra_args=None,
    ):
        """
        Export video using FFmpeg directly with potential GPU acceleration

        Args:
            output_path (str): Path for the output video file
            duration (float): Duration of the video in seconds
            video_codec (str, optional): Video codec to use
            audio_codec (str, optional): Audio codec to use
            video_bitrate (str, optional): Video bitrate
            audio_bitrate (str, optional): Audio bitrate
            preset (str, optional): Encoding preset
            crf (int, optional): Constant Rate Factor for quality
            threads (int, optional): Number of encoding threads
            gpu_acceleration (bool): Whether to use GPU acceleration
            extra_args (list, optional): Additional FFmpeg arguments
        """

        # Prepare output directory
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create a temporary file listing all frames with precise timing
        frames_list_file = os.path.join(self.temp_dir, "frames_list.txt")
        frame_duration = 1.0 / self.fps

        logger.info("Preparing frame list for FFmpeg")
        with open(frames_list_file, "w") as f:
            for i, frame_file in enumerate(self.frame_files):
                f.write(f"file '{frame_file}'\n")
                # Use exact frame duration to prevent drift
                f.write(f"duration {frame_duration}\n")

        # Check for NVIDIA GPU with NVENC support if GPU acceleration is requested
        has_nvidia = False
        if gpu_acceleration and (video_codec is None or video_codec == "h264_nvenc"):
            try:
                nvidia_check = subprocess.run(
                    ["nvidia-smi"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                has_nvidia = nvidia_check.returncode == 0
            except FileNotFoundError:
                pass

        # Set default threads if not specified
        if threads is None:
            threads = max(4, os.cpu_count() - 1)

        # Base FFmpeg command with improved sync options
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            frames_list_file,
            "-vsync",
            "cfr",  # Constant frame rate for better sync
            "-t",
            str(duration),
        ]

        # Add audio if provided
        if self.audio_path:
            ffmpeg_cmd.extend(
                [
                    "-i",
                    self.audio_path,
                    "-t",
                    str(duration),
                    "-map",
                    "0:v",
                    "-map",
                    "1:a",
                    "-async",
                    "1",  # Better audio sync
                ]
            )

        # Determine if we should use GPU encoding
        use_gpu = (
            has_nvidia
            and gpu_acceleration
            and (video_codec is None or video_codec == "h264_nvenc")
        )

        # Determine video codec and encoding settings
        if use_gpu:
            logger.info("Using NVIDIA GPU acceleration for video encoding")
            # Set default video codec for GPU
            video_codec = "h264_nvenc"

            # Convert x264 preset to NVENC preset
            nvenc_preset = "p3"  # Default balanced preset
            if preset in ["veryslow", "slower", "slow"]:
                nvenc_preset = "p1"  # Highest quality
            elif preset == "medium":
                nvenc_preset = "p3"  # Balanced
            elif preset in ["fast", "faster"]:
                nvenc_preset = "p5"  # Faster encoding
            elif preset in ["veryfast", "superfast", "ultrafast"]:
                nvenc_preset = "p7"  # Fastest encoding

            ffmpeg_cmd.extend(
                [
                    "-c:v",
                    video_codec,
                    "-preset",
                    nvenc_preset,
                    "-tune",
                    "hq",
                    "-rc",
                    "vbr",
                    "-b:v",
                    video_bitrate,
                    "-maxrate",
                    str(float(video_bitrate.rstrip("M")) * 1.25) + "M",
                ]
            )
        else:
            logger.info(f"Using CPU encoding with {threads} threads")
            # Set default video codec for CPU if not specified
            if video_codec is None:
                video_codec = "libx264"

            # For CPU encoding, use the x264 preset directly
            ffmpeg_cmd.extend(
                [
                    "-c:v",
                    video_codec,
                    "-preset",
                    preset,
                    "-crf",
                    str(crf),
                    "-threads",
                    str(threads),
                ]
            )

            # Add tune parameter only for libx264
            if video_codec == "libx264":
                ffmpeg_cmd.extend(["-tune", "film"])

        # Add audio encoding settings if audio is provided
        if self.audio_path:
            # Set default audio codec if not specified
            if audio_codec is None:
                audio_codec = "aac"

            ffmpeg_cmd.extend(["-c:a", audio_codec, "-b:a", audio_bitrate])

        # Add output format settings with improved sync options
        ffmpeg_cmd.extend(["-pix_fmt", "yuv420p", "-movflags", "+faststart"])

        # Add any extra arguments
        if extra_args:
            ffmpeg_cmd.extend(extra_args)

        # Add output path
        ffmpeg_cmd.append(output_path)

        # Run FFmpeg
        logger.info("Starting FFmpeg encoding process")
        logger.debug(f"FFmpeg command: {' '.join(ffmpeg_cmd)}")

        # Run FFmpeg with progress indication
        process = subprocess.Popen(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        # Simple progress indicator since FFmpeg output is complex
        with tqdm(total=100, desc="Encoding video", unit="%") as pbar:
            last_progress = 0
            for line in process.stdout:
                # Try to extract progress information from FFmpeg output
                if "time=" in line:
                    try:
                        time_str = line.split("time=")[1].split()[0]
                        h, m, s = time_str.split(":")
                        current_time = float(h) * 3600 + float(m) * 60 + float(s)
                        progress = min(int(current_time / duration * 100), 100)
                        if progress > last_progress:
                            pbar.update(progress - last_progress)
                            last_progress = progress
                    except Exception:
                        pass

        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, ffmpeg_cmd)

        logger.info(f"Video successfully encoded to {output_path}")

    def _export_video_with_moviepy(
        self,
        output_path,
        duration,
        video_codec=None,
        audio_codec=None,
        video_bitrate="8M",
        audio_bitrate="192k",
        preset="medium",
        threads=None,
    ):
        """
        Fallback method to export video using MoviePy

        Args:
            output_path (str): Path for the output video file
            duration (float): Duration of the video in seconds
            video_codec (str, optional): Video codec to use
            audio_codec (str, optional): Audio codec to use
            video_bitrate (str, optional): Video bitrate
            audio_bitrate (str, optional): Audio bitrate
            preset (str, optional): Encoding preset (x264 preset names)
            threads (int, optional): Number of encoding threads
        """

        # Import locally since this is a heavier dependency
        from moviepy.editor import ImageSequenceClip

        # Set default codecs if not specified
        if video_codec is None:
            video_codec = "libx264"
        if audio_codec is None:
            audio_codec = "aac"

        # Set default threads if not specified
        if threads is None:
            threads = max(4, os.cpu_count() - 1)

        logger.info("Loading frames for MoviePy")
        # Convert frames to video using the saved frame files
        video = ImageSequenceClip(self.frame_files, fps=self.fps)

        # Trim video to match duration
        video = video.subclip(0, duration)

        # Add audio if provided
        if self.audio_path:
            # Import locally since this is a heavier dependency
            from moviepy.editor import AudioFileClip

            logger.info(f"Adding audio from {self.audio_path}")
            audio = AudioFileClip(self.audio_path)
            audio = audio.subclip(0, duration)
            video = video.set_audio(audio)

        # Prepare ffmpeg parameters for MoviePy
        ffmpeg_params = ["-preset", preset]

        # Add bitrate parameter if specified
        if video_bitrate:
            ffmpeg_params.extend(["-b:v", video_bitrate])

        # Export video
        logger.info(f"Starting MoviePy encoding with {video_codec} codec")
        video.write_videofile(
            output_path,
            codec=video_codec,
            fps=self.fps,
            threads=threads,
            audio_codec=audio_codec,
            bitrate=video_bitrate,
            ffmpeg_params=ffmpeg_params,
            logger="bar",
        )
