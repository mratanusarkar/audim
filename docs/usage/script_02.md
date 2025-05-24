# **Audio + Subtitle** to **Podcast** Generation

## Use Case

You have an audio file or a recording and an original subtitle file and you want to generate a podcast video.

!!! note "Note"
    Use this script when you have the original subtitle file
    and you don't want to use `audim` to generate the subtitle file.

!!! warning "Assumption"
    This script assumes that the original subtitle file is in the same language as the audio file.
    If the original subtitle file is in a different language, you need to translate it to the same language as the audio file.
    You can use a tool like [OpenAI's Whisper](https://github.com/openai/whisper) to translate the subtitle file.

!!! danger "Caution"
    The subtitle file must be as per the format expected by `audim`, which adds speaker identification.
    
    Example of expected subtitle file format:
    
    ```txt
    1
    00:00:00,000 --> 00:00:04,500
    [Host] Welcome to our podcast!

    2
    00:00:04,600 --> 00:00:08,200
    [Guest] Thank you! Glad to be here.
    ```

    see [sub2pod/core](../audim/sub2pod/core.md) for more details.

## Script

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

# Set custom effects for the layout
layout.set_transition_effect("fade", frames=20)
layout.set_highlight_effect("none")

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
generator.export_video(f"output/podcast_underline_{datetime}.mp4")
```