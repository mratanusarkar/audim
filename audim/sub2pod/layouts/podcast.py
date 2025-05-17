import numpy as np

from ..elements.header import Header
from ..elements.profile import ProfilePicture
from ..elements.text import TextRenderer
from ..elements.watermark import Watermark
from .base import BaseLayout


class PodcastLayout(BaseLayout):
    """
    Standard podcast layout with profile pictures and subtitles

    This layout is designed for standard podcast videos with a header section,
    profile pictures, and subtitles. It provides a flexible structure for adding
    speakers and creating frames with customizable parameters.
    """

    def __init__(
        self,
        video_width=1920,
        video_height=1080,
        header_height=150,
        dp_size=(120, 120),
        show_speaker_names=True,
        content_horizontal_offset=0,
        show_watermark=True,
    ):
        """
        Initialize podcast layout

        Args:
            video_width (int): Width of the video
            video_height (int): Height of the video
            header_height (int): Height of the header section
            dp_size (tuple): Size of profile pictures
            show_speaker_names (bool): Whether to show speaker names
            content_horizontal_offset (int): Horizontal offset for the content
                (positive values move content right,
                negative values move content left)
            show_watermark (bool): Whether to show the watermark
        """

        super().__init__(video_width, video_height)

        # Layout parameters
        self.header_height = header_height
        self.dp_size = dp_size
        self.show_speaker_names = show_speaker_names
        self.dp_margin_left = 40
        self.text_margin = 50
        self.name_margin = 30
        self.content_horizontal_offset = content_horizontal_offset

        # Initialize components
        self.header = Header(height=header_height)
        self.text_renderer = TextRenderer()
        
        # Initialize watermark
        self.show_watermark = show_watermark
        if show_watermark:
            # Opposite of background color (which is typically dark)
            self.watermark = Watermark(color=(255, 255, 255))

        # Store profile pictures and positions
        self.speakers = {}
        self.dp_positions = {}
        self.logo_path = None
        self.title = "My Podcast"

        # Store the active subtitle area for highlighting
        self.active_subtitle_area = None

    def set_content_offset(self, offset):
        """
        Set horizontal offset for the content (display pictures and subtitles)

        Args:
            offset (int): Horizontal offset in pixels.
                Positive values move content right, 
                negative values move content left.
        """
        self.content_horizontal_offset = offset
        # Recalculate positions with the new offset
        self._calculate_positions()
        return self

    def _calculate_positions(self):
        """
        Calculate positions for all speakers based on the number of speakers and
        the size of the profile pictures. (mostly for internal use)

        This method calculates the positions of all speakers based on the number of
        speakers and the size of the profile pictures. It also takes into account
        the spacing between the speakers and the header height.
        """

        num_speakers = len(self.speakers)
        spacing, start_y = self._calculate_layout(num_speakers)

        for i, speaker in enumerate(self.speakers.keys()):
            y_pos = start_y + (i * (self.dp_size[1] + spacing))
            x_pos = self.dp_margin_left + self.content_horizontal_offset
            self.dp_positions[speaker] = (x_pos, y_pos)

    def _calculate_layout(self, num_speakers, min_spacing=40):
        """
        Calculate dynamic spacing for speaker rows
        (mostly for internal use)

        This method calculates the spacing between the speakers based on the number of
        speakers and the size of the profile pictures. It also takes into account the
        spacing between the speakers and the header height.

        Args:
            num_speakers (int): Number of speakers
            min_spacing (int): Minimum spacing between the speakers, defaults to 40
        """

        available_height = self.video_height - self.header_height
        total_dp_height = num_speakers * self.dp_size[1]

        # Calculate spacing between DPs
        num_spaces = num_speakers + 1
        spacing = (available_height - total_dp_height) // num_spaces
        spacing = max(spacing, min_spacing)

        # Calculate starting Y position
        start_y = self.header_height + spacing

        return spacing, start_y

    def _draw_subtitle(self, frame, draw, subtitle, opacity, subtitle_info=None):
        """
        Draw the current subtitle with speaker highlighting
        (mostly for internal use)

        This method draws the current subtitle with speaker highlighting.
        It highlights the active speaker and draws the subtitle text.

        Args:
            frame (Image): Frame to draw on
            draw (ImageDraw): Draw object to draw on the frame
            subtitle (Subtitle): Current subtitle
            opacity (int): Opacity of the subtitle (0-255)
            subtitle_info (dict, optional): Dictionary with subtitle position
                and duration info

        Returns:
            Image: The frame with subtitle and highlight effect applied
        """

        speaker, text = subtitle.text.split("] ")
        speaker = speaker.replace("[", "").strip()

        # Ensure opacity is a valid integer
        opacity = max(0, min(255, int(opacity)))

        # Highlight active speaker
        if speaker in self.speakers:
            highlight_color = (255, 200, 0)
            speaker_pos = self.dp_positions[speaker]
            self.speakers[speaker].highlight(
                draw, speaker_pos, color=highlight_color, opacity=opacity
            )

            # Calculate text position
            text_x = self.dp_margin_left + self.dp_size[0] + self.text_margin + self.content_horizontal_offset
            text_y = speaker_pos[1] + (self.dp_size[1] // 2)
            
            # Adjust text width based on horizontal offset to ensure it stays within the frame
            # If offset is negative (moves content left), we have more space for text
            # If offset is positive (moves content right), we have less space for text
            if self.content_horizontal_offset > 0:
                # Reduce available text width when moved right
                text_width = self.video_width - text_x - self.text_margin
            else:
                # Increase available text width when moved left (but ensure it doesn't go off screen)
                text_width = min(
                    self.video_width - text_x - self.text_margin,
                    self.video_width - self.text_margin * 2
                )

            # Store text area for possible highlight effects
            estimated_text_height = 100  # Approximate height for highlighting
            self.active_subtitle_area = (
                text_x,
                text_y - estimated_text_height / 2,
                text_x + text_width,
                text_y + estimated_text_height / 2,
            )

            # Draw the subtitle text
            self.text_renderer.draw_wrapped_text(
                draw,
                text,
                (text_x, text_y),
                max_width=text_width,
                font_size=40,
                color=(255, 255, 255, opacity),
                anchor="lm",
            )

            # Apply highlight effect if configured
            if self.highlight_effect and self.active_subtitle_area:
                # Get progress value from subtitle_info or use a default
                progress = 0.0
                if (
                    subtitle_info
                    and "position" in subtitle_info
                    and "duration" in subtitle_info
                ):
                    # Calculate progress as a ratio of position to duration
                    progress = (
                        subtitle_info["position"] / subtitle_info["duration"]
                        if subtitle_info["duration"] > 0
                        else 0.0
                    )

                # Apply the highlight effect
                frame = self.highlight_effect.apply(
                    frame, self.active_subtitle_area, progress=progress
                )

        return frame

    def add_speaker(self, name, image_path, shape="circle"):
        """
        Add a speaker to the layout

        Args:
            name (str): Name of the speaker
            image_path (str): Path to the speaker's image
            shape (str): Shape of the profile picture, defaults to "circle"
        """

        self.speakers[name] = ProfilePicture(image_path, self.dp_size, shape)

        # Recalculate positions when speakers are added
        self._calculate_positions()

        return self

    def create_frame(
        self, current_sub=None, opacity=255, background_color=(20, 20, 20), **kwargs
    ):
        """
        Create a frame with the podcast layout

        Args:
            current_sub (str): Current subtitle
            opacity (int): Opacity of the subtitle
            background_color (tuple): Background color in RGB format,
                                      defaults to (20, 20, 20)
            **kwargs: Additional keyword arguments:
                subtitle_position (float): Current position within subtitle in seconds
                subtitle_duration (float): Total duration of subtitle in seconds
        """
        # Instead of modifying the subtitle object, we'll add the position and duration
        # to a local dictionary that we'll use in _draw_subtitle
        subtitle_info = {}
        if "subtitle_position" in kwargs:
            subtitle_info["position"] = kwargs["subtitle_position"]
        if "subtitle_duration" in kwargs:
            subtitle_info["duration"] = kwargs["subtitle_duration"]

        # Ensure the opacity is a valid integer
        opacity = max(0, min(255, int(opacity)))

        # If we have a transition effect and opacity is specified,
        # use the transition effect to calculate opacity
        if hasattr(self, "transition_effect") and opacity != 255:
            # Calculate progress from opacity
            progress = opacity / 255.0
            # Use transition effect to apply the transition
            if self.transition_effect:
                # We'll handle the opacity ourselves in this method,
                # so just get the calculated opacity from the effect
                opacity = self.transition_effect.apply(
                    None, progress, opacity_only=True
                )

        # Create base frame
        frame, draw = self._create_base_frame(background_color)

        # Draw header
        if self.logo_path:
            self.header.set_logo(self.logo_path)
        self.header.draw(frame, draw, self.video_width, self.title, opacity)

        # Add all speaker DPs and names
        for speaker, profile in self.speakers.items():
            pos = self.dp_positions[speaker]
            frame.paste(profile.image, pos, profile.image)

            # Draw speaker name if enabled
            if self.show_speaker_names:
                name_y = pos[1] + self.dp_size[1] + self.name_margin
                self.text_renderer.draw_text(
                    draw,
                    speaker,
                    (pos[0] + self.dp_size[0] // 2, name_y),
                    font_size=30,
                    color=(200, 200, 200, opacity),
                    anchor="mm",
                )

        # Add subtitle if there's a current subtitle
        if current_sub:
            # Pass the subtitle_info dictionary as an additional parameter
            frame = self._draw_subtitle(
                frame, draw, current_sub, opacity, subtitle_info
            )

        # Draw watermark if enabled
        if self.show_watermark and self.watermark:
            self.watermark.draw(
                frame, draw, self.video_width, self.video_height, opacity
            )

        # If we have a transition effect and opacity is not max,
        # apply the full transition effect to the frame
        if (
            hasattr(self, "transition_effect")
            and self.transition_effect
            and opacity != 255
        ):
            progress = opacity / 255.0
            frame = self.transition_effect.apply(frame, progress)

        return np.array(frame)
