import pysrt
from moviepy.editor import AudioFileClip, ImageSequenceClip


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

    def __init__(self, layout, fps=30):
        """
        Initialize the video generator

        Args:
            layout: Layout object that defines the visual arrangement
            fps (int): Frames per second for the output video
        """

        self.layout = layout
        self.fps = fps
        self.frames = []
        self.audio_path = None
        self.logo_path = None
        self.title = None

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

        # Create frames for each subtitle
        for sub in subs:
            start_frame = sub.start.ordinal // (1000 // self.fps)
            end_frame = sub.end.ordinal // (1000 // self.fps)

            # Add fade-in effect
            fade_frames = min(15, end_frame - start_frame)
            for i in range(fade_frames):
                opacity = int((i / fade_frames) * 255)
                self.frames.append(
                    self.layout.create_frame(current_sub=sub, opacity=opacity)
                )

            # Add main frames
            for _ in range(start_frame + fade_frames, end_frame):
                self.frames.append(self.layout.create_frame(current_sub=sub))

        return self

    def export_video(self, output_path):
        """
        Export the generated frames as a video

        Args:
            output_path (str): Path for the output video file
        """

        # Convert frames to video
        video = ImageSequenceClip(self.frames, fps=self.fps)

        # Add audio if provided
        if self.audio_path:
            audio = AudioFileClip(self.audio_path)
            video = video.set_audio(audio)

        # Export video
        video.write_videofile(output_path, codec="libx264", fps=self.fps)

        return output_path
