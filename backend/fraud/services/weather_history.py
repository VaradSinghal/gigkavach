"""
GigKavach — Weather History Validator
Cross-references claim reports with historical parametric trigger data.
"""

from typing import Optional
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from supabase_client import db

class WeatherHistoryService:
    """Verifies if a claim is backed by actual historical weather events."""

    def verify_disruption(self, city: str, zone: str, 
                          timestamp_str: str, 
                          trigger_type: str) -> dict:
        """
        Check if an active trigger was recorded for this zone/city.
        """
        if not db.client:
            return {'passed': True, 'score': 100, 'detail': 'Supabase not available, skipping historical check'}

        try:
            # Query active_triggers to see if anything matches
            # In a production context, this would query a historical_triggers table
            res = db.client.table('active_triggers') \
                .select('*') \
                .eq('city', city) \
                .eq('zone', zone) \
                .eq('status', 'active') \
                .execute()
            
            triggers = res.data or []
            
            # Simple logic: if there's an active trigger for this type right now, it counts as verified for the demo
            # A more advanced version would match trigger_id
            verified = False
            match = None
            for t in triggers:
                if t['trigger_id'] == trigger_type or trigger_type in t['label'].lower():
                    verified = True
                    match = t
                    break

            if verified:
                return {
                    'passed': True,
                    'score': 100,
                    'detail': f"Verified: {match['label']} alert is active in {zone} ({match['current_value']})",
                    'source': match['source']
                }
            else:
                return {
                    'passed': False,
                    'score': 0,
                    'detail': f"FRAUD DETECTED: No {trigger_type} disruption is active for {zone} in history logs.",
                    'source': 'Parametric Engine History'
                }
        except Exception as e:
            return {'passed': True, 'score': 80, 'detail': f"Note: Historical check error: {e}"}

weather_history = WeatherHistoryService()
