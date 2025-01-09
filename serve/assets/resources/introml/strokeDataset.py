# Defines some utils for the stroke dataset
import random

import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

FNAME = "healthcare-dataset-stroke-data.csv"

def printStats(frame = None):
  """
  Loads our dataset,
  and prints some basic summary
  stats about it
  """
  if frame is None:
    frame = pd.read_csv(FNAME)

  print(frame.head())
  print()
  print(frame.describe())
  print()
  # Count nans
  print(frame.isna().sum())

def preproc():
  """
  Pre-processes the data,
  doing the following:
  1. Drop BMI, there are NaNs there
  2. Drop ID, it's not useful
  3. Scale all numerical values
     to between 0 and 1
  4. Encode all the categorical variables
     as labels(not one-hot, no need)
  """
  frame = pd.read_csv(FNAME)

  # Drop bmi column
  frame = frame.drop(columns=["bmi"])

  # Drop id column
  frame = frame.drop(columns=["id"])

  # Scale all numerical values using
  # Sklearn's MinMaxScaler
  scaler = MinMaxScaler()
  for col in frame.columns:
    if frame[col].dtype != "object":
      frame[col] = scaler.fit_transform(frame[[col]])
  
  # Encode all categorical variables
  # using sklearn's LabelEncoder
  encoder = LabelEncoder()
  for col in frame.columns:
    if frame[col].dtype == "object":
      frame[col] = encoder.fit_transform(frame[col])
  
  # Print stats of transformed data
  printStats(frame)

  # Take as x the concatentation
  # of everything except stroke
  X = np.array(frame.drop(columns=["stroke"]).values)
  y = np.array(frame["stroke"].values)

  # Print x shape, y shape
  print(f"X shape: {X.shape}")
  print(f"y shape: {y.shape}")

  return X, y

# printStats()
preproc()