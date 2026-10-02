import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score, f1_score


# ==========================================
# 1. LOAD DATASET
# ==========================================

dataset_path = r"ML\Dataset\luviner_industrial_faults.csv"

df = pd.read_csv(dataset_path)

print("Dataset loaded successfully.")
print("Shape:", df.shape)


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
# 3. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 4. DEFINE MODELS
# ==========================================

models = {

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(
            max_iter=2000,
            random_state=42
        ))
    ]),

    "SVM": Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVC(
            kernel="rbf",
            random_state=42
        ))
    ]),

    "KNN": Pipeline([
        ("scaler", StandardScaler()),
        ("model", KNeighborsClassifier(
            n_neighbors=5
        ))
    ])
}


# ==========================================
# 5. TRAIN AND COMPARE
# ==========================================

results = []

print("\n==========================================")
print("MODEL COMPARISON")
print("==========================================")

for name, model in models.items():

    print(f"\nTraining {name}...")

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
# 6. DISPLAY FINAL RESULTS
# ==========================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Macro F1",
    ascending=False
)

print("\n==========================================")
print("FINAL COMPARISON")
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