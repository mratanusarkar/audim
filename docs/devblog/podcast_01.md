# Basic Podcast Video Generation

> - **Author**: [@mratanusarkar](https://github.com/mratanusarkar)
> - **Created**: March 05, 2025
> - **Last Updated**: March 05, 2025
> - **Compatible with**: Audim v0.0.1

This example demonstrates how to generate a simple podcast video from a subtitle file and audio file using Audim's Sub2Pod module.

## Prerequisites

Before running this example, make sure you have:

1. Installed Audim following the [installation instructions](/setup/installation)
2. Created the required input files:

    - `input/podcast.srt` - Subtitle file with speaker tags
    - `input/podcast.mp3` - Audio file of the podcast
    - `input/host_dp.png` - Host profile picture
    - `input/guest_dp.png` - Guest profile picture
    - `input/logo.png` - Brand logo (optional)

## Example SRT File

Your SRT file should follow the standard [SubRip Subtitle format](https://en.wikipedia.org/wiki/SubRip) with added speaker tags as expected by Audim.

Below is an example of an SRT file with speaker tags:

```srt
1
00:00:00,000 --> 00:00:04,500
[Host] Welcome to our podcast!

2
00:00:04,600 --> 00:00:08,200
[Guest] Thank you! Glad to be here.

```

## Example Code Implementation

The following code demonstrates how to generate a podcast video from an SRT file and audio file using Audim's Sub2Pod module.

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
layout.add_speaker("Host", "input/host_dp.png")
layout.add_speaker("Guest", "input/guest_dp.png")

# Generate video
print("Generating video...")
generator = VideoGenerator(layout, fps=30)
generator.generate_from_srt(
    srt_path="input/podcast.srt",
    audio_path="input/podcast.mp3",
    logo_path="input/logo.png",
    title="My Awesome Podcast"
)

# Export the final video
print("Exporting video...")
datetime = datetime.now().strftime("%Y%m%d%H%M%S")
generator.export_video(f"output/podcast_{datetime}.mp4")
```

## Output

The output podcast video will be saved in the `output` directory with a timestamp in the filename.

## Troubleshooting

If you encounter issues with this example:
- Verify you're using the compatible version of Audim
- Check that all input files exist and are in the correct format
- Ensure your SRT file has proper speaker tags in the format `[SpeakerName]`

## See Also

- [API Documentation for PodcastLayout](/audim/sub2pod/layouts/podcast)
- [API Documentation for VideoGenerator](/audim/sub2pod/core)
