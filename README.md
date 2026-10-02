# AI Predictive Maintenance System

> An IoT and Machine Learning-based system for monitoring industrial equipment and classifying potential machine faults using sensor data.

## Overview

The **AI Predictive Maintenance System** combines IoT-based sensor monitoring, cloud data logging, and machine learning to explore an intelligent approach to industrial equipment fault detection.

The system collects real-time **sound and vibration data** from sensors connected to a NodeMCU ESP8266. Sensor readings are stored locally and can also be uploaded to **ThingSpeak** for cloud-based monitoring.

For machine fault classification, a separate industrial sensor dataset is used to train and evaluate machine learning models. Multiple classification algorithms are compared, followed by hyperparameter tuning and cross-validation to select a model configuration for the project's ML pipeline.

---

## Key Features

- Real-time sound and vibration monitoring using NodeMCU ESP8266
- Serial communication between hardware and Python
- Local sensor data storage in CSV format
- Cloud-based data logging using ThingSpeak
- Industrial fault classification using Machine Learning
- Comparison of multiple ML algorithms
- SVM hyperparameter tuning
- 5-fold stratified cross-validation
- Confusion matrix visualization
- Saved trained ML model using Joblib
- Modular project structure for IoT and ML components

---

## System Architecture

```text
                 ┌─────────────────────┐
                 │   Physical Sensors  │
                 │                     │
                 │  Sound + Vibration  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  NodeMCU ESP8266    │
                 │                     │
                 │ Sensor Acquisition  │
                 └──────────┬──────────┘
                            │
                     Serial / USB
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Python Backend    │
                 │                     │
                 │ Data Collection     │
                 │ CSV Logging         │
                 └───────┬─────┬───────┘
                         │     │
              ┌──────────┘     └──────────┐
              ▼                           ▼
     ┌─────────────────┐        ┌─────────────────┐
     │ Local CSV Data  │        │    ThingSpeak   │
     │                 │        │ Cloud Monitoring │
     └─────────────────┘        └─────────────────┘

                         ML Pipeline
                              │
                              ▼
                 ┌─────────────────────┐
                 │ Industrial Dataset │
                 │ 6,500 samples      │
                 │ 8 sensor features  │
                 │ 13 fault classes   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Model Comparison    │
                 │                     │
                 │ RF / ExtraTrees     │
                 │ Logistic Regression │
                 │ SVM / KNN           │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ SVM Tuning +        │
                 │ Cross Validation    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Final SVM Pipeline  │
                 │ RBF Kernel          │
                 │ C = 1               │
                 │ StandardScaler      │
                 └─────────────────────┘
