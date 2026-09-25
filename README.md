# Waqaya AI

## AI-Powered Preventive Health Intelligence Platform

**Waqaya AI** is an intelligent preventive health platform designed to analyze daily health indicators, detect unusual patterns, estimate potential health risks, and provide personalized preventive insights before small changes develop into more significant warning signs.

The project combines **Data Science, Machine Learning, Explainable AI, health analytics, and interactive visualization** within a unified bilingual platform.

---

## Project Overview

Most health applications focus on displaying isolated measurements such as heart rate, blood pressure, sleep, or daily steps.

Waqaya AI takes a different approach.

Instead of simply displaying health data, the platform analyzes multiple indicators together to build a broader understanding of the user's health pattern.

The system focuses on three main questions:

1. What is normal for this user?
2. Has the user's health pattern changed?
3. Could the change represent an early health risk?

The goal is to transform daily health data into meaningful and understandable preventive intelligence.

---

## Core Features

### Early Risk Analysis
Machine-learning models estimate potential health risks using multiple health and lifestyle indicators.

### Personal Health Baseline
The system calculates a personalized baseline from historical health data and compares new measurements against the user's normal pattern.

### Anomaly Detection
Unusual combinations of health measurements can be identified using anomaly-detection techniques.

### Health Trend Analysis
Waqaya AI analyzes changes in health indicators over time instead of relying only on individual measurements.

### Explainable AI
Feature importance helps explain which health indicators contributed most strongly to the model's analysis.

### Preventive Insights
The platform generates understandable preventive insights based on the user's measurements, lifestyle indicators, and detected patterns.

### Interactive Health Dashboard
The dashboard provides visual analysis of:

- Heart rate
- Blood pressure
- Blood oxygen level
- Sleep duration
- Daily steps
- Water intake
- Urination frequency
- BMI
- Health trends
- Risk indicators

### Diabetes Monitoring
Users with diabetes can manually record glucose readings and review them through tables and visual charts.

### Calorie and Nutrition Calculator
The platform estimates:

- Basal Metabolic Rate (BMR)
- Total Daily Energy Expenditure (TDEE)
- Daily calorie targets
- Macronutrient distribution

### Health Knowledge Search
Users can search common health conditions and symptoms to view educational information about associated symptoms, causes, and risk factors.

### Bilingual Interface
The platform supports both Arabic and English.

---

## Machine Learning Architecture

The machine-learning layer is separated from the user interface through the `WaqayaEngine` architecture.

The engine is responsible for:

- Loading trained models
- Preparing input features
- Risk prediction
- Personal baseline calculation
- Baseline deviation analysis
- Anomaly detection
- Trend analysis
- Feature-importance extraction
- Early-risk score calculation

This modular architecture makes the system easier to maintain, test, and extend.

---

## Model Features

The analytical engine currently processes the following features:

```text
age
gender
systolic_bp
diastolic_bp
heart_rate
spo2
sleep_hours
steps
water_liters
urination
bmi
```

---

## Technology Stack

**Machine Learning**
- Scikit-learn
- Joblib
- Isolation Forest
- Supervised Machine Learning

**Data Analysis**
- Python
- Pandas
- NumPy

**Visualization**
- Plotly

**Application**
- Streamlit

**Development and Version Control**
- Visual Studio Code
- Git
- GitHub

---

## Project Structure

```text
Waqaya-Ai/
│
├── app.py
├── waqaya_engine.py
├── waqaya_models.pkl
├── generate_data.py
├── train_model.py
├── waqaya_health_data.csv
├── requirements.txt
│
├── models/
├── Data/
└── notebooks/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/HadeelAlshammari111/Waqaya_Ai.git
```

Navigate to the project directory:

```bash
cd Waqaya_Ai
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

The application will open in your web browser.

---

## Requirements

The main Python dependencies include:

```text
streamlit
pandas
numpy
plotly
scikit-learn
joblib
```

---

## Data Science Workflow

The development of Waqaya AI follows a structured data-science workflow:

```text
Problem Definition
        ↓
Data Collection
        ↓
Data Preparation
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Machine Learning
        ↓
Model Evaluation
        ↓
Risk Analysis
        ↓
Explainable AI
        ↓
Preventive Insights
        ↓
Interactive Application
```

---

## Project Objective

Waqaya AI explores how artificial intelligence and data science can move health applications beyond passive monitoring toward **preventive health
