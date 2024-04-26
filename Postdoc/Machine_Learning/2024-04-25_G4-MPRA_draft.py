
# Step 1: Set up the environment and dependencies
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import matplotlib as plt


# Get current working directory
current_directory = os.getcwd()

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Get the directory of the current file
current_directory = os.path.dirname(current_file_path)

# Set the working directory to the directory of the current file
os.chdir('C:\\Users\\Danie\\Documents\\Python1\\Python\\Postdoc\\Machine_Learning')

#
print(f"Current working directory: {current_directory}")


# Step 2: Load and preprocess the data


# Load the data from a CSV file
data = pd.read_csv('random_dna_sequences.csv')

# Separate the sequences and read counts
sequences = data['sequence'].tolist()
read_counts = data['read_count'].tolist()

# Tokenize the sequences
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(sequences)
sequence_encoded = tokenizer.texts_to_sequences(sequences)

# Pad the encoded sequences to a fixed length
max_length = max(len(seq) for seq in sequence_encoded)
sequence_padded = pad_sequences(sequence_encoded, maxlen=max_length, padding='post')

# Normalize the read counts
read_counts_normalized = np.log1p(read_counts)


# Step 3: Prepare the data for training and testing


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(sequence_padded, read_counts_normalized, test_size=0.2, random_state=42)


# Step 4: Build the CNN model


# Define the CNN model architecture
model = Sequential([
    Conv1D(128, 3, activation='relu', input_shape=(max_length, 1)),
    Conv1D(64, 3, activation='relu'),
    MaxPooling1D(2),
    Conv1D(32, 3, activation='relu'),
    MaxPooling1D(2),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Print the model summary
model.summary()


# Step 5: Train the model


# Train the model
batch_size = 32
epochs = 10
history = model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)


# Step 6: Evaluate the model


# Evaluate the model on the testing set
loss, mae = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss:.4f}')
print(f'Test MAE: {mae:.4f}')


# Step 7: Make predictions and calculate G4 scores


# Make predictions on the testing set
predictions = model.predict(X_test)

# Calculate G4 scores based on the predicted read counts
g4_scores = predictions / np.max(predictions)


# Step 8: Visualize the results


import matplotlib.pyplot as plt

# Plot the training and validation loss
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Plot the predicted G4 scores
plt.figure(figsize=(10, 6))
plt.scatter(range(len(g4_scores)), g4_scores)
plt.xlabel('Sample Index')
plt.ylabel('G4 Score')
plt.title('Predicted G4 Scores')
plt.show()

