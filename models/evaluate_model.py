import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from sklearn.model_selection import train_test_split

# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv("dataset/training_dataset.csv")

# Use the same sample as training
df = df.sample(n=300000, random_state=42)

X = df.drop("Label", axis=1)
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# -----------------------------
# Load scaler
# -----------------------------

scaler = joblib.load("models/scaler.pkl")

X_test = scaler.transform(X_test)

# -----------------------------
# Load model
# -----------------------------

model = joblib.load("models/nids_model.pkl")

pred = model.predict(X_test)

# -----------------------------
# Metrics
# -----------------------------

print("\nAccuracy")
print("----------------------")
print(accuracy_score(y_test, pred))

print("\nConfusion Matrix")
print("----------------------")
print(confusion_matrix(y_test, pred))

print("\nClassification Report")
print("----------------------")
print(classification_report(y_test, pred))