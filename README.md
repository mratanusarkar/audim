<div align='center'>

# Audim ✨

[![Documentation](https://img.shields.io/badge/Audim-docs-blue)](https://mratanusarkar.github.io/audim)
[![Author: Atanu Sarkar](https://img.shields.io/badge/Author-Atanu%20Sarkar-purple)](https://github.com/mratanusarkar)

**Au**dio Po**d**cast An**im**ation Engine

> _An animation and video rendering engine for audio-based and voice-based podcast videos._

|
[Features](#-features) |
[Getting Started](#-getting-started) |
[Quick Links](#-quick-links)
|

</div>

## 🔗 Quick Links

1. Getting Started
    - See [Setup](https://mratanusarkar.github.io/audim/setup/installation.md) and ensure you have setup correctly before usage.
    - For developers and contributors, see [Development](https://mratanusarkar.github.io/audim/setup/development.md).
2. API Documentation
    - See [API Docs](https://mratanusarkar.github.io/audim/audim/index.md) for the `audim` API documentation.
3. Usage and Examples
    - See [Usage](https://mratanusarkar.github.io/audim/usage/index.md) for usage examples.
4. Dev Blog
    - See [Dev Blog](https://mratanusarkar.github.io/audim/devblog/index.md) for the development blog of the project to gain more insights into the project.
    - See [Changelog](https://mratanusarkar.github.io/audim/devblog/index.md#changelog) for the changelog of the project.

## 🎯 Introduction

Audim is an engine for precise programmatic animation and rendering of podcast videos from audio-based and voice-based file recordings.

## ✨ Features

- 💻 Precise programmatic animations.
- 🎬 Rendering of videos with layout based scenes.
- 📝 Generate subtitles and transcripts from audio/video files.
- 🎤 From subtitle and scene elements to podcast video generation.

## 🚀 Getting Started

### Prerequisites

- 🐍 Python ≥ 3.10
- 🖥️ Conda
- 🎥 FFmpeg (optional, for faster video encoding)

### Installation

#### 1. Clone the repository:

```bash
git clone https://github.com/mratanusarkar/audim.git
```

#### 2. Install FFmpeg locally (optional)

Using local FFmpeg is optional but recommended for speeding up the video encoding process.

On Ubuntu, install FFmpeg using:

```bash
sudo apt install ffmpeg libx264-dev
```

On Windows and other platforms, download and install FFmpeg from the official website:

- [Download FFmpeg](https://ffmpeg.org/download.html)
- Ensure FFmpeg is in your system PATH

#### 3. Install `uv` and setup project environment:

> [!IMPORTANT]
> If you are using conda base environment as the default base environment for your python projects, run the below command to activate the base environment. If not, skip this step and continue with the next step.
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

#### 4. Build and deploy documentation

You can build and serve the documentation by running:

```bash
uv pip install -e .[docs]
mkdocs serve
```

## Code Quality

Before committing, please ensure that the code is formatted and styled correctly.
Run the following commands to check and fix code style issues:

```bash
# Check and fix code style issues
ruff format .
ruff check --fix .
```

## 📄 License & Attribution

Audim is licensed under **Apache 2.0**. You can use it freely for personal and commercial projects.

**Attribution is encouraged.** If you use Audim, please:

- Keep the default watermark in videos, OR
- Add "Made with Audim" to video descriptions, OR  
- Link to this repo in your project documentation

> See [NOTICE](./NOTICE) file for complete attribution guidelines.
