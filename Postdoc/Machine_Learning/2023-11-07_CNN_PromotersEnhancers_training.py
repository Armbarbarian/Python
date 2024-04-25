import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import StandardScaler
from torch.utils.data import Dataset, DataLoader

# Load sequences and labels
data = np.loadtxt('MG1655_random_promoter_SAPPHIRE.tsv', delimiter='\t')
sequences = data[:, -1]  # first column
labels = data[:, 1]  # second column

# One-hot encode sequences
vocab = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
max_len = max([len(seq) for seq in sequences])
encoded_seqs = [[vocab[nuc] for nuc in seq] + [0]*(max_len-len(seq)) for seq in sequences]
encoded_seqs = np.array(encoded_seqs)

# Convert to tensors
encoded_seqs = torch.tensor(encoded_seqs, dtype=torch.long)
labels = torch.tensor(labels, dtype=torch.long)

# Normalize
scaler = StandardScaler()
normalized_seqs = scaler.fit_transform(encoded_seqs)
normalized_seqs = normalized_seqs.reshape(len(normalized_seqs), 4, max_len)  # reshape to (N, C, L)

# Split data
train_seqs, val_seqs, test_seqs = torch.split(normalized_seqs, [int(0.6*len(normalized_seqs)), int(0.2*len(normalized_seqs)), int(0.2*len(normalized_seqs))])
train_labels, val_labels, test_labels = torch.split(labels, [int(0.6*len(labels)), int(0.2*len(labels)), int(0.2*len(labels))])

# Model


class PromoterModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(PromoterModel, self).__init__()
        self.conv1 = nn.Conv1d(input_dim, hidden_dim, kernel_size=8)
        self.pool = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(hidden_dim, hidden_dim, kernel_size=5)
        self.fc1 = nn.Linear(hidden_dim*63, 64)
        self.fc2 = nn.Linear(64, output_dim)
        self.softmax = nn.Softmax(dim=1)  # output activation

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.softmax(self.fc2(x))  # normalize output to probabilities
        return x


model = PromoterModel(input_dim=4, hidden_dim=32, output_dim=2)

# Dataloader and training loop
train_dataset = TensorDataset(train_seqs, train_labels)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

val_dataset = TensorDataset(val_seqs, val_labels)
val_loader = DataLoader(val_dataset, batch_size=32)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10)  # reduce learning rate when validation loss stops improving

for epoch in range(100):
    train_loss = 0
    val_loss = 0
    for batch_seqs, batch_labels in train_loader:
        optimizer.zero_grad()
        predictions = model(batch_seqs)
        loss = loss_fn(predictions, batch_labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
    train_loss /= len(train_loader)
    for batch_seqs, batch_labels in val_loader:
        predictions = model(batch_seqs)
        loss = loss_fn(predictions, batch_labels)
        val_loss += loss.item()
    val_loss /= len(val_loader)
    scheduler.step(val_loss)  # update learning rate based on validation loss
    print(f'Epoch {epoch+1}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')

# Evaluate
test_dataset = TensorDataset(test_seqs, test_labels)
test_loader = DataLoader(test_dataset, batch_size=32)
test_acc = 0
for batch_seqs, batch_labels in test_loader:
    predictions = model(batch_seqs)
    correct = (predictions.argmax(dim=1) == batch_labels).sum().item()
    test_acc += correct
test_acc /= len(test_dataset)
print(f'Test Accuracy: {test_acc:.4f}')
