"""
GigKavach — Worker Administration Route
Handles Registration, Profiles, and Admin listings.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import random

from supabase_client import db

router = APIRouter(prefix="/api/v1/workers", tags=["Workers"])

class WorkerRegistration(BaseModel):
    name: str
    city: str
    zone: str
    primary_platform: str = "Swiggy"
    vehicle_type: str = "Bike"
    avg_daily_hours: float = 8.0
    experience_weeks: int = 12

@router.post("")
def register_worker(worker: WorkerRegistration):
    if not db.client:
        raise HTTPException(status_code=500, detail="Database not configured")

    worker_id = f"GK-{random.randint(10000, 99999)}"
    
    data = {
        "worker_id": worker_id,
        "city": worker.city,
        "zone": worker.zone,
        "primary_platform": worker.primary_platform,
        "vehicle_type": worker.vehicle_type,
        "avg_daily_hours": worker.avg_daily_hours,
        "avg_daily_income": worker.avg_daily_hours * 100, # mock logic
        "avg_weekly_income": worker.avg_daily_hours * 600,
        "trust_score": 100,
        "claim_count": 0,
        "created_at": datetime.now().isoformat()
    }

    try:
        res = db.client.table('workers').insert(data).execute()
        return {"status": "success", "worker": res.data[0] if res.data else data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
def get_all_workers():
    if not db.client:
        raise HTTPException(status_code=500, detail="Database not configured")
        
    try:
        res = db.client.table('workers').select('*').order('created_at', desc=True).limit(50).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
