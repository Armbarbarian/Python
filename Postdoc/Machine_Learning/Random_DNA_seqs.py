import numpy as np
import pandas as pd
import os

# Define the DNA alphabet
dna_alphabet = ['A', 'C', 'G', 'T']

# Function to generate a random DNA sequence of a given length
def generate_random_dna_sequence(length):
    return ''.join(np.random.choice(dna_alphabet, size=length))

# Generate 100 random DNA sequences of length 200bp
sequences = [generate_random_dna_sequence(300) for _ in range(300)]

# Generate random read counts for each sequence
read_counts = np.random.randint(0, 301, size=300)

# Create a Pandas DataFrame to store the sequences and read counts
data = pd.DataFrame({'sequence': sequences, 'read_count': read_counts})
data.head()

# Save the dataset to a CSV file (optional)
data.to_csv('random_dna_sequences_300.csv', index=False)

print("Generated 300 random DNA sequences of length 300bp with random read counts:")
print(data.head())