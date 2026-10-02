/*
  ESP32 Predictive Maintenance System

  Sensors:
  1. Vibration
  2. Temperature
  3. Current
  4. Sound

  Communication:
  ESP32 -> USB Serial -> Python

  Baud Rate:
  115200

  JSON format sent to Python:

  {
    "vibration_rms": 0.52,
    "temperature_c": 35.60,
    "current_a": 2.40,
    "sound_rms": 61.20
  }
*/

void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println(
    "Predictive Maintenance ESP32 Started"
  );
}


void loop() {

  /*
    ----------------------------------------
    SENSOR READINGS
    ----------------------------------------

    Replace these four sections with the
    actual sensor code once your sensors
    are selected.
  */


  // ---------------------------------------
  // 1. VIBRATION SENSOR
  // ---------------------------------------

  float vibration_rms = readVibration();


  // ---------------------------------------
  // 2. TEMPERATURE SENSOR
  // ---------------------------------------

  float temperature_c = readTemperature();


  // ---------------------------------------
  // 3. CURRENT SENSOR
  // ---------------------------------------

  float current_a = readCurrent();


  // ---------------------------------------
  // 4. SOUND SENSOR
  // ---------------------------------------

  float sound_rms = readSound();


  // ---------------------------------------
  // SEND DATA TO PYTHON
  // ---------------------------------------

  Serial.print("{");

  Serial.print("\"vibration_rms\":");
  Serial.print(vibration_rms, 3);

  Serial.print(",");

  Serial.print("\"temperature_c\":");
  Serial.print(temperature_c, 2);

  Serial.print(",");

  Serial.print("\"current_a\":");
  Serial.print(current_a, 2);

  Serial.print(",");

  Serial.print("\"sound_rms\":");
  Serial.print(sound_rms, 2);

  Serial.println("}");


  // Send data every 1 second
  delay(1000);
}


/*
  ========================================
  VIBRATION
  ========================================
*/

float readVibration() {

  /*
    Actual vibration sensor code will go here.

    Example sensors mentioned in your PDF:
    - MPU6050
    - ADXL345

    We will calculate RMS vibration from
    the accelerometer readings.
  */

  return 0.0;
}


/*
  ========================================
  TEMPERATURE
  ========================================
*/

float readTemperature() {

  /*
    Actual temperature sensor code will
    go here.

    The exact sensor has not been specified
    yet.
  */

  return 0.0;
}


/*
  ========================================
  CURRENT
  ========================================
*/

float readCurrent() {

  /*
    Actual current sensor code will
    go here.

    The exact current sensor has not been
    specified yet.
  */

  return 0.0;
}


/*
  ========================================
  SOUND
  ========================================
*/

float readSound() {

  /*
    Actual microphone/acoustic sensor code
    will go here.
  */

  return 0.0;
}