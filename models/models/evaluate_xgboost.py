import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

print("Loading dataset...")

df = pd.read_csv("dataset/training_dataset.csv")

X = df.drop("Label", axis=1)
y = df["Label"]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

scaler = joblib.load("models/xgboost_scaler.pkl")
model = joblib.load("models/xgboost_model.pkl")

X_test = scaler.transform(X_test)

pred = model.predict(X_test)

print("\nAccuracy")
print("----------------------")
print(accuracy_score(y_test, pred))

print("\nConfusion Matrix")
print("----------------------")
print(confusion_matrix(y_test, pred))

print("\nClassification Report")
print("----------------------")
print(classification_report(y_test, pred))
