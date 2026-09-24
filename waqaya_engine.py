import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
class WaqayaEngine:
    """
    Waqaya AI
    Preventive Health Intelligence Engine
    This engine combines:
    - Machine Learning risk estimation
    - Personal baseline analysis
    - Anomaly detection
    - Trend analysis
    - Explainable AI
    - Early risk scoring
    This is a Data Science prototype and is not a medical
    diagnostic system.
    """
    # ---------------------------------------------------------
    # FEATURES USED BY THE TRAINED MODELS
    # ---------------------------------------------------------
    DEFAULT_FEATURES = [
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
    # ---------------------------------------------------------
    # INITIALIZATION
    # ---------------------------------------------------------
    def __init__(self, model_path="waqaya_models.pkl"):
        self.model_path = model_path
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found: {self.model_path}"
            )
        package = joblib.load(self.model_path)
        if not isinstance(package, dict):
            raise ValueError(
                "waqaya_models.pkl must contain a dictionary."
            )
        self.package = package
        # -----------------------------------------------------
        # LOAD MODELS
        # -----------------------------------------------------
        self.models = package.get("models", {})
        if not isinstance(self.models, dict):
            self.models = {}
        # -----------------------------------------------------
        # LOAD FEATURES
        # -----------------------------------------------------
        self.features = package.get(
            "features",
            self.DEFAULT_FEATURES
        )
        if not isinstance(self.features, list):
            self.features = self.DEFAULT_FEATURES.copy()
        # -----------------------------------------------------
        # LOAD METRICS
        # -----------------------------------------------------
        self.metrics = package.get(
            "metrics",
            {}
        )
        # -----------------------------------------------------
        # LOAD FEATURE IMPORTANCE
        # -----------------------------------------------------
        self.feature_importance = package.get(
            "feature_importance",
            {}
        )
        # -----------------------------------------------------
        # ANOMALY DETECTION
        # -----------------------------------------------------
        self.anomaly_model = IsolationForest(
            n_estimators=300,
            contamination=0.08,
            random_state=42
        )
        self.anomaly_fitted = False
    # =========================================================
    # DATA PREPARATION
    # =========================================================
    def _prepare_data(self, data):
        if isinstance(data, pd.Series):
            data = data.to_frame().T
        elif isinstance(data, dict):
            data = pd.DataFrame([data])
        elif isinstance(data, np.ndarray):
            data = np.asarray(data)
            if data.ndim == 1:
                data = data.reshape(1, -1)
            elif data.ndim == 3:
                data = data.reshape(
                    data.shape[0],
                    data.shape[-1]
                )
            data = pd.DataFrame(
                data,
                columns=self.features
                if data.shape[1] == len(self.features)
                else None
            )
        elif not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        data = data.copy()
        # -----------------------------------------------------
        # MAKE SURE ALL REQUIRED FEATURES EXIST
        # -----------------------------------------------------
        for feature in self.features:
            if feature not in data.columns:
                data[feature] = 0
        # -----------------------------------------------------
        # KEEP ONLY MODEL FEATURES
        # -----------------------------------------------------
        data = data[self.features]
        # -----------------------------------------------------
        # NUMERIC CONVERSION
        # -----------------------------------------------------
        for feature in self.features:
            data[feature] = pd.to_numeric(
                data[feature],
                errors="coerce"
            )
        data = data.replace(
            [np.inf, -np.inf],
            np.nan
        )
        data = data.fillna(0)
        return data
    # =========================================================
    # SAFE 2D ARRAY
    # =========================================================
    def _to_2d_array(self, data):
        if isinstance(data, pd.DataFrame):
            X = data.to_numpy(dtype=float)
        else:
            X = np.asarray(
                data,
                dtype=float
            )
        # 1D -> 2D
        if X.ndim == 1:
            X = X.reshape(
                1,
                -1
            )
        # 3D -> 2D
        # Fixes:
        # ValueError: Must pass 2-d input
        # shape=(1, 1, 11)
        elif X.ndim == 3:
            X = X.reshape(
                X.shape[0],
                X.shape[-1]
            )
        # Anything unexpected
        elif X.ndim != 2:
            X = X.reshape(
                X.shape[0],
                -1
            )
        return X
    # =========================================================
    # FIND MODEL
    # =========================================================
    def _find_model(self, target):
        if target in self.models:
            return self.models[target]
        target_lower = target.lower()
        # Exact/partial matching
        for name, model in self.models.items():
            name_lower = str(name).lower()
            if target_lower in name_lower:
                return model
        # Common alternative names
        aliases = {
            "diabetes_risk": [
                "diabetes",
                "diabetesrisk"
            ],
            "cardio_risk": [
                "cardio",
                "cardiovascular",
                "cardiovascular_risk"
            ],
            "respiratory_risk": [
                "respiratory",
                "respiratoryrisk"
            ],
            "dehydration_risk": [
                "dehydration",
                "dehydrationrisk"
            ]
        }
        for alias in aliases.get(target, []):
            for name, model in self.models.items():
                if alias in str(name).lower():
                    return model
        return None
    # =========================================================
    # RISK PREDICTION
    # =========================================================
    def _predict_risk(self, model, X):
        if model is None:
            return 0.0
        try:
            # Always force correct 2D shape
            X = self._to_2d_array(X)
            # -------------------------------------------------
            # Probability
            # -------------------------------------------------
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(X)
                probabilities = np.asarray(
                    probabilities,
                    dtype=float
                )
                if probabilities.ndim == 2:
                    if probabilities.shape[1] >= 2:
                        value = probabilities[
                            0,
                            1
                        ]
                    else:
                        value = probabilities[
                            0,
                            0
                        ]
                else:
                    value = probabilities.ravel()[0]
            else:
                prediction = model.predict(X)
                value = float(
                    np.asarray(prediction).ravel()[0]
                )
            # -------------------------------------------------
            # Convert to percentage
            # -------------------------------------------------
            value = float(value)
            if value <= 1:
                value *= 100
            return float(
                np.clip(
                    value,
                    0,
                    100
                )
            )
        except Exception:
            return 0.0
    # =========================================================
    # RISK PREDICTIONS
    # =========================================================
    def predict_risks(self, current_data):
        data = self._prepare_data(
            current_data
        )
        X = self._to_2d_array(
            data
        )
        targets = [
            "diabetes_risk",
            "cardio_risk",
            "respiratory_risk",
            "dehydration_risk"
        ]
        results = {}
        for target in targets:
            model = self._find_model(
                target
            )
            results[target] = self._predict_risk(
                model,
                X
            )
        return results
    # =========================================================
    # PERSONAL BASELINE
    # =========================================================
    def calculate_baseline(
        self,
        current_data,
        history=None
    ):
        current = self._prepare_data(
            current_data
        )
        monitored_features = [
            "heart_rate",
            "spo2",
            "sleep_hours",
            "steps",
            "water_liters"
        ]
        baseline = {}
        if history is not None:
            history_df = self._prepare_data(
                history
            )
        else:
            history_df = None
        for feature in monitored_features:
            current_value = float(
                current.iloc[0][feature]
            )
            if (
                history_df is not None
                and feature in history_df.columns
                and len(history_df) > 0
            ):
                baseline_value = float(
                    history_df[feature].mean()
                )
            else:
                baseline_value = current_value
            baseline[feature] = baseline_value
        return baseline
    # =========================================================
    # BASELINE DEVIATION
    # =========================================================
    def calculate_baseline_deviation(
        self,
        current_data,
        baseline
    ):
        current = self._prepare_data(
            current_data
        )
        deviations = {}
        for feature in baseline:
            current_value = float(
                current.iloc[0][feature]
            )
            baseline_value = float(
                baseline[feature]
            )
            if abs(baseline_value) > 0.0001:
                percentage = (
                    (
                        current_value
                        - baseline_value
                    )
                    / abs(baseline_value)
                ) * 100
            else:
                percentage = 0.0
            deviations[feature] = float(
                percentage
            )
        return deviations
    # =========================================================
    # ANOMALY DETECTION
    # =========================================================
    def detect_anomaly(
        self,
        current_data,
        history=None
    ):
        current = self._prepare_data(
            current_data
        )
        monitored_features = [
            "heart_rate",
            "spo2",
            "sleep_hours",
            "steps",
            "water_liters"
        ]
        current_values = current[
            monitored_features
        ].astype(float)
        # -----------------------------------------------------
        # Build reference data
        # -----------------------------------------------------
        if (
            history is not None
            and len(history) >= 3
        ):
            history_df = self._prepare_data(
                history
            )
            reference = history_df[
                monitored_features
            ].astype(float)
        else:
            # Create a small reference set
            # around the current values.
            values = current_values.iloc[0].to_numpy(
                dtype=float
            )
            rng = np.random.default_rng(42)
            reference = pd.DataFrame(
                np.vstack([
                    values + rng.normal(
                        0,
                        np.maximum(
                            np.abs(values) * 0.03,
                            0.01
                        ),
                        size=len(values)
                    )
                    for _ in range(10)
                ]),
                columns=monitored_features
            )
        # -----------------------------------------------------
        # Fit anomaly detector
        # -----------------------------------------------------
        try:
            X_reference = self._to_2d_array(
                reference
            )
            X_current = self._to_2d_array(
                current_values
            )
            self.anomaly_model.fit(
                X_reference
            )
            self.anomaly_fitted = True
            prediction = self.anomaly_model.predict(
                X_current
            )[0]
            decision = self.anomaly_model.decision_function(
                X_current
            )[0]
            # Convert Isolation Forest score
            # into a simple 0-100 anomaly signal.
            anomaly_score = np.clip(
                (0.10 - decision) * 250,
                0,
                100
            )
            is_anomaly = prediction == -1
            if is_anomaly:
                anomaly_score = max(
                    anomaly_score,
                    60
                )
            return {
                "is_anomaly": bool(is_anomaly),
                "score": float(anomaly_score),
                "anomaly_score": float(anomaly_score),
                "decision_score": float(decision)
            }
        except Exception:
            return {
                "is_anomaly": False,
                "score": 0.0,
                "anomaly_score": 0.0,
                "decision_score": 0.0
            }
    # =========================================================
    # TREND ANALYSIS
    # =========================================================
    def calculate_trends(
        self,
        history
    ):
        if history is None:
            return {}
        history_df = self._prepare_data(
            history
        )
        monitored_features = [
            "heart_rate",
            "spo2",
            "sleep_hours",
            "steps",
            "water_liters"
        ]
        trends = {}
        for feature in monitored_features:
            values = history_df[
                feature
            ].astype(float).to_numpy()
            if len(values) < 2:
                trends[feature] = {
                    "change": 0.0,
                    "direction": "stable"
                }
                continue
            first = float(
                values[0]
            )
            last = float(
                values[-1]
            )
            change = last - first
            if abs(change) < 0.01:
                direction = "stable"
            elif change > 0:
                direction = "increasing"
            else:
                direction = "decreasing"
            trends[feature] = {
                "change": float(change),
                "direction": direction
            }
        return trends
    # =========================================================
    # FEATURE IMPORTANCE
    # =========================================================
    def get_feature_importance(self):
        # If training script already saved importance
        if isinstance(
            self.feature_importance,
            dict
        ) and len(
            self.feature_importance
        ) > 0:
            return self.feature_importance
        importance = {}
        # Otherwise extract from models
        for name, model in self.models.items():
            if hasattr(
                model,
                "feature_importances_"
            ):
                values = np.asarray(
                    model.feature_importances_,
                    dtype=float
                )
                for i, value in enumerate(values):
                    if i < len(self.features):
                        feature = self.features[i]
                        importance[feature] = (
                            importance.get(
                                feature,
                                0.0
                            )
                            + float(value)
                        )
        # Average importance
        if importance:
            total = sum(
                importance.values()
            )
            if total > 0:
                importance = {
                    key: value / total
                    for key, value in importance.items()
                }
        return importance
    # =========================================================
    # EARLY RISK SCORE
    # =========================================================
    def calculate_early_risk_score(
        self,
        risk_predictions,
        anomaly,
        baseline_deviation
    ):
        # -----------------------------------------------------
        # Average ML risk
        # -----------------------------------------------------
        risk_values = list(
            risk_predictions.values()
        )
        if risk_values:
            ml_score = float(
                np.mean(risk_values)
            )
        else:
            ml_score = 0.0
        # -----------------------------------------------------
        # Anomaly component
        # -----------------------------------------------------
        anomaly_score = float(
            anomaly.get(
                "score",
                anomaly.get(
                    "anomaly_score",
                    0
                )
            )
        )
        # -----------------------------------------------------
        # Baseline component
        # -----------------------------------------------------
        if baseline_deviation:
            deviations = [
                abs(float(value))
                for value
                in baseline_deviation.values()
            ]
            baseline_score = float(
                np.mean(deviations)
            )
            baseline_score = min(
                baseline_score,
                100
            )
        else:
            baseline_score = 0.0
        # -----------------------------------------------------
        # Combined preventive score
        # -----------------------------------------------------
        score = (
            ml_score * 0.60
            + anomaly_score * 0.20
            + baseline_score * 0.20
        )
        return float(
            np.clip(
                score,
                0,
                100
            )
        )
    # =========================================================
    # MAIN ANALYSIS
    # =========================================================
    def analyze(
        self,
        current_data,
        history=None
    ):
        # -----------------------------------------------------
        # Prepare current data
        # -----------------------------------------------------
        current = self._prepare_data(
            current_data
        )
        # -----------------------------------------------------
        # Risk prediction
        # -----------------------------------------------------
        risk_predictions = self.predict_risks(
            current
        )
        # -----------------------------------------------------
        # Personal baseline
        # -----------------------------------------------------
        baseline = self.calculate_baseline(
            current,
            history
        )
        # -----------------------------------------------------
        # Baseline deviation
        # -----------------------------------------------------
        baseline_deviation = (
            self.calculate_baseline_deviation(
                current,
                baseline
            )
        )
        # -----------------------------------------------------
        # Anomaly detection
        # -----------------------------------------------------
        anomaly = self.detect_anomaly(
            current,
            history
        )
        # -----------------------------------------------------
        # Trends
        # -----------------------------------------------------
        trends = self.calculate_trends(
            history
        )
        # -----------------------------------------------------
        # Feature importance
        # -----------------------------------------------------
        feature_importance = (
            self.get_feature_importance()
        )
        # -----------------------------------------------------
        # Early risk score
        # -----------------------------------------------------
        early_risk_score = (
            self.calculate_early_risk_score(
                risk_predictions,
                anomaly,
                baseline_deviation
            )
        )
        # -----------------------------------------------------
        # Final result
        # -----------------------------------------------------
        return {
            "risk_predictions":
                risk_predictions,
            "early_risk_score":
                early_risk_score,
            "anomaly":
                anomaly,
            "baseline":
                baseline,
            "baseline_deviation":
                baseline_deviation,
            "trends":
                trends,
            "feature_importance":
                feature_importance
        }
# =========================================================
# TEST
# =========================================================
if __name__ == "__main__":
    print("=" * 60)
    print("WAQAYA AI ENGINE")
    print("=" * 60)
    print("Engine file loaded successfully.")
    print(
        f"Features loaded: {len(WaqayaEngine.DEFAULT_FEATURES)}"
    )
    print("Ready for Streamlit.")