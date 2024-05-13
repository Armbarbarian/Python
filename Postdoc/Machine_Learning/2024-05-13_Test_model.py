
'''
Purpose: 
Test the G4-MPRA prediction model from .keras saved file
- Currently not working 2024-05-13

'''

import os
import sys
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt
import pandas as pd
import re

def progress_bar(current, total, bar_length=20):
    filled_length = int(bar_length * current // total)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    percent = round(100 * current / total, 1)
    sys.stdout.write(f'\rProgress: [{bar}] {percent}%')
    sys.stdout.flush()

def detect_g4(sequences):
    g4_data = []
    for seq in sequences:
        g4_features = {}
        g4_patterns = []
        for x in range(2, 5):
            for y in range(1, 10):
                pattern = f"G{{{x}}}[ACGT]{{{y}}}G{{{x}}}[ACGT]{{{y}}}G{{{x}}}[ACGT]{{{y}}}G{{{x}}}"
                matches = re.finditer(pattern, seq)
                for match in matches:
                    start = match.start()
                    end = match.end()
                    g4_patterns.append((start, end))

        if len(g4_patterns) > 0:
            g4_seq = seq[g4_patterns[0][0]:g4_patterns[-1][1]]
            g_tracts = re.findall(r"G+", g4_seq)
            g_tract_lengths = [len(tract) for tract in g_tracts]
            loop_lengths = [len(g4_seq[i:j]) for i, j in zip([m.end() for m in re.finditer(r"G+", g4_seq)][:-1], [m.start() for m in re.finditer(r"G+", g4_seq)][1:])]
            g4_features["num_guanines"] = sum(g_tract_lengths)
            g4_features["loop_lengths"] = loop_lengths
            if loop_lengths:
                g4_features["min_loop_length"] = min(loop_lengths)
                g4_features["max_loop_length"] = max(loop_lengths)
                g4_features["avg_loop_length"] = np.mean(loop_lengths)
            else:
                g4_features["min_loop_length"] = 0
                g4_features["max_loop_length"] = 0
                g4_features["avg_loop_length"] = 0
            if len(g4_seq) > 0:
                g4_features["gc_content"] = sum(c in "GC" for c in g4_seq) / len(g4_seq)
            else:
                g4_features["gc_content"] = 0
        else:
            g4_features["num_guanines"] = 0
            g4_features["loop_lengths"] = []
            g4_features["min_loop_length"] = 0
            g4_features["max_loop_length"] = 0
            g4_features["avg_loop_length"] = 0
            g4_features["gc_content"] = 0

        g4_data.append(g4_features)

    return g4_data


# Load the saved model
model = load_model('2024-05-28_best_model.keras')

# Load the CSV file
csv_file = 'random_dna_sequences_300.csv'  # Replace with the path to your CSV file
data = pd.read_csv(csv_file)

# Extract the sequences from the CSV file
sequences = data['sequence'].tolist()

# Tokenize the sequences
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(sequences)
sequence_encoded = tokenizer.texts_to_sequences(sequences)

# Pad the encoded sequences to a fixed length
max_length = model.input_shape[0][1]  # Get the expected input length from the model
sequence_padded = pad_sequences(sequence_encoded, maxlen=max_length, padding='post')

# Extract G4 features from the sequences
g4_features = detect_g4(sequences)
loop_lengths = [features["loop_lengths"] for features in g4_features]
max_loop_length = max(len(lengths) for lengths in loop_lengths)
padded_loop_lengths = [lengths + [0] * (max_loop_length - len(lengths)) for lengths in loop_lengths]
for features in g4_features:
    features.pop("loop_lengths")
g4_features_array = np.array([list(features.values()) for features in g4_features])
loop_lengths_array = np.array(padded_loop_lengths)
g4_features_array = np.concatenate((g4_features_array, loop_lengths_array), axis=1)

# Pad or truncate g4_features_array to match the expected input shape
expected_shape = model.input_shape[1][1]
if g4_features_array.shape[1] < expected_shape:
    # Pad g4_features_array with zeros
    pad_width = ((0, 0), (0, expected_shape - g4_features_array.shape[1]))
    g4_features_array = np.pad(g4_features_array, pad_width, mode='constant')
else:
    # Truncate g4_features_array to the expected shape
    g4_features_array = g4_features_array[:, :expected_shape]

# Make predictions using the loaded model
print('\nMaking predictions...')
num_sequences = len(sequences)
predictions = []
for i, sequence in enumerate(sequences):
    progress_bar(i + 1, num_sequences)
    prediction = model.predict([np.array([sequence_padded[i]]), np.array([g4_features_array[i]])])
    predictions.append(prediction[0][0])
    time.sleep(0.1)  # Add a small delay for demonstration purposes
print('\nPredictions completed.')

# Print the predicted G4 scores
for i, sequence in enumerate(sequences):
    print(f'Sequence {i+1}: {sequence}')
    print(f'Predicted G4 Score: {predictions[i]:.4f}')
    print('---')

# Create a bar plot of the predicted G4 scores
plt.figure(figsize=(10, 6))
plt.bar(range(len(sequences)), predictions, color='skyblue')
plt.xlabel('Sequence Index')
plt.ylabel('Predicted G4 Score')
plt.title('Predicted G4 Scores for Test Sequences')
plt.xticks(range(len(sequences)), range(1, len(sequences) + 1))
plt.ylim(0, max(predictions) * 1.1)  # Set y-axis limit with a 10% margin
plt.show()