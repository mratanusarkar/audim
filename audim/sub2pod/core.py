import os
import tempfile
import pysrt
from moviepy.editor import AudioFileClip, ImageSequenceClip
import concurrent.futures
import multiprocessing


class VideoGenerator:
    """
    Core engine for generating videos from SRT files

    This class is responsible for generating video frames from an SRT or subtitle file.
    The subtitle file must follow our extended SRT format, which adds speaker identification:
    
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
    
    The speaker tag is used to visually distinguish different speakers in the generated video,\
    and is mandatory for the core engine to work.
    
    It uses a layout object to define the visual arrangement of the video.
    """

    def __init__(self, layout, fps=30, batch_size=300):
        """
        Initialize the video generator

        Args:
            layout: Layout object that defines the visual arrangement
            fps (int): Frames per second for the output video
            batch_size (int): Number of frames to process in a batch before writing to disk
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

    def generate_from_srt(self, srt_path, audio_path=None, logo_path=None, title=None, cpu_core_utilization="most"):
        """
        Generate video frames from an SRT file

        Args:
            srt_path (str): Path to the SRT file
            audio_path (str, optional): Path to the audio file
            logo_path (str, optional): Path to the logo image
            title (str, optional): Title for the video
            cpu_core_utilization (str, optional): `single`, `half`, `most`, `max`
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
        subs = pysrt.open(srt_path)

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
        
        print(f"Using {num_workers} workers for parallel processing")
        
        # Process subtitles in parallel batches
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            # Prepare subtitle batches for parallel processing
            sub_batches = []
            current_batch = []
            current_batch_frames = 0
            
            for sub in subs:
                start_frame = sub.start.ordinal // (1000 // self.fps)
                end_frame = sub.end.ordinal // (1000 // self.fps)
                num_frames = (end_frame - start_frame) + min(15, end_frame - start_frame)  # Including fade frames
                
                if current_batch_frames + num_frames > self.batch_size and current_batch:
                    sub_batches.append(current_batch)
                    current_batch = []
                    current_batch_frames = 0
                
                current_batch.append(sub)
                current_batch_frames += num_frames
            
            # Add the last batch if not empty
            if current_batch:
                sub_batches.append(current_batch)
            
            # Process each batch in parallel
            batch_results = []
            for batch_idx, batch in enumerate(sub_batches):
                batch_results.append(
                    executor.submit(
                        self._process_subtitle_batch, 
                        batch, 
                        batch_idx,
                        self.layout,
                        self.fps,
                        self.temp_dir
                    )
                )
            
            # Collect results
            for future in concurrent.futures.as_completed(batch_results):
                batch_frame_files, batch_frame_count = future.result()
                self.frame_files.extend(batch_frame_files)
                self.total_frames += batch_frame_count
                print(f"Processed {self.total_frames} frames so far...")
        
        # Sort frame files by frame number to ensure correct sequence
        self.frame_files.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))
        
        return self

    def _process_subtitle_batch(self, subs_batch, batch_index, layout, fps, temp_dir):
        """
        Process a batch of subtitles in parallel
        
        Args:
            subs_batch (list): List of subtitles to process
            batch_index (int): Index of the current batch
            layout: Layout object to use for frame creation
            fps (int): Frames per second
            temp_dir (str): Directory to store temporary files
            
        Returns:
            tuple: (list of frame files, number of frames processed)
        """
        import numpy as np
        from PIL import Image
        
        # Create a batch directory
        batch_dir = os.path.join(temp_dir, f"batch_{batch_index}")
        os.makedirs(batch_dir, exist_ok=True)
        
        frame_files = []
        frame_count = 0
        
        # Process each subtitle in the batch
        for sub in subs_batch:
            start_frame = sub.start.ordinal // (1000 // fps)
            end_frame = sub.end.ordinal // (1000 // fps)
            
            # Add fade-in effect
            fade_frames = min(15, end_frame - start_frame)
            for i in range(fade_frames):
                opacity = int((i / fade_frames) * 255)
                frame = layout.create_frame(current_sub=sub, opacity=opacity)
                
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
                frame = layout.create_frame(current_sub=sub)
                
                frame_path = os.path.join(batch_dir, f"frame_{frame_idx:08d}.png")
                
                # Convert numpy array to PIL Image and save
                if isinstance(frame, np.ndarray):
                    Image.fromarray(frame).save(frame_path)
                else:
                    frame.save(frame_path)
                    
                frame_files.append(frame_path)
                frame_count += 1
        
        return frame_files, frame_count

    def export_video(self, output_path):
        """
        Export the generated frames as a video

        Args:
            output_path (str): Path for the output video file
        """
        
        import shutil
        
        print(f"Creating video from {self.total_frames} frames...")
        
        # Convert frames to video using the saved frame files
        video = ImageSequenceClip(self.frame_files, fps=self.fps)

        # Add audio if provided
        if self.audio_path:
            audio = AudioFileClip(self.audio_path)
            
            # Ensure video and audio durations match
            video_duration = video.duration
            audio_duration = audio.duration
            
            # Use the shorter duration to ensure sync
            final_duration = min(video_duration, audio_duration)
            
            # Trim both video and audio to the same duration
            video = video.subclip(0, final_duration)
            audio = audio.subclip(0, final_duration)
            
            # Set audio to video
            video = video.set_audio(audio)
            
            print(f"Video duration: {final_duration:.2f} seconds (adjusted to match audio)")

        # Export video with higher quality settings
        video.write_videofile(
            output_path, 
            codec="libx264", 
            fps=self.fps, 
            threads=max(4, os.cpu_count() - 1),  # Use more threads for encoding
            audio_codec="aac",
            bitrate="8000k"  # Higher bitrate for better quality
        )

        # Clean up temporary files
        try:
            shutil.rmtree(self.temp_dir)
            print(f"Cleaned up temporary files in {self.temp_dir}")
        except Exception as e:
            print(f"Warning: Could not clean up temporary files: {e}")

        return output_path
