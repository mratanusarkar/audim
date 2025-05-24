# **Video** to **Subtitle** Generation

## Use Case

You have a video file and you want to generate a subtitle file from it.

## Script

```python
import os
from audim.utils.extract import Extract
from audim.aud2sub.transcribers.podcast import PodcastTranscriber
from audim.aud2sub.core import SubtitleGenerator

# Set input and output file paths
input_file = "input/podcast.mp4"
audio_file = "temp/podcast.wav"
audio_format = "wav"
output_subtitle_file = f"output/podcast.srt"

# Extract audio from video
extractor = Extract()
extractor.extract_audio(input_file, audio_file, audio_format)

# Create transcriber object
print("Creating transcriber...")
transcriber = PodcastTranscriber(model_name="large-v2")

# Set speaker detection and subtitle formatting parameters
transcriber.set_speakers(min_speakers=1, max_speakers=10)
transcriber.set_speaker_names_display(True, pattern="[{speaker}]")
transcriber.set_line_properties(max_length=70, min_split_length=50)

# Create subtitle generator object
print("Generating subtitles...")
generator = SubtitleGenerator(transcriber)

# Process audio file
print("Processing extracted audio from video...")
generator.generate_from_mp3(audio_file)

# Delete the intermediate extracted audio file
os.remove(audio_file)

# Export the final subtitle
print("Exporting subtitles...")
generator.export_subtitle(output_subtitle_file)
print(f"Done! Check {output_subtitle_file} for results.")
```
