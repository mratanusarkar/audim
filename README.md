<div align='center'>

# Audim ✨

[![Documentation](https://img.shields.io/badge/Audim-docs-blue)](https://mratanusarkar.github.io/audim)
[![Author: Atanu Sarkar](https://img.shields.io/badge/Author-Atanu%20Sarkar-purple)](https://github.com/mratanusarkar)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-orange)](https://github.com/mratanusarkar/audim/blob/main/LICENSE)
[![Citation](https://img.shields.io/badge/Cite%20this-Repository-green)](https://github.com/mratanusarkar/audim/blob/main/CITATION.cff)

**Au**dio Po**d**cast An**im**ation Engine

> _An animation and video rendering engine for audio-based and voice-based podcast videos._

|
[Features](#-features) |
[Getting Started](#-getting-started) |
[Quick Links](#-quick-links)
|

</div>

## 🚀 Demo

<div align='center'>

https://github.com/user-attachments/assets/634df0ca-77ee-448b-ac35-f4eb3e4261b9

*A sample podcast video generated with Audim*

</div>

> [!NOTE]
> 
> For this example,
> we have transformed a conversation between Grant Sanderson (from [3Blue1Brown](https://www.3blue1brown.com/)) and Sal Khan (from [Khan Academy](https://www.khanacademy.org/)) from [YouTube](https://www.youtube.com/watch?v=SAhKohb5e_w&t=1179s) into a visually engaging podcast video using Audim.
> 
> See [docs/devblog/v0.0.7.md](https://mratanusarkar.github.io/audim/devblog/v0.0.7.md) for more details on how this video was generated.

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

## ⚖️ License & Attribution

Audim is licensed under **Apache 2.0**. You can use it freely for personal and commercial projects.

**Attribution is encouraged.** If you use Audim, please:

- Keep the default watermark in videos, OR
- Add "Made with Audim" to video descriptions, OR  
- Link to this repo in your project documentation

> See [NOTICE](./NOTICE) file for complete attribution guidelines.

## 📄 Citation

If you use Audim in your project or research, please cite it as follows:

```bibtex
@software{audim,
  title = {Audim: Audio Podcast Animation Engine},
  author = {Sarkar, Atanu},
  year = {2025},
  url = {https://github.com/mratanusarkar/audim},
  version = {0.0.7}
}
```

You can also click the **"Cite this repository"** button on GitHub for other citation formats.

## ⚠️ Disclaimer

> [!WARNING]
> **Early Development Stage**
> 
> - This project is actively under development and may contain bugs or limitations.
> - While stable for basic use cases, the rendering engine requires further development and testing across diverse scenarios.
> - The API is subject to change, so keep an eye at the documentation for the latest updates.

> [!TIP]
> **We encourage you to:**
> 
> - Try Audim for your projects and podcast videos.
> - [Report issues](https://github.com/mratanusarkar/audim/issues) when encountered.
> - Feel free to raise a PR to contribute and improve the project.

_Your feedback and contributions help make Audim better for everyone!_
