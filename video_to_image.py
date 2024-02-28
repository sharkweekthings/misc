import cv2
import os


def take_screenshots(video_path, base_folder):
    # Ensure the base folder exists, create if it doesn't
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    # Check if the video file exists
    if not os.path.isfile(video_path):
        print(f"Video file {video_path} not found.")
        return

    # Extract video file name and create a directory for screenshots within the base folder
    video_name = os.path.basename(video_path).split('.')[0]
    screenshots_dir = os.path.join(base_folder, video_name)
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    # Get total number of frames and calculate interval
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = total_frames // 30

    # Take 30 screenshots
    for i in range(30):
        frame_number = i * interval
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            # Save the frame as an image file
            screenshot_path = os.path.join(screenshots_dir, f"{i + 1:03d}.png")
            cv2.imwrite(screenshot_path, frame)
            print(f"Saved {screenshot_path}")
        else:
            print(f"Error reading frame {frame_number}")

    # Release the video capture object
    cap.release()
    print("Done.")


# Example usage:
video_path = 'D:/movies/'
base_folder = 'C:/Users/misc/Desktop/movie_trivia/video_flash'
take_screenshots(video_path, base_folder)