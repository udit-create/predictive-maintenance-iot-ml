import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


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
# 3. SAME 80/20 SPLIT USED EARLIER
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 4. FINAL SVM CONFIGURATION
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
# 5. TRAIN MODEL
# ==========================================

model.fit(X_train, y_train)


# ==========================================
# 6. PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 7. CLASS NAMES
# ==========================================

class_names = [
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


# ==========================================
# 8. CONFUSION MATRIX
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=list(range(13))
)


# ==========================================
# 9. CREATE COLORFUL CONFUSION MATRIX
# ==========================================

fig, ax = plt.subplots(figsize=(14, 12))

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=class_names
)

display.plot(
    ax=ax,
    cmap="Blues",
    values_format="d",
    colorbar=True
)

plt.title(
    "Confusion Matrix - SVM Predictive Maintenance Model",
    fontsize=16,
    fontweight="bold",
    pad=20
)

plt.xlabel(
    "Predicted Label",
    fontsize=12,
    fontweight="bold"
)

plt.ylabel(
    "True Label",
    fontsize=12,
    fontweight="bold"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()


# ==========================================
# 10. SAVE IMAGE
# ==========================================

output_path = r"ML\svm_confusion_matrix.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("==========================================")
print("CONFUSION MATRIX GENERATED")
print("==========================================")
print(f"Saved to: {output_path}")