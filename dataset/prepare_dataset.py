import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("Loading dataset...")

df = pd.read_csv("dataset/final_dataset.csv")

print("Original Shape:", df.shape)

# -------------------------------------------------
# Features that our live flow generator can produce
# -------------------------------------------------

selected_features = [
    "Protocol",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Fwd Packets Length Total",
    "Bwd Packets Length Total",
    "Flow Bytes/s",
    "Flow Packets/s",
    "SYN Flag Count",
    "ACK Flag Count",
    "Label"
]

df = df[selected_features]

print("Selected Shape:", df.shape)

# -------------------------------------------------
# Remove missing values
# -------------------------------------------------

df = df.replace([float("inf"), -float("inf")], 0)
df = df.fillna(0)

# -------------------------------------------------
# Encode labels
# -------------------------------------------------

encoder = LabelEncoder()

df["Label"] = encoder.fit_transform(df["Label"])

print("\nClasses Found:\n")

for i, label in enumerate(encoder.classes_):
    print(i, "->", label)

# -------------------------------------------------
# Save encoder
# -------------------------------------------------

import joblib
joblib.dump(encoder, "models/label_encoder.pkl")

# -------------------------------------------------
# Save processed dataset
# -------------------------------------------------

df.to_csv(
    "dataset/training_dataset.csv",
    index=False
)

print("\nSaved:")
print("dataset/training_dataset.csv")