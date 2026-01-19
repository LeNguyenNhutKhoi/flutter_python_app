import base64
import cv2
import numpy as np
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        # Get the base64-encoded image from the request body
        data = request.get_json()
        base64_image = data.get('image', '')
        print("Received base64 image data.")
        
        # Decode the base64 string to bytes
        image_bytes = base64.b64decode(base64_image)
        print(f"Base64 image string length: {len(base64_image)}")
        print(f"Decoded image bytes length: {len(image_bytes)}")
        
        # Save the image to a file for further inspection
        image_path = 'received_image.jpg'
        with open(image_path, 'wb') as img_file:
            img_file.write(image_bytes)
        print(f"Image saved as '{image_path}'")

        # Try reading the saved image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Failed to decode image with OpenCV from saved file")

        # If the image is successfully loaded, proceed with further processing
        # Example: Converting to RGB for further processing
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print("Image successfully loaded and converted to RGB.")

        # Further processing here...

        # Return a response (example)
        return jsonify({"message": "Image processed successfully."})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

