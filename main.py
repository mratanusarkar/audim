import pysrt
import cv2
import numpy as np
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager

# Load SRT file
subs = pysrt.open("input/podcast.srt")

# Define assets
# background_img = "background.jpg"  # Can be a static image or video
logo_img = "input/logo.png"
speaker_dps = {
    "Host": "input/host_dp.png",
    "Guest": "input/guest_dp.png",
}

# Define video parameters
video_width, video_height = 1280, 720
fps = 30

# Create video frames
frames = []
for sub in subs:
    start_time = sub.start.ordinal // 10  # Convert ms to frame count
    end_time = sub.end.ordinal // 10
    speaker, text = sub.text.split("] ")
    speaker = speaker.replace("[", "").strip()

    # Create frame with DP, text, and branding
    frame = Image.new("RGB", (video_width, video_height), (0, 0, 0))
    draw = ImageDraw.Draw(frame)
    # Use matplotlib's default font
    font_path = font_manager.findfont(font_manager.FontProperties(family='sans-serif'))
    font = ImageFont.truetype(font_path, 40)

    # Load Speaker DP
    if speaker in speaker_dps:
        dp = Image.open(speaker_dps[speaker]).resize((200, 200))
        frame.paste(dp, (50, 50))  # Position DP

    # Add subtitle text
    draw.text((300, 600), f"{speaker}: {text}", fill="white", font=font)

    # Convert to NumPy array for OpenCV
    frame_np = np.array(frame)
    frames.append(frame_np)

# Convert frames to video
video = ImageSequenceClip(frames, fps=fps)
audio = AudioFileClip("input/podcast.mp3")
final_video = video.set_audio(audio)

# Export video
final_video.write_videofile("output/podcast.mp4", codec="libx264", fps=fps)
