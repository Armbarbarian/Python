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
            # If no G4 patterns are found, append a dictionary with default values
            g4_features["num_guanines"] = 0
            g4_features["loop_lengths"] = []
            g4_features["min_loop_length"] = 0
            g4_features["max_loop_length"] = 0
            g4_features["avg_loop_length"] = 0
            g4_features["gc_content"] = 0
        
        g4_data.append(g4_features)
        print("Number of G4 features appended:", len(g4_data))
    
    return g4_data

# Step 2: Load and preprocess the data

# Load the data from a CSV file
if os.path.isfile('random_dna_sequences_300.csv'):
    data = pd.read_csv('random_dna_sequences_300.csv')
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
loop_lengths = [features["loop_lengths"] for features in g4_features]

# Find the maximum length of the loop_lengths array
max_loop_length = max(len(lengths) for lengths in loop_lengths)

# Pad the loop_lengths arrays to the maximum length
padded_loop_lengths = [lengths + [0] * (max_loop_length - len(lengths)) for lengths in loop_lengths]

# Remove the "loop_lengths" key from the g4_features dictionaries
for features in g4_features:
    features.pop("loop_lengths")

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
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, Flatten, Dense, Dropout, Concatenate, Reshape

# Define the CNN model architecture
sequence_input = Input(shape=(max_length,))
sequence_input_reshaped = Reshape((max_length, 1))(sequence_input)  # Reshape the input
conv1d_1 = Conv1D(128, 3, activation='relu')(sequence_input_reshaped)
conv1d_2 = Conv1D(64, 3, activation='relu')(conv1d_1)
max_pooling1d_1 = MaxPooling1D(2)(conv1d_2)
conv1d_3 = Conv1D(32, 3, activation='relu')(max_pooling1d_1)
max_pooling1d_2 = MaxPooling1D(2)(conv1d_3)
flattened_sequence = Flatten()(max_pooling1d_2)  # Flatten the output of max_pooling1d_2

g4_input = Input(shape=(g4_features_array.shape[1],))
merged_input = Concatenate()([flattened_sequence, g4_input])  # Concatenate flattened_sequence with g4_input

dense1 = Dense(64, activation='relu')(merged_input)
dropout1 = Dropout(0.5)(dense1)
output = Dense(1)(dropout1)

model = Model(inputs=[sequence_input, g4_input], outputs=output)

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Print the model summary
model.summary()

# Step 5: Train the model

# Define early stopping and model checkpointing callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=5)
model_checkpoint = ModelCheckpoint('best_model.keras', save_best_only=True)

# Train the model
batch_size = 32
epochs = 30
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

# Correlations
from sklearn.metrics import r2_score
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# Calculate R-squared (R^2) score
r2 = r2_score(y_test, predictions)
print(f'R-squared (R^2) score: {r2:.4f}')

# Reshape the arrays to 1D
y_test_1d = y_test.reshape(-1)
predictions_1d = predictions.reshape(-1)

# Calculate Pearson correlation coefficient
pearson_corr, _ = pearsonr(y_test_1d, predictions_1d)
print(f'Pearson correlation coefficient: {pearson_corr:.4f}')

# Create a scatter plot of predicted G4 scores vs. actual G4 scores
plt.figure(figsize=(8, 8))
plt.scatter(y_test_1d, predictions_1d, alpha=0.5)
plt.plot([y_test_1d.min(), y_test_1d.max()], [y_test_1d.min(), y_test_1d.max()], 'r--', lw=2)
plt.xlabel('Actual G4 Scores')
plt.ylabel('Predicted G4 Scores')
plt.title('Predicted G4 Scores vs. Actual G4 Scores')
plt.text(0.1, 0.9, f'R-squared = {r2:.4f}', transform=plt.gca().transAxes)
plt.text(0.1, 0.85, f'Pearson Corr = {pearson_corr:.4f}', transform=plt.gca().transAxes)
plt.show()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Test on new sequences
# Prepare the input sequences
input_sequences = [
    'CTGTGACTCCCGTACGGCTGGCCACAACGACATCCTCAGTCGGCTCCGACGGCTGCCCTGCAACTGACGATTTACCTGTAGCGTAGGGAGGTCGGGAAGGGGCGTGAGGATAGCCAATGAAGAATTCCAGGGTGGATAGGGCTTGATGCTTTTGCGCGGTATGTGTACTAAATATGGCGGATAACAATCTACGTCTGCGGAAGGGGACCCGGTAAGGGCTTCTGTGCCATATCAATGAAAACGCCCGTATATCGACAGCGGGTCGCCATTATATAGTGCTTGCGTGTTGATATGTGTACG',
    'GGGAGCGGGCTGGGCTGGGCCGGGCGCGATGGTCGGGTCTAGCCATATTACCCTGACTGAGCTACTTCATTGCAATTGTTGTTGTTGCAACTGTAATTTCTTTGCCTTAACAAGAGTGGTGATGGAGTGAGGAAGAACTTCAGAGAAAAACACCCAGTTCTCAAAAGTTTGTTTTTAGTCGTGAAATTGTTGAACAATTGACAAACAACAGATGGAGACAAAGGAAATTGGTTTTTCCAGGCATTGAATGTCTTATGAACACTGACACTTCTGCATGGGACTGTCCAGATGAG',
    # Add more sequences as needed
]

# Preprocess the input sequences
input_sequences_tokenized = tokenizer.texts_to_sequences(input_sequences)
input_sequences_padded = pad_sequences(input_sequences_tokenized, maxlen=max_length, padding='post')

# Extract G4 features from the input sequences
input_g4_features = detect_g4(input_sequences)
input_loop_lengths = [features["loop_lengths"] for features in input_g4_features]
input_padded_loop_lengths = [lengths + [0] * (max_loop_length - len(lengths)) for lengths in input_loop_lengths]
for features in input_g4_features:
    features.pop("loop_lengths")
input_g4_features_array = np.array([list(features.values()) for features in input_g4_features])
input_loop_lengths_array = np.array(input_padded_loop_lengths)
input_g4_features_array = np.concatenate((input_g4_features_array, input_loop_lengths_array), axis=1)

# Make predictions using the trained model
input_predictions = model.predict([input_sequences_padded, input_g4_features_array])

# Print the predicted G4 scores
for i, sequence in enumerate(input_sequences):
    print(f'Sequence {i+1}: {sequence}')
    print(f'Predicted G4 Score: {input_predictions[i][0]:.4f}')
    print('---')


# Create a bar plot of the predicted G4 scores
plt.figure(figsize=(10, 6))
plt.bar(range(len(input_sequences)), input_predictions.flatten(), color='skyblue')
plt.xlabel('Sequence Index')
plt.ylabel('Predicted G4 Score')
plt.title('Predicted G4 Scores for Input Sequences')
plt.xticks(range(len(input_sequences)), range(1, len(input_sequences) + 1))
plt.ylim(0, max(input_predictions.flatten()) * 1.1)  # Set y-axis limit with a 10% margin
plt.show()