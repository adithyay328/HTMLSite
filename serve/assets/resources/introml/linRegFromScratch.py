import random

import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt

def computeGradient(X, y, m, b, method="analytical"):
  """
  This function computes the gradient of the loss
  w.r.t m and b, and returns
  [dL/dm, dL/db]. Method let's you choose
  what method you want to use to compute the
  gradient. Options are "analytical" and "autograd".

  :param X: The input data
  :param y: The target data
  :param m: The slope
  :param b: The intercept
  """
  assert method in ["analytical", "autograd"], "Invalid method, must be 'analytical' or 'autograd'"
  if method == "analytical":
    # Compute the gradient analytically
    dist = y - (m * X + b)

    dL_dm = (-2 * X * dist).mean()
    dL_db = (-2 * dist).mean()
  else:
    # Compute the gradient using autograd
    # in pytorch
    m = torch.tensor(m, requires_grad=True)
    b = torch.tensor(b, requires_grad=True)
    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)
    y_pred = m * X + b
    loss = ((y - y_pred) ** 2).mean()
    loss.backward()
    dL_dm = m.grad
    dL_db = b.grad
  
  return np.array([dL_dm, dL_db])

def visualizeModel(X, y, m, b):
  """
  This function visualizes the model
  and the data.

  :param X: The input data
  :param y: The target data
  :param m: The slope
  :param b: The intercept
  """
  plt.scatter(X, y, label="Data")
  plt.plot(X, m * X + b, color="red", label="Model")
  plt.legend()
  plt.show()

def run():
  # Set all random seeds for reproducibility
  np.random.seed(42)
  torch.manual_seed(42)
  random.seed(42)

  # Load the data
  FNAME = "linear_reg.csv"
  frame = pd.read_csv(FNAME)

  # Print out the first few rows of the data,
  # and describe it
  print(frame.head())
  print()
  print(frame.describe())
  print()

  # Get X and y
  X = np.array(frame['x'].values)
  y = np.array(frame['y'].values)

  # Print shape of X and y
  print(f"X shape: {X.shape}")
  print(f"y shape: {y.shape}")

  # Initialize our weights; we'll sample
  # them from a gaussian distribution
  # for now
  m = np.random.randn()
  b = np.random.randn()

  # Print initial weights
  print(f"Initial weights: m = {m}, b = {b}")

  # Set learning rate
  learning_rate = 0.1

  # Set number of epochs; one epoch
  # is one step of our optimization.
  # In general though(mini-batch, stochastic),
  # more than one update per epoch is done.
  # For now though, we're doing batch gradient
  # descent, which means one update per epoch.
  epochs = 400

  losses = []

  for epcochIdx in range(epochs):
    # Compute the gradient
    grad = computeGradient(X, y, m, b, method="autograd")

    # Update the weights
    m -= learning_rate * grad[0]
    b -= learning_rate * grad[1]

    # Print out the weights
    print(f"Epoch {epcochIdx + 1}: m = {m}, b = {b}")

    # Print out the loss
    y_pred = m * X + b
    loss = ((y - y_pred) ** 2).mean()

    print(f"Epoch {epcochIdx + 1}: Loss = {loss}")

    losses.append(loss)
  
  # Visualize the model
  visualizeModel(X, y, m, b)

  # Plot the loss
  plt.plot(losses)
  plt.xlabel("Epoch")
  plt.ylabel("Loss")
  plt.show()

if __name__ == "__main__":
  run()