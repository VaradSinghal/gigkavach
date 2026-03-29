"""
GigKavach — Feature Engineering
Transforms raw data into ML-ready feature vectors for all models.
"""

import numpy as np
import pandas as pd


def engineer_premium_features(workers_df, weather_df, claims_df, zones_df):
    """
    Build feature matrix for dynamic premium pricing model.
    Each row = one worker's weekly premium calculation context.
    """
    features = []

    for _, worker in workers_df.iterrows():
        zone_data = zones_df[(zones_df['city'] == worker['city']) & (zones_df['zone'] == worker['zone'])]
        if len(zone_data) == 0:
            continue
        zone = zone_data.iloc[0]

        # Worker's claims history
        worker_claims = claims_df[claims_df['worker_id'] == worker['worker_id']]
        claim_count = len(worker_claims)
        claim_rate = claim_count / max(worker['experience_weeks'], 1)
        total_payout = worker_claims['payout_amount'].sum() if len(worker_claims) > 0 else 0

        # Zone weather stats
        zone_weather = weather_df[(weather_df['city'] == worker['city']) & (weather_df['zone'] == worker['zone'])]
        avg_rainfall = zone_weather['rainfall_mm'].mean() if len(zone_weather) > 0 else 0
        max_rainfall = zone_weather['rainfall_mm'].max() if len(zone_weather) > 0 else 0
        avg_aqi = zone_weather['aqi'].mean() if len(zone_weather) > 0 else 100
        heavy_rain_days = len(zone_weather[zone_weather['rainfall_mm'] > 30]) if len(zone_weather) > 0 else 0
        rain_day_ratio = heavy_rain_days / max(len(zone_weather), 1)

        # Compute target premium (actuarial approach)
        base_premium = 25.0
        zone_risk_factor = (zone['historical_flood_events'] / 20 * 0.4 +
                            (1 - zone['drainage_score']) * 0.3 +
                            rain_day_ratio * 0.3)
        zone_adjustment = round(zone_risk_factor * 20, 2)  # 0 to 20 rupees
        weather_adjustment = round(avg_rainfall / 10, 2)  # scaled
        claims_adjustment = round(claim_rate * 10, 2)
        loyalty_discount = min(worker['experience_weeks'] / 16 * 5, 10)  # max 10 rupees

        target_premium = max(15, base_premium + zone_adjustment + weather_adjustment + claims_adjustment - loyalty_discount)

        features.append({
            # Worker features
            'avg_daily_income': worker['avg_daily_income'],
            'avg_weekly_income': worker['avg_weekly_income'],
            'avg_daily_hours': worker['avg_daily_hours'],
            'experience_weeks': worker['experience_weeks'],
            'is_flood_zone': int(worker['is_flood_zone']),
            'trust_score': worker['trust_score'],

            # Zone features
            'elevation_m': zone['elevation_m'],
            'drainage_score': zone['drainage_score'],
            'historical_flood_events': zone['historical_flood_events'],
            'historical_disruption_days': zone['historical_disruption_days'],
            'road_density': zone['road_density'],

            # Weather features
            'avg_rainfall_mm': round(avg_rainfall, 2),
            'max_rainfall_mm': round(max_rainfall, 2),
            'avg_aqi': round(avg_aqi, 2),
            'heavy_rain_day_ratio': round(rain_day_ratio, 4),

            # Claims features
            'claim_count': claim_count,
            'claim_rate': round(claim_rate, 4),
            'total_payout': round(total_payout, 2),

            # Target
            'target_premium': round(target_premium, 2),
        })

    return pd.DataFrame(features)


def engineer_zone_risk_features(zones_df, weather_df):
    """
    Build feature matrix for zone risk clustering.
    Each row = one zone with composite risk features.
    """
    features = []

    for _, zone in zones_df.iterrows():
        zone_weather = weather_df[(weather_df['city'] == zone['city']) & (weather_df['zone'] == zone['zone'])]

        if len(zone_weather) == 0:
            continue

        avg_rain = zone_weather['rainfall_mm'].mean()
        max_rain = zone_weather['rainfall_mm'].max()
        rain_days = len(zone_weather[zone_weather['rainfall_mm'] > 10])
        heavy_rain_days = len(zone_weather[zone_weather['rainfall_mm'] > 30])
        avg_aqi = zone_weather['aqi'].mean()
        high_aqi_days = len(zone_weather[zone_weather['aqi'] > 300])
        avg_temp = zone_weather['temperature_c'].mean()
        extreme_heat_days = len(zone_weather[zone_weather['temperature_c'] > 43])

        features.append({
            'city': zone['city'],
            'zone': zone['zone'],
            'elevation_m': zone['elevation_m'],
            'drainage_score': zone['drainage_score'],
            'historical_flood_events': zone['historical_flood_events'],
            'historical_disruption_days': zone['historical_disruption_days'],
            'road_density': zone['road_density'],
            'population_density': zone['population_density'],
            'restaurant_density': zone['restaurant_density'],
            'avg_rainfall_mm': round(avg_rain, 2),
            'max_rainfall_mm': round(max_rain, 2),
            'rain_days_ratio': round(rain_days / len(zone_weather), 4),
            'heavy_rain_days_ratio': round(heavy_rain_days / len(zone_weather), 4),
            'avg_aqi': round(avg_aqi, 2),
            'high_aqi_days_ratio': round(high_aqi_days / len(zone_weather), 4),
            'avg_temperature_c': round(avg_temp, 2),
            'extreme_heat_days_ratio': round(extreme_heat_days / len(zone_weather), 4),
            'latitude': zone['latitude'],
            'longitude': zone['longitude'],
        })

    return pd.DataFrame(features)


def engineer_fraud_features(claims_df):
    """
    Build feature matrix for fraud detection model.
    Each row = one claim with fraud-relevant signals.
    """
    features = claims_df[[
        'rainfall_mm', 'aqi', 'temperature_c',
        'inactive_hours', 'payout_amount',
        'gps_consistent', 'activity_coherent',
        'timing_correlated', 'device_clean',
        'confidence_score',
    ]].copy()

    # Convert booleans to int
    for col in ['gps_consistent', 'activity_coherent', 'timing_correlated', 'device_clean']:
        features[col] = features[col].astype(int)

    # Environmental disruption indicator
    features['env_disruption'] = (
        (features['rainfall_mm'] > 30) |
        (features['aqi'] > 300) |
        (features['temperature_c'] > 43)
    ).astype(int)

    # Composite integrity score
    features['integrity_score'] = (
        features['gps_consistent'] * 25 +
        features['activity_coherent'] * 20 +
        features['timing_correlated'] * 15 +
        features['device_clean'] * 10
    )

    features['is_fraud'] = (~claims_df['is_legitimate']).astype(int)

    return features


def engineer_boost_features(earnings_df, weather_df):
    """
    Build feature matrix for earnings boost prediction.
    Predict earnings potential per zone/time based on conditions.
    """
    features = []

    for _, row in earnings_df.iterrows():
        weather_match = weather_df[
            (weather_df['city'] == row['city']) &
            (weather_df['zone'] == row['zone']) &
            (weather_df['date'] == row['date'])
        ]

        rainfall = weather_match['rainfall_mm'].iloc[0] if len(weather_match) > 0 else 0
        aqi = weather_match['aqi'].iloc[0] if len(weather_match) > 0 else 100
        temp = weather_match['temperature_c'].iloc[0] if len(weather_match) > 0 else 30
        humidity = weather_match['humidity_pct'].iloc[0] if len(weather_match) > 0 else 60

        # Cyclic time encoding
        day_of_week = row['day_of_week']
        day_sin = np.sin(2 * np.pi * day_of_week / 7)
        day_cos = np.cos(2 * np.pi * day_of_week / 7)

        features.append({
            'day_sin': round(day_sin, 4),
            'day_cos': round(day_cos, 4),
            'rainfall_mm': rainfall,
            'aqi': aqi,
            'temperature_c': temp,
            'humidity_pct': humidity,
            'is_weekend': int(day_of_week >= 5),
            'hours_worked': row['hours_worked'],
            'orders_completed': row['orders_completed'],
            'target_earnings': row['earnings'],
        })

    return pd.DataFrame(features)
