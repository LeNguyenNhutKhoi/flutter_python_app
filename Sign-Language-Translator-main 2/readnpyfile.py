import numpy as np
from matplotlib import pyplot as plt

# Load the keypoints data
keypoints = np.load('/Users/maz/VisualStudioCode/projectAIApp/Sign-Language-Translator-main 2/captured_data/hello/0/0.npy')

# Reshape the keypoints into a 2D array for visualization (21 landmarks * 3 coordinates)
keypoints = keypoints.reshape(-1, 3)

# Plot the keypoints
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extract x, y, z coordinates
x = keypoints[:, 0]
y = keypoints[:, 1]
z = keypoints[:, 2]

# Plot the landmarks
ax.scatter(x, y, z, c='r', marker='o')
ax.set_title('3D Landmarks')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

