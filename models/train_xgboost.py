import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier

print("Loading training dataset...")

df = pd.read_csv("dataset/training_dataset.csv")

print(df.shape)

X = df.drop("Label", axis=1)
y = df["Label"]

print("\nFeatures :", X.shape)
print("Labels   :", y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples :", len(X_train))
print("Testing samples  :", len(X_test))

# Scale data
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("\nTraining XGBoost...")

model = XGBClassifier(
    objective="multi:softprob",
    num_class=len(y.unique()),

    n_estimators=300,
    max_depth=8,
    learning_rate=0.1,

    subsample=0.8,
    colsample_bytree=0.8,

    tree_method="hist",

    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training Finished.")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy : {accuracy*100:.2f}%")

joblib.dump(model, "models/xgboost_model.pkl")
joblib.dump(scaler, "models/xgboost_scaler.pkl")

print("\nSaved")
print("models/xgboost_model.pkl")
print("models/xgboost_scaler.pkl")