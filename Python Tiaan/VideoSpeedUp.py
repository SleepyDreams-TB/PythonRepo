from moviepy.editor import VideoFileClip, vfx
import os

# Set up paths
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
input_file = "wallpaper.mp4"  # Replace with your video file name
input_path = os.path.join(desktop_path, input_file)
output_file = "output_sped_up.mp4"  # Output file name
output_path = os.path.join(desktop_path, output_file)

# Speed-up factor (15 seconds to 2 seconds)
speed_factor = 15 / 2

try:
    # Load the video
    video = VideoFileClip(input_path)

    # Apply the speed-up effect
    sped_up_video = video.fx(vfx.speedx, factor=speed_factor)

    # Save the sped-up video
    sped_up_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Video successfully saved to {output_path}")

except FileNotFoundError:
    print(f"File not found: {input_path}")
except Exception as e:
    print(f"An error occurred: {e}")
