# Audim API Documentation

Audim is an engine for precise programmatic animation and rendering of podcast videos from audio-based and voice-based file recordings.

## Modules

- `aud2sub` - Audio to subtitle generation.
- `sub2pod` - Subtitle to podcast video generation.
- `utils` - Utility functions for audio and video processing.
- `vid2sub` - Video to subtitle extraction.

## Submodules

### aud2sub

- **core** - Core audio-to-subtitle generation pipeline.
- **transcribers**
    - **base** - Base transcriber interface.
    - **podcast** - Transcriber implementation using WhisperX model.

### sub2pod

- **core** - Core subtitle-to-podcast video generation and rendering pipeline.
- **elements** - video elements
    - **header** - Header and title elements.
    - **profile** - Speaker profile and avatar components.
    - **text** - Text styling and display components.
    - **watermark** - Branding and watermark elements.
- **effects** - effects on elements
    - **highlights** - Text and visual highlighting effects.
    - **transitions** - Scene and element transition animations.
- **layouts** - layouts for podcast videos
    - **base** - Base layout framework.
    - **podcast** - Podcast-specific layouts.

### utils

- **extract** - Audio and video extraction utilities.
- **playback** - Media playback and control.
- **subtitle** - Subtitle parsing, formatting, and manipulation.
