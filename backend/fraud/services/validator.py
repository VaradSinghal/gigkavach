"""
GigKavach — Fraud Validation Service
Multi-signal claim validation using the trained Isolation Forest + Random Forest models.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from ai.model_loader import loader
from fraud.services.gps_detector import detector as gps_detector
from fraud.services.weather_history import weather_history


class FraudValidator:
    """Validates claims using the 3-truth-layer approach with ML scoring."""

    def __init__(self):
        try:
            loader.load_all()
        except Exception:
            pass

    def validate_claim(self, claim_data: dict) -> dict:
        """
        Run multi-signal validation on a claim.
        Returns confidence score (0-100) and action recommendation.
        """
        # 1. Direct Signal: GPS Spoofing Detection
        gps_verify = gps_detector.verify_location_consistency(
            current_lat=claim_data.get('latitude', 0),
            current_lon=claim_data.get('longitude', 0),
            last_lat=claim_data.get('last_lat', 0),
            last_lon=claim_data.get('last_lon', 0),
            time_diff_seconds=claim_data.get('time_diff_seconds', 0)
        )

        # 2. Direct Signal: Weather History Check (Disruption Verification)
        weather_verify = weather_history.verify_disruption(
            city=claim_data.get('city', 'Unknown'),
            zone=claim_data.get('zone', 'Unknown'),
            timestamp_str=claim_data.get('timestamp', ''),
            trigger_type=claim_data.get('trigger_type', 'unknown')
        )

        # 3. Preparation for ML Model
        # Map original signals or use the new detector outputs
        env_disruption = 1 if weather_verify['passed'] else 0
        gps_consistent = 1 if gps_verify['passed'] else 0
        
        features = {
            'rainfall_mm': claim_data.get('rainfall_mm', 0),
            'aqi': claim_data.get('aqi', 100),
            'temperature_c': claim_data.get('temperature_c', 30),
            'inactive_hours': claim_data.get('inactive_hours', 5),
            'payout_amount': claim_data.get('payout_amount', 400),
            'gps_consistent': gps_consistent,
            'activity_coherent': int(claim_data.get('activity_coherent', True)),
            'timing_correlated': int(claim_data.get('timing_correlated', True)),
            'device_clean': int(claim_data.get('device_clean', True)),
            'env_disruption': env_disruption,
            'integrity_score': (
                gps_consistent * 25 +
                int(claim_data.get('activity_coherent', True)) * 20 +
                int(claim_data.get('timing_correlated', True)) * 15 +
                int(claim_data.get('device_clean', True)) * 10
            ),
        }

        # Run ML Inference
        result = loader.predict_fraud_score(features)

        # Map to action
        confidence = result['confidence']
        
        # Override action if high-confidence spoofing or weather mismatch detected
        if not weather_verify['passed']:
            confidence = min(confidence, 10)
            reason = weather_verify['detail']
        elif not gps_verify['passed']:
            confidence = min(confidence, 20)
            reason = gps_verify['detail']
        else:
            reason = "ML validation patterns are consistent."

        if confidence >= 80:
            action = 'auto_approve'
            action_label = 'Auto-Approved'
        elif confidence >= 50:
            action = 'soft_review'
            action_label = 'Manual Review Required'
        else:
            action = 'reject'
            action_label = f'Rejected: {reason}'

        return {
            'confidence_score': int(confidence),
            'fraud_probability': result.get('fraud_probability', 0),
            'anomaly_score': result.get('anomaly_score', 0),
            'action': action,
            'action_label': action_label,
            'reason': reason,
            'signals': {
                'environmental': {'score': 30, 'passed': bool(env_disruption), 'detail': weather_verify['detail']},
                'location': {'score': 25, 'passed': bool(gps_consistent), 'detail': gps_verify['detail']},
                'activity': {'score': 20, 'passed': bool(features['activity_coherent'])},
                'timing': {'score': 15, 'passed': bool(features['timing_correlated'])},
                'device': {'score': 10, 'passed': bool(features['device_clean'])},
            },
        }
