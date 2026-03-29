"""
GigKavach — Backend API & Mock Data Feeds
Provides REST endpoints for mock disruption APIs and parametric engine controls.
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import random
from typing import Optional, List
from datetime import datetime
import asyncio

from insurance.services.parametric_engine import ParametricEngine
from insurance.services.claim_processor import ClaimProcessor
from insurance.services.premium_calculator import PremiumCalculator
from supabase_client import db

app = FastAPI(title="GigKavach Mock External APIs")

# Keep singletons
engine = ParametricEngine()
processor = ClaimProcessor()
premium_calc = PremiumCalculator()

# Simulation State
class SimulationState:
    weather_override = None
    aqi_override = None
    flood_override = False
    civic_override = False

sim_state = SimulationState()

class SimulateRequest(BaseModel):
    city: str = "Chennai"
    zone: str = "Adyar"
    weather: Optional[dict] = None  # { "temperature_c": 44, "rainfall_6hr_mm": 50 }
    aqi: Optional[int] = None
    flood: Optional[bool] = None
    civic: Optional[bool] = None

@app.post("/api/mock/simulate")
def override_mock_state(req: SimulateRequest):
    """Overrides the internal mock state to manually trigger disruptions for the demo."""
    if req.weather:
        sim_state.weather_override = req.weather
    if req.aqi:
        sim_state.aqi_override = req.aqi
    if req.flood is not None:
        sim_state.flood_override = req.flood
    if req.civic is not None:
        sim_state.civic_override = req.civic
    
    return {"status": "success", "message": "Simulation overrides applied.", "state": __dict_state()}

def __dict_state():
    return {
        "weather": sim_state.weather_override,
        "aqi": sim_state.aqi_override,
        "flood": sim_state.flood_override,
        "civic": sim_state.civic_override
    }

@app.post("/api/mock/reset")
def reset_mock_state():
    sim_state.weather_override = None
    sim_state.aqi_override = None
    sim_state.flood_override = False
    sim_state.civic_override = False
    return {"status": "success", "message": "Simulation cleared back to normal local weather."}

# OVERRIDE the _fetch methods in ParametricEngine dynamically for the demo
original_fetch_weather = engine._fetch_weather
original_fetch_aqi = engine._fetch_aqi
original_check_flood = engine._check_flood_alert
original_check_civic = engine._check_civic_disruption

def demo_fetch_weather(city, zone):
    if sim_state.weather_override:
        return {
            'temperature_c': sim_state.weather_override.get('temperature_c', 32),
            'humidity_pct': 80,
            'rainfall_6hr_mm': sim_state.weather_override.get('rainfall_6hr_mm', 0),
            'wind_speed_kmh': 15,
            'condition': 'Custom',
            'source': 'OpenWeather API (Sim)',
            'timestamp': datetime.now().isoformat()
        }
    return original_fetch_weather(city, zone)

def demo_fetch_aqi(city, zone):
    if sim_state.aqi_override:
        return {
            'aqi': sim_state.aqi_override,
            'category': 'Hazardous',
            'consecutive_hours': 4,
            'pm25': sim_state.aqi_override * 0.4,
            'pm10': sim_state.aqi_override * 0.6,
            'source': 'AQICN API (Sim)',
            'timestamp': datetime.now().isoformat()
        }
    return original_fetch_aqi(city, zone)

def demo_check_flood(city, zone):
    if sim_state.flood_override:
        return {
            'active_alert': True,
            'alert_message': f'! CRITICAL: Flash Flood Warning in {zone}',
            'severity': 'critical',
            'zone': zone,
            'source': 'IMD Alert Feed (Sim)'
        }
    return original_check_flood(city, zone)

def demo_check_civic(city, zone):
    if sim_state.civic_override:
        return {
            'active': True,
            'description': 'Section 144 Imposed / Road Blockade',
            'severity': 'high',
            'type': 'protest',
            'zone': zone,
            'source': 'Traffic API (Sim)'
        }
    return original_check_civic(city, zone)

# Patch the engine instance
engine._fetch_weather = demo_fetch_weather
engine._fetch_aqi = demo_fetch_aqi
engine._check_flood_alert = demo_check_flood
engine._check_civic_disruption = demo_check_civic


@app.post("/api/engine/evaluate")
def run_parametric_engine(city: str = "Chennai", zone: str = "Adyar", limit: int = 5):
    """
    1. Checks current weather/disruption APIs for the zone.
    2. Upserts trigger status to Supabase.
    3. If any trigger is active, queries Supabase for impacted workers.
    4. Auto-generates claims through Phase 2 AI Validator.
    """
    if not db.client:
        raise HTTPException(status_code=500, detail="Supabase not configured.")
        
    print(f"🚀 Running Parametric Engine for {zone}, {city}...")
    
    # 1. Evaluate triggers and sync to DB
    status = engine.get_trigger_status(zone, city)
    active_triggers = engine.check_all_triggers(zone, city)
    
    # 2. Process impacted workers if there are active triggers
    claims_generated = []
    
    if len(active_triggers) > 0:
        print(f"⚠ Detected {len(active_triggers)} active triggers! Processing claims...")
        
        # Fetch bounded number of workers in that zone to simulate payout
        res = db.client.table('workers').select('*').eq('city', city).eq('zone', zone).limit(limit).execute()
        impacted_workers = res.data or []
        
        for w in impacted_workers:
            # For each worker and each trigger, process a claim
            for act_trigger in active_triggers:
                claim = processor.process_claim(act_trigger, w)
                claims_generated.append(claim)
    
    return {
        "status": "success",
        "triggers_checked": len(status),
        "active_triggers": len(active_triggers),
        "claims_generated": len(claims_generated),
        "claims": [c['claim_id'] for c in claims_generated]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
