"""
GigKavach — Fraud Validation Service
Multi-signal claim validation using the trained Isolation Forest + Random Forest models.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from ai.model_loader import loader


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
        features = {
            'rainfall_mm': claim_data.get('rainfall_mm', 0),
            'aqi': claim_data.get('aqi', 100),
            'temperature_c': claim_data.get('temperature_c', 30),
            'inactive_hours': claim_data.get('inactive_hours', 5),
            'payout_amount': claim_data.get('payout_amount', 400),
            'gps_consistent': int(claim_data.get('gps_consistent', True)),
            'activity_coherent': int(claim_data.get('activity_coherent', True)),
            'timing_correlated': int(claim_data.get('timing_correlated', True)),
            'device_clean': int(claim_data.get('device_clean', True)),
            'env_disruption': int(claim_data.get('env_disruption', True)),
            'integrity_score': (
                int(claim_data.get('gps_consistent', True)) * 25 +
                int(claim_data.get('activity_coherent', True)) * 20 +
                int(claim_data.get('timing_correlated', True)) * 15 +
                int(claim_data.get('device_clean', True)) * 10
            ),
        }

        result = loader.predict_fraud_score(features)

        # Map to action
        confidence = result['confidence']
        if confidence >= 80:
            action = 'auto_approve'
            action_label = 'Auto-Approved'
        elif confidence >= 50:
            action = 'soft_review'
            action_label = 'Manual Review Required'
        else:
            action = 'reject'
            action_label = 'Rejected - Low Confidence'

        return {
            'confidence_score': confidence,
            'fraud_probability': result.get('fraud_probability', 0),
            'anomaly_score': result.get('anomaly_score', 0),
            'action': action,
            'action_label': action_label,
            'signals': {
                'environmental': {'score': 30, 'passed': bool(features['env_disruption'])},
                'location': {'score': 25, 'passed': bool(features['gps_consistent'])},
                'activity': {'score': 20, 'passed': bool(features['activity_coherent'])},
                'timing': {'score': 15, 'passed': bool(features['timing_correlated'])},
                'device': {'score': 10, 'passed': bool(features['device_clean'])},
            },
        }
