import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)


# ============================================================
# Waqaya AI - Machine Learning Training Pipeline
# ============================================================

DATA_FILE = "waqaya_health_data.csv"
MODEL_FILE = "waqaya_models.pkl"

RANDOM_STATE = 42


# ============================================================
# 1. Load Dataset
# ============================================================

print("=" * 70)
print("WAQAYA AI - MODEL TRAINING")
print("=" * 70)

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}\n"
        "Please run generate_data.py first."
    )

df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully.")
print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")


# ============================================================
# 2. Define Features
# ============================================================

features = [
    "age",
    "gender",
    "systolic_bp",
    "diastolic_bp",
    "heart_rate",
    "spo2",
    "sleep_hours",
    "steps",
    "water_liters",
    "urination",
    "bmi"
]


# ============================================================
# 3. Define Prediction Targets
# ============================================================

targets = {
    "Diabetes Risk": "diabetes_risk",
    "Cardiovascular Risk": "cardio_risk",
    "Respiratory Risk": "respiratory_risk",
    "Dehydration Risk": "dehydration_risk"
}


# ============================================================
# 4. Validate Dataset
# ============================================================

required_columns = features + list(targets.values())

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        "\nMissing columns in dataset:\n"
        + "\n".join(f"- {column}" for column in missing_columns)
    )

print("\nDataset validation: PASSED")


# ============================================================
# 5. Prepare Features
# ============================================================

X = df[features].copy()

X = X.replace([np.inf, -np.inf], np.nan)

if X.isnull().sum().sum() > 0:
    print("\nMissing feature values detected.")
    print("Applying median imputation...")

    X = X.fillna(X.median())

print(f"Features used: {len(features)}")


# ============================================================
# 6. Train Models
# ============================================================

models = {}
metrics = {}
feature_importance = {}


for risk_name, target_column in targets.items():

    print("\n" + "-" * 70)
    print(f"TRAINING: {risk_name}")
    print("-" * 70)

    y = df[target_column].astype(int)

    print(f"Target column : {target_column}")
    print(f"Positive cases: {y.sum():,}")
    print(f"Negative cases: {(y == 0).sum():,}")

    # --------------------------------------------------------
    # Train/Test Split
    # --------------------------------------------------------

    try:

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=RANDOM_STATE,
            stratify=y
        )

    except ValueError:

        print(
            "Warning: Stratified split could not be used. "
            "Using regular split."
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=RANDOM_STATE
        )


    # --------------------------------------------------------
    # Random Forest Model
    # --------------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=400,
        max_depth=14,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced_subsample",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )


    print("Training model...")

    model.fit(X_train, y_train)

    print("Training completed.")


    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]


    # --------------------------------------------------------
    # Evaluation Metrics
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    try:
        roc_auc = roc_auc_score(
            y_test,
            probabilities
        )
    except ValueError:
        roc_auc = 0.0


    # --------------------------------------------------------
    # Confusion Matrix
    # --------------------------------------------------------

    cm = confusion_matrix(
        y_test,
        predictions
    )


    # --------------------------------------------------------
    # Feature Importance
    # --------------------------------------------------------

    importance_values = model.feature_importances_

    importance_dict = dict(
        sorted(
            zip(features, importance_values),
            key=lambda item: item[1],
            reverse=True
        )
    )


    # --------------------------------------------------------
    # Store Results
    # --------------------------------------------------------

    models[risk_name] = model

    metrics[risk_name] = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "roc_auc": float(roc_auc),
        "test_samples": int(len(y_test)),
        "positive_cases": int(y.sum()),
        "confusion_matrix": cm.tolist()
    }

    feature_importance[risk_name] = {
        key: float(value)
        for key, value in importance_dict.items()
    }


    # --------------------------------------------------------
    # Print Results
    # --------------------------------------------------------

    print("\nMODEL PERFORMANCE")

    print(f"Accuracy  : {accuracy:.2%}")
    print(f"Precision : {precision:.2%}")
    print(f"Recall    : {recall:.2%}")
    print(f"F1 Score  : {f1:.3f}")
    print(f"ROC-AUC   : {roc_auc:.3f}")

    print("\nTop Predictive Features:")

    for feature, importance in list(
        importance_dict.items()
    )[:5]:

        print(
            f"  {feature:<20} "
            f"{importance:.4f}"
        )


# ============================================================
# 7. Global Training Information
# ============================================================

training_info = {
    "dataset": DATA_FILE,
    "rows": int(len(df)),
    "features": features,
    "targets": targets,
    "model_type": "RandomForestClassifier",
    "n_estimators": 400,
    "max_depth": 14,
    "random_state": RANDOM_STATE,
    "purpose": (
        "Preventive health risk estimation prototype. "
        "Not a clinical diagnostic system."
    )
}


# ============================================================
# 8. Create Model Package
# ============================================================

model_package = {
    "models": models,
    "features": features,
    "metrics": metrics,
    "feature_importance": feature_importance,
    "training_info": training_info
}


# ============================================================
# 9. Save Models
# ============================================================

joblib.dump(
    model_package,
    MODEL_FILE
)


# ============================================================
# 10. Final Report
# ============================================================

print("\n" + "=" * 70)
print("TRAINING COMPLETED SUCCESSFULLY")
print("=" * 70)

print(f"\nModel file created:")
print(f"  {MODEL_FILE}")

print("\nModels trained:")

for model_name in models:
    print(f"  - {model_name}")

print("\nSaved components:")
print("  - Machine Learning models")
print("  - Model performance metrics")
print("  - Feature importance")
print("  - Training information")
print("  - Feature list")

print("\nWaqaya AI model package is ready.")
print("=" * 70)