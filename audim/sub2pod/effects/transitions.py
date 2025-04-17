"""
Transition effects for videos

This module provides transition effects that can be applied to frames during video
generation. Transitions are used for fade-in, fade-out, dissolve and other similar
effects between frames.
"""

import numpy as np
from PIL import Image


class BaseTransition:
    """Base class for all transition effects (internal use only)"""

    def __init__(self, frames=15):
        """
        Initialize the transition effect

        Args:
            frames (int): Number of frames for the transition
        """
        self.frames = frames

    def apply(self, frame, progress, **kwargs):
        """
        Apply the transition effect to a frame

        Args:
            frame: The frame to apply the effect to (PIL Image or numpy array)
            progress (float): Progress of the transition, from 0.0 to 1.0
            **kwargs: Additional arguments specific to the transition

        Returns:
            The modified frame with the transition effect applied
        """

        return frame


class Transition:
    """
    Transition effects for video frames

    This class provides various transition effects that can be applied to frames
    during video generation.

    Available effects:
    - "fade": Simple fade-in transition
    - "slide": Slide-in from the specified direction
    - "none": No transition effect
    """

    def __init__(self, effect_type="none", **kwargs):
        """
        Initialize a transition effect

        Args:
            effect_type (str): Type of transition effect
                "fade": Fade-in transition
                "slide": Slide-in transition
                "none": No transition (default)
            **kwargs: Additional parameters for the specific effect:
                frames (int): Number of frames for the transition
                direction (str): Direction for slide transition
                ("left", "right", "up", "down")
        """
        self.effect_type = effect_type.lower()
        self.frames = kwargs.get("frames", 15)
        self.direction = kwargs.get("direction", "left")

    def apply(self, frame, progress, **kwargs):
        """
        Apply the selected transition effect to a frame

        Args:
            frame: The frame to apply the effect to (PIL Image or numpy array)
            progress (float): Progress of the transition, from 0.0 to 1.0
            **kwargs: Additional arguments that may include:
                opacity_only (bool): If True, just return the opacity value
                (for fade effect)

        Returns:
            The modified frame with the transition effect applied
        """
        # Handle different effect types
        if self.effect_type == "fade":
            return self._apply_fade(frame, progress, **kwargs)
        elif self.effect_type == "slide":
            return self._apply_slide(frame, progress, **kwargs)
        elif self.effect_type == "none":
            return frame
        else:
            # Default to fade if unknown effect type
            return self._apply_fade(frame, progress, **kwargs)

    def _apply_fade(self, frame, progress, **kwargs):
        """
        Apply fade-in effect to a frame

        Args:
            frame: The frame to apply the effect to (PIL Image or numpy array)
            progress (float): Progress of the transition, from 0.0 to 1.0
            **kwargs: Additional arguments

        Returns:
            The modified frame with fade-in effect applied
        """
        opacity = int(progress * 255)

        # If caller just wants the opacity value, return it
        if kwargs.get("opacity_only", False):
            return opacity

        # Handle different frame types
        if isinstance(frame, np.ndarray):
            # For numpy arrays, apply opacity to alpha channel
            if frame.shape[2] == 4:  # Has alpha channel
                frame[:, :, 3] = np.minimum(frame[:, :, 3], opacity)
            return frame
        elif isinstance(frame, Image.Image):
            # For PIL images, use putalpha or convert as needed
            if frame.mode == "RGBA":
                # Get alpha channel, apply opacity, and put it back
                alpha = frame.split()[3]
                alpha = Image.eval(alpha, lambda a: min(a, opacity))
                frame.putalpha(alpha)
            elif frame.mode == "RGB":
                # Convert to RGBA and add alpha channel
                frame = frame.convert("RGBA")
                frame.putalpha(opacity)
            return frame

        # Unknown frame type, return unchanged
        return frame

    def _apply_slide(self, frame, progress, **kwargs):
        """
        Apply slide-in effect to a frame

        Args:
            frame: The frame to apply the effect to (PIL Image or numpy array)
            progress (float): Progress of the transition, from 0.0 to 1.0
            **kwargs: Additional arguments

        Returns:
            The modified frame with slide-in effect applied
        """
        # If caller just wants the opacity value (for backwards compatibility),
        # calculate it based on progress
        if kwargs.get("opacity_only", False):
            return int(progress * 255)

        # If no frame provided, just return the opacity
        if frame is None:
            return int(progress * 255)

        # Convert numpy array to PIL if needed
        if isinstance(frame, np.ndarray):
            frame = Image.fromarray(frame)

        # If not a PIL image, return unchanged
        if not isinstance(frame, Image.Image):
            return frame

        # Ensure we're working with an RGBA image
        if frame.mode != "RGBA":
            frame = frame.convert("RGBA")

        # Create a blank frame
        width, height = frame.size
        result = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        # Calculate offset based on direction and progress
        offset_x, offset_y = 0, 0
        if self.direction == "left":
            offset_x = int((1.0 - progress) * width)
        elif self.direction == "right":
            offset_x = int((progress - 1.0) * width)
        elif self.direction == "up":
            offset_y = int((1.0 - progress) * height)
        elif self.direction == "down":
            offset_y = int((progress - 1.0) * height)

        # Also apply a fade-in effect with the slide for smoother transition
        opacity = int(progress * 255)
        frame_copy = frame.copy()

        # Apply opacity to the frame
        if frame_copy.mode == "RGBA":
            alpha = frame_copy.split()[3]
            alpha = Image.eval(alpha, lambda a: min(a, opacity))
            frame_copy.putalpha(alpha)

        # Paste the frame at the offset position
        result.paste(frame_copy, (offset_x, offset_y), frame_copy)

        # Convert back to numpy array if input was numpy
        if isinstance(kwargs.get("original_frame"), np.ndarray):
            return np.array(result)

        return result
