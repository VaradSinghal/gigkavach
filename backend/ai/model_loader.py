"""
GigKavach — Model Loader
Loads trained ML models from saved_models/ for inference in API services.
"""

import os
import joblib
import numpy as np


MODEL_DIR = os.path.join(os.path.dirname(__file__), 'saved_models')


class ModelLoader:
    """Singleton model loader — loads all models once at startup."""

    _instance = None
    _loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_all(self):
        """Load all trained models into memory."""
        if self._loaded:
            return

        print("Loading GigKavach ML models...")

        # Premium pricing model
        self.premium_model = self._load('premium_model.joblib')
        self.premium_scaler = self._load('premium_scaler.joblib')
        self.premium_features = self._load('premium_features.joblib')

        # Zone risk model
        self.zone_risk_kmeans = self._load('zone_risk_kmeans.joblib')
        self.zone_risk_scaler = self._load('zone_risk_scaler.joblib')
        self.zone_risk_features = self._load('zone_risk_features.joblib')

        # Fraud detection models
        self.fraud_iso_forest = self._load('fraud_isolation_forest.joblib')
        self.fraud_classifier = self._load('fraud_rf_classifier.joblib')
        self.fraud_scaler = self._load('fraud_scaler.joblib')
        self.fraud_features = self._load('fraud_features.joblib')

        # Earnings boost model
        self.boost_model = self._load('boost_model.joblib')
        self.boost_scaler = self._load('boost_scaler.joblib')
        self.boost_features = self._load('boost_features.joblib')

        # Forecast models
        self.forecast_models = self._load('forecast_models.joblib')

        self._loaded = True
        print("✓ All models loaded successfully!")

    def _load(self, filename):
        """Load a single model file."""
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            return joblib.load(path)
        print(f"  ⚠ Model not found: {filename}")
        return None

    def predict_premium(self, features_dict):
        """Predict dynamic weekly premium for a worker."""
        if self.premium_model is None:
            return {'premium': 45.0, 'error': 'Model not loaded'}

        X = np.array([[features_dict.get(f, 0) for f in self.premium_features]])
        X_scaled = self.premium_scaler.transform(X)
        premium = float(self.premium_model.predict(X_scaled)[0])
        return {
            'premium': round(max(15, premium), 2),
            'breakdown': {
                'base': 25.0,
                'zone_risk': round(max(0, premium - 25 - features_dict.get('claim_rate', 0) * 10), 2),
                'weather': round(features_dict.get('avg_rainfall_mm', 0) / 10, 2),
                'claims_history': round(features_dict.get('claim_rate', 0) * 10, 2),
                'loyalty_discount': round(min(features_dict.get('experience_weeks', 0) / 16 * 5, 10), 2),
            }
        }

    def predict_fraud_score(self, features_dict):
        """Predict fraud confidence score for a claim."""
        if self.fraud_classifier is None:
            return {'confidence': 85, 'is_fraud': False}

        X = np.array([[features_dict.get(f, 0) for f in self.fraud_features]])
        X_scaled = self.fraud_scaler.transform(X)

        # Random Forest probability
        fraud_prob = float(self.fraud_classifier.predict_proba(X_scaled)[0][1])
        confidence = int((1 - fraud_prob) * 100)

        # Isolation Forest anomaly score
        anomaly = float(self.fraud_iso_forest.decision_function(X_scaled)[0])

        return {
            'confidence': confidence,
            'fraud_probability': round(fraud_prob, 4),
            'anomaly_score': round(anomaly, 4),
            'is_fraud': fraud_prob > 0.5,
            'action': 'auto_approve' if confidence >= 80 else ('soft_review' if confidence >= 50 else 'reject'),
        }

    def predict_earnings(self, features_dict):
        """Predict earnings potential for boost recommendations."""
        if self.boost_model is None:
            return {'predicted_earnings': 700}

        X = np.array([[features_dict.get(f, 0) for f in self.boost_features]])
        X_scaled = self.boost_scaler.transform(X)
        earnings = float(self.boost_model.predict(X_scaled)[0])
        return {'predicted_earnings': round(max(0, earnings), 2)}


# Global singleton
loader = ModelLoader()
