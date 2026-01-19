# import os
# import numpy as np
# from sklearn.model_selection import train_test_split
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Dropout
# from tensorflow.keras.callbacks import EarlyStopping, TensorBoard, ReduceLROnPlateau
# from tensorflow.keras.utils import to_categorical
# from itertools import product
# import datetime

# # Load actions and data
# PATH = os.path.join('captured_data')
# actions = np.array(os.listdir(PATH))
# sequences = 20
# frames = 10
# label_map = {label: num for num, label in enumerate(actions)}

# landmarks, labels = [], []
# for action, sequence in product(actions, range(sequences)):
#     temp = []
#     for frame in range(frames):
#         npy = np.load(os.path.join(PATH, action, str(sequence), f"{frame}.npy"))
#         temp.append(npy)
#     landmarks.append(temp)
#     labels.append(label_map[action])

# X = np.array(landmarks)
# Y = to_categorical(labels).astype(int)

# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10, random_state=42, stratify=Y)

# # Model architecture
# # model = Sequential([
# #     LSTM(32, return_sequences=True, activation='relu', input_shape=(frames, 126)),
# #     LSTM(64, return_sequences=True, activation='relu'),
# #     LSTM(32, return_sequences=False, activation='relu'),
# #     Dense(32, activation='relu'),
# #     Dense(actions.shape[0], activation='softmax')
# # ])
# model = Sequential([
#     LSTM(32, return_sequences=True, activation='relu', input_shape=(frames, 126)),
#     Dropout(0.2),
#     LSTM(64, return_sequences=True, activation='relu'),
#     Dropout(0.2),
#     LSTM(32, return_sequences=False, activation='relu'),
#     Dropout(0.2),
#     Dense(32, activation='relu'),
#     Dense(actions.shape[0], activation='softmax')
# ])

# model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# # TensorBoard
# # log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# # tensorboard_callback = TensorBoard(log_dir=log_dir)
# # early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
# log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# tensorboard_callback = TensorBoard(log_dir=log_dir)
# early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
# reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)

# # Train the model
# # model.fit(X_train, Y_train, epochs=100, validation_split=0.1, callbacks=[tensorboard_callback, early_stopping], verbose=1)
# model.fit(X_train, Y_train, epochs=100, validation_split=0.1, callbacks=[tensorboard_callback, early_stopping, reduce_lr], verbose=1)

# # Save the model
# model.save('train_model.keras')

# # Evaluate model
# predictions = np.argmax(model.predict(X_test), axis=1)
# accuracy = np.mean(predictions == np.argmax(Y_test, axis=1))
# print(f"Test Accuracy: {accuracy:.2%}")



import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from tensorflow.keras.utils import to_categorical
from itertools import product
import datetime

# Load actions and data
PATH = os.path.join('captured_data')
actions = np.array(os.listdir(PATH))
sequences = 20
frames = 10
label_map = {label: num for num, label in enumerate(actions)}

# Load dataset
landmarks, labels = [], []
for action, sequence in product(actions, range(sequences)):
    temp = []
    for frame in range(frames):
        npy = np.load(os.path.join(PATH, action, str(sequence), f"{frame}.npy"))
        temp.append(npy)
    landmarks.append(temp)
    labels.append(label_map[action])

X = np.array(landmarks)
Y = to_categorical(labels).astype(int)

# Split dataset
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10, random_state=42, stratify=Y)

# Model architecture
model = Sequential([
    LSTM(64, return_sequences=True, activation='relu', input_shape=(frames, X.shape[2])),
    BatchNormalization(),
    Dropout(0.3),
    LSTM(128, return_sequences=True, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),
    LSTM(64, return_sequences=False, activation='relu'),
    Dense(64, activation='relu'),
    Dense(actions.shape[0], activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# Callbacks
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = TensorBoard(log_dir=log_dir)
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Train model
history = model.fit(
    X_train, Y_train, 
    epochs=200, 
    validation_split=0.1, 
    callbacks=[tensorboard_callback, early_stopping], 
    verbose=1
)

# Save model
model.save('improved_train_model.keras')

# Evaluate model
predictions = np.argmax(model.predict(X_test), axis=1)
true_labels = np.argmax(Y_test, axis=1)

# Test Accuracy
accuracy = np.mean(predictions == true_labels)
print(f"Test Accuracy: {accuracy:.2%}")

# Classification Report
# print("\nClassification Report:")
# print(classification_report(true_labels, predictions, target_names=actions))

# Confusion Matrix
# conf_matrix = confusion_matrix(true_labels, predictions)
# plt.figure(figsize=(10, 8))
# sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=actions, yticklabels=actions)
# plt.xlabel('Predicted')
# plt.ylabel('True')
# plt.title('Confusion Matrix')
# plt.show()








# import os
# import numpy as np
# from sklearn.model_selection import train_test_split
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
# from tensorflow.keras.utils import to_categorical
# import datetime

# # Paths and configurations
# PATH = os.path.join('captured_data')
# actions = np.array(os.listdir(PATH))  # Actions as folder names
# frames_per_sequence = 10  # Number of frames per sequence
# label_map = {label: num for num, label in enumerate(actions)}

# # Data loading
# landmarks, labels = [], []
# for action in actions:
#     action_path = os.path.join(PATH, action)
#     files = sorted([f for f in os.listdir(action_path) if f.endswith('.npy')])  # Sorted list of .npy files
#     for i in range(0, len(files) - frames_per_sequence + 1, frames_per_sequence):
#         temp = []
#         for j in range(frames_per_sequence):
#             frame_path = os.path.join(action_path, files[i + j])
#             npy = np.load(frame_path)  # Load the .npy file
#             temp.append(npy)
#         landmarks.append(temp)  # Append the sequence
#         labels.append(label_map[action])  # Append the corresponding label

# # Convert to NumPy arrays
# X = np.array(landmarks)  # Shape: (num_sequences, frames_per_sequence, keypoints)
# Y = to_categorical(labels).astype(int)  # One-hot encoded labels

# # Train-test split
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10, random_state=42, stratify=Y)

# # Model architecture
# model = Sequential([
#     LSTM(32, return_sequences=True, activation='relu', input_shape=(frames_per_sequence, X.shape[2])),
#     LSTM(64, return_sequences=True, activation='relu'),
#     LSTM(32, return_sequences=False, activation='relu'),
#     Dense(32, activation='relu'),
#     Dense(actions.shape[0], activation='softmax')
# ])

# # Compile the model
# model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# # TensorBoard and EarlyStopping
# log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# tensorboard_callback = TensorBoard(log_dir=log_dir)
# early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# # Train the model
# model.fit(X_train, Y_train, epochs=100, validation_split=0.1, callbacks=[tensorboard_callback, early_stopping], verbose=1)

# # Save the model
# model.save('train_model.keras')





