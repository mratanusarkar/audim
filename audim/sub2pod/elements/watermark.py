from .text import TextRenderer


class Watermark:
    """
    Watermark component for video layouts
    
    This component is responsible for displaying a watermark text at the bottom
    of the video frame. It can be customized with different positions, colors,
    and opacity levels.
    """
    
    def __init__(
        self, 
        text="made with ❤️ by audim",
        position="bottom-right",
        color=(255, 255, 255),
        opacity=150,
        font_size=20,
        margin=10
    ):
        """
        Initialize the watermark
        
        Args:
            text (str): Text to display as watermark
            position (str): Position of the watermark
                            'bottom-left', 'bottom-center', or 'bottom-right'
            color (tuple): RGB color of the watermark text
            opacity (int): Opacity of the watermark (0-255)
            font_size (int): Font size of the watermark text
            margin (int): Margin from the edges in pixels
        """

        self.text = text
        self.position = position
        self.color = color
        self.opacity = opacity
        self.font_size = font_size
        self.margin = margin
        self.text_renderer = TextRenderer()
        
    def set_text(self, text):
        """
        Set the watermark text
        
        Args:
            text (str): Text to display as watermark
        """

        self.text = text
        return self
        
    def set_position(self, position):
        """
        Set the watermark position
        
        Args:
            position (str): Position of the watermark
                            'bottom-left', 'bottom-center', or 'bottom-right'
        """

        if position not in ["bottom-left", "bottom-center", "bottom-right"]:
            raise ValueError(
                "Position must be 'bottom-left', 'bottom-center', or 'bottom-right'"
            )
        self.position = position
        return self
        
    def set_color(self, color):
        """
        Set the watermark color
        
        Args:
            color (tuple): RGB color of the watermark text
        """

        self.color = color
        return self
        
    def set_opacity(self, opacity):
        """
        Set the watermark opacity
        
        Args:
            opacity (int): Opacity of the watermark (0-255)
        """

        self.opacity = max(0, min(255, opacity))
        return self
        
    def set_font_size(self, font_size):
        """
        Set the watermark font size
        
        Args:
            font_size (int): Font size of the watermark text
        """

        self.font_size = font_size
        return self
        
    def draw(self, frame, draw, width, height, frame_opacity=255):
        """
        Draw the watermark on the frame
        
        Args:
            frame: Frame to draw the watermark on
            draw: Draw object to draw on the frame
            width (int): Width of the frame
            height (int): Height of the frame
            frame_opacity (int): Opacity of the entire frame (for transitions)
        """

        # Ensure opacity values are valid integers
        watermark_opacity = max(0, min(255, self.opacity))
        frame_opacity = max(0, min(255, frame_opacity))
        
        # Calculate final opacity (product of watermark opacity and frame opacity)
        # Use a proportion to maintain proper alpha blending
        final_opacity = int((watermark_opacity / 255.0) * (frame_opacity / 255.0) * 255)
        
        # Create the color tuple with the final opacity
        if isinstance(self.color, tuple) and len(self.color) >= 3:
            color_with_opacity = self.color[:3] + (final_opacity,)
        else:
            color_with_opacity = (255, 255, 255, final_opacity)
        
        # Calculate position based on the selected position
        # for anchor keys, see: https://pillow.readthedocs.io/en/latest/handbook/text-anchors.html
        if self.position == "bottom-left":
            position = (self.margin, height - self.margin)
            anchor = "ls"
        elif self.position == "bottom-center":
            position = (width // 2, height - self.margin)
            anchor = "ms"
        else:
            position = (width - self.margin, height - self.margin)
            anchor = "rs"
            
        # Draw the watermark text
        self.text_renderer.draw_text(
            draw,
            self.text,
            position,
            font_size=self.font_size,
            color=color_with_opacity,
            anchor=anchor,
        )
