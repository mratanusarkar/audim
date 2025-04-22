from abc import ABC, abstractmethod


class BaseTranscriber(ABC):
    """
    Base class for all transcriber implementations.

    This abstract class defines the interface that all transcriber implementations
    must follow. Each implementation should handle transcription, diarization,
    and formatting internally.
    """

    @abstractmethod
    def process_audio(self, audio_path: str) -> None:
        """
        Process an audio file to generate transcription.

        Args:
            audio_path: Path to the audio file.
        """
        pass

    @abstractmethod
    def export_subtitle(self, output_path: str) -> None:
        """
        Export the processed transcription to a subtitle file.

        Args:
            output_path: Path to the output subtitle file.
        """
        pass
