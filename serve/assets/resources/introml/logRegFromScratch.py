import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt

from strokeDataset import *

def run():
  X, y = preproc()

  # Init model params for
  # log reg model from gaussian
  feature_dim = X.shape[1]
  m = torch.rand(feature_dim, requires_grad=True)
  b = torch.rand(1, requires_grad=True)

  X = torch.tensor(X, dtype=torch.float32)
  y = torch.tensor(y, dtype=torch.float32)

  # Set epochs
  epochs = 100

  # Set learning rate
  learning_rate = 0.1

  # Keep track of losses
  losses = []

  # Keep track of accuracies
  accs = []

  # Train the model
  for epochIdx in range(epochs):
    # First, get model predictions
    y_pred = torch.sigmoid(torch.matmul(X, m) + b)

    # Compute the loss
    loss = -((y * torch.log(y_pred)) + ((1 - y) * torch.log(1 - y_pred))).mean()

    # Compute the gradient
    loss.backward()

    # Update the weights
    with torch.no_grad():
      m -= learning_rate * m.grad
      b -= learning_rate * b.grad
    
    # Zero the gradients
    m.grad.zero_()
    b.grad.zero_()

    # Print accuracy
    y_pred = torch.round(y_pred)
    acc = (y_pred == y).float().mean()

    losses.append(loss.detach().numpy())
    accs.append(acc.detach().numpy())

    # Print out the loss
    print(f"Epoch {epochIdx + 1}: Loss = {loss}")

    # Print out the accuracy
    print(f"Epoch {epochIdx + 1}: Accuracy = {acc}")
  
  # Visualize losses and accuracies
  plt.plot(losses)
  plt.xlabel("Epoch")
  plt.ylabel("Loss")
  plt.show()

  plt.plot(accs)
  plt.xlabel("Epoch")
  plt.ylabel("Accuracy")

  plt.show()

if __name__ == "__main__":
  run()