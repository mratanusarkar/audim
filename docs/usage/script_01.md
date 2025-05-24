# **Audio** to **Subtitle** Generation

## Use Case

You have an audio file and you want to generate subtitles and transcriptions with speaker diarization.

## Script

```python
from audim.aud2sub.transcribers.podcast import PodcastTranscriber
from audim.aud2sub.core import SubtitleGenerator

# Create transcriber object
print("Creating transcriber...")
transcriber = PodcastTranscriber(model_name="large-v2")

# Set speaker detection and subtitle formatting parameters
transcriber.set_speakers(min_speakers=1, max_speakers=5)
transcriber.set_speaker_names_display(True, pattern="[{speaker}]")
transcriber.set_line_properties(max_length=70, min_split_length=50)

# Create subtitle generator object
print("Generating subtitles...")
generator = SubtitleGenerator(transcriber)

# Process audio file
print("Processing audio...")
generator.generate_from_mp3("input/podcast.mp3")

# Export the final subtitle
print("Exporting subtitles...")
generator.export_subtitle("output/podcast.srt")
print("Done! Check output/podcast.srt for results.")
```
