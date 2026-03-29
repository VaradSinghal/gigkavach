"""
GigKavach — Fraud Detection Model
Isolation Forest for anomaly detection + Random Forest for classification.
Generates confidence scores for automatic claim validation.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pipelines.data_pipeline import generate_all_data
from pipelines.feature_engineering import engineer_fraud_features


FRAUD_FEATURES = [
    'rainfall_mm', 'aqi', 'temperature_c',
    'inactive_hours', 'payout_amount',
    'gps_consistent', 'activity_coherent',
    'timing_correlated', 'device_clean',
    'env_disruption', 'integrity_score',
]


def train():
    """Train the fraud detection model (dual: Isolation Forest + Random Forest)."""
    print("=" * 60)
    print("  GigKavach — Fraud Detection Model Training")
    print("=" * 60)

    # Generate or load data
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(os.path.join(data_dir, 'claims.csv')):
        print("\n[1/5] Generating synthetic data...")
        _, _, _, claims_df, _ = generate_all_data(data_dir)
    else:
        print("\n[1/5] Loading existing data...")
        claims_df = pd.read_csv(os.path.join(data_dir, 'claims.csv'))

    # Feature engineering
    print("[2/5] Engineering fraud features...")
    features_df = engineer_fraud_features(claims_df)
    print(f"  Feature matrix shape: {features_df.shape}")
    print(f"  Fraud ratio: {features_df['is_fraud'].mean():.2%}")

    X = features_df[FRAUD_FEATURES].values
    y = features_df['is_fraud'].values

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ── Model 1: Isolation Forest (unsupervised anomaly detection) ──
    print("\n[3/5] Training Isolation Forest (anomaly detection)...")
    iso_forest = IsolationForest(
        n_estimators=200,
        contamination=0.15,
        random_state=42,
        max_features=0.8,
    )
    iso_forest.fit(X_scaled)

    # Anomaly scores (-1 = anomaly, 1 = normal)
    anomaly_labels = iso_forest.predict(X_scaled)
    anomaly_scores = iso_forest.decision_function(X_scaled)

    iso_detected = (anomaly_labels == -1).sum()
    iso_actual = y.sum()
    print(f"  Isolation Forest flagged: {iso_detected} anomalies (actual fraud: {iso_actual})")

    # ── Model 2: Random Forest Classifier (supervised) ──
    print("[4/5] Training Random Forest Classifier...")
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    rf_classifier = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        class_weight='balanced',
        random_state=42,
    )
    rf_classifier.fit(X_train, y_train)

    y_pred = rf_classifier.predict(X_test)
    y_proba = rf_classifier.predict_proba(X_test)[:, 1]

    print(f"\n  ── Classification Report ──")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraudulent']))

    print(f"  ── Confusion Matrix ──")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  TN={cm[0][0]}  FP={cm[0][1]}")
    print(f"  FN={cm[1][0]}  TP={cm[1][1]}")

    # Feature importance
    print(f"\n  ── Feature Importance ──")
    importance = pd.Series(rf_classifier.feature_importances_, index=FRAUD_FEATURES).sort_values(ascending=False)
    for feat, imp in importance.items():
        print(f"  {feat:25s} {imp:.4f}")

    # Save models
    print("\n[5/5] Saving model artifacts...")
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(iso_forest, os.path.join(model_dir, 'fraud_isolation_forest.joblib'))
    joblib.dump(rf_classifier, os.path.join(model_dir, 'fraud_rf_classifier.joblib'))
    joblib.dump(scaler, os.path.join(model_dir, 'fraud_scaler.joblib'))
    joblib.dump(FRAUD_FEATURES, os.path.join(model_dir, 'fraud_features.joblib'))

    print(f"  ✓ Saved to: {model_dir}")
    print(f"\n{'=' * 60}")
    print(f"  Fraud Detection Model — Training Complete!")
    print(f"{'=' * 60}")

    return iso_forest, rf_classifier, scaler


if __name__ == '__main__':
    train()
