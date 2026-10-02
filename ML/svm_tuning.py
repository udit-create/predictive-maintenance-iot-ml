import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score


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
# 3. SAME TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 4. SVM CONFIGURATIONS
# ==========================================

configurations = [
    ("SVM C=0.1 gamma=scale",
     SVC(C=0.1, kernel="rbf", gamma="scale")),

    ("SVM C=1 gamma=scale",
     SVC(C=1, kernel="rbf", gamma="scale")),

    ("SVM C=10 gamma=scale",
     SVC(C=10, kernel="rbf", gamma="scale")),

    ("SVM C=100 gamma=scale",
     SVC(C=100, kernel="rbf", gamma="scale")),

    ("SVM C=1 gamma=auto",
     SVC(C=1, kernel="rbf", gamma="auto")),

    ("SVM C=10 gamma=auto",
     SVC(C=10, kernel="rbf", gamma="auto"))
]


# ==========================================
# 5. TRAIN AND EVALUATE
# ==========================================

results = []

print("==========================================")
print("SVM HYPERPARAMETER TUNING")
print("==========================================")

for name, svm in configurations:

    print(f"\nTraining: {name}")

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", svm)
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    macro_f1 = f1_score(
        y_test,
        predictions,
        average="macro"
    )

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Macro F1": macro_f1
    })

    print(f"Accuracy : {accuracy * 100:.2f}%")
    print(f"Macro F1 : {macro_f1:.4f}")


# ==========================================
# 6. RESULTS
# ==========================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Macro F1",
    ascending=False
)

print("\n==========================================")
print("SVM TUNING RESULTS")
print("==========================================")

print(
    results_df.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Macro F1": "{:.4f}".format
        }
    )
)