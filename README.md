
# Waqaya AI
### AI-Powered Preventive Health Intelligence Platform

**From Health Data to Preventive Intelligence**

Waqaya AI is an end-to-end Data Science and Machine Learning platform designed to analyze daily health indicators, identify unusual patterns, estimate potential health risks, and provide personalized preventive insights.

The platform combines predictive modeling, anomaly detection, personal health baselines, explainable AI, and interactive dashboards within a bilingual Arabic-English application.

### Live Demo

**[🚀 Launch Waqaya AI](https://waqiya-ai-app.streamlit.app)**

**Deployment:** Streamlit Community Cloud  
**Status:** Deployed and accessible online  
**Developer:** Hadeel Mohammad Alshammari  
**Field:** Data Science | Machine Learning | AI

---

## 1. Project Overview

Traditional health applications primarily display isolated measurements such as heart rate, blood pressure, sleep duration, and daily steps.

Waqaya AI explores a more intelligent approach by analyzing multiple health and lifestyle indicators together to identify meaningful changes and estimate potential risks.

The platform addresses three fundamental questions:

1. What is normal for this user?
2. How has the user's health pattern changed?
3. Could these changes indicate a potential health risk?

The objective is to transform daily measurements into understandable, data-driven preventive insights.

---

## 2. Key Features

### Predictive Health Risk Analysis

Machine-learning models evaluate health and lifestyle indicators to estimate potential health risks.

The experimental prediction modules include:

- Diabetes risk estimation
- Dehydration risk estimation

### Personal Health Baseline

The platform establishes a personal baseline using available historical measurements and compares new observations against the user's typical patterns.

### Anomaly Detection

Anomaly-detection techniques identify unusual combinations of health indicators that may require attention.

### Health Trend Analysis

The system analyzes changes in health indicators over time rather than relying exclusively on individual measurements.

### Explainable AI

Feature-importance analysis helps users understand which input indicators contribute to model predictions.

### Preventive Insights

The platform generates educational, data-driven observations based on measurements, risk estimates, and detected patterns.

### Interactive Health Dashboard

Waqaya AI visualizes indicators including:

- Heart rate
- Blood pressure
- Blood oxygen saturation (SpO2)
- Sleep duration
- Daily steps
- Water consumption
- Urination frequency
- Body Mass Index (BMI)
- Health trends
- Estimated risk indicators

### Diabetes Monitoring

Users can manually enter glucose readings and review the recorded measurements through tables and interactive charts.

### Calorie and Nutrition Calculator

The application provides estimates for:

- Basal Metabolic Rate (BMR)
- Total Daily Energy Expenditure (TDEE)
- Daily calorie requirements
- Macronutrient distribution

### Health Knowledge Search

An educational search feature provides information about common health conditions, symptoms, possible causes, and associated risk factors.

### Bilingual User Interface

The application supports Arabic and English to improve accessibility and usability.

---

## 3. Dataset

The project was developed using an experimental synthetic dataset containing:

**10,000 records and 15 columns**

The data represents simulated demographic, lifestyle, and health measurements.

The machine-learning engine uses features including:

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

### Data Preparation

The development workflow involved:

- Data generation and preparation
- Data quality and consistency checks
- Exploratory Data Analysis (EDA)
- Feature selection and preprocessing
- Model training and evaluation
- Integration with the prediction engine

**Note:** The dataset is synthetic and does not represent a clinically validated patient population.

---

## 4. Machine Learning Performance

Waqaya AI includes experimental machine-learning models developed to estimate health-related risks using multiple input indicators.

### Model Evaluation Results

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Diabetes Risk | 83.85% | 45.34% | 37.33% | 0.410 | 0.778 |
| Dehydration Risk | 88.90% | 81.55% | 73.64% | 0.774 | 0.887 |

### Performance Interpretation

**Diabetes Risk Model**

- Achieved 83.85% accuracy.
- Obtained a ROC-AUC score of 0.778.
- Demonstrated limitations in precision and recall, indicating the need for further improvement before any real-world use.

**Dehydration Risk Model**

- Achieved 88.90% accuracy.
- Obtained a ROC-AUC score of 0.887.
- Demonstrated stronger classification performance on the experimental dataset.

These results describe evaluation on synthetic data only.

They do not demonstrate clinical validity, diagnostic accuracy in real patients, or suitability for medical decision-making.

---

## 5. Machine Learning Architecture

Waqaya AI separates the analytical engine from the application interface through a modular architecture.

The `WaqayaEngine` component is responsible for:

- Loading trained machine-learning models
- Preparing and validating input features
- Generating risk predictions
- Establishing personal health baselines
- Measuring deviations from baseline values
- Detecting anomalous observations
- Analyzing health trends
- Extracting feature-importance information
- Calculating early-risk indicators

### Application Workflow

```text
User Health Inputs
        |
        v
Data Preparation
        |
        v
Feature Processing
        |
        v
Machine Learning Engine
        |
        +--------------------+
        |                    |
        v                    v
Risk Prediction      Anomaly Detection
        |                    |
        +---------+----------+
                  |
                  v
       Baseline and Trend Analysis
                  |
                  v
        Explainable Insights
                  |
                  v
       Interactive Dashboard
```

The modular design supports maintainability and future development.

---

## 6. Technology Stack

### Programming and Data Analysis

- Python
- Pandas
- NumPy

### Machine Learning

- Scikit-learn
- Joblib
- Supervised machine learning
- Isolation Forest

### Data Visualization

- Plotly

### Application Development

- Streamlit

### Development and Version Control

- Visual Studio Code
- Git
- GitHub

### Cloud Deployment

- Streamlit Community Cloud

---

## 7. Project Structure

```text
Waqaya-Ai/
|
|-- app.py
|-- waqaya_engine.py
|-- waqaya_models.pkl
|-- generate_data.py
|-- train_model.py
|-- waqaya_health_data.csv
|-- requirements.txt
|-- README.md
|
|-- models/
|-- Data/
|-- notebooks/
```

### Main Components

**app.py**  
Implements the interactive user interface, dashboards, user inputs, and visualization components.

**waqaya_engine.py**  
Contains the analytical functionality supporting machine-learning inference and health-pattern analysis.

**train_model.py**  
Supports machine-learning model training and evaluation.

**generate_data.py**  
Supports synthetic dataset generation.

**waqaya_models.pkl**  
Stores serialized machine-learning model artifacts.

**requirements.txt**  
Defines the Python package dependencies required to run the application.

---

## 8. Data Science Workflow

The project follows a structured machine-learning development lifecycle.

```text
Problem Definition
        |
        v
Synthetic Data Generation
        |
        v
Data Preparation
        |
        v
Exploratory Data Analysis
        |
        v
Feature Engineering
        |
        v
Model Development
        |
        v
Model Evaluation
        |
        v
Risk Analysis
        |
        v
Explainable AI
        |
        v
Application Development
        |
        v
Cloud Deployment
```

This workflow demonstrates the integration of data science, machine learning, and application development into a working prototype.

---

## 9. Installation and Local Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/HadeelAlshammari111/Waqaya_Ai.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Waqaya_Ai
```

### Step 3: Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application should open in your default web browser.

---

## 10. Cloud Deployment

Waqaya AI is deployed through Streamlit Community Cloud with source code managed on GitHub.

### Deployment Configuration

| Component | Configuration |
|---|---|
| Platform | Streamlit Community Cloud |
| Repository | HadeelAlshammari111/Waqaya_Ai |
| Branch | main |
| Application Entry Point | app.py |
| Framework | Streamlit |
| Language | Python |

### Access the Application

**[Open Waqaya AI — Live Application](https://waqiya-ai-app.streamlit.app)**

The deployed application allows visitors to explore the interactive prototype without configuring a local Python environment.

---

## 11. Application Screenshots

The following application sections demonstrate the platform's primary functionality:

- Home and preventive health overview
- Interactive health dashboard
- Risk analysis results
- Health trends and baseline comparison
- Preventive insights

For the current interactive interface, visit:

**[Explore the Live Application](https://waqiya-ai-app.streamlit.app)**

---

## 12. Current Limitations

Waqaya AI is an experimental prototype with several important limitations:

- The training and evaluation data is synthetic.
- Model performance has not been clinically validated.
- Predictions may not generalize to real-world populations.
- The diabetes model demonstrates limited recall in its experimental evaluation.
- Model outputs should not be interpreted as medical diagnoses.
- Educational insights do not replace professional medical consultation.

These limitations provide opportunities for further research and model development.

---

## 13. Future Development

Potential directions for future improvements include:

- Evaluation using appropriately sourced real-world datasets
- Improving model generalization and recall
- More extensive model calibration and validation
- Expanded explainability and model monitoring
- Improved mobile responsiveness and accessibility
- Integration with supported wearable-device data
- Enhanced time-series analysis
- Improved privacy and security controls

Any future real-world health-data integration would require appropriate consent, privacy safeguards, and validation.

---

## 14. Project Impact

Waqaya AI demonstrates how Data Science and Machine Learning can be integrated into an interactive preventive-health analytics prototype.

The project brings together:

- Data preparation and feature engineering
- Predictive modeling
- Experimental model evaluation
- Anomaly detection
- Explainable AI
- Interactive data visualization
- Full application development
- Cloud deployment

The overall objective is to explore how health-related data can be transformed into understandable insights through artificial intelligence.

---

## 15. Developer

**Hadeel Mohammad Alshammari**

Data Science | Machine Learning | Artificial Intelligence

**GitHub:** [HadeelAlshammari111](https://github.com/HadeelAlshammari111)

**Project Repository:** [Waqaya AI](https://github.com/HadeelAlshammari111/Waqaya_Ai)

**Live Application:** [Waqaya AI on Streamlit](https://waqiya-ai-app.streamlit.app)

---

## Medical and Research Disclaimer

Waqaya AI is an experimental educational and research prototype.

It is not a certified medical device and is not intended to diagnose, treat, cure, or prevent medical conditions.

All machine-learning performance metrics were obtained from experimental evaluation using synthetic data.

Users should not rely on the platform for clinical decisions or as a replacement for qualified healthcare professionals.

---

**Waqaya AI — Turning Health Data into Preventive Intelligence.**
