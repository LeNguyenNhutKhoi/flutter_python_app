import cv2
import os

def split_video_to_frames(video_path, output_folder, frame_count=200):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")

    # Calculate the interval to sample frames to get exactly 'frame_count' frames
    interval = max(1, total_frames // frame_count)
    print(f"Sampling every {interval} frames.")

    # Initialize frame index and count
    frame_index = 0
    saved_frame_count = 0

    while saved_frame_count < frame_count and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame at the specified interval
        if frame_index % interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count:03d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Saved: {frame_filename}")
            saved_frame_count += 1

        frame_index += 1

    cap.release()
    print(f"Total saved frames: {saved_frame_count}")

# Example usage
video_path = "/Users/maz/VisualStudioCode/projectAIApp/Sign-Language-Translator-main 2/video/hello.mp4"  # Replace with your video file path
output_folder = "/Users/maz/VisualStudioCode/projectAIApp/Sign-Language-Translator-main 2/images"       # Replace with your desired output folder
split_video_to_frames(video_path, output_folder, frame_count=100)
