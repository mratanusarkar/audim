from abc import ABC, abstractmethod

from PIL import Image, ImageDraw
from audim.sub2pod.effects import Transition, Highlight


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
        # Default transition effect
        self.transition_effect = Transition("fade")
        # No default highlight effect
        self.highlight_effect = None

    def set_transition_effect(self, effect_type, **kwargs):
        """
        Set the transition effect for this layout
        
        Args:
            effect_type (str): Type of transition effect
                "fade": Fade-in transition (default)
                "slide": Slide-in transition
                "none": No transition
            **kwargs: Additional parameters for the effect
                frames (int): Number of frames for the transition
                direction (str): Direction for slide transition ("left", "right", "up", "down")
        """
        self.transition_effect = Transition(effect_type, **kwargs)
        
    def set_highlight_effect(self, effect_type, **kwargs):
        """
        Set the highlight effect for this layout
        
        Args:
            effect_type (str): Type of highlight effect
                "pulse": Pulsing highlight 
                "glow": Glowing highlight
                "underline": Underline highlight
                "box": Box highlight
                "none": No highlight
            **kwargs: Additional parameters for the effect
                color (tuple): RGBA color for the highlight
                padding (int): Padding around the highlighted area
                min_size (float): For pulse, minimum size factor (e.g., 0.8)
                max_size (float): For pulse, maximum size factor (e.g., 1.2)
                blur_radius (int): Blur radius for glow effect
            thickness (int): Line thickness for underline/box
        """
        self.highlight_effect = Highlight(effect_type, **kwargs)

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
