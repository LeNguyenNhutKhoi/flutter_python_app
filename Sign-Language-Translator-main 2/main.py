# %% Import necessary libraries
import numpy as np
import os
import string
import mediapipe as mp
import cv2
from all_functions import *  # Custom functions for your project
from tensorflow.keras.models import load_model
import language_tool_python
import pyttsx3  # For text-to-speech functionality

# Set the path to the data directory
PATH = os.path.join('captured_data')

# Create an array of action labels by listing the contents of the data directory
actions = np.array(os.listdir(PATH))

# Load the trained model
model = load_model('improved_train_model.keras')

# Create an instance of the grammar correction tool
tool = language_tool_python.LanguageToolPublicAPI('en-UK')

# Initialize the TTS engine
tts_engine = pyttsx3.init()

# Optional: Configure TTS properties (e.g., voice, speed, volume)
tts_engine.setProperty('rate', 150)  # Speed of speech
tts_engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Initialize the lists
sentence, keypoints, last_prediction, grammar_result = [], [], [], ""

# Access the camera and check if the camera is opened successfully
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot access camera.")
    exit()

# Get the device's screen resolution for scaling
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a holistic object for sign prediction
with mp.solutions.holistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7) as holistic:
    while cap.isOpened():
        # Read a frame from the camera
        _, image = cap.read()

        # Resize the image to fit the mobile screen
        image = cv2.resize(image, (screen_width, screen_height))
        
        # Process the image and obtain sign landmarks using image_process function from my_functions.py
        results = image_process(image, holistic)
        
        # Draw the sign landmarks on the image using draw_landmarks function from my_functions.py
        draw_landmarks(image, results)
        
        # Extract keypoints from the pose landmarks using keypoint_extraction function from my_functions.py
        keypoints.append(keypoint_extraction(results))

        # Check if 10 frames have been accumulated
        if len(keypoints) == 10:
            keypoints = np.array(keypoints)
            prediction = model.predict(keypoints[np.newaxis, :, :])
            keypoints = []

            # Check if the maximum prediction value is above 0.9
            if np.amax(prediction) > 0.9:
                detected_action = actions[np.argmax(prediction)]  # Save the detected action
                if last_prediction != detected_action:
                    sentence.append(detected_action)  # Append the predicted sign to the sentence list
                    last_prediction = detected_action
                    # Automatically grammar-check the updated sentence
                    grammar_result = tool.correct(' '.join(sentence))
                    # Read the detected action aloud
                    tts_engine.say(detected_action)  # Queue the detected action for speaking
                    tts_engine.runAndWait()  # Process the speech queue immediately

        # Limit the sentence length to 5 words and reset automatically
        if len(sentence) >= 5:
            sentence = []  # Reset sentence when it exceeds 5 words

        # Combine letters into words
        if len(sentence) >= 2:
            if sentence[-1] in string.ascii_lowercase or sentence[-1] in string.ascii_uppercase:
                if sentence[-2] in string.ascii_lowercase or sentence[-2] in string.ascii_uppercase or (
                        sentence[-2] not in actions and sentence[-2] not in list(x.capitalize() for x in actions)):
                    sentence[-1] = sentence[-2] + sentence[-1]
                    sentence.pop(len(sentence) - 2)
                    sentence[-1] = sentence[-1].capitalize()

                    # Automatically grammar-check the updated sentence
                    grammar_result = tool.correct(' '.join(sentence))

        # Display the grammar-corrected sentence
        text_to_display = (grammar_result if grammar_result else ' '.join(sentence)).capitalize()
        textsize = cv2.getTextSize(text_to_display, cv2.FONT_HERSHEY_DUPLEX, 1, 2)[0]
        text_X_coord = (image.shape[1] - textsize[0]) // 2
        cv2.putText(image, text_to_display, (text_X_coord, 470),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Show the image on the display
        cv2.imshow('Camera', image)

        # Break the loop if the "Camera" window is closed
        if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
            break

        # Check if 'q' key is pressed to exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting program.")
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

    # Shut off the grammar tool
    tool.close()

