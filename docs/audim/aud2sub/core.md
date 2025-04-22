# Core (Subtitle Generation Module)

The core module is the main **Subtitle Generation Engine**.
It is responsible for the overall structure and flow of the subtitle generation.

This module provides the high-level API for generating subtitles from audio files.
It uses a **transcriber object** to define the format of the subtitle.

The **transcriber object** internally uses an **ASR model** to transcribe the audio,
**aligns** the transcription segment timestamps with the audio,
and a **diarization model** to detect the speakers.
Finally it uses a **formatter** to determine the format of the subtitle generation.

Below is the API documentation for the core module:

::: audim.aud2sub.core
