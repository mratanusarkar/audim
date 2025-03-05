from matplotlib import font_manager
from PIL import ImageFont


class TextRenderer:
    """
    Handles text rendering with various styles and wrapping

    This component is responsible for rendering text on the frame with various styles and wrapping.
    It can handle different fonts, sizes, colors, and anchor points.
    """

    def __init__(self):
        """
        Initialize the text renderer with default fonts
        """

        self.font_path = font_manager.findfont(
            font_manager.FontProperties(family=["sans"])
        )
        self.fonts = {}

    def get_font(self, size):
        """
        Get or create a font of the specified size

        Args:
            size (int): Size of the font
        """

        if size not in self.fonts:
            self.fonts[size] = ImageFont.truetype(self.font_path, size)
        return self.fonts[size]

    def draw_text(
        self,
        draw,
        text,
        position,
        font_size=40,
        color=(255, 255, 255, 255),
        anchor="mm",
    ):
        """
        Draw text at the specified position

        Args:
            draw (ImageDraw): Draw object to draw on the frame
            text (str): Text to draw
            position (tuple): Position of the text
            font_size (int): Size of the font, defaults to 40
            color (tuple): Color of the text, defaults to RGB (255, 255, 255, 255)
            anchor (str): Anchor of the text (from PIL library), defaults to "mm".
                          See [pillow docs: text anchors](https://pillow.readthedocs.io/en/latest/handbook/text-anchors.html)
                          for all possible options.
        """

        font = self.get_font(font_size)
        draw.text(position, text, fill=color, font=font, anchor=anchor)

    def draw_wrapped_text(
        self,
        draw,
        text,
        position,
        max_width,
        font_size=40,
        color=(255, 255, 255, 255),
        anchor="lm",
    ):
        """
        Draw text with word wrapping

        Args:
            draw (ImageDraw): Draw object to draw on the frame
            text (str): Text to draw
            position (tuple): Position of the text
            max_width (int): Maximum width of the text before wrapping
            font_size (int): Size of the font, defaults to 40
            color (tuple): Color of the text, defaults to RGB (255, 255, 255, 255)
            anchor (str): Anchor of the text (from PIL library), defaults to "lm".
                          See [pillow docs: text anchors](https://pillow.readthedocs.io/en/latest/handbook/text-anchors.html)
                          for all possible options.
        """

        font = self.get_font(font_size)

        # Get font metrics for dynamic calculations
        font_ascent, font_descent = font.getmetrics()
        line_height = font_ascent + font_descent
        line_spacing = line_height * 0.5  # 50% of line height for spacing
        total_line_height = line_height + line_spacing

        # Word wrap
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            w = draw.textlength(" ".join(current_line), font=font)
            if w > max_width:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))

        # Calculate vertical offset for multiple lines to maintain center alignment
        text_x, text_y = position
        total_text_height = len(lines) * total_line_height

        if anchor == "lm":
            text_start_y = text_y - (total_text_height // 2) + (line_height // 2)
        else:
            text_start_y = text_y

        # Draw each line
        for i, line in enumerate(lines):
            line_y = text_start_y + (i * total_line_height)
            draw.text((text_x, line_y), line, fill=color, font=font, anchor=anchor)
