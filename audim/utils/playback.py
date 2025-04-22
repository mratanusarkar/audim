import threading
import time
from datetime import datetime

import pysrt
from pydub import AudioSegment
from pydub.playback import play


class Playback:
    """
    Class for synchronized audio and video playback with subtitles

    Use it to playback various outputs and generations from Audim
    and testing and validating the results
    """

    def _srt_audio_player(self, subs, start_time):
        """
        Play audio with subtitles in CLI in realtime and in sync

        Args:
            subs (list): List of pysrt.SubRipItem objects
            start_time (datetime): Start time of the playback
        """

        for sub in subs:
            # Calculate wait time until this subtitle should be shown
            # Convert subtitle time to seconds from start
            start_seconds = (
                sub.start.hours * 3600
                + sub.start.minutes * 60
                + sub.start.seconds
                + sub.start.milliseconds / 1000
            )
            current_time = (datetime.now() - start_time).total_seconds()

            # If we need to wait, sleep until it's time to show this subtitle
            if start_seconds > current_time:
                time.sleep(start_seconds - current_time)

            # Clear previous subtitle and display current one
            print("\033[H\033[J", end="")
            print(f"\n\n\n\n\n{sub.text}\n")

            # Calculate duration of this subtitle
            end_seconds = (
                sub.end.hours * 3600
                + sub.end.minutes * 60
                + sub.end.seconds
                + sub.end.milliseconds / 1000
            )
            duration = end_seconds - start_seconds

            # If next subtitle doesn't start immediately, clear screen
            if duration > 0:
                time.sleep(duration)
                print("\033[H\033[J", end="")

    def play_audio_with_srt(self, audio_file, srt_file):
        """
        Play audio file with synchronized subtitles in CLI

        Args:
            audio_file (str): Path to the audio file
            srt_file (str): Path to the SRT subtitle file
        """

        try:
            # Load the audio file
            audio = AudioSegment.from_file(audio_file)

            # Load the subtitles
            subs = pysrt.open(srt_file)

            print("Playing audio with subtitles. Press Ctrl+C to stop.")
            time.sleep(1)
            print("\033[H\033[J", end="")

            # Start the subtitle display thread
            start_time = datetime.now()
            subtitle_thread = threading.Thread(
                target=self._srt_audio_player, args=(subs, start_time)
            )
            subtitle_thread.daemon = True
            subtitle_thread.start()

            # Play the audio
            play(audio)

        except KeyboardInterrupt:
            print("\nPlayback stopped.")
        except Exception as e:
            print(f"Error: {e}")
            raise
