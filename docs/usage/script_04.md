# **Video** to **Audio** Extraction

## Use Case

You have a video file and you want to extract the audio from it.

## Script

```python
from audim.utils.extract import Extract


# Set input and output file paths
input_file = "input/podcast.mp4"
output_file = "output/podcast.wav"
output_format = "wav"

# Extract audio from video
extractor = Extract()
extractor.extract_audio(input_file, output_file, output_format)
```
