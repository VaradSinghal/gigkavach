"""
GigKavach — Dynamic Premium Pricing Model
Uses Ridge Regression (GLM) to predict personalized weekly premiums
based on worker profile, zone risk, weather, and claims history.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Add parent paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pipelines.data_pipeline import generate_all_data
from pipelines.feature_engineering import engineer_premium_features


FEATURE_COLS = [
    'avg_daily_income', 'avg_weekly_income', 'avg_daily_hours',
    'experience_weeks', 'is_flood_zone', 'trust_score',
    'elevation_m', 'drainage_score', 'historical_flood_events',
    'historical_disruption_days', 'road_density',
    'avg_rainfall_mm', 'max_rainfall_mm', 'avg_aqi', 'heavy_rain_day_ratio',
    'claim_count', 'claim_rate', 'total_payout',
]

TARGET_COL = 'target_premium'


def train():
    """Train the premium pricing model."""
    print("=" * 60)
    print("  GigKavach — Dynamic Premium Pricing Model Training")
    print("=" * 60)

    # Generate or load data
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(os.path.join(data_dir, 'workers.csv')):
        print("\n[1/4] Generating synthetic data...")
        workers_df, weather_df, zones_df, claims_df, _ = generate_all_data(data_dir)
    else:
        print("\n[1/4] Loading existing data...")
        workers_df = pd.read_csv(os.path.join(data_dir, 'workers.csv'))
        weather_df = pd.read_csv(os.path.join(data_dir, 'weather.csv'))
        zones_df = pd.read_csv(os.path.join(data_dir, 'zones.csv'))
        claims_df = pd.read_csv(os.path.join(data_dir, 'claims.csv'))

    # Feature engineering
    print("[2/4] Engineering features...")
    features_df = engineer_premium_features(workers_df, weather_df, claims_df, zones_df)
    print(f"  Feature matrix shape: {features_df.shape}")

    X = features_df[FEATURE_COLS].values
    y = features_df[TARGET_COL].values

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Ridge Regression
    print("[3/4] Training Ridge Regression model...")
    model = Ridge(alpha=1.0)
    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\n  -- Model Performance --")
    print(f"  MAE:  RS.{mae:.2f}")
    print(f"  R2:   {r2:.4f}")

    # Feature importance
    print(f"\n  -- Feature Importance (Top 10) --")
    importance = pd.Series(np.abs(model.coef_), index=FEATURE_COLS).sort_values(ascending=False)
    for feat, imp in importance.head(10).items():
        print(f"  {feat:35s} {imp:.4f}")

    # Save model and scaler
    print("\n[4/4] Saving model artifacts...")
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(model, os.path.join(model_dir, 'premium_model.joblib'))
    joblib.dump(scaler, os.path.join(model_dir, 'premium_scaler.joblib'))
    joblib.dump(FEATURE_COLS, os.path.join(model_dir, 'premium_features.joblib'))

    print(f"  * Saved to: {model_dir}")
    print(f"\n{'=' * 60}")
    print(f"  Premium Pricing Model - Training Complete!")
    print(f"{'=' * 60}")

    return model, scaler


if __name__ == '__main__':
    train()
