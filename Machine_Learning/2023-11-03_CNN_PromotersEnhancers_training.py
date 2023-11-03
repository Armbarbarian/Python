import torch
import torch.nn as nn
import numpy as np
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torchvision import transforms
import pytorch_lightning as pl


# Load and augment data
aug = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
])

sequences = np.loadtxt('MG1655_random_promoter_SAPPHIRE.tsv', delimiter='\t')

sequences = []
for row in promoters:
    sequence = row[0]  # assuming sequence is first column
    sequences.append(sequence)

sequences = np.array(sequences)

sequences = aug(sequences)
labels = ['promoter_MG1655']

# Normalize and split
sequences = StandardScaler().fit_transform(sequences)
train_seqs, val_seqs, test_seqs, train_labels, val_labels, test_labels = split_data(sequences, labels)

# Model using 2D CNN


class Net(pl.LightningModule):

    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(4, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)

        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, padding=2)

        self.fc1 = nn.Linear(64*500, 128)
        self.fc2 = nn.Linear(128, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))

        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# DataLoader, training loop, etc...


# Evaluate on test set
test_acc = trainer.test(test_loader)
print(f'Test Accuracy: {test_acc:.4f}')
