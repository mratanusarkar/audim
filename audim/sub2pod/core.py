import os
import tempfile

import pysrt
from moviepy.editor import AudioFileClip, ImageSequenceClip


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
            batch_size (int): Number of frames to process in a batch before
                              writing to disk
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

        # Process frames in batches
        current_batch = []
        batch_count = 0

        # Create frames for each subtitle
        for sub in subs:
            start_frame = sub.start.ordinal // (1000 // self.fps)
            end_frame = sub.end.ordinal // (1000 // self.fps)

            # Add fade-in effect
            fade_frames = min(15, end_frame - start_frame)
            for i in range(fade_frames):
                opacity = int((i / fade_frames) * 255)
                frame = self.layout.create_frame(current_sub=sub, opacity=opacity)
                current_batch.append(frame)

                # Write batch to disk if it reaches the batch size
                if len(current_batch) >= self.batch_size:
                    self._write_batch_to_disk(current_batch, batch_count)
                    current_batch = []
                    batch_count += 1

            # Add main frames
            for _ in range(start_frame + fade_frames, end_frame):
                frame = self.layout.create_frame(current_sub=sub)
                current_batch.append(frame)

                # Write batch to disk if it reaches the batch size
                if len(current_batch) >= self.batch_size:
                    self._write_batch_to_disk(current_batch, batch_count)
                    current_batch = []
                    batch_count += 1

        # Write any remaining frames
        if current_batch:
            self._write_batch_to_disk(current_batch, batch_count)

        return self

    def _write_batch_to_disk(self, frames, batch_index):
        """
        Write a batch of frames to disk as a temporary file

        Args:
            frames (list): List of frames to write
            batch_index (int): Index of the current batch
        """

        import numpy as np
        from PIL import Image

        # Create a batch directory
        batch_dir = os.path.join(self.temp_dir, f"batch_{batch_index}")
        os.makedirs(batch_dir, exist_ok=True)

        # Write each frame to disk
        for i, frame in enumerate(frames):
            frame_index = self.total_frames + i
            frame_path = os.path.join(batch_dir, f"frame_{frame_index:08d}.png")

            # Convert numpy array to PIL Image and save
            if isinstance(frame, np.ndarray):
                Image.fromarray(frame).save(frame_path)
            else:
                frame.save(frame_path)

            self.frame_files.append(frame_path)

        self.total_frames += len(frames)
        print(f"Processed {self.total_frames} frames so far...")

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
            video = video.set_audio(audio)

        # Export video
        video.write_videofile(
            output_path, codec="libx264", fps=self.fps, threads=4, audio_codec="aac"
        )

        # Clean up temporary files
        try:
            shutil.rmtree(self.temp_dir)
            print(f"Cleaned up temporary files in {self.temp_dir}")
        except Exception as e:
            print(f"Warning: Could not clean up temporary files: {e}")

        return output_path
