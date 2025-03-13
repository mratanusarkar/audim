# Creating a Professional Podcast Video with Audim

> - **Author**: [@mratanusarkar](https://github.com/mratanusarkar)
> - **Created**: March 13, 2025
> - **Last Updated**: March 13, 2025
> - **Compatible with**: Audim v0.0.1

This example demonstrates how to create a professional-looking podcast video using Audim's Sub2Pod module, featuring real speakers with profile pictures, custom branding, and high-quality output.

## Overview

In this tutorial, we'll transform a conversation between Grant Sanderson (3Blue1Brown) and Sal Khan (Khan Academy) into a visually engaging podcast video. We'll walk through:

1. Preparing the input files
2. Setting up the podcast layout
3. Generating the video with Audim
4. Reviewing the final output

## Input Files

### Audio File

Below is a sample of the podcast audio we'll be using:

<div style="margin: 20px 0;">
  <audio controls style="width: 100%;">
    <source src="./assets/podcast_02/podcast.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
  <p style="text-align: center; font-style: italic; margin-top: 5px;">Sample from "3b1b Podcast: Sal Khan: Beyond Khan Academy"</p>
</div>

### Subtitle File (SRT)

The SRT file contains the transcription with speaker tags:

<div style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; background-color: #f8f8f8; font-family: monospace; margin: 20px 0;">
</div>

### Other Files

- Profile Pictures of Grant and Sal
- Brand Logo of 3Blue1Brown

## Code Implementation

Here's the complete code to generate our podcast video:

```python
from datetime import datetime
from audim.sub2pod.layouts.podcast import PodcastLayout
from audim.sub2pod.core import VideoGenerator

# Create a podcast layout
print("Creating layout...")
layout = PodcastLayout(
    video_width=1920,
    video_height=1080,
    show_speaker_names=True
)

# Add speakers
print("Adding speakers...")
layout.add_speaker("Grant Sanderson", "input/grant.png")
layout.add_speaker("Sal Khan", "input/sal.png")

# Generate video
print("Generating video...")
generator = VideoGenerator(layout, fps=30)
generator.generate_from_srt(
    srt_path="input/podcast.srt",
    audio_path="input/podcast.mp3",
    logo_path="input/logo.png",
    title="3b1b Podcast: Sal Khan: Beyond Khan Academy",
    cpu_core_utilization="max"
)

# Export the final video
print("Exporting video...")
datetime = datetime.now().strftime("%Y%m%d%H%M%S")
generator.export_video(f"output/podcast_{datetime}.mp4")
```

## Output Video

<div style="text-align: center; margin: 20px 0;">
  <video controls style="width: 100%;">
    <source src="./assets/podcast_02/podcast.mp4" type="video/mp4">
    Your browser does not support the video element.
  </video>

