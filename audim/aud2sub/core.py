import os

from audim.aud2sub.transcribers.base import BaseTranscriber


class SubtitleGenerator:
    """
    High-level generator for creating subtitles from audio.

    This class provides a simple interface for generating subtitles from audio files
    using a configured transcriber.

    Args:
        transcriber: Configured transcriber to use for processing audio
    """

    def __init__(self, transcriber: BaseTranscriber):
        self.transcriber = transcriber
        self._processed = False

    def generate_from_mp3(self, mp3_path: str) -> None:
        """
        Generate subtitles from an MP3 file.

        This method processes the audio file and prepares subtitles for export.

        Args:
            mp3_path: Path to the MP3 file
        """

        self._process_audio_file(mp3_path)

    def generate_from_wav(self, wav_path: str) -> None:
        """
        Generate subtitles from a WAV file.

        This method processes the audio file and prepares subtitles for export.

        Args:
            wav_path: Path to the WAV file
        """

        self._process_audio_file(wav_path)

    def generate_from_audio(self, audio_path: str) -> None:
        """
        Generate subtitles from any supported audio file.

        This method processes the audio file and prepares subtitles for export.

        Args:
            audio_path: Path to the audio file
        """

        self._process_audio_file(audio_path)

    def _process_audio_file(self, audio_path: str) -> None:
        """
        Process an audio file using the configured transcriber.

        Args:
            audio_path: Path to the audio file
        """

        # Process the audio file
        self.transcriber.process_audio(audio_path)
        self._processed = True

    def export_subtitle(self, output_path: str) -> None:
        """
        Export the generated subtitles to a file.

        Args:
            output_path: Path to the output subtitle file
        """

        if not self._processed:
            raise ValueError(
                "No processed audio available. Run `generate_from_*()` methods first."
            )

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Export the subtitle file
        self.transcriber.export_subtitle(output_path)
