

###############################################################################
#                           Custom function for G4s - Llama3 70B
###############################################################################


import re
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def detect_g4(sequences):
    g4_data = []
    for seq in sequences:
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

def normalize_read_counts(read_counts):
    log_read_counts = np.log1p(read_counts)
    scaler = MinMaxScaler()
    normalized_read_counts = scaler.fit_transform(log_read_counts.reshape(-1, 1)).flatten()
    return normalized_read_counts


# Separate the sequences and read counts
sequences = data['sequence'].tolist()
read_counts = data['read_count'].tolist()

#
g4_data = detect_g4(sequences)
normalized_read_counts = normalize_read_counts(read_counts)

g4_features = ['num_guanines', 'min_loop_length', 'max_loop_length', 'avg_loop_length', 'gc_content']
fig, axs = plt.subplots(nrows=len(g4_features), ncols=1, figsize=(8, 12))
for i, feature in enumerate(g4_features):
    axs[i].hist([g4[feature] for g4 in g4_data], bins=20)
    axs[i].set_title(feature)
    axs[i].set_xlabel('Value')
    axs[i].set_ylabel('Frequency')
plt.tight_layout()
plt.show()

plt.hist(normalized_read_counts, bins=20)
plt.title('Normalized Read Counts')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()