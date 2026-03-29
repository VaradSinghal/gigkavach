"""
GigKavach — Hyperlocal Zone Risk Engine
Uses trained K-Means clustering model for zone risk scoring.
"""

import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from ai.model_loader import loader


class RiskEngine:
    """Computes zone-level risk scores using ML clustering model."""

    def __init__(self):
        self._scores_cache = None
        try:
            loader.load_all()
        except Exception:
            pass
        self._load_precomputed_scores()

    def _load_precomputed_scores(self):
        """Load pre-computed risk scores from training output."""
        scores_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'ai', 'saved_models', 'zone_risk_scores.json'
        )
        try:
            with open(scores_path) as f:
                self._scores_cache = json.load(f)
        except Exception:
            self._scores_cache = []

    def get_zone_risk_score(self, city: str, zone: str) -> dict:
        """Get risk score for a specific zone."""
        for entry in (self._scores_cache or []):
            if entry['city'] == city and entry['zone'] == zone:
                return {
                    'city': city,
                    'zone': zone,
                    'risk_score': entry['risk_score'],
                    'risk_label': entry['risk_label'],
                    'cluster': entry['cluster'],
                }
        # Default if not found
        return {
            'city': city,
            'zone': zone,
            'risk_score': 50.0,
            'risk_label': 'Moderate',
            'cluster': 1,
        }

    def get_city_heatmap(self, city: str) -> list:
        """Get risk scores for all zones in a city."""
        return [
            self.get_zone_risk_score(entry['city'], entry['zone'])
            for entry in (self._scores_cache or [])
            if entry['city'] == city
        ]

    def get_all_scores(self) -> list:
        """Get all precomputed zone risk scores."""
        return self._scores_cache or []
