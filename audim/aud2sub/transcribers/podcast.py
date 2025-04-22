import datetime
import gc
import os
import re
from typing import Optional
from pathlib import Path

import torch
import whisperx
from whisperx.SubtitlesProcessor import SubtitlesProcessor

from audim.aud2sub.transcribers.base import BaseTranscriber


def format_timestamp(seconds: float) -> str:
    """
    Convert seconds to SRT timestamp format (HH:MM:SS,mmm)
    """

    td = datetime.timedelta(seconds=seconds)
    ms = int((seconds - int(seconds)) * 1000)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"


class PodcastTranscriber(BaseTranscriber):
    """
    Podcast transcriber implementation using WhisperX.

    This class provides a complete implementation for podcast transcription,
    using WhisperX for ASR, diarization, and subtitle formatting.

    Args:
        model_name: WhisperX model name
            (tiny, base, small, medium, large, large-v2, large-v3)
        language: Language code (e.g., 'en', 'hi', 'bn') or None for auto-detection
        device: Device to run inference on (cpu, cuda, mps)
        compute_type: Compute type (float16, float32, int8)
        batch_size: Batch size for processing
        min_speakers: Minimum number of speakers
        max_speakers: Maximum number of speakers
        hf_token: HuggingFace token for accessing diarization models
            If not provided, will try to use HF_TOKEN environment variable
            or the token stored by huggingface-cli login
        max_line_length: Maximum length of subtitle lines
        min_char_length_splitter: Minimum characters before line splitting
        show_speaker_names: Whether to show speaker names in subtitles
        speaker_name_pattern: Pattern for formatting speaker names
        clear_gpu_memory: Whether to clear GPU memory after completing
            major processing steps
    """

    def __init__(
        self,
        model_name: str = "large-v2",
        language: Optional[str] = None,
        device: Optional[str] = None,
        compute_type: str = "float16",
        batch_size: int = 16,
        min_speakers: Optional[int] = 1,
        max_speakers: Optional[int] = 5,
        hf_token: Optional[str] = None,
        max_line_length: int = 70,
        min_char_length_splitter: int = 50,
        show_speaker_names: bool = True,
        speaker_name_pattern: str = "[{speaker}]",
        clear_gpu_memory: bool = False,
    ):
        # ASR Model parameters
        self.model_name = model_name
        self.language = language
        self.compute_type = compute_type
        self.batch_size = batch_size

        # Auto-detect device and correctly set to CPU if CUDA is not available
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        elif device == "cuda" and not torch.cuda.is_available():
            print("CUDA not available, using CPU instead.")
            device = "cpu"

        self.device = device

        # Adjust compute type based on device
        if self.device == "cpu" and self.compute_type == "float16":
            print("float16 not supported on CPU, using float32 instead.")
            self.compute_type = "float32"

        # Diarization parameters
        self.min_speakers = min_speakers
        self.max_speakers = max_speakers
        
        # HuggingFace token handling (following best practices)
        self.hf_token = self._resolve_huggingface_token(hf_token)

        # Formatting parameters
        self.max_line_length = max_line_length
        self.min_char_length_splitter = min_char_length_splitter
        self.show_speaker_names = show_speaker_names
        self.speaker_name_pattern = speaker_name_pattern

        # Memory management
        self.clear_gpu_memory = clear_gpu_memory

        # Results storage
        self._transcript_result = None
        self._diarize_segments = None
        self._segments_with_speakers = None
        self._processed_segments = None
        self._detected_language = None

    def _resolve_huggingface_token(self, provided_token: Optional[str] = None) -> Optional[str]:
        """
        Resolve HuggingFace token from various sources with priority:
        1. Directly provided token
        2. HF_TOKEN environment variable
        3. Token stored by huggingface-cli login

        Args:
            provided_token: Token directly provided to the method

        Returns:
            Resolved token or None if no token is found
        """
        # Priority 1: Directly provided token
        if provided_token:
            return provided_token
            
        # Priority 2: Environment variable
        env_token = os.environ.get("HF_TOKEN")
        if env_token:
            return env_token
            
        # Priority 3: Token stored by huggingface-cli login
        try:
            from huggingface_hub.constants import HF_TOKEN_PATH
            token_path = Path(HF_TOKEN_PATH)
            if token_path.exists():
                return token_path.read_text().strip()
        except (ImportError, Exception):
            # If huggingface_hub is not installed or any other error occurs
            pass
            
        return None

    def _clear_gpu_memory(self, message: str = None) -> None:
        """
        Clear GPU memory by collecting garbage and emptying CUDA cache.

        Args:
            message: Optional message to display when clearing memory
        """

        if not self.clear_gpu_memory or self.device != "cuda":
            return

        if message:
            print(f"Clearing GPU memory: {message}")

        gc.collect()
        torch.cuda.empty_cache()

    def process_audio(self, audio_path: str) -> None:
        """
        Process audio file to generate transcription with diarization.

        Args:
            audio_path: Path to the audio file.
        """

        print(f"Processing {audio_path}...")

        # 1. Load the audio file
        audio = whisperx.load_audio(audio_path)

        # 2. Load the ASR model (Whisper)
        print(f"Loading Whisper {self.model_name} model...")
        model = whisperx.load_model(
            self.model_name,
            device=self.device,
            compute_type=self.compute_type,
            language=self.language,
            download_root=None,
            local_files_only=False,
            asr_options={"beam_size": 5},
        )

        # 3. Transcribe audio with whisperX
        print("Transcribing audio...")
        result = model.transcribe(audio, batch_size=self.batch_size)

        self._detected_language = result["language"]
        print(f"Detected language: {self._detected_language}")

        # Clear GPU memory after transcription if requested
        self._clear_gpu_memory("after transcription")
        if self.clear_gpu_memory and self.device == "cuda":
            del model

        # 4. Align whisper output
        print("Aligning whisper output...")
        align_model, align_metadata = whisperx.load_align_model(
            language_code=self._detected_language, device=self.device
        )

        result = whisperx.align(
            result["segments"],
            align_model,
            align_metadata,
            audio,
            self.device,
            return_char_alignments=False,
        )

        self._transcript_result = result

        # Clear GPU memory after alignment if requested
        self._clear_gpu_memory("after alignment")
        if self.clear_gpu_memory and self.device == "cuda":
            del align_model

        # 5. Speaker diarization
        if self.hf_token:
            print("Running speaker diarization...")
            diarize_model = whisperx.DiarizationPipeline(
                model_name="pyannote/speaker-diarization-3.1",
                use_auth_token=self.hf_token,
                device=self.device,
            )

            self._diarize_segments = diarize_model(
                audio, min_speakers=self.min_speakers, max_speakers=self.max_speakers
            )

            # Assign speaker labels to segments
            print("Assigning speaker labels to segments...")
            result = whisperx.assign_word_speakers(
                self._diarize_segments, self._transcript_result
            )
            self._segments_with_speakers = result["segments"]

            # Clear GPU memory after diarization if requested
            self._clear_gpu_memory("after diarization")
            if self.clear_gpu_memory and self.device == "cuda":
                del diarize_model
        else:
            print("Warning: No HuggingFace token found. Skipping diarization.")
            print("To use diarization, provide a huggingface token by one of these methods:")
            print("  1. Pass directly: transcriber = PodcastTranscriber(hf_token='your_token')")
            print("  2. Set environment variable: export HF_TOKEN='your_token'")
            print("  3. Login with CLI using: huggingface-cli login")
            self._segments_with_speakers = self._transcript_result["segments"]
            for segment in self._segments_with_speakers:
                segment["speaker"] = "Speaker"

        # 6. Process subtitles with SubtitlesProcessor for line length control
        print("Processing subtitles for optimal line length...")
        subtitles_processor = SubtitlesProcessor(
            segments=self._segments_with_speakers,
            lang=self._detected_language,
            max_line_length=self.max_line_length,
            min_char_length_splitter=self.min_char_length_splitter,
        )

        self._processed_segments = subtitles_processor.process_segments(
            advanced_splitting=True
        )

        # Final memory cleanup
        self._clear_gpu_memory("final cleanup")

        print("Audio processing completed successfully.")

    def export_subtitle(self, output_path: str) -> None:
        """
        Export the processed transcription to an SRT subtitle file.

        Args:
            output_path: Path to the output SRT file.
        """

        if self._processed_segments is None:
            raise ValueError(
                "No processed audio available. Run `process_audio()` first."
            )

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        print(f"Saving SRT to {output_path}...")
        with open(output_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(self._processed_segments, 1):
                # Find the original segment that this processed segment came from
                # by finding which original segment contains this timestamp
                original_segment = next(
                    (
                        s
                        for s in self._segments_with_speakers
                        if s["start"] <= segment["start"]
                        and s["end"] >= segment["start"]
                    ),
                    {"speaker": "Speaker"},
                )

                speaker = original_segment.get("speaker", "Speaker")
                # Replace SPEAKER_0, SPEAKER_1, etc. with simple Speaker labels
                speaker_label = re.sub(
                    r"SPEAKER_\d+",
                    lambda m: f"Speaker {int(m.group(0).split('_')[1]) + 1}",
                    speaker,
                )

                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = segment["text"].strip()

                if self.show_speaker_names:
                    prefix = self.speaker_name_pattern.format(speaker=speaker_label)
                    text = f"{prefix} {text}"

                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

        print(f"Successfully created SRT file: {output_path}")

    def get_language(self) -> str:
        """
        Get the detected language.

        Returns:
            str: Detected language code
        """

        return self._detected_language

    def set_model(self, model_name: str) -> None:
        """
        Set the Whisper model name.

        Args:
            model_name: Whisper model name
        """

        self.model_name = model_name

    def set_language(self, language: str) -> None:
        """
        Set the language code.

        Args:
            language: Language code (e.g., 'en', 'hi', 'bn')
        """

        self.language = language

    def set_device(self, device: str) -> None:
        """
        Set the device for computation.

        Args:
            device: Device to run on (cpu, cuda, mps)
        """

        self.device = device
        if self.device == "cpu" and self.compute_type == "float16":
            print("float16 not supported on CPU, using float32 instead.")
            self.compute_type = "float32"

    def set_speakers(
        self, min_speakers: Optional[int] = None, max_speakers: Optional[int] = None
    ) -> None:
        """
        Set the number of speakers for diarization.

        Args:
            min_speakers: Minimum number of speakers
            max_speakers: Maximum number of speakers
        """

        self.min_speakers = min_speakers
        self.max_speakers = max_speakers

    def set_huggingface_token(self, hf_token: str) -> None:
        """
        Set the HuggingFace token for diarization.
        
        Note: It's recommended to use environment variables or the HuggingFace CLI
        login for better security rather than hardcoding tokens in your code.

        Args:
            hf_token: HuggingFace token
        """

        self.hf_token = hf_token

    def set_speaker_names_display(
        self, show_speaker_names: bool, pattern: Optional[str] = None
    ) -> None:
        """
        Configure how speaker names are displayed.

        Args:
            show_speaker_names: Whether to show speaker names
            pattern: Pattern for formatting speaker names (e.g., "[{speaker}]")
        """

        self.show_speaker_names = show_speaker_names
        if pattern is not None:
            self.speaker_name_pattern = pattern

    def set_line_properties(
        self, max_length: int = 70, min_split_length: int = 50
    ) -> None:
        """
        Configure subtitle line properties.

        Args:
            max_length: Maximum length of subtitle lines
            min_split_length: Minimum characters before considering a line split
        """

        self.max_line_length = max_length
        self.min_char_length_splitter = min_split_length

    def set_memory_management(self, clear_gpu_memory: bool) -> None:
        """
        Configure memory management.

        Args:
            clear_gpu_memory: Whether to clear GPU memory after major processing steps
        """

        self.clear_gpu_memory = clear_gpu_memory
