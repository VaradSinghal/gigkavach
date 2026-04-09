"""
GigKavach — GPS Fraud Detector
Analyzes location trails to detect spoofing, teleportation, or unrealistic velocity.
"""

import math
from datetime import datetime

class GPSDetector:
    """Verifies GPS consistency using velocity and geographical constraints."""

    def __init__(self):
        # Velocity limit in km/h (e.g., 80km/h for city delivery)
        self.MAX_DELIVERY_VELOCITY_KMH = 80.0

    def verify_location_consistency(self, current_lat: float, current_lon: float, 
                                   last_lat: float, last_lon: float, 
                                   time_diff_seconds: float) -> dict:
        """
        Check if the distance traveled between two points is realistic for the given time.
        """
        if time_diff_seconds <= 0:
            return {'passed': True, 'score': 100, 'detail': 'Insufficient history for velocity check'}

        # Calculate distance using Haversine
        distance_km = self._haversine(last_lat, last_lon, current_lat, current_lon)
        
        # Calculate velocity
        velocity_kmh = (distance_km / (time_diff_seconds / 3600))

        is_realistic = velocity_kmh <= self.MAX_DELIVERY_VELOCITY_KMH
        
        # Score calculation: 100 for realistic, scales down based on overage
        if is_realistic:
            score = 100
            detail = f"Velocity consistent ({velocity_kmh:.1f} km/h)"
        else:
            # Drop score quickly if velocity is ridiculous (e.g. teleportation)
            score = max(0, 100 - int((velocity_kmh - self.MAX_DELIVERY_VELOCITY_KMH) * 2))
            detail = f"SUSPICIOUS: Unrealistic velocity ({velocity_kmh:.1f} km/h) - Likely GPS Spoofing"

        return {
            'passed': is_realistic,
            'velocity_kmh': round(velocity_kmh, 2),
            'distance_km': round(distance_km, 3),
            'score': score,
            'detail': detail
        }

    def _haversine(self, lat1, lon1, lat2, lon2):
        """Calculate the great circle distance between two points on the earth."""
        R = 6371.0 # Earth radius in km
        
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        
        a = math.sin(d_lat / 2)**2 + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(d_lon / 2)**2
            
        c = 2 * math.asin(math.sqrt(a))
        return R * c

detector = GPSDetector()
