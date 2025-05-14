#!/usr/bin/env python
import os
import subprocess


class Extract:
    """
    A class for extracting and converting various forms of media data from various types of media files
    """

    def extract_audio(self, input_path, output_path, output_format='wav', bitrate='192k', sample_rate=44100) -> str | None:
        """
        Extract audio from a video file with no loss in quality.
        
        Args:
            input_path (str): Path to the input video file
            output_path (str): Path to save the output audio file
            output_format (str): Format of the output audio file. e.g.: mp3, wav, flac (default: wav)
            bitrate (str): Bitrate for the output audio. e.g.: 128k, 192k, 320k (default: 192k)
            sample_rate (int): Sample rate for the output audio. e.g.: 44100, 48000, 96000 (default: 44100)

        Returns:
            str | None: Path to the output audio file if extraction was successful, None otherwise
        """

        # Check if input file exists
        if not os.path.isfile(input_path):
            print(f"Error: Input file '{input_path}' does not exist.")
            return None

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # If output_path doesn't have the correct extension, add it
        if not output_path.lower().endswith(f'.{output_format.lower()}'):
            output_path = f"{output_path}.{output_format.lower()}"
        
        # Prepare FFmpeg command
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-vn",
            "-acodec", self._get_audio_codec(output_format),
            "-ab", bitrate,
            "-ar", str(sample_rate),
            "-y",
            output_path
        ]
        
        # Run the command
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Successfully extracted audio to {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")
            return None

    def _get_audio_codec(self, format):
        """
        Get the appropriate audio codec based on the output format.
        
        Args:
            format (str): Output audio format
        
        Returns:
            str: Audio codec to use
        """
        
        # Audio formats to ffmpeg codecs mappings
        codecs = {
            "mp3": "libmp3lame",
            "aac": "aac",
            "m4a": "aac",
            "ogg": "libvorbis",
            "wav": "pcm_s16le",
            "flac": "flac",
            "opus": "libopus",
            "wma": "wmav2",
        }

        # Get the appropriate ffmpeg codec
        # Note: "copy" tells FFmpeg to stream copy the audio without re-encoding it.
        format = format.lower()
        ffmpeg_codec = codecs.get(format, "copy")

        return ffmpeg_codec
