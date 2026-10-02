from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    BASE_DIR
    / "models"
    / "predictive_maintenance_model.pkl"
)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

def load_model():

    if not MODEL_FILE.exists():

        raise FileNotFoundError(
            "Model not found. "
            "Run ML/train_model.py first."
        )

    return joblib.load(
        MODEL_FILE
    )


# --------------------------------------------------
# PREDICT MACHINE CONDITION
# --------------------------------------------------

def predict_condition(
    vibration,
    temperature,
    current,
    sound
):

    model = load_model()

    data = pd.DataFrame(
        [[
            vibration,
            temperature,
            current,
            sound
        ]],
        columns=[
            "vibration_rms",
            "temperature_c",
            "current_a",
            "sound_rms"
        ]
    )

    prediction = model.predict(
        data
    )[0]

    probabilities = model.predict_proba(
        data
    )[0]

    confidence = max(
        probabilities
    ) * 100

    return prediction, confidence


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    # Example sensor values
    vibration = 0.45
    temperature = 35.0
    current = 2.0
    sound = 50.0

    try:

        condition, confidence = predict_condition(
            vibration,
            temperature,
            current,
            sound
        )

        print("----------------------------------------")
        print("   PREDICTIVE MAINTENANCE PREDICTION")
        print("----------------------------------------")

        print(
            f"Vibration    : {vibration:.3f}"
        )

        print(
            f"Temperature  : {temperature:.2f} °C"
        )

        print(
            f"Current      : {current:.2f} A"
        )

        print(
            f"Sound        : {sound:.2f}"
        )

        print("----------------------------------------")

        print(
            f"Prediction   : {condition}"
        )

        print(
            f"Confidence   : {confidence:.2f}%"
        )

        print("----------------------------------------")

    except FileNotFoundError as error:

        print(error)