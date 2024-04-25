
# Step 1: Set up the environment and dependencies

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import matplotlib as plt



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



###############################################################################
#                           Custom function for G4s
###############################################################################

import re
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def detect_g4(sequences):
    """
    Detect potential G-quadruplex formations in each sequence.

    Parameters:
    sequences (list): List of DNA sequences

    Returns:
    g4_data (list): List of dictionaries containing G4 features for each sequence
    """
    g4_data = []
    for seq in sequences:
        g4_features = {}
        # Identify potential G4 formations
        g4_patterns = []
        for x in range(2, 5):  # variable x (2-4)
            for y in range(1, 10):  # variable y (highly variable)
                pattern = f"G{{{x}}}[ACGT]{{{y}}}G{{{x}}}[ACGT]{{{y}}}G{{{x}}}[ACGT]{{{y}}}G{{{x}}}"
                matches = re.finditer(pattern, seq)
                for match in matches:
                    g4_patterns.append((match.start(), match.end()))
        # Calculate G4 features for each potential G4
        for start, end in g4_patterns:
            g4_features = {}
            g4_seq = seq[start:end]
            g_tracts = re.findall(r"G+", g4_seq)
            g_tract_lengths = [len(tract) for tract in g_tracts]
            loop_lengths = [len(g4_seq[i:j]) for i, j in zip(g_tracts[:-1], g_tracts[1:])]
            g4_features["num_guanines"] = sum(g_tract_lengths)
            g4_features["loop_lengths"] = loop_lengths
            g4_features["min_loop_length"] = min(loop_lengths)
            g4_features["max_loop_length"] = max(loop_lengths)
            g4_features["avg_loop_length"] = np.mean(loop_lengths)
            g4_features["gc_content"] = sum(c in "GC" for c in g4_seq) / len(g4_seq)
            g4_data.append(g4_features)
    return g4_data

def normalize_read_counts(read_counts):
    """
    Normalize read count data.

    Parameters:
    read_counts (list): List of read counts

    Returns:
    normalized_read_counts (list): List of normalized read counts
    """
    # Log-transform read counts
    log_read_counts = np.log1p(read_counts)
    # Scale read counts to a consistent range (0-1)
    scaler = MinMaxScaler()
    normalized_read_counts = scaler.fit_transform(log_read_counts.reshape(-1, 1)).flatten()
    return normalized_read_counts

# Example usage
sequences = ["ATCGGCTAGCTAGCTAGCTAGC", "TGCTAGCTAGCTAGCTAGCTA", ...]
g4_data = detect_g4(sequences)
read_counts = [10, 20, 30, ...]
normalized_read_counts = normalize_read_counts(read_counts)