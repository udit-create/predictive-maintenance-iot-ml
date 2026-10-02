import serial
import time

# ==========================================
# SERIAL CONFIGURATION
# ==========================================

PORT = "COM7"
BAUD_RATE = 115200


# ==========================================
# CONNECT TO NODEMCU
# ==========================================

try:
    ser = serial.Serial(
        PORT,
        BAUD_RATE,
        timeout=1
    )

    time.sleep(2)

    print("======================================")
    print(" AI PREDICTIVE MAINTENANCE SYSTEM")
    print("======================================")
    print()
    print("Connected to NodeMCU on", PORT)
    print("Baud Rate:", BAUD_RATE)
    print("Waiting for sensor data...")
    print("Press Ctrl+C to stop.")
    print()

except serial.SerialException as e:

    print("ERROR: Could not connect to", PORT)
    print("Error:", e)
    exit()


# ==========================================
# READ SERIAL DATA
# ==========================================

try:

    while True:

        data = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not data:
            continue

        print("Received:", data)

        try:

            # Expected:
            # Sound: 512 | Vibration: 1

            parts = data.split("|")

            if len(parts) != 2:
                print("Invalid data format")
                continue

            # ------------------------------
            # SOUND
            # ------------------------------

            sound = int(
                parts[0]
                .split(":")[1]
                .strip()
            )

            # ------------------------------
            # VIBRATION
            # ------------------------------

            vibration = int(
                parts[1]
                .split(":")[1]
                .strip()
            )

            # ------------------------------
            # DISPLAY VALUES
            # ------------------------------

            print(
                f"Sound: {sound} | "
                f"Vibration: {vibration}"
            )

        except (ValueError, IndexError):

            print("Skipping invalid data:", data)


except KeyboardInterrupt:

    print("\nStopping serial reader...")


finally:

    ser.close()

    print("Serial connection closed.")