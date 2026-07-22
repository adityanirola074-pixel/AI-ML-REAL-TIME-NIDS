import joblib
import numpy as np

# ============================
# LOAD MODEL
# ============================

model = joblib.load("models/xgboost_model.pkl")
scaler = joblib.load("models/xgboost_scaler.pkl")

EXPECTED_FEATURE_COUNT = model.n_features_in_

# ============================
# ATTACK LABELS
# ============================

attack_labels = {
    0: "Benign",
    1: "Bot",
    2: "DDoS",
    3: "DoS GoldenEye",
    4: "DoS Hulk",
    5: "DoS SlowHTTPTest",
    6: "DoS Slowloris",
    7: "FTP-Patator",
    8: "Heartbleed",
    9: "Infiltration",
    10: "PortScan",
    11: "SSH-Patator",
    12: "Web Attack Brute Force",
    13: "Web Attack SQL Injection",
    14: "Web Attack XSS"
}

# ============================
# RISK TABLE
# ============================

risk_table = {
    "Benign": "LOW",

    "Bot": "MEDIUM",
    "PortScan": "MEDIUM",

    "FTP-Patator": "HIGH",
    "SSH-Patator": "HIGH",

    "Web Attack Brute Force": "HIGH",
    "Web Attack SQL Injection": "HIGH",
    "Web Attack XSS": "HIGH",

    "DoS Hulk": "CRITICAL",
    "DoS GoldenEye": "CRITICAL",
    "DoS SlowHTTPTest": "CRITICAL",
    "DoS Slowloris": "CRITICAL",
    "DDoS": "CRITICAL",

    "Heartbleed": "CRITICAL",
    "Infiltration": "CRITICAL"
}

# ============================
# PREDICT FUNCTION
# ============================

def predict(features):

    print("\nSending flow to AI model...")
    print("FEATURES SENT TO MODEL:")
    print(features)

    sample = np.array(features, dtype=float).reshape(1, -1)

    print("Shape:", sample.shape)
    print("Model expects:", model.n_features_in_)

    sample = scaler.transform(sample)

    prediction = model.predict(sample)[0]

    print("MODEL PREDICTION CLASS:", prediction)

    probabilities = model.predict_proba(sample)[0]

    confidence = float(np.max(probabilities) * 100)

    attack = attack_labels.get(int(prediction), "Unknown")

    risk = risk_table.get(attack, "UNKNOWN")

    return {
        "attack": attack,
        "confidence": round(confidence, 2),
        "risk": risk
    }