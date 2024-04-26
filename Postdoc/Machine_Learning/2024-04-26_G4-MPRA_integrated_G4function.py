# Step 1: Set up the environment and dependencies
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, Flatten, Dense, Dropout, Concatenate
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import re

# Set the working directory to the directory of the current file
os.chdir('C:\\Users\\Danie\\Documents\\Python1\\Python\\Postdoc\\Machine_Learning')


# Function to detect G4 patterns and extract features
'''def detect_g4(sequences):
    print("Number of sequences:", len(sequences))
    g4_data = []
    for seq in sequences:
        print("Processing sequence:", seq)
        g4_features = {}
        g4_patterns = []
        for x in range(2, 5):  # variable x (2-4)
            for y in range(1, 10):  # variable y (highly variable)
                pattern = f"G{{{x}}}[ACGT]{{{y}}}G{{{x}}}[ACGT]{{{y}}}G{{{x}}}[ACGT]{{{y}}}G{{{x}}}"
                matches = re.finditer(pattern, seq)
                for match in matches:
                    start = match.start()
                    end = match.end()
                    g4_patterns.append((start, end))
        for start, end in g4_patterns:
            g4_seq = seq[start:end]
            g_tracts = re.findall(r"G+", g4_seq)
            g_tract_lengths = [len(tract) for tract in g_tracts]
            loop_lengths = [len(g4_seq[i:j]) for i, j in zip([m.end() for m in re.finditer(r"G+", g4_seq)][:-1], [m.start() for m in re.finditer(r"G+", g4_seq)][1:])]
            g4_features["num_guanines"] = sum(g_tract_lengths)
            g4_features["loop_lengths"] = loop_lengths
            g4_features["min_loop_length"] = min(loop_lengths)
            g4_features["max_loop_length"] = max(loop_lengths)
            g4_features["avg_loop_length"] = np.mean(loop_lengths)
            g4_features["gc_content"] = sum(c in "GC" for c in g4_seq) / len(g4_seq)
            g4_data.append(g4_features)
    return g4_data
'''
def detect_g4(sequences):
    print("Number of sequences:", len(sequences))
    g4_data = []
    for seq in sequences:
        print("Processing sequence:", seq)
        g4_features = {}
        g4_patterns = []
        for x in range(2, 5):  # variable x (2-4)
            for y in range(1, 10):  # variable y (highly variable)
                pattern = f"G{{{x}}}[ACGT]{{{y}}}G{{{x}}}[ACGT]{{{y}}}G{{{x}}}[ACGT]{{{y}}}G{{{x}}}"
                matches = re.finditer(pattern, seq)
                for match in matches:
                    start = match.start()
                    end = match.end()
                    g4_patterns.append((start, end))
        print("Number of G4 patterns found:", len(g4_patterns))
        for start, end in g4_patterns:
            g4_seq = seq[start:end]
            g_tracts = re.findall(r"G+", g4_seq)
            g_tract_lengths = [len(tract) for tract in g_tracts]
            loop_lengths = [len(g4_seq[i:j]) for i, j in zip([m.end() for m in re.finditer(r"G+", g4_seq)][:-1], [m.start() for m in re.finditer(r"G+", g4_seq)][1:])]
            g4_features["num_guanines"] = sum(g_tract_lengths)
            g4_features["loop_lengths"] = loop_lengths
            g4_features["min_loop_length"] = min(loop_lengths)
            g4_features["max_loop_length"] = max(loop_lengths)
            g4_features["avg_loop_length"] = np.mean(loop_lengths)
            g4_features["gc_content"] = sum(c in "GC" for c in g4_seq) / len(g4_seq)
            g4_data.append(g4_features)
        print("Number of G4 features appended:", len(g4_data))
    return g4_data






# Step 2: Load and preprocess the data

# Load the data from a CSV file
if os.path.isfile('random_dna_sequences.csv'):
    data = pd.read_csv('random_dna_sequences.csv')
else:
    raise FileNotFoundError("The CSV file 'random_dna_sequences.csv' does not exist.")

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

# Detect G4 patterns and extract features
g4_features = detect_g4(sequences)

# Extract loop_lengths as a separate feature
loop_lengths = [features.pop("loop_lengths") for features in g4_features]

# Find the maximum length of the loop_lengths array
max_loop_length = max(len(lengths) for lengths in loop_lengths)

# Pad the loop_lengths arrays to the maximum length
padded_loop_lengths = [lengths + [0] * (max_loop_length - len(lengths)) for lengths in loop_lengths]

# Convert the g4_features list to a numpy array
g4_features_array = np.array([list(features.values()) for features in g4_features])

# Convert padded_loop_lengths to a numpy array
loop_lengths_array = np.array(padded_loop_lengths)

# Concatenate g4_features_array and loop_lengths_array
g4_features_array = np.concatenate((g4_features_array, loop_lengths_array), axis=1)

print("Shapes of input arrays:")
print("sequence_padded:", sequence_padded.shape)
print("g4_features_array:", g4_features_array.shape)
print("read_counts_normalized:", read_counts_normalized.shape)


# Split the data into training and testing sets
X_train_seq, X_test_seq, X_train_g4, X_test_g4, y_train, y_test = train_test_split(
    sequence_padded, g4_features_array, read_counts_normalized, test_size=0.2, random_state=42)

print("Shapes of training data:")
print("X_train_seq:", X_train_seq.shape)
print("X_train_g4:", X_train_g4.shape)
print("y_train:", y_train.shape)

print("Shapes of testing data:")
print("X_test_seq:", X_test_seq.shape)
print("X_test_g4:", X_test_g4.shape)
print("y_test:", y_test.shape)

# Step 4: Build the CNN model

# Define the CNN model architecture
sequence_input = Input(shape=(max_length,))
conv1d_1 = Conv1D(128, 3, activation='relu')(sequence_input)
conv1d_2 = Conv1D(64, 3, activation='relu')(conv1d_1)
max_pooling1d_1 = MaxPooling1D(2)(conv1d_2)
conv1d_3 = Conv1D(32, 3, activation='relu')(max_pooling1d_1)
max_pooling1d_2 = MaxPooling1D(2)(conv1d_3)

g4_input = Input(shape=(g4_features_array.shape[1],))
merged_input = Concatenate()([max_pooling1d_2, g4_input])

flattened = Flatten()(merged_input)
dense1 = Dense(64, activation='relu')(flattened)
dropout1 = Dropout(0.5)(dense1)
output = Dense(1)(dropout1)

model = Model(inputs=[sequence_input, g4_input], outputs=output)

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Print the model summary
model.summary()

# Step 5: Train the model

# Define early stopping and model checkpointing callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=3)
model_checkpoint = ModelCheckpoint('best_model.h5', save_best_only=True)

# Train the model
batch_size = 32
epochs = 10
history = model.fit([X_train_seq, X_train_g4], y_train, 
                    batch_size=batch_size, epochs=epochs, 
                    validation_split=0.1, 
                    callbacks=[early_stopping, model_checkpoint])

# Step 6: Evaluate the model

# Evaluate the model on the testing set
loss, mae = model.evaluate([X_test_seq, X_test_g4], y_test)
print(f'Test Loss: {loss:.4f}')
print(f'Test MAE: {mae:.4f}')

# Step 7: Make predictions and calculate G4 scores

# Make predictions on the testing set
predictions = model.predict([X_test_seq, X_test_g4])

# Calculate G4 scores based on the predicted read counts
g4_scores = predictions / np.max(predictions)

# Step 8: Visualize the results

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