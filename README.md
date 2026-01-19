# AI Sign Language Translator App

An AI-powered Sign Language Recognition application that captures hand gestures via camera, recognizes sign language using a deep learning model, and converts it into readable text in real time.  
The project focuses on improving communication support for deaf and mute users using LLMs, Media Pipe model and Flutter mobile technologies.

---

## Overview

This project integrates a mobile application with an AI backend to recognize sign language gestures. The system uses computer vision to extract hand landmarks and a trained neural network to predict gestures, which are then converted into meaningful text sentences.

---

## Features

- Real-time hand gesture capture using device camera  
- Hand landmark detection using MediaPipe  
- Deep learning-based gesture recognition  
- Conversion of sign language gestures into text  
- Grammar correction for improved sentence readability  
- Cross-platform mobile interface built with Flutter  
- Python backend for AI inference  

---

## Technologies Used

### Frontend
- Flutter (Dart)
- Camera integration
- REST API communication

### Backend and AI
- Python 3
- TensorFlow / Keras
- MediaPipe
- OpenCV
- NumPy

---

## System Architecture

The Flutter mobile application communicates with a Python backend via REST API.  
The backend processes camera frames using MediaPipe to extract hand landmarks, performs prediction using a trained deep learning model, applies grammar correction, and returns the result to the mobile application.

---

## Project Structure

flutter_app/
├── lib/
└── ui/

backend/
├── main.py
├── model.py
├── data_collection.py
├── my_functions.py

model/
└── sign_language_model.h5


---

## Workflow

1. User performs sign language gestures in front of the camera  
2. Hand landmarks are extracted from video frames  
3. Landmark data is converted into feature vectors  
4. AI model predicts the corresponding gesture  
5. Predicted gestures are combined into sentences  
6. Grammar correction improves output readability  
7. Final text result is displayed on the mobile application  

---

## Model Training

- Gesture data collected using live camera input  
- Hand landmark coordinates used as training features  
- Neural network trained using TensorFlow  
- Model optimized for real-time inference  

---

## Use Cases

- Communication support for deaf and mute users  
- Educational tool for learning sign language  
- Demonstration of AI and mobile application integration  
- Foundation for real-time sign language translation systems  

---

## Challenges and Solutions

- Ensuring real-time performance through optimized frame sampling and preprocessing  
- Improving prediction accuracy using landmark-based feature extraction  
- Integrating mobile and AI systems using REST-based architecture  

---

## Future Enhancements

- Support for additional sign languages  
- Text-to-speech integration  
- Offline inference on mobile devices  
- Cloud deployment for backend services  
- UI and accessibility improvements  

