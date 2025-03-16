# Audim

[![Documentation](https://img.shields.io/badge/Audim-docs-blue)](https://mratanusarkar.github.io/audim)

**Au**dio Po**d**cast An**im**ation Engine

_An animation and video rendering engine for audio-based and voice-based podcast videos._

---

Audim is an engine for precise programmatic animation and rendering of podcast videos from audio-based and voice-based file recordings.

## Features

- Precise programmatic animations.
- Rendering of videos.
- Layout based scenes.
- Support for audio to subtitle generation.
- Support for video to subtitle and scene elements generation.
- Support for subtitle and scene elements to video generation.

## Prerequisites

- Python ≥ 3.10
- Conda
- FFmpeg (optional, for faster video encoding)

## Setup

### 1. Clone the repository:

```bash
git clone https://github.com/mratanusarkar/audim.git
```

### 2. Install FFmpeg locally (optional)

Using local FFmpeg is optional but recommended for speeding up the video encoding process.

On Ubuntu, install FFmpeg using:

```bash
sudo apt install ffmpeg libx264-dev
```

On Windows and other platforms, download and install FFmpeg from the official website:

- [Download FFmpeg](https://ffmpeg.org/download.html)
- Ensure FFmpeg is in your system PATH

### 3. Install `uv` and setup project environment:

> **Note**: If you are using conda base environment as the default base environment for your python projects, run the below command to activate the base environment. If not, skip this step and continue with the next step.
>
> ```bash
> conda activate base
> ```

```bash
# Install uv
pip install uv

# Setup project environment
uv venv

source .venv/bin/activate   # on Linux
# .venv\Scripts\activate    # on Windows

uv pip install -e ".[dev,docs]"
```

## Code Quality

Before committing, please ensure that the code is formatted and styled correctly.
Run the following commands to check and fix code style issues:

```bash
# Check and fix code style issues
ruff format .
ruff check --fix .
```
