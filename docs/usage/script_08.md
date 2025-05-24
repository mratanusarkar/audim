# Audio Playback with Subtitles

## Use Case

You have an audio file and a subtitle file and you want to play the audio with the subtitles.

This might come in handy when:

- you have generated a subtitle with `audim` and wish to validate and preview it in sync with the audio.
- you have a subtitle file and original audio file, and wish to listen to it in sync to figure out the speaker names.
- idk, just like to listen to the audio with the subtitles the terminal cauz it's cool!

## Script

```python
from audim.utils.playback import Playback


# Create a playback instance
playback = Playback()

# Play an audio file with synchronized subtitles
playback.play_audio_with_srt("input/podcast.mp3", "output/podcast.srt")
```

!!! tip "Tips"
    You might want to generate subtitles with `audim` first,
    and then use this script to play the audio with the subtitles.

    see: [script 01](./script_01.md) to generate subtitles.

!!! tip "Tips"
    You might want to replace the speaker names with the actual names,
    and then use this script again to play the audio with the subtitles.

    see: [script 10](./script_10.md) to replace the speaker names.
