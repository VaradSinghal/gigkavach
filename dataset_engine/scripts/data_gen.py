"""
GigKavach — Dataset Engine
Generates synthetic training datasets for all insurance and fraud models.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

CITIES = {
    'Chennai': {
        'zones': ['Adyar', 'Velachery', 'T. Nagar', 'Mylapore', 'Anna Nagar',
                  'Guindy', 'Porur', 'Tambaram', 'Sholinganallur', 'Chromepet'],
        'lat_range': (12.85, 13.15),
        'lon_range': (80.15, 80.30),
        'flood_prone': ['Velachery', 'Adyar', 'Tambaram', 'Porur'],
        'avg_temp_range': (28, 38),
        'monsoon_months': [10, 11, 12],
    },
    'Delhi': {
        'zones': ['Connaught Place', 'Dwarka', 'Rohini', 'Saket', 'Lajpat Nagar',
                  'Karol Bagh', 'Chandni Chowk', 'Nehru Place', 'Janakpuri', 'Pitampura'],
        'lat_range': (28.50, 28.75),
        'lon_range': (77.10, 77.30),
        'flood_prone': ['Dwarka', 'Rohini', 'Chandni Chowk'],
        'avg_temp_range': (22, 46),
        'monsoon_months': [7, 8, 9],
    },
    'Mumbai': {
        'zones': ['Andheri', 'Bandra', 'Dadar', 'Borivali', 'Kurla',
                  'Goregaon', 'Malad', 'Powai', 'Thane', 'Navi Mumbai'],
        'lat_range': (19.00, 19.25),
        'lon_range': (72.82, 72.95),
        'flood_prone': ['Kurla', 'Dadar', 'Andheri', 'Malad'],
        'avg_temp_range': (25, 37),
        'monsoon_months': [6, 7, 8, 9],
    }
}

def generate_worker_data(n_workers=500):
    workers = []
    platforms = ['Swiggy', 'Zomato', 'Zepto']
    vehicle_types = ['Bike', 'Scooter', 'Bicycle']

    for i in range(n_workers):
        city = random.choice(list(CITIES.keys()))
        city_config = CITIES[city]
        zone = random.choice(city_config['zones'])
        primary = random.choice(platforms)
        secondary_options = [p for p in platforms if p != primary] + [None]

        worker = {
            'worker_id': f'GK-{10000 + i}',
            'city': city,
            'zone': zone,
            'primary_platform': primary,
            'secondary_platform': random.choice(secondary_options),
            'vehicle_type': random.choice(vehicle_types),
            'avg_daily_hours': round(np.random.uniform(6, 14), 1),
            'experience_weeks': random.randint(4, 120),
            'avg_daily_income': round(np.random.normal(700, 150), 2),
            'avg_weekly_income': 0,
            'latitude': round(np.random.uniform(*city_config['lat_range']), 6),
            'longitude': round(np.random.uniform(*city_config['lon_range']), 6),
            'is_flood_zone': zone in city_config['flood_prone'],
            'trust_score': round(np.random.uniform(0.5, 1.0), 3),
        }
        worker['avg_weekly_income'] = round(worker['avg_daily_income'] * np.random.uniform(5, 6.5), 2)
        workers.append(worker)

    return pd.DataFrame(workers)

def generate_weather_data(n_days=180):
    records = []
    start_date = datetime(2025, 10, 1)

    for city, config in CITIES.items():
        for zone in config['zones']:
            is_flood_prone = zone in config['flood_prone']
            for day_offset in range(n_days):
                date = start_date + timedelta(days=day_offset)
                month = date.month
                is_monsoon = month in config['monsoon_months']

                base_temp = np.random.uniform(*config['avg_temp_range'])
                if month in [12, 1, 2]:
                    base_temp -= np.random.uniform(3, 8)
                elif month in [4, 5, 6]:
                    base_temp += np.random.uniform(2, 5)
                temp = round(np.clip(base_temp, 15, 48), 1)

                if is_monsoon:
                    rain_prob = 0.6 if is_flood_prone else 0.4
                    rainfall_mm = round(np.random.exponential(20) if random.random() < rain_prob else 0, 1)
                else:
                    rain_prob = 0.1
                    rainfall_mm = round(np.random.exponential(5) if random.random() < rain_prob else 0, 1)

                if city == 'Delhi' and month in [11, 12, 1]:
                    aqi = int(np.random.normal(350, 80))
                else:
                    aqi = int(np.random.normal(120, 50))
                aqi = max(20, min(500, aqi))

                humidity = round(np.random.uniform(50, 95) if is_monsoon else np.random.uniform(30, 70), 1)
                wind_speed = round(np.random.uniform(5, 30), 1)

                records.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'city': city,
                    'zone': zone,
                    'temperature_c': temp,
                    'rainfall_mm': rainfall_mm,
                    'aqi': aqi,
                    'humidity_pct': humidity,
                    'wind_speed_kmh': wind_speed,
                    'is_monsoon': is_monsoon,
                    'is_flood_prone': is_flood_prone,
                    'month': month,
                    'day_of_week': date.weekday(),
                })

    return pd.DataFrame(records)

def generate_zone_features():
    records = []
    for city, config in CITIES.items():
        for zone in config['zones']:
            is_flood_prone = zone in config['flood_prone']
            records.append({
                'city': city,
                'zone': zone,
                'elevation_m': round(np.random.uniform(2, 50) if is_flood_prone else np.random.uniform(20, 100), 1),
                'drainage_score': round(np.random.uniform(0.2, 0.5) if is_flood_prone else np.random.uniform(0.6, 0.95), 2),
                'road_density': round(np.random.uniform(0.4, 0.9), 2),
                'historical_flood_events': random.randint(5, 20) if is_flood_prone else random.randint(0, 3),
                'historical_disruption_days': random.randint(15, 50) if is_flood_prone else random.randint(2, 12),
                'avg_traffic_density': round(np.random.uniform(0.4, 0.95), 2),
                'population_density': round(np.random.uniform(5000, 25000), 0),
                'restaurant_density': round(np.random.uniform(10, 100), 0),
                'avg_order_demand': round(np.random.uniform(50, 300), 0),
                'latitude': round(np.random.uniform(*config['lat_range']), 6),
                'longitude': round(np.random.uniform(*config['lon_range']), 6),
            })
    return pd.DataFrame(records)

def generate_claims_data(workers_df, weather_df, n_claims=2000):
    claims = []
    claim_types = ['Heavy Rainfall', 'Severe AQI', 'Extreme Heat', 'Flooding', 'Civic Disruption']
    bad_weather = weather_df[(weather_df['rainfall_mm'] > 30) | (weather_df['aqi'] > 300) | (weather_df['temperature_c'] > 43)]

    for i in range(n_claims):
        worker = workers_df.sample(1).iloc[0]
        is_legitimate = random.random() < 0.85

        if is_legitimate and len(bad_weather) > 0:
            weather_row = bad_weather[(bad_weather['city'] == worker['city']) & (bad_weather['zone'] == worker['zone'])]
            if len(weather_row) == 0:
                weather_row = bad_weather[bad_weather['city'] == worker['city']]
            weather_event = weather_row.sample(1).iloc[0] if len(weather_row) > 0 else weather_df.sample(1).iloc[0]
        else:
            weather_event = weather_df.sample(1).iloc[0]

        if weather_event['rainfall_mm'] > 40:
            claim_type = 'Heavy Rainfall' if random.random() > 0.3 else 'Flooding'
        elif weather_event['aqi'] > 350:
            claim_type = 'Severe AQI'
        elif weather_event['temperature_c'] > 43:
            claim_type = 'Extreme Heat'
        else:
            claim_type = random.choice(claim_types)

        inactive_hours = round(np.random.uniform(3, 10), 1)
        hourly_income = worker['avg_daily_income'] / worker['avg_daily_hours']
        payout_amount = round(inactive_hours * hourly_income * 0.7, 2)

        gps_consistent = random.random() < (0.95 if is_legitimate else 0.3)
        activity_coherent = random.random() < (0.9 if is_legitimate else 0.25)
        timing_correlated = random.random() < (0.92 if is_legitimate else 0.2)
        device_clean = random.random() < (0.98 if is_legitimate else 0.5)

        env_score = 30 if (weather_event['rainfall_mm'] > 30 or weather_event['aqi'] > 300 or weather_event['temperature_c'] > 43) else random.randint(5, 15)
        loc_score = 25 if gps_consistent else random.randint(3, 10)
        act_score = 20 if activity_coherent else random.randint(2, 8)
        time_score = 15 if timing_correlated else random.randint(1, 6)
        dev_score = 10 if device_clean else random.randint(1, 4)
        confidence_score = env_score + loc_score + act_score + time_score + dev_score

        claims.append({
            'claim_id': f'CLM-{100000 + i}',
            'worker_id': worker['worker_id'],
            'city': worker['city'],
            'zone': worker['zone'],
            'date': weather_event['date'],
            'claim_type': claim_type,
            'inactive_hours': inactive_hours,
            'payout_amount': payout_amount,
            'rainfall_mm': weather_event['rainfall_mm'],
            'aqi': weather_event['aqi'],
            'temperature_c': weather_event['temperature_c'],
            'gps_consistent': gps_consistent,
            'activity_coherent': activity_coherent,
            'timing_correlated': timing_correlated,
            'device_clean': device_clean,
            'confidence_score': confidence_score,
            'is_legitimate': is_legitimate,
            'status': 'approved' if confidence_score >= 80 else ('review' if confidence_score >= 50 else 'rejected'),
        })
    return pd.DataFrame(claims)

def generate_earnings_data(workers_df, weather_df, n_records=5000):
    records = []
    
    for _ in range(n_records):
        worker = workers_df.sample(1).iloc[0]
        # Choose a random date from weather data
        weather_row = weather_df[(weather_df['city'] == worker['city']) & (weather_df['zone'] == worker['zone'])].sample(1).iloc[0]
        
        # Base earnings
        base_rate = worker['avg_daily_income'] / 6 # Assuming 6 hours avg
        hours_worked = round(np.random.normal(worker['avg_daily_hours'], 1.5), 1)
        hours_worked = max(2, min(14, hours_worked))
        
        # Environmental impact
        env_impact = 1.0
        if weather_row['rainfall_mm'] > 20: env_impact -= 0.2
        if weather_row['aqi'] > 300: env_impact -= 0.1
        if weather_row['temperature_c'] > 42: env_impact -= 0.15
        
        # Boost probability
        is_weekend = weather_row['day_of_week'] >= 5
        boost = 1.2 if is_weekend else 1.0
        
        earnings = round(base_rate * hours_worked * env_impact * boost * np.random.uniform(0.9, 1.1), 2)
        orders = int(hours_worked * np.random.uniform(1.5, 3.0))
        
        records.append({
            'worker_id': worker['worker_id'],
            'city': worker['city'],
            'zone': worker['zone'],
            'date': weather_row['date'],
            'day_of_week': weather_row['day_of_week'],
            'hours_worked': hours_worked,
            'orders_completed': orders,
            'rainfall_mm': weather_row['rainfall_mm'],
            'aqi': weather_row['aqi'],
            'temperature_c': weather_row['temperature_c'],
            'humidity_pct': weather_row['humidity_pct'],
            'earnings': earnings,
            'target_earnings': earnings # For training
        })
    
    return pd.DataFrame(records)

def generate_all_data(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(output_dir, exist_ok=True)

    print("Generating datasets...")
    workers_df = generate_worker_data(2000) # Increased for DL
    workers_df.to_csv(os.path.join(output_dir, 'workers.csv'), index=False)
    
    weather_df = generate_weather_data(180)
    weather_df.to_csv(os.path.join(output_dir, 'weather.csv'), index=False)
    
    zones_df = generate_zone_features()
    zones_df.to_csv(os.path.join(output_dir, 'zones.csv'), index=False)
    
    claims_df = generate_claims_data(workers_df, weather_df, 5000) # Increased for DL
    claims_df.to_csv(os.path.join(output_dir, 'claims.csv'), index=False)
    
    earnings_df = generate_earnings_data(workers_df, weather_df, 10000)
    earnings_df.to_csv(os.path.join(output_dir, 'earnings.csv'), index=False)
    
    print(f"[SUCCESS] All data saved to: {output_dir}")
    return workers_df, weather_df, zones_df, claims_df, earnings_df

if __name__ == '__main__':
    generate_all_data()
