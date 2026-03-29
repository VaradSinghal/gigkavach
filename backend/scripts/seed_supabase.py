"""
GigKavach — Supabase Seeding Script
Uploads locally generated AI data (workers, zone risks, mock claims) to Supabase tables.
"""

import os
import sys
import json
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from supabase_client import db

def seed():
    if not db.client:
        print("❌ Cannot seed Supabase: Please configure .env and install supabase-py.")
        return

    print("=" * 60)
    print("  GigKavach — Seeding Supabase Database")
    print("=" * 60)

    # 1. Seed Zone Risks
    print("\n[1/3] Uploading ML Zone Risks...")
    try:
        with open('ai/saved_models/zone_risk_scores.json', 'r') as f:
            zone_risks = json.load(f)
            
        for z in zone_risks:
            db.client.table('zone_risks').upsert({
                'city': z['city'],
                'zone': z['zone'],
                'risk_score': z['risk_score'],
                'risk_label': z['risk_label'],
                'cluster_id': z['cluster']
            }, on_conflict='city,zone').execute()
        print(f"  ✓ Uploaded exactly {len(zone_risks)} zone risk records.")
    except Exception as e:
        print(f"  ⚠ Failed to upload zone risks: {e}")

    # 2. Seed Workers
    print("\n[2/3] Uploading Synthetic Workers Profile Data...")
    try:
        workers_df = pd.read_csv('ai/data/workers.csv')
        # Take a subset for the demo to save API calls
        demo_workers = workers_df.head(50).to_dict('records')
        
        for w in demo_workers:
            db.client.table('workers').upsert({
                'worker_id': w['worker_id'],
                'city': w['city'],
                'zone': w['zone'],
                'primary_platform': w['primary_platform'],
                'secondary_platform': w.get('secondary_platform'),
                'vehicle_type': w['vehicle_type'],
                'avg_daily_hours': w['avg_daily_hours'],
                'experience_weeks': w['experience_weeks'],
                'trust_score': w['trust_score'],
                'avg_daily_income': w['avg_daily_income'],
                'avg_weekly_income': w['avg_weekly_income'],
                'claim_count': w['claim_count'],
                'claim_rate': w['claim_rate'],
                'total_payout': w['total_payout'],
                'is_flood_zone': bool(w['is_flood_zone'])
            }, on_conflict='worker_id').execute()
        print(f"  ✓ Uploaded {len(demo_workers)} worker profiles.")
    except Exception as e:
        print(f"  ⚠ Failed to upload workers: {e}")

    print("\n[3/3] Demo setup complete.")
    print("Run parametric_engine.py periodically to trigger live claims sync.")
    print("=" * 60)

if __name__ == '__main__':
    seed()
