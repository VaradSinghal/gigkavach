"""
GigKavach — Dynamic Premium Calculator Service
Uses the trained ML model for real-time premium pricing.
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from ai.model_loader import loader


class PremiumCalculator:
    """Calculates dynamic weekly premiums using ML model + business rules."""

    PLAN_TIERS = {
        'basic': {'base_rate': 25, 'coverage_pct': 50, 'triggers': 3},
        'standard': {'base_rate': 45, 'coverage_pct': 70, 'triggers': 5},
        'premium': {'base_rate': 65, 'coverage_pct': 85, 'triggers': 5},
    }

    def __init__(self):
        try:
            loader.load_all()
        except Exception:
            pass

    def calculate_premium(self, worker: dict, zone_risk_score: float = 50,
                          weather_forecast_risk: float = 0.3, plan_tier: str = 'standard') -> dict:
        """
        Calculate personalized weekly premium.

        Args:
            worker: Worker profile dict with earnings, experience, claims history
            zone_risk_score: 0-100 risk score from zone risk model
            weather_forecast_risk: 0-1 weather risk factor
            plan_tier: 'basic', 'standard', or 'premium'
        """
        tier = self.PLAN_TIERS.get(plan_tier, self.PLAN_TIERS['standard'])
        base_rate = tier['base_rate']

        # Try ML model first
        ml_premium = self._predict_with_model(worker, zone_risk_score)

        if ml_premium is not None:
            # Use ML prediction as base, apply tier multiplier
            tier_multiplier = base_rate / 45  # normalize to standard tier
            premium = ml_premium * tier_multiplier
        else:
            # Fallback: rule-based calculation
            premium = self._rule_based_calculation(worker, zone_risk_score,
                                                    weather_forecast_risk, base_rate)

        # Build breakdown
        zone_adj = round(zone_risk_score / 100 * 20, 2)
        weather_adj = round(weather_forecast_risk * 15, 2)
        claims_adj = round(worker.get('claim_rate', 0) * 10, 2)
        loyalty_disc = round(min(worker.get('experience_weeks', 0) / 16 * 5, 10), 2)

        premium = round(max(15, premium), 2)
        coverage_ceiling = round(worker.get('avg_weekly_income', 4200) * tier['coverage_pct'] / 100, 2)

        return {
            'weekly_premium': premium,
            'plan_tier': plan_tier,
            'coverage_percentage': tier['coverage_pct'],
            'coverage_ceiling': coverage_ceiling,
            'triggers_covered': tier['triggers'],
            'breakdown': {
                'base_rate': base_rate,
                'zone_risk_adjustment': zone_adj,
                'weather_forecast_adjustment': weather_adj,
                'claims_history_adjustment': claims_adj,
                'loyalty_discount': loyalty_disc,
                'safe_zone_discount': 2.0 if zone_risk_score < 30 else 0.0,
            },
            'factors': {
                'zone_risk_score': zone_risk_score,
                'weather_forecast_risk': weather_forecast_risk,
                'experience_weeks': worker.get('experience_weeks', 0),
                'claim_count': worker.get('claim_count', 0),
                'is_flood_zone': worker.get('is_flood_zone', False),
            },
            'model_used': 'ml' if ml_premium else 'rule_based',
        }

    def _predict_with_model(self, worker: dict, zone_risk_score: float):
        """Use trained ML model for premium prediction."""
        if loader.premium_model is None:
            return None

        try:
            features = {
                'avg_daily_income': worker.get('avg_daily_income', 700),
                'avg_weekly_income': worker.get('avg_weekly_income', 4200),
                'avg_daily_hours': worker.get('avg_daily_hours', 10),
                'experience_weeks': worker.get('experience_weeks', 12),
                'is_flood_zone': int(worker.get('is_flood_zone', False)),
                'trust_score': worker.get('trust_score', 0.8),
                'elevation_m': worker.get('elevation_m', 30),
                'drainage_score': worker.get('drainage_score', 0.6),
                'historical_flood_events': worker.get('historical_flood_events', 5),
                'historical_disruption_days': worker.get('historical_disruption_days', 15),
                'road_density': worker.get('road_density', 0.7),
                'avg_rainfall_mm': worker.get('avg_rainfall_mm', 8),
                'max_rainfall_mm': worker.get('max_rainfall_mm', 50),
                'avg_aqi': worker.get('avg_aqi', 120),
                'heavy_rain_day_ratio': worker.get('heavy_rain_day_ratio', 0.1),
                'claim_count': worker.get('claim_count', 2),
                'claim_rate': worker.get('claim_rate', 0.08),
                'total_payout': worker.get('total_payout', 800),
            }
            result = loader.predict_premium(features)
            return result['premium']
        except Exception:
            return None

    def _rule_based_calculation(self, worker: dict, zone_risk: float,
                                 weather_risk: float, base_rate: float) -> float:
        """Fallback rule-based premium calculation."""
        zone_adj = zone_risk / 100 * 20
        weather_adj = weather_risk * 15
        claims_adj = worker.get('claim_rate', 0) * 10
        loyalty_disc = min(worker.get('experience_weeks', 0) / 16 * 5, 10)
        safe_zone_disc = 2.0 if zone_risk < 30 else 0.0

        return base_rate + zone_adj + weather_adj + claims_adj - loyalty_disc - safe_zone_disc
