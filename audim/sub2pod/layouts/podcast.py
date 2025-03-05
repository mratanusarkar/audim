import numpy as np

from ..elements.header import Header
from ..elements.profile import ProfilePicture
from ..elements.text import TextRenderer
from .base import BaseLayout


class PodcastLayout(BaseLayout):
    """Standard podcast layout with profile pictures and subtitles"""

    def __init__(
        self,
        video_width=1920,
        video_height=1080,
        header_height=150,
        dp_size=(120, 120),
        show_speaker_names=True,
    ):
        """
        Initialize podcast layout

        Args:
            video_width (int): Width of the video
            video_height (int): Height of the video
            header_height (int): Height of the header section
            dp_size (tuple): Size of profile pictures
            show_speaker_names (bool): Whether to show speaker names
        """
        super().__init__(video_width, video_height)
        self.header_height = header_height
        self.dp_size = dp_size
        self.show_speaker_names = show_speaker_names

        # Layout parameters
        self.dp_margin_left = 40
        self.text_margin = 50
        self.name_margin = 30

        # Initialize components
        self.header = Header(height=header_height)
        self.text_renderer = TextRenderer()

        # Store profile pictures and positions
        self.speakers = {}
        self.dp_positions = {}
        self.logo_path = None
        self.title = "My Podcast"

    def add_speaker(self, name, image_path, shape="circle"):
        """Add a speaker to the layout"""
        self.speakers[name] = ProfilePicture(image_path, self.dp_size, shape)

        # Recalculate positions when speakers are added
        self._calculate_positions()

        return self

    def _calculate_positions(self):
        """Calculate positions for all speakers"""
        num_speakers = len(self.speakers)
        spacing, start_y = self._calculate_layout(num_speakers)

        for i, speaker in enumerate(self.speakers.keys()):
            y_pos = start_y + (i * (self.dp_size[1] + spacing))
            self.dp_positions[speaker] = (self.dp_margin_left, y_pos)

    def _calculate_layout(self, num_speakers, min_spacing=40):
        """Calculate dynamic spacing for speaker rows"""
        available_height = self.video_height - self.header_height
        total_dp_height = num_speakers * self.dp_size[1]

        # Calculate spacing between DPs
        num_spaces = num_speakers + 1
        spacing = (available_height - total_dp_height) // num_spaces
        spacing = max(spacing, min_spacing)

        # Calculate starting Y position
        start_y = self.header_height + spacing

        return spacing, start_y

    def create_frame(
        self, current_sub=None, opacity=255, background_color=(20, 20, 20)
    ):
        """Create a frame with the podcast layout"""
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
            self._draw_subtitle(frame, draw, current_sub, opacity)

        return np.array(frame)

    def _draw_subtitle(self, frame, draw, subtitle, opacity):
        """Draw the current subtitle with speaker highlighting"""
        speaker, text = subtitle.text.split("] ")
        speaker = speaker.replace("[", "").strip()

        # Highlight active speaker
        if speaker in self.speakers:
            highlight_color = (255, 200, 0)
            speaker_pos = self.dp_positions[speaker]
            self.speakers[speaker].highlight(
                draw, speaker_pos, color=highlight_color, opacity=opacity
            )

            # Calculate text position
            text_x = self.dp_margin_left + self.dp_size[0] + self.text_margin
            text_y = speaker_pos[1] + (self.dp_size[1] // 2)
            text_width = self.video_width - text_x - self.text_margin

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
