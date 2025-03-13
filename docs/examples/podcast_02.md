# Creating a Professional Podcast Video with Audim

> - **Author**: [@mratanusarkar](https://github.com/mratanusarkar)
> - **Created**: March 13, 2025
> - **Last Updated**: March 14, 2025
> - **Compatible with**: Audim v0.0.2


This example demonstrates how to create a professional-looking podcast video using Audim's Sub2Pod module, featuring real speakers with profile pictures, custom branding, and high-quality output.

## Overview

In this tutorial, we'll transform a conversation between Grant Sanderson (from [3Blue1Brown](https://www.3blue1brown.com/)) and Sal Khan (from [Khan Academy](https://www.khanacademy.org/)) into a visually engaging podcast video. We'll walk through:

1. Preparing the input files
2. Setting up the podcast layout
3. Generating the video with **Audim**
4. Reviewing the final output

Note: The conversation between Grant and Sal is taken from [this podcast](https://www.youtube.com/watch?v=SAhKohb5e_w&t=1179s).

## Input Files

### Audio File

Below is a sample of the podcast audio we'll be using:

<div style="margin: 20px 0;">
  <audio controls style="width: 100%;">
    <source src="./assets/podcast_02/podcast.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>
  <p style="text-align: center; font-style: italic; margin-top: 5px;">Audio snippet from "Sal Khan: Beyond Khan Academy | 3b1b Podcast #2"</p>
</div>

### Subtitle File (SRT)

The SRT file contains the transcription with speaker tags. The SRT file should follow the standard [SubRip Subtitle format](https://en.wikipedia.org/wiki/SubRip) with added speaker tags as expected by Audim.

Below is the SRT file used for this example:

## Podcast Subtitles

<div style="max-height: 400px; overflow: auto; border: 1px solid #ddd; padding: 10px;">
<pre>
00:00:01,500 --> 00:00:04,000
Welcome to our podcast!

00:00:04,500 --> 00:00:07,000
Today, we're going to talk about something interesting.

...
</pre>
</div>

### Other Files

- Profile Picture of Grant Sanderson
- Profile Picture of Sal Khan
- Brand Logo of 3Blue1Brown

## Code Implementation

After gathering all the files, we can now generate the podcast video using **Audim**.

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

Here is the terminal logs upon running the code:

```bash
(audim) (base) atanu@atanu-LOQ-15APH8:~/Workspace/GitHub/audim$ python test.py 
Creating layout...
Adding speakers...
Generating video...
[2025-03-13 23:25:10] VideoGenerator (INFO) - Loading subtitles from input/podcast.srt
[2025-03-13 23:25:10] VideoGenerator (INFO) - Using 16 CPU cores for parallel processing
[2025-03-13 23:25:10] VideoGenerator (INFO) - Processing subtitle to generate frames in 23 batches
Processing batch: 100%|███████████████████████████████████████████████████| 23/23 [00:37<00:00,  1.64s/batch, frames processed=4727]
[2025-03-13 23:25:48] VideoGenerator (INFO) - Frame generation completed: Total 4727 frames created
Exporting video...
[2025-03-13 23:25:48] VideoGenerator (INFO) - Starting video generation process with 4727 frames
[2025-03-13 23:25:48] VideoGenerator (INFO) - Video duration: 156.06s (adjusted to match audio)
[2025-03-13 23:25:48] VideoGenerator (INFO) - Attempting video export with FFmpeg encoding
[2025-03-13 23:25:48] VideoGenerator (INFO) - Preparing frame list for FFmpeg
[2025-03-13 23:25:48] VideoGenerator (INFO) - Using NVIDIA GPU acceleration for video encoding
[2025-03-13 23:25:48] VideoGenerator (INFO) - Starting FFmpeg encoding process
Encoding video:  99%|██████████████████████████████████████████████████████████████████████████████▏| 99/100 [01:09<00:00,  1.42%/s]
[2025-03-13 23:26:58] VideoGenerator (INFO) - Video successfully encoded to output/podcast_20250313232548.mp4
[2025-03-13 23:26:58] VideoGenerator (INFO) - Cleaned up temporary files in /tmp/tmpoqv_t5x6
[2025-03-13 23:26:58] VideoGenerator (INFO) - Video generation completed! Exported to: output/podcast_20250313232548.mp4
```

## Output Video

Here's how the generated video looks like upon rendering:

<div style="text-align: center; margin: 20px 0;">
  <video controls style="width: 100%;">
    <source src="./assets/podcast_02/podcast.mp4" type="video/mp4">
    Your browser does not support the video element.
  </video>
</div>

