"""
Highlight effects for videos

This module provides highlight effects that can be applied to text or other elements
during video generation. Highlights are used to emphasize important parts of the
content.
"""

import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


class BaseHighlight:
    """Base class for all highlight effects (internal use only)"""

    def __init__(self, color=(255, 255, 0, 128), padding=5):
        """
        Initialize the highlight effect

        Args:
            color (tuple): RGBA color for the highlight
                (default: semi-transparent yellow)
            padding (int): Padding around the highlighted area in pixels
        """
        self.color = color
        self.padding = padding

    def apply(self, frame, area, **kwargs):
        """
        Apply the highlight effect to a specific area of a frame

        Args:
            frame: The frame to apply the effect to (PIL Image or numpy array)
            area (tuple): The area to highlight as (x1, y1, x2, y2)
            **kwargs: Additional arguments specific to the highlight

        Returns:
            The modified frame with the highlight effect applied
        """

        return frame


class Highlight:
    """
    Highlight effects for video elements

    This class provides various highlight effects that can be applied to text
    or other elements during video generation.

    Available effects:
    - "pulse": Pulsing highlight that grows and shrinks
    - "glow": Glowing highlight with blur effect
    - "underline": Simple underline highlight
    - "box": Box around the highlighted area
    - "none": No highlight effect
    """

    def __init__(self, effect_type="none", **kwargs):
        """
        Initialize a highlight effect

        Args:
            effect_type (str): Type of highlight effect
                "pulse": Pulsing highlight
                "glow": Glowing highlight
                "underline": Underline highlight
                "box": Box highlight
                "none": No highlight (default)
            **kwargs: Additional parameters for the specific effect:
                color (tuple): RGBA color for the highlight
                padding (int): Padding around the highlighted area
                min_size (float): For pulse, minimum size factor (e.g., 0.8)
                max_size (float): For pulse, maximum size factor (e.g., 1.2)
                blur_radius (int): Blur radius for glow effect
                thickness (int): Line thickness for underline/box
        """
        self.effect_type = effect_type.lower()

        # Common parameters
        self.color = kwargs.get("color", (255, 255, 0, 128))  # Semi-transparent yellow
        self.padding = kwargs.get("padding", 5)

        # Pulse-specific parameters
        self.min_size = kwargs.get("min_size", 0.8)
        self.max_size = kwargs.get("max_size", 1.2)

        # Glow-specific parameters
        self.blur_radius = kwargs.get("blur_radius", 5)

        # Line-based effect parameters
        self.thickness = kwargs.get("thickness", 3)

    def apply(self, frame, area, progress=0.0, **kwargs):
        """
        Apply the selected highlight effect to a specific area

        Args:
            frame: The frame to apply the effect to (PIL Image or numpy array)
            area (tuple): Area to highlight as (x1, y1, x2, y2)
            progress (float): Animation progress from 0.0 to 1.0
            **kwargs: Additional arguments

        Returns:
            The modified frame with the highlight effect applied
        """
        # Convert numpy array to PIL if needed
        original_type = type(frame)
        if isinstance(frame, np.ndarray):
            frame = Image.fromarray(frame)

        # If not a PIL image, return unchanged
        if not isinstance(frame, Image.Image):
            return frame

        # Handle different effect types
        if self.effect_type == "pulse":
            result = self._apply_pulse(frame, area, progress)
        elif self.effect_type == "glow":
            result = self._apply_glow(frame, area, progress)
        elif self.effect_type == "underline":
            result = self._apply_underline(frame, area)
        elif self.effect_type == "box":
            result = self._apply_box(frame, area)
        elif self.effect_type == "none":
            result = frame
        else:
            # Default to pulse if unknown effect type
            result = self._apply_pulse(frame, area, progress)

        # Convert back to numpy array if input was numpy
        if original_type == np.ndarray:
            return np.array(result)

        return result

    def _apply_pulse(self, frame, area, progress):
        """Apply pulse highlight effect"""
        # Ensure we're working with an RGBA image
        if frame.mode != "RGBA":
            frame = frame.convert("RGBA")

        # Create a copy to avoid modifying the original
        result = frame.copy()
        overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Calculate pulse size
        # Use sine wave to create smooth oscillation between min and max size
        pulse_factor = self.min_size + (self.max_size - self.min_size) * (
            (math.sin(progress * 2 * math.pi) + 1) / 2
        )

        # Calculate expanded/contracted area
        x1, y1, x2, y2 = area
        center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
        width, height = x2 - x1, y2 - y1

        new_width = width * pulse_factor
        new_height = height * pulse_factor

        new_x1 = center_x - new_width / 2 - self.padding
        new_y1 = center_y - new_height / 2 - self.padding
        new_x2 = center_x + new_width / 2 + self.padding
        new_y2 = center_y + new_height / 2 + self.padding

        # Draw the highlight
        draw.rectangle((new_x1, new_y1, new_x2, new_y2), fill=self.color, outline=None)

        # Apply blur if requested
        if self.blur_radius > 0:
            overlay = overlay.filter(ImageFilter.GaussianBlur(self.blur_radius))

        # Composite the overlay with the original frame
        result = Image.alpha_composite(result, overlay)

        return result

    def _apply_glow(self, frame, area, progress):
        """Apply glow highlight effect"""
        # Ensure we're working with an RGBA image
        if frame.mode != "RGBA":
            frame = frame.convert("RGBA")

        # Create a copy to avoid modifying the original
        result = frame.copy()
        overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Animate the glow opacity if needed
        alpha = self.color[3]
        if progress is not None:
            # Make the glow pulse in opacity
            alpha = int(alpha * (0.6 + 0.4 * math.sin(progress * 2 * math.pi)))

        # Create the glow color with the animated alpha
        glow_color = (self.color[0], self.color[1], self.color[2], alpha)

        # Apply padding to the area
        x1, y1, x2, y2 = area
        x1 -= self.padding
        y1 -= self.padding
        x2 += self.padding
        y2 += self.padding

        # Draw the highlight
        draw.rectangle((x1, y1, x2, y2), fill=glow_color)

        # Apply blur
        overlay = overlay.filter(ImageFilter.GaussianBlur(self.blur_radius))

        # Composite the overlay with the original frame
        result = Image.alpha_composite(result, overlay)

        return result

    def _apply_underline(self, frame, area):
        """Apply underline highlight effect"""
        # Ensure we're working with an RGBA image
        if frame.mode != "RGBA":
            frame = frame.convert("RGBA")

        # Create a copy to avoid modifying the original
        result = frame.copy()
        overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Get the underline position (bottom of the area)
        x1, y1, x2, y2 = area

        # Draw the underline with specified thickness
        for i in range(self.thickness):
            draw.line((x1, y2 + i, x2, y2 + i), fill=self.color)

        # Composite the overlay with the original frame
        result = Image.alpha_composite(result, overlay)

        return result

    def _apply_box(self, frame, area):
        """Apply box highlight effect"""
        # Ensure we're working with an RGBA image
        if frame.mode != "RGBA":
            frame = frame.convert("RGBA")

        # Create a copy to avoid modifying the original
        result = frame.copy()
        overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Apply padding to the area
        x1, y1, x2, y2 = area
        x1 -= self.padding
        y1 -= self.padding
        x2 += self.padding
        y2 += self.padding

        # Draw the box
        draw.rectangle((x1, y1, x2, y2), outline=self.color, width=self.thickness)

        # Composite the overlay with the original frame
        result = Image.alpha_composite(result, overlay)

        return result
