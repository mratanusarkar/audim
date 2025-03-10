import concurrent.futures
import os
import tempfile
import multiprocessing

import pysrt
from moviepy.editor import AudioFileClip, ImageSequenceClip
from tqdm import tqdm


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

    def __init__(self, layout, fps=30, batch_size=300, max_workers=None):
        """
        Initialize the video generator

        Args:
            layout: Layout object that defines the visual arrangement
            fps (int): Frames per second for the output video
            batch_size (int): Number of frames to process in a batch before
                              writing to disk
            max_workers (int, optional): Maximum number of worker processes for
                                        parallel processing. Default is None
                                        (uses CPU count)
        """

        self.layout = layout
        self.fps = fps
        self.batch_size = batch_size
        # Default to using all available CPU cores if not specified
        self.max_workers = max_workers if max_workers is not None else multiprocessing.cpu_count()
        self.audio_path = None
        self.logo_path = None
        self.title = None
        self.temp_dir = None
        self.frame_files = []
        self.total_frames = 0

    def generate_from_srt(self, srt_path, audio_path=None, logo_path=None, title=None):
        """
        Generate video frames from an SRT file

        Args:
            srt_path (str): Path to the SRT file
            audio_path (str, optional): Path to the audio file
            logo_path (str, optional): Path to the logo image
            title (str, optional): Title for the video
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
        subs = pysrt.open(srt_path)

        # Create temporary directory for frame storage
        self.temp_dir = tempfile.mkdtemp()
        self.frame_files = []
        self.total_frames = 0

        # Create frames for each subtitle and organize them into batches
        frame_batches = []
        current_batch = []
        
        for sub in subs:
            start_frame = sub.start.ordinal // (1000 // self.fps)
            end_frame = sub.end.ordinal // (1000 // self.fps)

            # Add fade-in effect
            fade_frames = min(15, end_frame - start_frame)
            for i in range(fade_frames):
                opacity = int((i / fade_frames) * 255)
                current_batch.append(("fade", sub, opacity, self.total_frames))
                self.total_frames += 1
                
                # Create a new batch if the current one is full
                if len(current_batch) >= self.batch_size:
                    frame_batches.append(current_batch)
                    current_batch = []

            # Add main frames
            for _ in range(start_frame + fade_frames, end_frame):
                current_batch.append(("main", sub, 255, self.total_frames))
                self.total_frames += 1
                
                # Create a new batch if the current one is full
                if len(current_batch) >= self.batch_size:
                    frame_batches.append(current_batch)
                    current_batch = []
        
        # Add the last batch if it's not empty
        if current_batch:
            frame_batches.append(current_batch)
        
        # Create batch directories in advance
        batch_count = len(frame_batches)
        for i in range(batch_count):
            batch_dir = os.path.join(self.temp_dir, f"batch_{i}")
            os.makedirs(batch_dir, exist_ok=True)
        
        # Process batches sequentially, but frames within each batch in parallel
        print(f"Generating {self.total_frames} frames in {batch_count} batches using {self.max_workers} CPU cores...")
        
        for batch_index, batch in enumerate(frame_batches):
            print(f"Processing batch {batch_index+1}/{batch_count}...")
            batch_dir = os.path.join(self.temp_dir, f"batch_{batch_index}")
            
            # Process frames in this batch in parallel
            # Use ProcessPoolExecutor for CPU-bound tasks
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                # Create a list to store all futures
                futures = []
                
                # Submit all frame generation tasks for this batch
                for task_type, sub, opacity, frame_index in batch:
                    future = executor.submit(
                        self._generate_and_save_frame_task, 
                        task_type, 
                        sub, 
                        opacity, 
                        frame_index, 
                        batch_dir
                    )
                    futures.append((future, frame_index))
                
                # Process results as they complete
                for future, frame_index in tqdm(
                    futures,
                    total=len(futures),
                    desc=f"Batch {batch_index+1}/{batch_count}"
                ):
                    frame_path = os.path.join(batch_dir, f"frame_{frame_index:08d}.png")
                    
                    try:
                        # Wait for the future to complete
                        future.result()
                        self.frame_files.append(frame_path)
                    except Exception as e:
                        print(f"Error processing frame {frame_index}: {e}")
            
            # Force garbage collection after each batch
            import gc
            gc.collect()

        return self

    def _generate_and_save_frame_task(self, task_type, sub, opacity, frame_index, batch_dir):
        """
        Generate a single frame and save it to disk (for parallel processing)

        Args:
            task_type (str): Type of frame ('fade' or 'main')
            sub: Subtitle object
            opacity (int): Opacity value for the frame
            frame_index (int): Index of the frame
            batch_dir (str): Directory to save the frame

        Returns:
            str: Path to the saved frame
        """
        import numpy as np
        from PIL import Image
        
        # Generate the frame
        if task_type == "fade":
            frame = self.layout.create_frame(current_sub=sub, opacity=opacity)
        else:
            frame = self.layout.create_frame(current_sub=sub)
        
        # Save the frame
        frame_path = os.path.join(batch_dir, f"frame_{frame_index:08d}.png")
        
        # Convert numpy array to PIL Image and save
        if isinstance(frame, np.ndarray):
            Image.fromarray(frame).save(frame_path, optimize=True)
        else:
            frame.save(frame_path, optimize=True)
            
        return frame_path

    def export_video(self, output_path, preset="medium", encoder="auto"):
        """
        Export the generated frames as a video

        Args:
            output_path (str): Path for the output video file
            preset (str): Encoding preset for libx264:
                          `ultrafast`, `superfast`, `veryfast`, `faster`,
                          `fast`, `medium`, `slow`, `slower`, `veryslow`.
                          Slower presets provide better quality but
                          take longer to encode, and vice versa.
                          For more info see:
                          [FFmpeg H.264 Video Encoding Guide](https://trac.ffmpeg.org/wiki/Encode/H.264#a2.Chooseapresetandtune)
            encoder (str): Encoding method to use:
                          `auto`: Automatically choose the best available method
                          `ffmpeg`: Use FFmpeg directly (faster)
                          `moviepy`: Use MoviePy (more compatible)
        """
        import shutil
        import subprocess
        import os
        from pathlib import Path

        print(f"Creating video from {len(self.frame_files)} frames...")

        # Sort frame files by index to ensure correct order
        self.frame_files.sort()
        
        # Check if FFmpeg is available
        ffmpeg_available = False
        if encoder != "moviepy":  # Skip check if user explicitly wants moviepy
            try:
                # Check if FFmpeg is installed
                subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                ffmpeg_available = True
                print("FFmpeg found. Using FFmpeg for video encoding.")
            except (subprocess.SubprocessError, FileNotFoundError):
                if encoder == "ffmpeg":
                    raise RuntimeError("FFmpeg was explicitly requested but is not available in the system PATH.")
                print("FFmpeg not found in PATH. Falling back to moviepy for video encoding.")
        elif encoder == "moviepy":
            print("MoviePy encoder explicitly requested.")
        
        # Use FFmpeg if available and not explicitly overridden
        use_ffmpeg = ffmpeg_available and encoder != "moviepy"
        
        if use_ffmpeg:
            try:
                # Create a temporary directory for the FFmpeg input file
                ffmpeg_temp_dir = tempfile.mkdtemp()
                input_file_path = os.path.join(ffmpeg_temp_dir, "input.txt")
                
                # Create an FFmpeg input file listing all frames
                with open(input_file_path, 'w') as f:
                    for frame_file in self.frame_files:
                        f.write(f"file '{os.path.abspath(frame_file)}'\n")
                        f.write(f"duration {1/self.fps}\n")
                    # Write the last frame again with a small duration to avoid issues
                    f.write(f"file '{os.path.abspath(self.frame_files[-1])}'\n")
                    f.write(f"duration 0.001\n")
                
                # First create video without audio
                temp_video_path = os.path.join(ffmpeg_temp_dir, "temp_video.mp4")
                
                # Command to create video from frames
                video_cmd = [
                    "ffmpeg",
                    "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", input_file_path,
                    "-c:v", "libx264",
                    "-preset", preset,
                    "-crf", "23",
                    "-pix_fmt", "yuv420p",
                    "-r", str(self.fps),
                    "-threads", str(os.cpu_count()),
                    temp_video_path
                ]
                
                print(f"Creating video file using FFmpeg...")
                subprocess.run(video_cmd, check=True)
                
                # If audio is provided, add it in a separate step
                if self.audio_path and os.path.exists(self.audio_path):
                    audio_cmd = [
                        "ffmpeg",
                        "-y",
                        "-i", temp_video_path,
                        "-i", self.audio_path,
                        "-c:v", "copy",  # Copy video stream without re-encoding
                        "-c:a", "aac",
                        "-b:a", "192k",
                        "-shortest",
                        output_path
                    ]
                    
                    print(f"Adding audio to video...")
                    subprocess.run(audio_cmd, check=True)
                else:
                    # If no audio, just rename the temp video
                    shutil.move(temp_video_path, output_path)
                
                print(f"Video successfully created at {output_path}")
                
                # Clean up FFmpeg temp dir
                shutil.rmtree(ffmpeg_temp_dir)
                
            except Exception as e:
                print(f"Error during FFmpeg encoding: {e}")
                if encoder == "ffmpeg":
                    raise  # Re-raise if FFmpeg was explicitly requested
                print("Falling back to moviepy for video encoding...")
                use_ffmpeg = False
                
                # Clean up FFmpeg temp dir if it exists
                if 'ffmpeg_temp_dir' in locals():
                    try:
                        shutil.rmtree(ffmpeg_temp_dir)
                    except Exception:
                        pass
        
        # Use moviepy if FFmpeg is not available, failed, or explicitly requested
        if not use_ffmpeg:
            from moviepy.editor import ImageSequenceClip, AudioFileClip
            
            print("Using moviepy for video encoding (this may be slower)...")
            video = ImageSequenceClip(self.frame_files, fps=self.fps)
            if self.audio_path and os.path.exists(self.audio_path):
                audio = AudioFileClip(self.audio_path)
                video = video.set_audio(audio)
            
            video.write_videofile(
                output_path,
                codec="libx264",
                fps=self.fps,
                threads=os.cpu_count(),
                audio_codec="aac",
                preset=preset,
                bitrate="5000k",
                ffmpeg_params=["-pix_fmt", "yuv420p"],
            )
        
        # Clean up temporary files
        try:
            shutil.rmtree(self.temp_dir)
            print(f"Cleaned up temporary files in {self.temp_dir}")
        except Exception as e:
            print(f"Warning: Could not clean up temporary files: {e}")

        return output_path
