# Import necessary libraries
import os
import numpy as np
import cv2
import mediapipe as mp
from itertools import product
from all_functions import *

# Define the actions (signs) that will be recorded and stored in the dataset
actions = np.array(['my'])

# Define the number of sequences and frames to be recorded for each action
sequences = 20
frames = 10

# Set the path where the dataset will be stored
PATH = os.path.join('captured_data')

# Create directories for each action, sequence, and frame in the dataset
for action, sequence in product(actions, range(sequences)):
    os.makedirs(os.path.join(PATH, action, str(sequence)), exist_ok=True)

# Access the camera and check if the camera is opened successfully
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot access camera.")
    exit()

# Create a MediaPipe Holistic object for hand tracking and landmark extraction
with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    try:
        # Loop through each action and sequence
        for action, sequence in product(actions, range(sequences)):
            # Display a message and wait 1 second before starting the sequence
            _, image = cap.read()
            cv2.putText(image, 'Preparing to record...', (200, 200), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Camera', image)
            cv2.waitKey(1000)  # Wait for 1 second

            # Start recording frames for the current sequence
            for frame in range(frames):
                # Read an image from the camera
                _, image = cap.read()

                # Process the image and extract holistic results
                results = image_process(image, holistic)
                draw_landmarks(image, results)

                # Display text on the image indicating the action and sequence number being recorded
                cv2.putText(image, f'Recording "{action}", Sequence {sequence}, Frame {frame}',
                            (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow('Camera', image)
                cv2.waitKey(1)

                # Extract the landmarks from both hands and save them in arrays
                keypoints = keypoint_extraction(results)
                frame_path = os.path.join(PATH, action, str(sequence), f"{frame}.npy")
                np.save(frame_path, keypoints)

                # Check if the 'Camera' window was closed and exit the program
                if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
                    raise KeyboardInterrupt

                # Stop the program if 'q' is pressed
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Exiting.")
                    raise KeyboardInterrupt

    except KeyboardInterrupt:
        print("Data collection interrupted by user.")

    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()




# # Import necessary libraries
# import os
# import numpy as np
# import cv2
# import mediapipe as mp
# from itertools import product
# from all_functions import *

# # Define the actions (signs) that will be recorded and stored in the dataset
# actions = np.array(['help'])

# # Define the number of sequences and frames to be recorded for each action
# sequences = 30
# frames = 10

# # Set the path where the dataset will be stored
# PATH = os.path.join('captured_data')

# # Create directories for each action, sequence, and frame in the dataset
# for action, sequence in product(actions, range(sequences)):
#     os.makedirs(os.path.join(PATH, action, str(sequence)), exist_ok=True)

# # Access the camera and check if the camera is opened successfully
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Cannot access camera.")
#     exit()

# # Create a MediaPipe Holistic object for hand tracking and landmark extraction
# with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
#     try:
#         # Loop through each action, sequence, and frame to record data continuously
#         for action, sequence, frame in product(actions, range(sequences), range(frames)):
#             # Read an image from the camera
#             _, image = cap.read()

#             # Process the image and extract holistic results
#             results = image_process(image, holistic)
#             draw_landmarks(image, results)

#             # Display text on the image indicating the action and sequence number being recorded
#             cv2.putText(image, f'Recording data for "{action}". Sequence number {sequence}.',
#                         (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
#             cv2.imshow('Camera', image)
#             cv2.waitKey(1)

#             # Extract the landmarks from both hands and save them in arrays
#             keypoints = keypoint_extraction(results)
#             frame_path = os.path.join(PATH, action, str(sequence), f"{frame}.npy")
#             np.save(frame_path, keypoints)

#             # Check if the 'Camera' window was closed and exit the program
#             if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
#                 break

#             # Stop the program if 'q' is pressed
#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('q'):
#                 print("Exiting.")
#                 break

#     finally:
#         # Release the camera and close all OpenCV windows
#         cap.release()
#         cv2.destroyAllWindows()



