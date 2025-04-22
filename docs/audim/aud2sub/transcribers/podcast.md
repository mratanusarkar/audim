# Podcast Transcriber

The podcast transcriber is a transcriber implementation that uses the [WhisperX](https://github.com/m-bain/whisperx) under the hood.
WhisperX provides **Automatic Speech Recognition** with **Word-level Timestamps** and **Diarization**.

It uses `faster-whisper` as the ASR and Transcription model, it's own alignment logic and `pyannote-audio` for diarization.

!!! warning "Warning"
    WhisperX uses a local offline ASR model.
    So, all the models are downloaded and run locally.
    You must have a good system specification and NVIDIA GPU with 12GB VRAM to run this.

    In future, we will support to work with online model vendors like `OpenAI` and `HuggingFace`.

Below is the API documentation for the podcast transcriber:

::: audim.aud2sub.transcribers.podcast