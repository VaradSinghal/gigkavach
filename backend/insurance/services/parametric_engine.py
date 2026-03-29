"""
GigKavach — Parametric Trigger Engine
Monitors real-time API data and detects income-disrupting events.
5 automated triggers using public/mock APIs.
"""

import random
from datetime import datetime


class ParametricEngine:
    """Monitors 5 disruption triggers and auto-creates claims."""

    TRIGGERS = {
        'heavy_rainfall': {
            'label': 'Heavy Rainfall',
            'threshold': '>40mm in 6-hour window',
            'threshold_value': 40,
            'source': 'OpenWeather API',
            'poll_interval_min': 15,
        },
        'severe_aqi': {
            'label': 'Severe AQI',
            'threshold': '>350 for 3+ consecutive hours',
            'threshold_value': 350,
            'source': 'AQICN API',
            'poll_interval_min': 30,
        },
        'extreme_heat': {
            'label': 'Extreme Heat',
            'threshold': '>43°C during work hours (8AM-8PM)',
            'threshold_value': 43,
            'source': 'OpenWeather API',
            'poll_interval_min': 30,
        },
        'flooding': {
            'label': 'Flood Alert',
            'threshold': 'Active IMD flood warning for zone',
            'threshold_value': None,
            'source': 'IMD Alert Feed (Mock)',
            'poll_interval_min': 60,
        },
        'civic_disruption': {
            'label': 'Civic Disruption',
            'threshold': 'Bandh/strike/curfew detected',
            'threshold_value': None,
            'source': 'News API + Traffic (Mock)',
            'poll_interval_min': 60,
        },
    }

    def check_all_triggers(self, zone: str, city: str) -> list:
        """
        Check all 5 triggers for a given zone.
        Returns list of triggered events.
        """
        results = []
        weather_data = self._fetch_weather(city, zone)
        aqi_data = self._fetch_aqi(city, zone)
        flood_data = self._check_flood_alert(city, zone)
        civic_data = self._check_civic_disruption(city, zone)

        # Trigger 1: Heavy Rainfall
        if weather_data['rainfall_6hr_mm'] > 40:
            results.append({
                'trigger': 'heavy_rainfall',
                'label': 'Heavy Rainfall',
                'value': f"{weather_data['rainfall_6hr_mm']}mm in 6hrs",
                'threshold': '>40mm in 6hrs',
                'severity': self._severity(weather_data['rainfall_6hr_mm'], 40, 80),
                'data': weather_data,
            })

        # Trigger 2: Severe AQI
        if aqi_data['aqi'] > 350 and aqi_data['consecutive_hours'] >= 3:
            results.append({
                'trigger': 'severe_aqi',
                'label': 'Severe AQI',
                'value': f"AQI {aqi_data['aqi']} for {aqi_data['consecutive_hours']}hrs",
                'threshold': '>350 for 3+ hours',
                'severity': self._severity(aqi_data['aqi'], 350, 500),
                'data': aqi_data,
            })

        # Trigger 3: Extreme Heat
        hour = datetime.now().hour
        if weather_data['temperature_c'] > 43 and 8 <= hour <= 20:
            results.append({
                'trigger': 'extreme_heat',
                'label': 'Extreme Heat',
                'value': f"{weather_data['temperature_c']}°C",
                'threshold': '>43°C during work hours',
                'severity': self._severity(weather_data['temperature_c'], 43, 50),
                'data': weather_data,
            })

        # Trigger 4: Flooding
        if flood_data['active_alert']:
            results.append({
                'trigger': 'flooding',
                'label': 'Flood Alert',
                'value': flood_data['alert_message'],
                'threshold': 'Active IMD alert',
                'severity': flood_data['severity'],
                'data': flood_data,
            })

        # Trigger 5: Civic Disruption
        if civic_data['active']:
            results.append({
                'trigger': 'civic_disruption',
                'label': 'Civic Disruption',
                'value': civic_data['description'],
                'threshold': 'Zone closure/bandh',
                'severity': civic_data['severity'],
                'data': civic_data,
            })

        return results

    def get_trigger_status(self, zone: str, city: str) -> list:
        """Get current status of all 5 triggers (for dashboard display) and sync to Supabase."""
        weather = self._fetch_weather(city, zone)
        aqi = self._fetch_aqi(city, zone)
        flood = self._check_flood_alert(city, zone)
        civic = self._check_civic_disruption(city, zone)

        triggers = [
            {
                'id': 'heavy_rainfall',
                'label': 'Heavy Rainfall',
                'threshold': '>40mm / 6hrs',
                'current_value': f"{weather['rainfall_6hr_mm']}mm",
                'risk_level': min(weather['rainfall_6hr_mm'] / 60, 1.0),
                'status': 'triggered' if weather['rainfall_6hr_mm'] > 40 else 'monitoring',
                'source': 'OpenWeather API',
            },
            {
                'id': 'severe_aqi',
                'label': 'Severe AQI',
                'threshold': '>350 / 3hrs',
                'current_value': f"AQI {aqi['aqi']}",
                'risk_level': min(aqi['aqi'] / 500, 1.0),
                'status': 'triggered' if aqi['aqi'] > 350 else 'monitoring',
                'source': 'AQICN API',
            },
            {
                'id': 'extreme_heat',
                'label': 'Extreme Heat',
                'threshold': '>43°C',
                'current_value': f"{weather['temperature_c']}°C",
                'risk_level': max(0, (weather['temperature_c'] - 35) / 15),
                'status': 'triggered' if weather['temperature_c'] > 43 else 'monitoring',
                'source': 'OpenWeather API',
            },
            {
                'id': 'flooding',
                'label': 'Flood Alert',
                'threshold': 'IMD alert active',
                'current_value': flood['alert_message'] if flood['active_alert'] else 'No alerts',
                'risk_level': 0.9 if flood['active_alert'] else 0.0,
                'status': 'triggered' if flood['active_alert'] else 'safe',
                'source': 'IMD Alert Feed',
            },
            {
                'id': 'civic_disruption',
                'label': 'Civic Disruption',
                'threshold': 'Zone closure',
                'current_value': civic['description'] if civic['active'] else 'All clear',
                'risk_level': 0.8 if civic['active'] else 0.0,
                'status': 'triggered' if civic['active'] else 'safe',
                'source': 'News + Traffic API',
            },
        ]

        # [SUPABASE] Sync triggers to remote database
        try:
            from supabase_client import db
            if db.client:
                for t in triggers:
                    db_trigger = {
                        'trigger_id': t['id'],
                        'city': city,
                        'zone': zone,
                        'label': t['label'],
                        'threshold': t['threshold'],
                        'current_value': t['current_value'],
                        'risk_level': t['risk_level'],
                        'status': t['status'],
                        'source': t['source']
                    }
                    db.client.table('active_triggers').upsert(db_trigger, on_conflict='trigger_id,city,zone').execute()
        except Exception as e:
            print(f"[Supabase Sync Error] Failed to upload triggers: {e}")

        return triggers

    # ─── Mock API Data Sources ────────────────────────────────────

    def _fetch_weather(self, city: str, zone: str) -> dict:
        """Simulated OpenWeather API response."""
        # In production: calls OpenWeather API
        # For demo: returns realistic simulated data
        base_temp = {'Chennai': 33, 'Delhi': 35, 'Mumbai': 31}.get(city, 32)
        base_rain = random.uniform(0, 20)

        return {
            'temperature_c': round(base_temp + random.uniform(-3, 5), 1),
            'humidity_pct': round(random.uniform(55, 90), 1),
            'rainfall_6hr_mm': round(base_rain, 1),
            'wind_speed_kmh': round(random.uniform(5, 25), 1),
            'condition': 'Light Rain' if base_rain > 5 else 'Clear',
            'source': 'OpenWeather API',
            'timestamp': datetime.now().isoformat(),
        }

    def _fetch_aqi(self, city: str, zone: str) -> dict:
        """Simulated AQICN API response."""
        base_aqi = {'Chennai': 95, 'Delhi': 250, 'Mumbai': 110}.get(city, 100)
        aqi = int(base_aqi + random.uniform(-30, 50))

        return {
            'aqi': aqi,
            'category': 'Hazardous' if aqi > 400 else 'Very Unhealthy' if aqi > 300
                        else 'Unhealthy' if aqi > 200 else 'Moderate' if aqi > 100 else 'Good',
            'consecutive_hours': random.randint(0, 6) if aqi > 300 else 0,
            'pm25': round(aqi * 0.4, 1),
            'pm10': round(aqi * 0.6, 1),
            'source': 'AQICN API',
            'timestamp': datetime.now().isoformat(),
        }

    def _check_flood_alert(self, city: str, zone: str) -> dict:
        """Simulated IMD flood alert check."""
        flood_prone = {
            'Chennai': ['Velachery', 'Adyar', 'Tambaram', 'Porur'],
            'Delhi': ['Dwarka', 'Rohini'],
            'Mumbai': ['Kurla', 'Dadar', 'Andheri'],
        }
        is_flood_prone = zone in flood_prone.get(city, [])

        return {
            'active_alert': False,  # Set to True for demo scenarios
            'alert_message': f'Flood warning for {zone}' if is_flood_prone else 'No alerts',
            'severity': 'high' if is_flood_prone else 'none',
            'zone': zone,
            'source': 'IMD Alert Feed',
        }

    def _check_civic_disruption(self, city: str, zone: str) -> dict:
        """Simulated civic disruption check."""
        return {
            'active': False,  # Set to True for demo scenarios
            'description': 'All clear',
            'severity': 'none',
            'type': None,
            'zone': zone,
            'source': 'News + Traffic API',
        }

    def _severity(self, value: float, threshold: float, critical: float) -> str:
        """Calculate severity level."""
        ratio = (value - threshold) / (critical - threshold) if critical != threshold else 0
        if ratio > 0.7:
            return 'critical'
        elif ratio > 0.3:
            return 'high'
        return 'moderate'
