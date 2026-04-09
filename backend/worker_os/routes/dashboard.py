"""
GigKavach — Dashboard Routes
Provides aggregated statistics and predictive analytics for workers and admins.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
from datetime import datetime, timedelta
import random

from supabase_client import db

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats():
    """Returns top-level stats for the Admin Dashboard."""
    if not db.client:
        return {
            "loss_ratio": 0.35,
            "active_policies": 120,
            "total_payouts": 45000,
            "total_premiums": 130000
        }

    try:
        # Fetch policies and claims to calculate loss ratio
        claims_res = db.client.table('claims').select('payout_amount').execute()
        policies_res = db.client.table('policies').select('weekly_premium').execute()

        total_payouts = sum([float(c['payout_amount'] or 0) for c in claims_res.data or []])
        total_premiums = sum([float(p['weekly_premium'] or 0) for p in policies_res.data or []])
        
        loss_ratio = (total_payouts / total_premiums) if total_premiums > 0 else 0

        return {
            "active_policies": len(policies_res.data or []),
            "premium_pool": total_premiums,
            "total_payouts": total_payouts,
            "loss_ratio": round(loss_ratio, 2),
            "status": "healthy" if loss_ratio < 0.6 else "high_risk"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predictions")
def get_predictive_analytics():
    """
    Simulates ML-based prediction for next week's likely claims.
    In a real app, this would use a time-series model.
    """
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # Generate a 'predicted' claim curve based on historical averages + mock weather forecast
    base_claims = [12, 15, 45, 20, 18, 25, 22] # Historical
    predicted_claims = []
    
    for i, base in enumerate(base_claims):
        # Add some 'AI' variance
        pred = base + random.randint(-5, 15)
        predicted_claims.append({
            "day": days[i],
            "historical": base,
            "predicted": pred,
            "risk_level": "high" if pred > 35 else "normal"
        })

    return {
        "forecast_week": "Current + 1",
        "total_predicted_claims": sum([p['predicted'] for p in predicted_claims]),
        "data": predicted_claims,
        "confidence": 0.88
    }

@router.get("/worker/{worker_id}")
def get_worker_dashboard(worker_id: str):
    """Specific stats for a worker's app dashboard."""
    if not db.client:
        return {"protected_earnings": 1200, "active_coverage": True}

    try:
        res = db.client.table('workers').select('*').eq('worker_id', worker_id).single().execute()
        worker = res.data
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")

        # Mock calculation for 'protected earnings'
        protected = worker.get('total_payout', 0)
        
        return {
            "worker_id": worker_id,
            "protected_earnings": protected,
            "active_coverage": True,
            "trust_score": worker.get('trust_score', 0.9),
            "next_payout_est": 0 if random.random() > 0.3 else random.randint(200, 800)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
