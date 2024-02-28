import cv2
import os


def convert_video_to_pngs(video_path, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the video
    cap = cv2.VideoCapture(video_path)

    frame_count = 0

    while True:
        # Read frame
        ret, frame = cap.read()

        # Break the loop if there are no more frames
        if not ret:
            break

        # Save frame as PNG
        frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_path, frame)

        frame_count += 1

    # Release the video capture object
    cap.release()
    print(f"Finished. Extracted {frame_count} frames.")


# Example usage
video_path = 'E:/download/'
output_dir = 'C:/Users/'
convert_video_to_pngs(video_path, output_dir)