# Audim

[![Documentation](https://img.shields.io/badge/Audim-docs-blue)](https://mratanusarkar.github.io/audim)
[![Author: Atanu Sarkar](https://img.shields.io/badge/Author-Atanu%20Sarkar-purple)](https://github.com/mratanusarkar)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-orange)](https://github.com/mratanusarkar/audim/blob/main/LICENSE)
[![Citation](https://img.shields.io/badge/Cite%20this-Repository-green)](https://github.com/mratanusarkar/audim/blob/main/CITATION.cff)

**Au**dio Po**d**cast An**im**ation Engine

_An animation and video rendering engine for audio-based and voice-based podcast videos._

## 🚀 Demo

<div style="text-align: center; margin: 20px 0;">
  <video controls style="width: 100%;">
    <source src="./assets/example_03/podcast.mp4" type="video/mp4">
    Your browser does not support the video element.
  </video>
  <p style="text-align: center; font-style: italic; margin-top: 5px;">A sample podcast video generated with Audim</p>
</div>

!!! quote "About the Demo"

    > For this example, we have transformed a conversation between Grant Sanderson (from [3Blue1Brown](https://www.3blue1brown.com/)) and Sal Khan (from [Khan Academy](https://www.khanacademy.org/)) from [YouTube](https://www.youtube.com/watch?v=SAhKohb5e_w&t=1179s) into a visually engaging podcast video using Audim.
    >
    > See [docs/devblog/v0.0.7.md](./devblog/v0.0.7.md) for more details on how this video was generated.

## 🎯 Introduction

Audim is an engine for precise programmatic animation and rendering of podcast videos from audio-based and voice-based file recordings.

## ✨ Features

- 💻 Precise programmatic animations.
- 🎬 Rendering of videos with layout based scenes.
- 📝 Generate subtitles and transcripts from audio/video files.
- 🎤 From subtitle and scene elements to podcast video generation.

## 🔗 Quick Links

1. Getting Started
    - See [Setup](./setup/installation.md) and ensure you have setup correctly before usage.
    - For developers and contributors, see [Development](./setup/development.md).
2. API Documentation
    - See [API Docs](./audim/index.md) for the `audim` API documentation.
3. Usage and Examples
    - See [Usage](./usage/index.md) for usage examples.
4. Dev Blog
    - See [Dev Blog](./devblog/index.md) for the development blog of the project to gain more insights into the project.
    - See [Changelog](./devblog/index.md#changelog) for the changelog of the project.

## ⚖️ License & Attribution

Audim is licensed under **Apache 2.0**. You can use it freely for personal and commercial projects.

**Attribution is encouraged.** If you use Audim, please:

- Keep the default watermark in videos, OR
- Add "Made with Audim" to video descriptions, OR  
- Link to this repo in your project documentation

!!! info "Additional Information"

    - See [NOTICE](https://github.com/mratanusarkar/audim/blob/main/NOTICE) file for complete attribution guidelines.
    - See [LICENSE](https://github.com/mratanusarkar/audim/blob/main/LICENSE) file for the license of the project.
    - For additional attribution examples, see [Watermark](./audim/sub2pod/elements/watermark/) documentation.

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

!!! warning "Early Development Stage"

    - This project is actively under development and may contain bugs or limitations.
    - While stable for basic use cases, the rendering engine requires further development and testing across diverse scenarios.
    - The API is subject to change, so keep an eye at the documentation for the latest updates.

!!! tip "We encourage you to:"

    - Try Audim for your projects and podcast videos.
    - [Report issues](https://github.com/mratanusarkar/audim/issues) when encountered.  
    - Feel free to raise a PR to contribute and improve the project.

_Your feedback and contributions help make Audim better for everyone!_
