import numpy as np
import pandas as pd

np.random.seed(42)

N = 10000

age = np.random.randint(18, 80, N)
gender = np.random.randint(0, 2, N)

systolic_bp = np.clip(
    np.random.normal(120 + (age - 40) * 0.25, 15, N),
    90,
    190
)

diastolic_bp = np.clip(
    np.random.normal(78 + (age - 40) * 0.12, 10, N),
    50,
    120
)

heart_rate = np.clip(
    np.random.normal(72, 12, N),
    45,
    130
)

spo2 = np.clip(
    np.random.normal(97, 1.5, N),
    88,
    100
)

sleep_hours = np.clip(
    np.random.normal(7, 1.4, N),
    3,
    11
)

steps = np.clip(
    np.random.normal(7000, 2800, N),
    500,
    18000
)

water_liters = np.clip(
    np.random.normal(2.0, 0.7, N),
    0.3,
    5
)

urination = np.clip(
    np.random.normal(6, 2, N),
    1,
    15
)

bmi = np.clip(
    np.random.normal(25, 4.5, N),
    15,
    45
)

# -----------------------------
# Risk scores used to create
# synthetic training labels
# -----------------------------

diabetes_score = (
    0.04 * (age - 40)
    + 0.12 * (bmi - 25)
    + 0.5 * (sleep_hours < 5)
    + 0.0008 * (steps * -1 + 7000)
)

cardio_score = (
    0.04 * (age - 40)
    + 0.07 * (systolic_bp - 120)
    + 0.03 * (diastolic_bp - 80)
    + 0.03 * (heart_rate - 70)
    + 0.08 * (bmi - 25)
)

resp_score = (
    0.8 * (spo2 < 95)
    + 0.03 * (heart_rate - 70)
    + 0.2 * (sleep_hours < 5)
)

dehydration_score = (
    1.2 * (water_liters < 1.5)
    + 0.25 * (steps > 10000)
    + 0.3 * (urination < 4)
)

# Add random variation
diabetes_score += np.random.normal(0, 1.5, N)
cardio_score += np.random.normal(0, 1.5, N)
resp_score += np.random.normal(0, 0.7, N)
dehydration_score += np.random.normal(0, 0.5, N)

# Convert scores into binary labels
diabetes_risk = (diabetes_score > 1.8).astype(int)
cardio_risk = (cardio_score > 2.2).astype(int)
respiratory_risk = (resp_score > 1.0).astype(int)
dehydration_risk = (dehydration_score > 0.8).astype(int)

df = pd.DataFrame({
    "age": age,
    "gender": gender,
    "systolic_bp": systolic_bp,
    "diastolic_bp": diastolic_bp,
    "heart_rate": heart_rate,
    "spo2": spo2,
    "sleep_hours": sleep_hours,
    "steps": steps,
    "water_liters": water_liters,
    "urination": urination,
    "bmi": bmi,
    "diabetes_risk": diabetes_risk,
    "cardio_risk": cardio_risk,
    "respiratory_risk": respiratory_risk,
    "dehydration_risk": dehydration_risk
})

df.to_csv("waqaya_health_data.csv", index=False)

print("===================================")
print("Waqaya AI Dataset Created")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("File: waqaya_health_data.csv")
print("===================================")