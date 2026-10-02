import pandas as pd
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import classification_report


# ==========================================
# 1. LOAD DATASET
# ==========================================

dataset_path = r"ML\Dataset\luviner_industrial_faults.csv"

df = pd.read_csv(dataset_path)


# ==========================================
# 2. FEATURES AND TARGET
# ==========================================

features = [
    "vibration_x",
    "vibration_y",
    "vibration_z",
    "temperature",
    "pressure",
    "current",
    "flow_rate",
    "acoustic_db"
]

X = df[features]
y = df["label"]


# ==========================================
# 3. CREATE FINAL SVM PIPELINE
# ==========================================

model = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        C=1,
        kernel="rbf",
        gamma="scale"
    ))
])


# ==========================================
# 4. TRAIN ON COMPLETE DATASET
# ==========================================

print("==========================================")
print("FINAL SVM MODEL TRAINING")
print("==========================================")

print(f"Training samples : {len(X)}")
print(f"Features         : {len(features)}")
print("Model            : SVM")
print("Kernel           : RBF")
print("C                : 1")
print("Gamma            : scale")
print()


model.fit(X, y)


# ==========================================
# 5. SAVE MODEL
# ==========================================

model_path = r"ML\predictive_maintenance_svm.pkl"

joblib.dump(model, model_path)


# ==========================================
# 6. TRAINING DATA PREDICTIONS
# ==========================================

predictions = model.predict(X)

print("Model training completed.")
print(f"Model saved to   : {model_path}")
print()

print("==========================================")
print("TRAINING DATA CLASSIFICATION REPORT")
print("==========================================")

print(
    classification_report(
        y,
        predictions,
        target_names=[
            "normal",
            "bearing_degradation",
            "shaft_imbalance",
            "gear_tooth_crack",
            "misalignment",
            "thermal_runaway",
            "thermal_cycling",
            "electrical_fault",
            "sensor_drift",
            "intermittent_contact",
            "cavitation",
            "blockage",
            "leakage"
        ]
    )
)