import pandas as pd

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


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
# 3. DEFINE MODELS
# ==========================================

svm_model = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        C=1,
        kernel="rbf",
        gamma="scale"
    ))
])

random_forest = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)


# ==========================================
# 4. 5-FOLD STRATIFIED CROSS-VALIDATION
# ==========================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# ==========================================
# 5. EVALUATE MODELS
# ==========================================

models = {
    "SVM (C=1)": svm_model,
    "Random Forest": random_forest
}

print("==========================================")
print("5-FOLD CROSS-VALIDATION")
print("==========================================")

results = []

for name, model in models.items():

    print(f"\nEvaluating: {name}")

    scores = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring={
            "accuracy": "accuracy",
            "macro_f1": "f1_macro"
        },
        n_jobs=-1
    )

    accuracy_mean = scores["test_accuracy"].mean()
    accuracy_std = scores["test_accuracy"].std()

    f1_mean = scores["test_macro_f1"].mean()
    f1_std = scores["test_macro_f1"].std()

    results.append({
        "Model": name,
        "Accuracy Mean": accuracy_mean,
        "Accuracy Std": accuracy_std,
        "Macro F1 Mean": f1_mean,
        "Macro F1 Std": f1_std
    })

    print(f"Accuracy : {accuracy_mean:.4f} ± {accuracy_std:.4f}")
    print(f"Macro F1 : {f1_mean:.4f} ± {f1_std:.4f}")


# ==========================================
# 6. FINAL RESULTS
# ==========================================

results_df = pd.DataFrame(results)

print("\n==========================================")
print("CROSS-VALIDATION RESULTS")
print("==========================================")

print(
    results_df.to_string(
        index=False,
        formatters={
            "Accuracy Mean": "{:.4f}".format,
            "Accuracy Std": "{:.4f}".format,
            "Macro F1 Mean": "{:.4f}".format,
            "Macro F1 Std": "{:.4f}".format
        }
    )
)