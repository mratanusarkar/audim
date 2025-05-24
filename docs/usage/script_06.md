# **Video + Subtitle** to **Podcast** Generation

## Use Case

You have a video file and an original subtitle file and you want to generate a podcast video using `audim`.

!!! note "Note"
    Use this script when you have the original subtitle file
    and you don't want to use `audim` to generate the subtitle file.

!!! warning "Assumption"
    This script assumes that the original subtitle file is in the same language as the video file.
    If the original subtitle file is in a different language, you need to translate it to the same language as the video file.
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
import os
from datetime import datetime
from audim.utils.extract import Extract
from audim.sub2pod.layouts.podcast import PodcastLayout
from audim.sub2pod.core import VideoGenerator

# Set input and output files
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
input_video_file = "input/podcast.mp4"
input_subtitle_file = "input/podcast.srt"
output_video_file = f"output/podcast_{timestamp}.mp4"
speakers = [
    {
        "name": "Grant Sanderson",
        "dp": "input/grant.png"
    },
    {
        "name": "Sal Khan",
        "dp": "input/sal.png"
    }
]
podcast_logo = "input/logo.png"
podcast_title = "3b1b Podcast: Sal Khan: Beyond Khan Academy"

# Extract audio from video
temp_audio_file = "temp/podcast.wav"
temp_audio_format = "wav"
extractor = Extract()
extractor.extract_audio(input_video_file, temp_audio_file, temp_audio_format)

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
for speaker in speakers:
    layout.add_speaker(speaker["name"], speaker["dp"])

# Generate video
print("Generating video...")
generator = VideoGenerator(layout, fps=30)
generator.generate_from_srt(
    srt_path=input_subtitle_file,
    audio_path=temp_audio_file,
    logo_path=podcast_logo,
    title=podcast_title,
    cpu_core_utilization="max"
)

# Delete the intermediate extracted audio file
os.remove(temp_audio_file)

# Export the final video
print("Exporting video...")
generator.export_video(output_video_file)
print(f"Done! Check {output_video_file} for results.")
```
