import pysrt
import cv2
import numpy as np
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager

def create_circular_mask(size):
    """Create a circular mask for profile pictures"""
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    return mask

# Load SRT file
subs = pysrt.open("input/podcast.srt")

# Define assets
logo_img = "input/logo.png"
speaker_dps = {
    "Host": "input/host_dp.png",
    "Guest": "input/guest_dp.png"
}

# Define video parameters
video_width, video_height = 1920, 1080
fps = 30

# Define layout parameters
header_height = 150
dp_size = (120, 120)
dp_margin = 20
text_margin = 50

# Load and create circular DPs
speaker_images = {}
for speaker, dp_path in speaker_dps.items():
    img = Image.open(dp_path).convert('RGBA')
    img = img.resize(dp_size)
    
    # Create circular mask
    mask = create_circular_mask(dp_size)
    
    # Apply circular mask
    img.putalpha(mask)
    speaker_images[speaker] = img

# Load and resize logo
logo = Image.open(logo_img).convert('RGBA')
logo_size = (100, 100)
logo = logo.resize(logo_size)

# Calculate DP positions (vertically aligned on left)
dp_positions = {}
for i, speaker in enumerate(speaker_dps.keys()):
    y_pos = header_height + (i * (dp_size[1] + dp_margin))
    dp_positions[speaker] = (dp_margin, y_pos)

# Font setup
font_path = font_manager.findfont(font_manager.FontProperties(family=['sans']))
title_font = ImageFont.truetype(font_path, 60)
subtitle_font = ImageFont.truetype(font_path, 40)
speaker_font = ImageFont.truetype(font_path, 30)

def create_frame(current_sub, fade_in=False, opacity=255):
    # Create base frame
    frame = Image.new("RGBA", (video_width, video_height), (20, 20, 20, 255))
    draw = ImageDraw.Draw(frame)
    
    # Add header with title and logo
    draw.rectangle([0, 0, video_width, header_height], fill=(30, 30, 30, 255))
    frame.paste(logo, (video_width - logo_size[0] - 50, (header_height - logo_size[1])//2), logo)
    draw.text((video_width//2, header_height//2), "My Awesome Podcast", 
              fill=(255, 255, 255, opacity), font=title_font, anchor="mm")
    
    # Add all speaker DPs and names
    for speaker, pos in dp_positions.items():
        frame.paste(speaker_images[speaker], pos, speaker_images[speaker])
        draw.text((pos[0] + dp_size[0]//2, pos[1] + dp_size[1] + 10),
                 speaker, fill=(200, 200, 200, opacity), font=speaker_font, anchor="mm")
    
    if current_sub:
        speaker, text = current_sub.text.split("] ")
        speaker = speaker.replace("[", "").strip()
        
        # Highlight active speaker
        highlight_color = (255, 200, 0, opacity)
        speaker_pos = dp_positions[speaker]
        draw.ellipse([
            speaker_pos[0] - 5, speaker_pos[1] - 5,
            speaker_pos[0] + dp_size[0] + 5, speaker_pos[1] + dp_size[1] + 5
        ], outline=highlight_color, width=3)
        
        # Calculate text position (to the right of the DP)
        text_x = dp_margin + dp_size[0] + text_margin
        text_y = speaker_pos[1]
        text_width = video_width - text_x - text_margin
        
        # Word wrap and draw text
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            w = draw.textlength(" ".join(current_line), font=subtitle_font)
            if w > text_width:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))
        
        for i, line in enumerate(lines):
            draw.text((text_x, text_y + (i * 50)), line,
                     fill=(255, 255, 255, opacity), font=subtitle_font, anchor="lm")
    
    return np.array(frame)

# Create video frames
frames = []
for sub in subs:
    start_frame = sub.start.ordinal // (1000 // fps)
    end_frame = sub.end.ordinal // (1000 // fps)
    
    # Add fade-in effect
    fade_frames = min(15, end_frame - start_frame)
    for i in range(fade_frames):
        opacity = int((i / fade_frames) * 255)
        frames.append(create_frame(sub, fade_in=True, opacity=opacity))
    
    # Add main frames
    for _ in range(start_frame + fade_frames, end_frame):
        frames.append(create_frame(sub))

# Convert frames to video
video = ImageSequenceClip(frames, fps=fps)
audio = AudioFileClip("input/podcast.mp3")
final_video = video.set_audio(audio)

# Export video
final_video.write_videofile("output/podcast.mp4", codec="libx264", fps=fps)
