from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from PIL import Image
import io
import os
import mediapipe as mp
from tensorflow.keras.models import load_model
import language_tool_python

app = Flask(__name__)

# Initialize variables to store keypoints
keypoints_buffer = []

# Load the trained model
print("Loading model...")
model = load_model('improved_train_model.keras')
print("Model loaded successfully.")

# Create an instance of the grammar correction tool
tool = language_tool_python.LanguageToolPublicAPI('en-UK')

# Define the actions
PATH = os.path.join('captured_data')
actions = np.array(os.listdir(PATH))

"""
    Extract the keypoints from the hand landmarks.
    Args:
        results: The processed results containing hand landmarks.
    Returns:
        keypoints (numpy.ndarray): Flattened keypoints array from both hands.
"""
def keypoint_extraction(results):
    # Extract landmarks for left and right hands, use zeros if not available
    left_hand = np.array([[landmark.x, landmark.y, landmark.z] for landmark in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(63)
    right_hand = np.array([[landmark.x, landmark.y, landmark.z] for landmark in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(63)

    # Concatenate left and right hand keypoints
    keypoints = np.concatenate([left_hand, right_hand])
    return keypoints

# def keypoint_extraction(results):
#     left_hand = np.array([[landmark.x, landmark.y, landmark.z] for landmark in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(63)
#     right_hand = np.array([[landmark.x, landmark.y, landmark.z] for landmark in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(63)
#     keypoints = np.concatenate([left_hand, right_hand])
#     return keypoints

@app.route('/process_frame', methods=['POST'])
def process_frame():
    # Initialize the lists
    sentence, last_prediction, grammar_result = [], [], ""
    global keypoints_buffer
    try:
        data = request.get_json()
        image_data = base64.b64decode(data['image'])
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            image = Image.open(io.BytesIO(image_data))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        mp_holistic = mp.solutions.holistic
        mp_drawing = mp.solutions.drawing_utils

        with mp_holistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7) as holistic:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            results = holistic.process(image_rgb)
            image_rgb.flags.writeable = True
            image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            if results.left_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            if results.right_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            keypoints = keypoint_extraction(results)
            keypoints_buffer.append(keypoints)

            if len(keypoints_buffer) == 10:
                keypoints_array = np.array(keypoints_buffer)
                keypoints_array = keypoints_array.reshape(1, 10, 126)
                prediction = model.predict(keypoints_array)
                keypoints_buffer = []

                if np.amax(prediction) > 0.7:
                    detected_action = actions[np.argmax(prediction)]
                    # if last_prediction != detected_action:
                    # last_prediction = detected_action
                    grammar_result = tool.correct(detected_action)
                    return jsonify({"text": grammar_result if grammar_result else detected_action})
                # else:
            #     return jsonify({""})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

# # from flask import Flask, request, jsonify
# # import cv2
# # import numpy as np
# # import base64
# # from PIL import Image
# # import io

# # app = Flask(__name__)

# # @app.route('/process_image', methods=['POST'])
# # def process_image():
# #     data = request.get_json()
# #     image_data = base64.b64decode(data['image'])
# #     np_arr = np.frombuffer(image_data, np.uint8)
# #     image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

# #     if image is None:
# #         # Fallback to Pillow if OpenCV fails
# #         image = Image.open(io.BytesIO(image_data))
# #         image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# #     # Process the image with OpenCV
# #     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# #     text = "Processed Image"

# #     return jsonify({'text': text})

# # if __name__ == '__main__':
# #     app.run(debug=True)

# import base64
# from io import BytesIO
# import io
# from PIL import Image
# from flask import Flask, request, jsonify
# import numpy as np
# import os
# import mediapipe as mp
# import cv2
# from tensorflow.keras.models import load_model
# import language_tool_python

# app = Flask(__name__)

# # def decode_base64_image(base64_data):
# #     try:
# #         # Check if the base64 string has a valid header
# #         if base64_data.startswith("data:image"):
# #             base64_data = base64_data.split(",")[1]

# #         # Decode the base64 string to bytes
# #         image_bytes = base64.b64decode(base64_data)

# #         # Try loading the image with PIL
# #         image_pil = Image.open(BytesIO(image_bytes))

# #         return image_pil
# #     except Exception as e:
# #         print(f"Error loading image with PIL: {e}")
# #         return None
    
# @app.route('/process_frame', methods=['POST'])
# def process_frame():
#     try:
#         # # Get the base64-encoded image from the request body
#         # data = request.json
#         # base64_image = data.get('image', '')
        
#         # # Ensure base64_image is a valid string
#         # if not base64_image:
#         #     return jsonify({"error": "No image data provided"}), 400

#         # # Decode the image using PIL
#         # pil_image = decode_base64_image(base64_image)
        
#         # if pil_image is None:
#         #     return jsonify({"error": "Failed to decode image"}), 400

#         # # Convert the PIL image to a format OpenCV can handle
#         # image = np.array(pil_image)
#         # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         data = request.get_json()
#         image_data = base64.b64decode(data['image'])
#         np_arr = np.frombuffer(image_data, np.uint8)
#         image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#         if image is None:
#             # Fallback to Pillow if OpenCV fails
#             image = Image.open(io.BytesIO(image_data))
#             image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

#         def keypoint_extraction(results):
#             """
#             Extract the keypoints from the hand landmarks.
#             Args:
#                 results: The processed results containing hand landmarks.
#             Returns:
#                 keypoints (numpy.ndarray): Flattened keypoints array from both hands.
#             """
#             # Extract landmarks for left and right hands, use zeros if not available
#             left_hand = np.array([[landmark.x, landmark.y, landmark.z] for landmark in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(63)
#             right_hand = np.array([[landmark.x, landmark.y, landmark.z] for landmark in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(63)

#             # Concatenate left and right hand keypoints
#             keypoints = np.concatenate([left_hand, right_hand])
#             return keypoints

#         mp_holistic = mp.solutions.holistic  # Holistic model for hand and body tracking
#         mp_drawing = mp.solutions.drawing_utils  # Drawing utilities for visualization

#         # Set the path to the data directory
#         PATH = os.path.join('captured_data')

#         # Create an array of action labels by listing the contents of the data directory
#         actions = np.array(os.listdir(PATH))

#         # Create an instance of the grammar correction tool
#         tool = language_tool_python.LanguageToolPublicAPI('en-UK')

#         # Load the trained model
#         print("Loading model...")
#         model = load_model('train_model.keras')
#         print("Model loaded successfully.")

#         # Create a holistic object for sign prediction
#         with mp.solutions.holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75) as holistic:    
#             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             image_rgb.flags.writeable = False
#             results = holistic.process(image_rgb)
#             image_rgb.flags.writeable = True
#             image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

#             # Draw landmarks for left hand
#             if results.left_hand_landmarks:
#                 mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            
#             # Draw landmarks for right hand
#             if results.right_hand_landmarks:
#                 mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

#             keypoints = keypoint_extraction(results)
#             print(f"Extracted keypoints: {keypoints}")

#             # Reshape to match input shape for the model
#             keypoints = np.array(keypoints).reshape(1, -1)
#             print(f"Reshaped keypoints for model prediction: {keypoints.shape}")

#             # Make a prediction if keypoints are extracted
#             prediction = model.predict(keypoints)
#             print(f"Prediction: {prediction}")

#             # Get the predicted action (sign language detection)
#             detected_action = actions[np.argmax(prediction)]
#             print(f"Detected action: {detected_action}")

#             # Grammar check (if needed)
#             grammar_result = tool.correct(detected_action)
#             print(f"Grammar correction result: {grammar_result}")

#             # Return the result as JSON
#             return jsonify({"text": grammar_result if grammar_result else detected_action})

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)


    