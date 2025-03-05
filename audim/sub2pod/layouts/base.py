from abc import ABC, abstractmethod

from PIL import Image, ImageDraw


class BaseLayout(ABC):
    """
    Base class for all layouts

    This class defines the base structure for all layout classes.
    It provides a common interface for adding speakers and creating frames and scenes.
    """

    def __init__(self, video_width=1920, video_height=1080):
        """
        Initialize the base layout

        Args:
            video_width (int): Width of the video
            video_height (int): Height of the video
        """

        self.video_width = video_width
        self.video_height = video_height

    @abstractmethod
    def add_speaker(self, name, image_path):
        """
        Add a speaker to the layout

        Args:
            name (str): Name of the speaker
            image_path (str): Path to the speaker's image
        """

        pass

    @abstractmethod
    def create_frame(self, current_sub=None, opacity=255):
        """
        Create a frame with the current subtitle

        Args:
            current_sub (str): Current subtitle
            opacity (int): Opacity of the subtitle
        """

        pass

    def _create_base_frame(self, background_color=(20, 20, 20)):
        """
        Create a base frame with the specified background color
        (mostly for internal use)

        Args:
            background_color (tuple): Background color in RGB format
        """

        frame = Image.new(
            "RGBA", (self.video_width, self.video_height), background_color + (255,)
        )
        draw = ImageDraw.Draw(frame)
        return frame, draw
