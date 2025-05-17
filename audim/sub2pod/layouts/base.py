from abc import ABC, abstractmethod

from PIL import Image, ImageDraw

from audim.sub2pod.effects import Highlight, Transition
from audim.sub2pod.elements.watermark import Watermark


class BaseLayout(ABC):
    """
    Base class for all layouts

    This class defines the base structure for all layout classes.
    It provides a common interface for adding speakers and creating frames and scenes.
    """

    def __init__(self, video_width=1920, video_height=1080, content_horizontal_offset=0):
        """
        Initialize the base layout

        Args:
            video_width (int): Width of the video
            video_height (int): Height of the video
            content_horizontal_offset (int): Horizontal offset for the content
                (positive values move content right, negative values move content left).
                This allows shifting the main content (display pictures and subtitles)
                within the frame while keeping the header fixed.
        """

        self.video_width = video_width
        self.video_height = video_height
        self.content_horizontal_offset = content_horizontal_offset

        # Default transition effect
        self.transition_effect = Transition("fade")

        # No default highlight effect
        self.highlight_effect = None
        
        # Default watermark (enabled)
        self.watermark = Watermark()
        self.show_watermark = True

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
                direction (str): Direction for slide transition
                ("left", "right", "up", "down")
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

    def set_content_offset(self, offset):
        """
        Set horizontal offset for the main content area
        
        This method allows shifting the main content (display pictures and subtitles)
        horizontally within the frame while keeping the header fixed.
        Useful for adjusting the layout based on subtitle length.
        
        Args:
            offset (int): Horizontal offset in pixels.
            Positive values move content right, 
            negative values move content left.
        """

        self.content_horizontal_offset = offset
        return self

    def enable_watermark(self, show=True):
        """
        Enable or disable the watermark
        
        Args:
            show (bool): Whether to show the watermark
        """

        self.show_watermark = show
        if show and self.watermark is None:
            self.watermark = Watermark()
        return self

    def set_watermark_text(self, text):
        """
        Set the watermark text
        
        Args:
            text (str): Text to display as watermark
        """

        if self.watermark is None:
            self.watermark = Watermark(text=text)
        else:
            self.watermark.set_text(text)
        return self

    def set_watermark_position(self, position):
        """
        Set the watermark position
        
        Args:
            position (str): Position of the watermark
                'bottom-left', 'bottom-center', or 'bottom-right'
        """

        if self.watermark is None:
            self.watermark = Watermark(position=position)
        else:
            self.watermark.set_position(position)
        return self

    def set_watermark_color(self, color):
        """
        Set the watermark color
        
        Args:
            color (tuple): RGB color of the watermark text
        """

        if self.watermark is None:
            self.watermark = Watermark(color=color)
        else:
            self.watermark.set_color(color)
        return self

    def set_watermark_opacity(self, opacity):
        """
        Set the watermark opacity
        
        Args:
            opacity (int): Opacity of the watermark (0-255)
        """

        if self.watermark is None:
            self.watermark = Watermark(opacity=opacity)
        else:
            self.watermark.set_opacity(opacity)
        return self

    def set_watermark_properties(self, **kwargs):
        """
        Set multiple watermark properties at once
        
        Args:
            **kwargs: Keyword arguments for watermark properties:
                text (str): Watermark text
                position (str): Watermark position
                color (tuple): RGB color
                opacity (int): Opacity
                font_size (int): Font size
                margin (int): Margin from edges
        """

        if self.watermark is None:
            self.watermark = Watermark(**kwargs)
        else:
            if "text" in kwargs:
                self.watermark.set_text(kwargs["text"])
            if "position" in kwargs:
                self.watermark.set_position(kwargs["position"])
            if "color" in kwargs:
                self.watermark.set_color(kwargs["color"])
            if "opacity" in kwargs:
                self.watermark.set_opacity(kwargs["opacity"])
            if "font_size" in kwargs:
                self.watermark.set_font_size(kwargs["font_size"])
            if "margin" in kwargs:
                self.watermark.margin = kwargs["margin"]
        return self

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
