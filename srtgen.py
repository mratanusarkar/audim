#!/usr/bin/env python3

import os
import whisperx
from whisperx.SubtitlesProcessor import SubtitlesProcessor
import torch
import datetime
from typing import List, Dict, Any, Tuple, Optional
import re


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    td = datetime.timedelta(seconds=seconds)
    ms = int((seconds - int(seconds)) * 1000)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"

def process_audio(
    audio_file: str,
    output_file: str = None,
    model_name: str = "large-v2",
    language: str = None,
    device: str = "cpu",
    min_speakers: int = None,
    max_speakers: int = None,
    hf_token: str = None,
    batch_size: int = 16,
    compute_type: str = "float16"
) -> None:
    """
    Process audio file using WhisperX and create SRT with speaker diarization.
    
    Args:
        audio_file: Path to the audio file
        output_file: Path to the output SRT file (default: input filename with .srt extension)
        model_name: Whisper model name (tiny, base, small, medium, large, large-v2, large-v3)
        language: Language code (e.g., 'en', 'hi', 'bn', or None for auto-detection)
        device: Device to run inference on ('cpu', 'cuda', 'mps')
        min_speakers: Minimum number of speakers (optional)
        max_speakers: Maximum number of speakers (optional)
        hf_token: HuggingFace token for accessing models (needed for diarization)
        batch_size: Batch size for processing
        compute_type: Compute type (float16, float32, int8)
    """
    print(f"Processing {audio_file}...")
    
    # Set device
    if device == "cuda" and not torch.cuda.is_available():
        print("CUDA not available, using CPU instead.")
        device = "cpu"
    
    # Default output file if not specified
    if not output_file:
        output_file = os.path.splitext(audio_file)[0] + ".srt"
    
    try:
        # 1. Load model
        print(f"Loading Whisper {model_name} model...")
        model = whisperx.load_model(
            model_name, 
            device=device, 
            compute_type=compute_type,
            language=language,
            download_root=None,
            local_files_only=False,
            asr_options={ "beam_size": 5 }
        )

        # 2. Load audio
        print(f"Loading audio from {audio_file}...")
        audio = whisperx.load_audio(audio_file)
        
        # 3. Transcribe with whisper
        print("Transcribing audio...")
        result = model.transcribe(
            audio,
            batch_size=batch_size
        )
        
        detected_language = result["language"]
        print(f"Detected language: {detected_language}")

        # delete model if low on GPU resources
        # import gc; gc.collect(); torch.cuda.empty_cache(); del model
        
        # 4. Align whisper output
        print("Aligning whisper output...")
        model_a, metadata = whisperx.load_align_model(
            language_code=detected_language, 
            device=device
        )
        
        result = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            device,
            return_char_alignments=False
        )

        # delete model if low on GPU resources
        # import gc; gc.collect(); torch.cuda.empty_cache(); del model_a
        
        # 5. Speaker diarization
        if hf_token:
            print("Running speaker diarization...")
            diarize_model = whisperx.DiarizationPipeline(
                model_name="pyannote/speaker-diarization-3.1",
                use_auth_token=hf_token,
                device=device
            )
            
            diarize_segments = diarize_model(
                audio,
                min_speakers=min_speakers,
                max_speakers=max_speakers
            )
            
            # Assign speaker labels to segments
            result = whisperx.assign_word_speakers(diarize_segments, result)
        else:
            print("Warning: No HuggingFace token provided. Skipping diarization.")
            for segment in result["segments"]:
                segment["speaker"] = "Speaker"
        
        # 6. Process subtitles with SubtitlesProcessor for line length control
        print("Processing subtitles for optimal line length...")
        subtitles_processor = SubtitlesProcessor(
            segments=result["segments"],
            lang=detected_language,
            max_line_length=70,
            min_char_length_splitter=50
        )

        processed_segments = subtitles_processor.process_segments(advanced_splitting=True)

        # 7. Format and save SRT with Audim speaker tags
        print(f"Saving SRT to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(processed_segments, 1):
                # Find the original segment that this processed segment came from
                # by finding which original segment contains this timestamp
                original_segment = next(
                    (s for s in result["segments"] if 
                     s["start"] <= segment["start"] and s["end"] >= segment["start"]),
                    {"speaker": "Speaker"}
                )
                
                speaker = original_segment.get("speaker", "Speaker")
                # Replace SPEAKER_0, SPEAKER_1, etc. with simple Speaker labels
                speaker_label = re.sub(
                    r"SPEAKER_\d+", 
                    lambda m: f"Speaker {int(m.group(0).split('_')[1])+1}", 
                    speaker
                )
                
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = f"[{speaker_label}] {segment['text'].strip()}"
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

        print(f"Successfully created SRT file: {output_file}")
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        raise

def main():

    # ================ CONFIGURATION ================
    # Input/output configuration
    audio_file = "./input/podcast.mp3"                          # Replace with your audio file path
    output_file = "./output/podcast.srt"                        # Output SRT file path (or None to use audio filename with .srt extension)
    
    # Model configuration
    model_name = "large-v2"                                     # Options: tiny, base, small, medium, large, large-v2, large-v3
    language = None                                             # Language code (e.g., 'en', 'hi', 'bn') or None for auto-detection
    device = "cuda" if torch.cuda.is_available() else "cpu"     # Device to run on: 'cpu', 'cuda', 'mps'
    compute_type = "float16"                                    # Compute type: float16, float32, int8 (use int8 for CPU)
    batch_size = 16                                             # Reduce if low on GPU memory
    
    # Speaker diarization configuration
    hf_token = "YOUR_HF_TOKEN"                                  # Replace with your HuggingFace token
    min_speakers = 1                                            # Minimum number of speakers (set to None if unknown)
    max_speakers = 5                                            # Maximum number of speakers (set to None if unknown)
    # ===========================================
    
    # Process the audio file
    process_audio(
        audio_file=audio_file,
        output_file=output_file,
        model_name=model_name,
        language=language,
        device=device,
        min_speakers=min_speakers,
        max_speakers=max_speakers,
        hf_token=hf_token,
        batch_size=batch_size,
        compute_type=compute_type
    )

if __name__ == "__main__":
    main()
