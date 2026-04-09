"""
GigKavach — Risk Forecast Time-Series Model
Uses a simple seasonal decomposition approach for disruption forecasting.
(Replaces Prophet dependency for easier portability.)
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pipelines.data_pipeline import generate_all_data


def train():
    """Train a time-series forecast model for disruption risk prediction."""
    print("=" * 60)
    print("  GigKavach — Risk Forecast Model Training")
    print("=" * 60)

    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(os.path.join(data_dir, 'weather.csv')):
        print("\n[1/4] Generating synthetic data...")
        _, weather_df, _, _, _ = generate_all_data(data_dir)
    else:
        print("\n[1/4] Loading existing data...")
        weather_df = pd.read_csv(os.path.join(data_dir, 'weather.csv'))

    print("[2/4] Building daily risk time-series per zone...")

    # Ensure date-derived columns exist
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    if 'day_of_week' not in weather_df.columns:
        weather_df['day_of_week'] = weather_df['date'].dt.weekday
    if 'month' not in weather_df.columns:
        weather_df['month'] = weather_df['date'].dt.month

    # Compute daily disruption risk score per zone
    weather_df['disruption_risk'] = (
        np.clip(weather_df['rainfall_mm'] / 50, 0, 1) * 0.40 +
        np.clip((weather_df['aqi'] - 100) / 400, 0, 1) * 0.30 +
        np.clip((weather_df['temperature_c'] - 35) / 13, 0, 1) * 0.20 +
        np.clip(weather_df['humidity_pct'] / 100, 0, 1) * 0.10
    )
    weather_df['disruption_risk'] = np.round(weather_df['disruption_risk'] * 100, 1)

    # Aggregate per zone for seasonal patterns
    zone_results = {}

    cities_zones = weather_df.groupby(['city', 'zone'])

    print("[3/4] Training forecast models per zone...")
    models = {}

    for (city, zone), grp in cities_zones:
        group = grp.copy().sort_values('date').reset_index(drop=True)
        group['day_index'] = np.arange(len(group))

        # Features: day index, day of week, month (cyclic)
        group['day_sin'] = np.sin(2 * np.pi * group['day_of_week'] / 7)
        group['day_cos'] = np.cos(2 * np.pi * group['day_of_week'] / 7)
        group['month_sin'] = np.sin(2 * np.pi * group['month'] / 12)
        group['month_cos'] = np.cos(2 * np.pi * group['month'] / 12)

        X = group[['day_index', 'day_sin', 'day_cos', 'month_sin', 'month_cos']].values
        y = group['disruption_risk'].values

        # Polynomial regression for trend + seasonality
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = poly.fit_transform(X)

        model = LinearRegression()
        model.fit(X_poly, y)

        # Generate 7-day forecast
        last_idx = group['day_index'].max()
        last_date = pd.to_datetime(group['date'].iloc[-1])

        forecast = []
        for d in range(1, 8):
            future_date = last_date + pd.Timedelta(days=d)
            dow = future_date.weekday()
            fut_month = future_date.month
            x_new = np.array([[last_idx + d,
                               np.sin(2 * np.pi * dow / 7),
                               np.cos(2 * np.pi * dow / 7),
                               np.sin(2 * np.pi * fut_month / 12),
                               np.cos(2 * np.pi * fut_month / 12)]])
            x_poly = poly.transform(x_new)
            pred = float(np.clip(model.predict(x_poly)[0], 0, 100))

            forecast.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'day_of_week': future_date.strftime('%a'),
                'predicted_risk': round(pred, 1),
                'risk_label': 'Low' if pred < 30 else ('Moderate' if pred < 55 else ('High' if pred < 75 else 'Critical')),
            })

        key = f"{city}_{zone}"
        zone_results[key] = {
            'city': city,
            'zone': zone,
            'avg_historical_risk': round(group['disruption_risk'].mean(), 1),
            'forecast': forecast,
        }
        models[key] = {'model': model, 'poly': poly}

    # Save outputs
    print("\n[4/4] Saving model artifacts...")
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(models, os.path.join(model_dir, 'forecast_models.joblib'))

    with open(os.path.join(model_dir, 'forecast_results.json'), 'w') as f:
        json.dump(zone_results, f, indent=2)

    # Print sample forecast
    print(f"\n  -- Sample 7-Day Forecast (Chennai, Adyar) --")
    sample = zone_results.get('Chennai_Adyar', list(zone_results.values())[0])
    for day in sample['forecast']:
        bar = '=' * int(day['predicted_risk'] / 5)
        print(f"  {day['date']} ({day['day_of_week']})  {day['predicted_risk']:5.1f}  {bar}  [{day['risk_label']}]")

    print(f"\n  * Forecast generated for {len(zone_results)} zones")
    print(f"\n{'=' * 60}")
    print(f"  Risk Forecast Model - Training Complete!")
    print(f"{'=' * 60}")

    return models, zone_results


if __name__ == '__main__':
    train()
