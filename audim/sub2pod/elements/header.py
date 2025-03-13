from PIL import Image

from .text import TextRenderer


class Header:
    """
    Header component for podcast layouts

    This component is responsible for displaying the header at the top of the
    podcast video frame. It may include various elements like logo, title,
    host profile, guest profile, etc.
    """

    def __init__(self, height=150, background_color=(30, 30, 30)):
        """
        Initialize the layout header

        Args:
            height (int): Height of the header, defaults to 150
            background_color (tuple): RGB background color, defaults to RGB (30, 30, 30)
            text_renderer (TextRenderer): optional text renderer for the header,
                                          defaults to a new instance
            logo (Image): optional logo image, defaults to None
            logo_size (tuple): optional size of the logo, defaults to (100, 100)
        """

        self.height = height
        self.background_color = background_color
        self.text_renderer = TextRenderer()
        self.logo = None
        self.logo_size = (100, 100)

    def set_logo(self, logo_path, size=(100, 100)):
        """
        Set the logo for the header

        Args:
            logo_path (str): Path to the logo image
            size (tuple): Size of the logo, defaults to (100, 100)
        """

        if logo_path:
            self.logo = Image.open(logo_path).convert("RGBA")
            self.logo_size = size
            self.logo = self.logo.resize(self.logo_size)
        return self

    def draw(self, frame, draw, width, title="My Podcast", opacity=255):
        """
        Draws the header on the frame

        Args:
            frame (Image): Frame to draw the header on
            draw (ImageDraw): Draw object to draw on the frame
            width (int): Width of the frame
            title (str): Title of the podcast
            opacity (int): Opacity of the header, defaults to 255
        """

        # Draw header background
        draw.rectangle([0, 0, width, self.height], fill=self.background_color + (255,))

        # Add logo if available
        if self.logo:
            frame.paste(
                self.logo,
                (
                    width - self.logo_size[0] - 50,
                    (self.height - self.logo_size[1]) // 2,
                ),
                self.logo,
            )

        # Add title
        self.text_renderer.draw_text(
            draw,
            title,
            (width // 2, self.height // 2),
            font_size=60,
            color=(255, 255, 255, opacity),
            anchor="mm",
        )
