import mediapipe as mp
import cv2
import numpy as np

mp_holistic = mp.solutions.holistic  # Holistic model for hand and body tracking
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities for visualization

def draw_landmarks(image, results):
    """
    Draw the landmarks for both hands on the image.
    Args:
        image (numpy.ndarray): The input image.
        results: The landmarks detected by Mediapipe.
    """
    # Draw landmarks for left hand
    if results.left_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    
    # Draw landmarks for right hand
    if results.right_hand_landmarks:
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

def image_process(image, model):
    """
    Process the image and obtain the landmarks using MediaPipe.
    Args:
        image (numpy.ndarray): The input image.
        model: The MediaPipe Holistic object for processing.
    Returns:
        results: The processed results containing sign landmarks.
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False
    results = model.process(image_rgb)
    image_rgb.flags.writeable = True
    image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    return results

def keypoint_extraction(results):
    """
    Extract the keypoints from the hand landmarks.
    Args:
        results: The processed results containing hand landmarks.
    Returns:
        keypoints (numpy.ndarray): Flattened keypoints array from both hands.
    """
    # Extract landmarks for left and right hands, use zeros if not available
    left_hand = np.array([[landmark.x, landmark.y, landmark.z] for landmark in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(63)
    right_hand = np.array([[landmark.x, landmark.y, landmark.z] for landmark in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(63)

    # Concatenate left and right hand keypoints
    keypoints = np.concatenate([left_hand, right_hand])
    return keypoints





