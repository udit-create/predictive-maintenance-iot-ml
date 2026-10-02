import serial
import time
import csv
import os
import requests

# ==============================
# SERIAL SETTINGS
# ==============================

PORT = "COM7"
BAUD_RATE = 115200

# ==============================
# THINGSPEAK SETTINGS
# ==============================

THINGSPEAK_URL = "https://api.thingspeak.com/update"
THINGSPEAK_WRITE_API_KEY = "I7AZNS9CMQ9Q14YI"

UPLOAD_INTERVAL = 15
last_upload_time = 0

# ==============================
# CSV SETTINGS
# ==============================

DATA_DIR = "Data"
CSV_FILE = os.path.join(DATA_DIR, "sensor_data.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# ==============================
# CONNECT TO NODEMCU
# ==============================

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)

    print("======================================")
    print(" AI PREDICTIVE MAINTENANCE SYSTEM")
    print("======================================")
    print()
    print("Connected to NodeMCU on", PORT)
    print("Baud Rate:", BAUD_RATE)
    print("Starting data collection...")
    print("ThingSpeak upload interval:", UPLOAD_INTERVAL, "seconds")
    print("Press Ctrl+C to stop.")
    print()

except serial.SerialException as e:
    print("ERROR: Could not connect to", PORT)
    print("Make sure the NodeMCU is connected.")
    print("Error:", e)
    exit()

# ==============================
# OPEN CSV FILE
# ==============================

file_exists = os.path.exists(CSV_FILE)

with open(CSV_FILE, "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "timestamp",
            "sound",
            "vibration"
        ])

        print("Created:", CSV_FILE)

    # ==============================
    # MAIN LOOP
    # ==============================

    try:

        while True:

            data = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not data:
                continue

            print("\nReceived:")
            print(data)

            try:

                # Example:
                # Sound: 21 | Vibration: 1

                parts = data.split("|")

                if len(parts) != 2:
                    print("Invalid data format. Skipping...")
                    continue

                sound = int(
                    parts[0].split(":")[1].strip()
                )

                vibration = int(
                    parts[1].split(":")[1].strip()
                )

                timestamp = time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                # ==============================
                # SAVE TO CSV
                # ==============================

                writer.writerow([
                    timestamp,
                    sound,
                    vibration
                ])

                file.flush()

                print()
                print("Sensor Data:")
                print("Sound     :", sound)
                print("Vibration :", vibration)

                # ==============================
                # THINGSPEAK UPLOAD
                # ==============================

                current_time = time.time()

                if current_time - last_upload_time >= UPLOAD_INTERVAL:

                    payload = {
                        "api_key": THINGSPEAK_WRITE_API_KEY,
                        "field1": sound,
                        "field2": vibration
                    }

                    try:

                        response = requests.get(
                            THINGSPEAK_URL,
                            params=payload,
                            timeout=10
                        )

                        if response.status_code == 200:

                            if response.text != "0":

                                print()
                                print(
                                    "ThingSpeak: Upload successful"
                                )

                                print(
                                    "Entry ID:",
                                    response.text
                                )

                                last_upload_time = current_time

                            else:

                                print(
                                    "ThingSpeak: Upload failed"
                                )

                        else:

                            print(
                                "ThingSpeak HTTP Error:",
                                response.status_code
                            )

                    except requests.RequestException as e:

                        print(
                            "ThingSpeak connection error:",
                            e
                        )

                else:

                    remaining = int(
                        UPLOAD_INTERVAL -
                        (current_time - last_upload_time)
                    )

                    print(
                        "ThingSpeak upload in approximately",
                        remaining,
                        "seconds"
                    )

            except (ValueError, IndexError):

                print(
                    "Skipping invalid sensor data:",
                    data
                )

    except KeyboardInterrupt:

        print()
        print("======================================")
        print("Data collection stopped.")
        print("======================================")

    finally:

        ser.close()

        print("Serial connection closed.")