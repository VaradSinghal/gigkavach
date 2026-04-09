"""
GigKavach — Earnings Boost Regression Model
XGBoost / Gradient Boosted Trees to predict zone-level earnings potential.
Generates actionable boost recommendations for workers.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pipelines.data_pipeline import generate_all_data
from pipelines.feature_engineering import engineer_boost_features


BOOST_FEATURES = [
    'day_sin', 'day_cos', 'rainfall_mm', 'aqi',
    'temperature_c', 'humidity_pct', 'is_weekend',
    'hours_worked', 'orders_completed',
]

TARGET_COL = 'target_earnings'


def train():
    """Train the earnings boost prediction model."""
    print("-" * 60)
    print("  GigKavach - Earnings Boost Model Training")
    print("-" * 60)

    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(os.path.join(data_dir, 'earnings.csv')):
        print("\n[1/4] Generating synthetic data...")
        _, weather_df, _, _, earnings_df = generate_all_data(data_dir)
    else:
        print("\n[1/4] Loading existing data...")
        weather_df = pd.read_csv(os.path.join(data_dir, 'weather.csv'))
        earnings_df = pd.read_csv(os.path.join(data_dir, 'earnings.csv'))

    print("[2/4] Engineering boost features...")
    features_df = engineer_boost_features(earnings_df, weather_df)
    print(f"  Feature matrix shape: {features_df.shape}")

    X = features_df[BOOST_FEATURES].values
    y = features_df[TARGET_COL].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("[3/4] Training Gradient Boosted Regression...")
    model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        random_state=42,
    )
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\n  -- Model Performance --")
    print(f"  MAE:  RS.{mae:.2f}")
    print(f"  R2:   {r2:.4f}")

    print(f"\n  -- Feature Importance --")
    importance = pd.Series(model.feature_importances_, index=BOOST_FEATURES).sort_values(ascending=False)
    for feat, imp in importance.items():
        print(f"  {feat:25s} {imp:.4f}")

    print("\n[4/4] Saving model artifacts...")
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(model, os.path.join(model_dir, 'boost_model.joblib'))
    joblib.dump(scaler, os.path.join(model_dir, 'boost_scaler.joblib'))
    joblib.dump(BOOST_FEATURES, os.path.join(model_dir, 'boost_features.joblib'))

    print(f"  [SUCCESS] Saved to: {model_dir}")
    print(f"\n{'-' * 60}")
    print(f"  Earnings Boost Model - Training Complete!")
    print(f"{'-' * 60}")

    return model, scaler


if __name__ == '__main__':
    train()
