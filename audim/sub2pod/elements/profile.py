from PIL import Image, ImageDraw


class ProfilePicture:
    """
    Handles user profile pictures or display picture with various shapes and effects

    This component is responsible for displaying the profile picture of the speaker.
    It may also include various shapes and effects like circle, square, highlight, etc.
    """

    def __init__(self, image_path, size=(120, 120), shape="circle"):
        """
        Initialize a profile picture

        Args:
            image_path (str): Path to the profile image
            size (tuple): Width and height of the profile picture
            shape (str): Shape of the profile picture ("circle" or "square"),
            defaults to "circle"
        """

        self.image_path = image_path
        self.size = size
        self.shape = shape
        self.image = self._load_and_process_image()

    def _load_and_process_image(self):
        """
        Load and process the profile image based on shape
        (mostly for internal use)

        Returns:
            Image: Processed profile image
        """

        img = Image.open(self.image_path).convert("RGBA")
        img = img.resize(self.size)

        if self.shape == "circle":
            mask = self._create_circular_mask()
            img.putalpha(mask)
        elif self.shape == "square":
            mask = self._create_square_mask()
            img.putalpha(mask)

        return img

    def _create_circular_mask(self):
        """
        Create a circular mask for profile pictures
        (mostly for internal use)

        Returns:
            Image: Circular mask
        """

        mask = Image.new("L", self.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + self.size, fill=255)
        return mask

    def _create_square_mask(self):
        """
        Create a square mask for profile pictures
        (mostly for internal use)

        Returns:
            Image: Square mask
        """

        mask = Image.new("L", self.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle((0, 0) + self.size, fill=255)
        return mask

    def highlight(self, draw, position, color=(255, 200, 0), width=3, opacity=255):
        """
        Add highlight around the profile picture

        Args:
            draw (ImageDraw): Draw object to draw on the frame
            position (tuple): Position of the profile picture
        """

        highlight_color = color + (opacity,)

        if self.shape == "circle":
            draw.ellipse(
                [
                    position[0] - width,
                    position[1] - width,
                    position[0] + self.size[0] + width,
                    position[1] + self.size[1] + width,
                ],
                outline=highlight_color,
                width=width,
            )
        else:
            draw.rectangle(
                [
                    position[0] - width,
                    position[1] - width,
                    position[0] + self.size[0] + width,
                    position[1] + self.size[1] + width,
                ],
                outline=highlight_color,
                width=width,
            )
