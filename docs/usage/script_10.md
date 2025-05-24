# Replace Speaker Names in Subtitle

## Use Case

You have generated a subtitle file with `audim` or you have a original subtitle file (with manual speaker diarization).
Now, you want to replace the speaker names with the actual names or you wish to add speaker names to the subtitle.

!!! warning "Disclaimer"
    `Audim > Aud2Sub` can perform speaker diarization,
    but it generates a subtitle file with speaker placeholders
    like `[Speaker 1]`, `[Speaker 2]`, etc.

    Currently, you have to manually identify the speakers and replace the placeholders with the actual names.

    🚧 We will soon have a `util` tool to aid you with in this manual process.
    
    **It is theoritically impossible to identify the speaker names**,
    as it could be anyone's voice and a code has no way to determine that.

## Script

```python
from audim.utils.subtitle import Subtitle

subtitle = Subtitle()

# Replace speaker placeholders with actual names
subtitle.preview_replacement(
    "output/podcast.srt",
    speakers=["Grant Sanderson", "Sal Khan"],
    pretty_print=True
)

subtitle.replace_speakers(
    "output/podcast.srt",
    speakers=["Grant Sanderson", "Sal Khan"],
    in_place=True
)
```

!!! tip "Tips"
    You might want to generate subtitles with `audim` first,
    and then use this script to replace the speaker names.

    see: [script 01](./script_01.md) to generate subtitles.

!!! tip "Tips"
    You might want to verify the new subtitle file after replacement,
    Or, you might want some playback help to identify the speakers first.

    see: [script 08](./script_08.md) to play the audio with the subtitles.