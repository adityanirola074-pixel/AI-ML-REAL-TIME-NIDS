import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)
from sklearn.metrics import accuracy_score

print("Loading training dataset...")

df = pd.read_csv("dataset/training_dataset.csv")

print(df.shape)

# -------------------------
# Features and Labels
# -------------------------

X = df.drop("Label", axis=1)
y = df["Label"]

print("\nFeatures:", X.shape)
print("Labels:", y.shape)

# -------------------------
# Train/Test Split
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples :", len(X_test))

# -------------------------
# Feature Scaling
# -------------------------

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -------------------------
# Train Random Forest
# -------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training Finished.")

# -------------------------
# Accuracy
# -------------------------

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print("\nAccuracy:", round(acc * 100, 2), "%")

# -------------------------
# Save Model
# -------------------------

joblib.dump(model, "models/nids_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("\nSaved")

print("models/nids_model.pkl")
print("models/scaler.pkl")