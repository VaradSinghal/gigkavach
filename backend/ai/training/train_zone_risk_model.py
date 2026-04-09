"""
GigKavach — Hyperlocal Zone Risk Clustering Model
Uses K-Means clustering to group zones by risk profile,
then assigns composite risk scores (0-100) per zone.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pipelines.data_pipeline import generate_all_data
from pipelines.feature_engineering import engineer_zone_risk_features


RISK_FEATURES = [
    'elevation_m', 'drainage_score', 'historical_flood_events',
    'historical_disruption_days', 'road_density',
    'avg_rainfall_mm', 'max_rainfall_mm',
    'rain_days_ratio', 'heavy_rain_days_ratio',
    'avg_aqi', 'high_aqi_days_ratio',
    'avg_temperature_c', 'extreme_heat_days_ratio',
]


def train():
    """Train the zone risk clustering model."""
    print("=" * 60)
    print("  GigKavach — Zone Risk Clustering Model Training")
    print("=" * 60)

    # Generate or load data
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(os.path.join(data_dir, 'zones.csv')):
        print("\n[1/4] Generating synthetic data...")
        _, weather_df, zones_df, _, _ = generate_all_data(data_dir)
    else:
        print("\n[1/4] Loading existing data...")
        zones_df = pd.read_csv(os.path.join(data_dir, 'zones.csv'))
        weather_df = pd.read_csv(os.path.join(data_dir, 'weather.csv'))

    # Feature engineering
    print("[2/4] Engineering zone risk features...")
    features_df = engineer_zone_risk_features(zones_df, weather_df)
    print(f"  Feature matrix shape: {features_df.shape}")

    X = features_df[RISK_FEATURES].values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-Means clustering (4 risk tiers)
    print("[3/4] Training K-Means clustering (k=4)...")
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    features_df['cluster'] = clusters

    # Compute composite risk score (0-100) based on risk-correlated features
    # Higher flood events, rainfall, lower drainage = higher risk
    risk_components = features_df[['historical_flood_events', 'heavy_rain_days_ratio',
                                    'high_aqi_days_ratio', 'extreme_heat_days_ratio']].copy()
    risk_components['inv_drainage'] = 1 - features_df['drainage_score']
    risk_components['inv_elevation'] = 1 - MinMaxScaler().fit_transform(features_df[['elevation_m']])

    weights = [0.25, 0.20, 0.15, 0.10, 0.15, 0.15]
    risk_score_raw = np.zeros(len(features_df))
    for col, w in zip(risk_components.columns, weights):
        normalized = MinMaxScaler().fit_transform(risk_components[[col]]).flatten()
        risk_score_raw += normalized * w

    # Scale to 0-100
    risk_scores = MinMaxScaler(feature_range=(5, 95)).fit_transform(risk_score_raw.reshape(-1, 1)).flatten()
    features_df['risk_score'] = np.round(risk_scores, 1)

    # Map clusters to risk labels based on mean risk score
    cluster_means = features_df.groupby('cluster')['risk_score'].mean().sort_values()
    risk_labels = ['Low', 'Moderate', 'High', 'Critical']
    cluster_label_map = {cluster: label for cluster, label in zip(cluster_means.index, risk_labels)}
    features_df['risk_label'] = features_df['cluster'].map(cluster_label_map)

    # Print results
    print(f"\n  -- Zone Risk Scores --")
    for _, row in features_df.iterrows():
        print(f"  {row['city']:10s} {row['zone']:20s} -> Score: {row['risk_score']:5.1f}  [{row['risk_label']}]")

    # Save outputs
    print("\n[4/4] Saving model artifacts...")
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(kmeans, os.path.join(model_dir, 'zone_risk_kmeans.joblib'))
    joblib.dump(scaler, os.path.join(model_dir, 'zone_risk_scaler.joblib'))
    joblib.dump(RISK_FEATURES, os.path.join(model_dir, 'zone_risk_features.joblib'))

    # Export risk scores as JSON for Flutter app embedding
    scores_export = features_df[['city', 'zone', 'risk_score', 'risk_label', 'cluster']].to_dict('records')
    with open(os.path.join(model_dir, 'zone_risk_scores.json'), 'w') as f:
        json.dump(scores_export, f, indent=2)

    print(f"  * Saved to: {model_dir}")
    print(f"\n{'=' * 60}")
    print(f"  Zone Risk Clustering - Training Complete!")
    print(f"{'=' * 60}")

    return kmeans, scaler, features_df


if __name__ == '__main__':
    train()
