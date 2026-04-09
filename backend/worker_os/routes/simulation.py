"""
GigKavach — Simulation Routes
Defines scenarios for end-to-end demonstrations (Honest vs Fraudulent).
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
import random
from datetime import datetime, timedelta

from insurance.services.premium_calculator import PremiumCalculator
from fraud.services.validator import FraudValidator
from insurance.services.claim_processor import ClaimProcessor

router = APIRouter(prefix="/api/v1/simulation", tags=["Simulation"])

premium_calc = PremiumCalculator()
fraud_val = FraudValidator()
processor = ClaimProcessor()

@router.get("/scenarios")
def get_simulation_scenarios():
    """
    Returns 4 distinct worker profiles for the fraud demonstration.
    """
    scenarios = [
        {
            "id": "scenario-1",
            "name": "Arun (Honest Worker)",
            "profile": {
                "worker_id": "GK-HONEST-01",
                "city": "Chennai",
                "zone": "Adyar",
                "avg_daily_income": 850,
                "avg_daily_hours": 10,
                "experience_weeks": 45,
                "trust_score": 0.98,
                "latitude": 13.0067,
                "longitude": 80.2206
            },
            "fraud_type": "none",
            "expected_outcome": "auto_approve"
        },
        {
            "id": "scenario-2",
            "name": "Vikram (Virtual Teleporter)",
            "profile": {
                "worker_id": "GK-FRAUD-GPS",
                "city": "Chennai",
                "zone": "Adyar",
                "avg_daily_income": 700,
                "avg_daily_hours": 8,
                "experience_weeks": 12,
                "trust_score": 0.65,
                "latitude": 13.0067,
                "longitude": 80.2206,
                # Force suspicious GPS history
                "last_lat": 12.8500, 
                "last_lon": 80.1500,
                "time_diff_seconds": 60 # 20km in 1 min = 1200km/h
            },
            "fraud_type": "gps_spoofing",
            "expected_outcome": "reject"
        },
        {
            "id": "scenario-3",
            "name": "Suresh (Weather Faker)",
            "profile": {
                "worker_id": "GK-FRAUD-WEATHER",
                "city": "Chennai",
                "zone": "Mylapore", # In a city with no rain
                "avg_daily_income": 900,
                "avg_daily_hours": 9,
                "experience_weeks": 24,
                "trust_score": 0.82,
                "latitude": 13.0330,
                "longitude": 80.2700
            },
            "fraud_type": "fake_weather",
            "expected_outcome": "reject"
        },
        {
            "id": "scenario-4",
            "name": "Rahul (Bot/Emulator)",
            "profile": {
                "worker_id": "GK-FRAUD-DEVICE",
                "city": "Chennai",
                "zone": "Adyar",
                "avg_daily_income": 650,
                "avg_daily_hours": 12,
                "experience_weeks": 4,
                "trust_score": 0.40,
                "latitude": 13.0067,
                "longitude": 80.2206,
                "device_clean": False
            },
            "fraud_type": "compromised_device",
            "expected_outcome": "soft_review"
        }
    ]
    return scenarios

@router.post("/run/{scenario_id}")
def run_scenario(scenario_id: str):
    """
    Executes a specific scenario: Calc Premium -> Trigger Disruption -> Process Claim.
    """
    scenarios = get_simulation_scenarios()
    scenario = next((s for s in scenarios if s['id'] == scenario_id), None)
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    worker = scenario['profile']
    
    # 1. Premium Calculation (Real-time)
    premium = premium_calc.calculate_premium(worker, zone_risk_score=45, weather_forecast_risk=0.2)
    
    # 2. Mock Disruption Trigger
    # If scenario 3, we simulate a 'Rainfall' claim but the engine will check the actual DB.
    trigger = {
        "trigger": "rainfall",
        "label": "Heavy Rainfall",
        "value": 45.5 if scenario_id != "scenario-3" else 0.0,
        "severity": "high",
        "data": {"rainfall_6hr_mm": 45.5 if scenario_id != "scenario-3" else 0.0}
    }

    # 3. Process Claim (thru Fraud AI)
    # Inject specific fraud signals for the scenario
    claim_input_override = {
        "latitude": worker['latitude'],
        "longitude": worker['longitude'],
        "last_lat": worker.get('last_lat', worker['latitude']),
        "last_lon": worker.get('last_lon', worker['longitude']),
        "time_diff_seconds": worker.get('time_diff_seconds', 3600),
        "device_clean": worker.get('device_clean', True),
        "activity_coherent": True if scenario_id != "scenario-4" else False
    }

    # We manually call processor logic or simulate it
    # For the demo, we'll return the full traceability object
    
    # Actually use the processor to sync to Supabase
    processed_claim = processor.process_claim(trigger, {**worker, **claim_input_override})
    
    return {
        "scenario": scenario['name'],
        "premium": premium,
        "trigger": trigger,
        "claim": processed_claim,
        "trust_layer_results": processed_claim.get('validation_signals', {})
    }
