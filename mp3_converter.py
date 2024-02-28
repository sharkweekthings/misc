from pydub import AudioSegment
from pydub.utils import which
import os
import shutil

# Explicitly set the path to ffmpeg and ffprobe
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# If the automatic detection with `which` does not work, you may manually specify the paths:
# For example:
# AudioSegment.converter = "C:/Users/Tort/PycharmProjects/misc/package"
# AudioSegment.ffprobe = "C:/Users/Tort/PycharmProjects/misc/package"

def convert_audio(folder_path):
    # Supported formats to convert from
    formats_to_convert = ['.aiff', '.wav', '.m4a', '.ogg', '.flac']

    for root, dirs, files in os.walk(folder_path):
        # Skip any 'old_audio' subdirectories
        if 'old_audio' in root:
            continue

        for file in files:
            # Check if the file has one of the supported formats
            if any(file.lower().endswith(fmt) for fmt in formats_to_convert):
                full_file_path = os.path.join(root, file)
                # Define the output file name and path (replace extension with .mp3)
                mp3_file = full_file_path.rsplit('.', 1)[0] + '.mp3'

                try:
                    # Load the original audio file
                    audio = AudioSegment.from_file(full_file_path)
                    # Export the loaded audio in MP3 format
                    audio.export(mp3_file, format='mp3')
                    print(f"Converted {file} to MP3.")

                    # Move the original file to the 'old_audio' subfolder
                    old_audio_folder = os.path.join(root, 'old_audio')
                    if not os.path.exists(old_audio_folder):
                        os.makedirs(old_audio_folder)
                    shutil.move(full_file_path, os.path.join(old_audio_folder, file))
                    print(f"Moved {file} to {old_audio_folder}.")

                except Exception as e:
                    print(f"Failed to convert {file}: {e}")

# Example usage
folder_path = 'C:/Users/misc/Desktop/'  # Change this to your folder path
convert_audio(folder_path)
