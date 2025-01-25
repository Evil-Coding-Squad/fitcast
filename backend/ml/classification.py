import numpy as np
import pandas as pd
import os
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Should be a 28x28 greyscale image, represented as a 784-long 1d array
input_image = np.array([])

# Convert to a tensor
input_tensor = torch.tensor(input_image, dtype=torch.float32).reshape(-1, 1, 28, 28)


class SimpleCNN(nn.Module):
    def __init__(self, conv1_out=32, conv2_out=64, fc1_out=128):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, conv1_out, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(conv1_out)
        self.conv2 = nn.Conv2d(conv1_out, conv2_out, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(conv2_out)
        self.fc1 = nn.Linear(conv2_out * 7 * 7, fc1_out)
        self.bn3 = nn.BatchNorm1d(fc1_out)
        self.fc2 = nn.Linear(fc1_out, 10)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.max_pool2d(x, 2)
        x = x.view(x.size(0), -1)
        x = F.relu(self.bn3(self.fc1(x)))
        x = self.fc2(x)
        return x
