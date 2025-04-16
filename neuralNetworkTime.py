import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

def selectGamesOf(champion):
    return df[df["champion"] == champion]

df = pd.read_json("output/league_data.json")
df = selectGamesOf("Gwen")

df["hour"] = df["hour"]
df["day_of_week"] = df["dayOfWeek"]

X = df.drop(columns=["win", "champion", "dayOfWeek"])
y = df["win"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize Features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Convert to PyTorch tensors
X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1)  # Reshape to column vector

# Split into Train & Test Sets
X_train, X_test, y_train, y_test = train_test_split(X_tensor, y_tensor, test_size=0.2, random_state=42)

# Define the MLP Model
class MLP(nn.Module):
    def __init__(self, input_size):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)  # First hidden layer
        self.fc2 = nn.Linear(64, 32)  # Second hidden layer
        self.output = nn.Linear(32, 1)  # Output layer
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()  # Sigmoid for binary classification

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.sigmoid(self.output(x))
        return x

# Initialize Model
input_size = X_train.shape[1]
model = MLP(input_size)

# Loss Function & Optimizer
criterion = nn.BCELoss()  # Binary Cross Entropy Loss (for classification)
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training Loop
num_epochs = 20
batch_size = 32

for epoch in range(num_epochs):
    optimizer.zero_grad()  # Clear previous gradients
    outputs = model(X_train)  # Forward pass
    loss = criterion(outputs, y_train)  # Compute loss
    loss.backward()  # Backpropagation
    optimizer.step()  # Update weights

    if (epoch + 1) % 5 == 0:
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

# Evaluate Model
with torch.no_grad():
    y_pred = model(X_test)
    y_pred = (y_pred > 0.5).float()  # Convert probabilities to 0/1 labels
    accuracy = (y_pred.eq(y_test).sum().item()) / y_test.shape[0]
    print(f"Test Accuracy: {accuracy:.2f}")