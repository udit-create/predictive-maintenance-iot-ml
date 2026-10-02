import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# ----------------------------------------
# PROJECT PATH
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Import prediction function
from ML.predict import predict_condition

# Dataset file
DATA_FILE = BASE_DIR / "Data" / "sensor_data.csv"

# ----------------------------------------
# PAGE SETTINGS
# ----------------------------------------

st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# ----------------------------------------
# HEADER
# ----------------------------------------

st.title("⚙️ Predictive Maintenance Dashboard")

st.markdown(
    """
    Monitor machine health using:

    - Vibration Sensor
    - Temperature Sensor
    - Current Sensor
    - Sound Sensor
    """
)

st.divider()

# ----------------------------------------
# SENSOR INPUT
# ----------------------------------------

st.subheader("Sensor Values")

col1, col2 = st.columns(2)

with col1:

    vibration = st.number_input(
        "Vibration RMS",
        min_value=0.0,
        value=0.50,
        step=0.01
    )

    current = st.number_input(
        "Current (A)",
        min_value=0.0,
        value=2.00,
        step=0.1
    )

with col2:

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        value=35.00,
        step=0.5
    )

    sound = st.number_input(
        "Sound RMS",
        min_value=0.0,
        value=50.00,
        step=0.1
    )

st.divider()

# ----------------------------------------
# PREDICTION BUTTON
# ----------------------------------------

if st.button("Analyze Machine"):

    try:

        prediction, confidence = predict_condition(
            vibration,
            temperature,
            current,
            sound
        )

        st.subheader("Prediction Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Machine Condition",
                prediction
            )

        with col2:
            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )

        # Status
        if prediction == "NORMAL":

            st.success(
                "✅ Machine is operating normally."
            )

        else:

            st.warning(
                f"⚠️ Fault Detected: {prediction}"
            )

    except Exception as e:

        st.error(str(e))

# ----------------------------------------
# DATASET DISPLAY
# ----------------------------------------

st.divider()

st.subheader("Collected Sensor Data")

if DATA_FILE.exists():

    data = pd.read_csv(DATA_FILE)

    st.dataframe(
        data,
        use_container_width=True
    )

    st.write(
        f"Total Records: {len(data)}"
    )

else:

    st.info(
        "No sensor data available."
    )