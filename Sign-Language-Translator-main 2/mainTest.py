from flask import Flask, request, jsonify
import numpy as np
import os
import string
import cv2
from all_functions import *
from tensorflow.keras.models import load_model
import language_tool_python
import pyttsx3

# Initialize Flask app
app = Flask(__name__)

# Load model and configurations
PATH = os.path.join('captured_data')
actions = np.array(os.listdir(PATH))
model = load_model('train_model.keras')
tool = language_tool_python.LanguageToolPublicAPI('en-UK')
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 1)

# Initialize variables
sentence, keypoints, last_prediction, grammar_result = [], [], [], ""

# Flask route for processing camera frames
@app.route('/predict', methods=['POST'])
def predict():
    global keypoints, sentence, last_prediction, grammar_result

    # Check if an image is provided in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # Read the image file
    image_file = request.files['image']
    image = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Process the image
    with mp.solutions.holistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7) as holistic:
        results = image_process(image, holistic)
        draw_landmarks(image, results)
        keypoints.append(keypoint_extraction(results))

        # Perform prediction if 10 frames are accumulated
        if len(keypoints) == 10:
            keypoints_array = np.array(keypoints)
            prediction = model.predict(keypoints_array[np.newaxis, :, :])
            keypoints = []

            if np.amax(prediction) > 0.9:
                detected_action = actions[np.argmax(prediction)]
                if last_prediction != detected_action:
                    sentence.append(detected_action)
                    last_prediction = detected_action
                    grammar_result = tool.correct(' '.join(sentence))
                    tts_engine.say(detected_action)
                    tts_engine.runAndWait()

        # Limit sentence length to 5 words
        if len(sentence) >= 5:
            sentence = []

        # Combine letters into words and grammar-check
        if len(sentence) >= 2:
            if sentence[-1] in string.ascii_lowercase or sentence[-1] in string.ascii_uppercase:
                if sentence[-2] in string.ascii_lowercase or sentence[-2] in string.ascii_uppercase:
                    sentence[-1] = sentence[-2] + sentence[-1]
                    sentence.pop(len(sentence) - 2)
                    sentence[-1] = sentence[-1].capitalize()
                    grammar_result = tool.correct(' '.join(sentence))

        # Generate response
        response = {
            'sentence': ' '.join(sentence).capitalize(),
            'grammar_result': grammar_result,
            'last_prediction': last_prediction
        }
        return jsonify(response)

    return jsonify({'error': 'Processing failed'}), 500

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
