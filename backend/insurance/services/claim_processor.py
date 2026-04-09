"""
GigKavach — Zero-Touch Claim Processor
Automatically validates, scores, and processes claims triggered by the parametric engine.
"""

import os
import sys
from datetime import datetime
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from ai.model_loader import loader
from fraud.services.validator import FraudValidator


class ClaimProcessor:
    """Processes claims through the zero-touch pipeline."""

    STATUSES = ['detected', 'validating', 'approved', 'soft_review', 'rejected', 'processing', 'paid', 'closed']

    def __init__(self):
        try:
            loader.load_all()
        except Exception:
            pass
        self.validator = FraudValidator()

    def process_claim(self, trigger_event: dict, worker: dict) -> dict:
        """
        Process a claim from trigger detection to payout.
        """
        claim_id = f"CLM-{random.randint(100000, 999999)}"
        timestamp = datetime.now()

        # Step 1: Create claim event
        claim = {
            'claim_id': claim_id,
            'worker_id': worker.get('worker_id', 'GK-00000'),
            'trigger_type': trigger_event.get('trigger', 'unknown'),
            'trigger_label': trigger_event.get('label', 'Unknown'),
            'trigger_data': str(trigger_event.get('value', '')),
            'zone': worker.get('zone', 'Unknown'),
            'city': worker.get('city', 'Unknown'),
            'created_at': timestamp.isoformat(),
            'status': 'detected',
        }

        # Step 2: Fraud validation (Advanced Phase 2)
        # Prepare data for validator
        validation_input = {
            'city': claim['city'],
            'zone': claim['zone'],
            'timestamp': claim['created_at'],
            'trigger_type': claim['trigger_type'],
            'rainfall_mm': trigger_event.get('data', {}).get('rainfall_6hr_mm', 0),
            'aqi': trigger_event.get('data', {}).get('aqi', 100),
            'temperature_c': trigger_event.get('data', {}).get('temperature_c', 30),
            'latitude': worker.get('latitude', 13.0),
            'longitude': worker.get('longitude', 80.2),
            # In a real app, these would come from recent GPS history
            'last_lat': worker.get('latitude', 13.0) + random.uniform(-0.001, 0.001),
            'last_lon': worker.get('longitude', 80.2) + random.uniform(-0.001, 0.001),
            'time_diff_seconds': 300, 
            'payout_amount': 400,
        }
        
        val_result = self.validator.validate_claim(validation_input)
        
        claim['confidence_score'] = val_result['confidence_score']
        claim['fraud_probability'] = val_result['fraud_probability']
        claim['validation_signals'] = val_result['signals']
        claim['status'] = 'validating'

        # Step 3: Calculate payout
        payout = self._calculate_payout(trigger_event, worker)
        claim['inactive_hours'] = payout['inactive_hours']
        claim['hourly_rate'] = payout['hourly_rate']
        claim['coverage_pct'] = payout['coverage_pct']
        claim['payout_amount'] = payout['amount']

        # Step 4: Determine action
        if val_result['action'] == 'auto_approve':
            claim['status'] = 'approved'
            claim['action'] = 'auto_approved'
            claim['review_required'] = False
        elif val_result['action'] == 'soft_review':
            claim['status'] = 'soft_review'
            claim['action'] = 'soft_review'
            claim['review_required'] = True
            claim['review_reason'] = 'Confidence between 50-79. Flagged for manual audit.'
        else:
            claim['status'] = 'rejected'
            claim['action'] = 'rejected'
            claim['review_required'] = False
            claim['rejection_reason'] = val_result.get('reason', 'Low confidence score.')

        # Step 5: Instant Payout Simulation
        if claim['status'] == 'approved':
            self._simulate_instant_payout(worker, claim['payout_amount'])
            claim['status'] = 'paid'

        # Step 6: Create timeline
        claim['timeline'] = self._generate_timeline(claim, timestamp)

        # [SUPABASE] Sync
        try:
            from supabase_client import db
            if db.client:
                db_claim = {
                    'claim_id': claim['claim_id'],
                    'worker_id': claim['worker_id'],
                    'zone': claim['zone'],
                    'city': claim['city'],
                    'trigger_type': claim['trigger_type'],
                    'trigger_label': claim['trigger_label'],
                    'trigger_data': claim['trigger_data'],
                    'status': claim['status'],
                    'action': claim['action'],
                    'confidence_score': claim['confidence_score'],
                    'fraud_probability': claim['fraud_probability'],
                    'validation_signals': claim['validation_signals'],
                    'inactive_hours': claim['inactive_hours'],
                    'hourly_rate': claim['hourly_rate'],
                    'coverage_pct': claim['coverage_pct'],
                    'payout_amount': claim['payout_amount'],
                    'timeline': claim['timeline'],
                }
                db.client.table('claims').insert(db_claim).execute()
        except Exception as e:
            print(f"[Supabase Sync Error] {e}")

        return claim

    def _simulate_instant_payout(self, worker: dict, amount: float):
        """Simulates MOCK integration with Stripe/Razorpay and updates wallet balance."""
        print(f"--- [MOCK PAYOUT] Processing RS.{amount} for {worker['worker_id']} via Razorpay...")
        
        try:
            from supabase_client import db
            if db.client:
                # Update total_payout in real Supabase
                # Note: wallet_balance will be added to schema
                current_payout = worker.get('total_payout', 0) or 0
                db.client.table('workers').update({
                    'total_payout': float(current_payout) + float(amount)
                }).eq('worker_id', worker['worker_id']).execute()
                print(f"[OK] [SUCCESS] Wallet balance updated for {worker['worker_id']}.")
        except Exception as e:
            print(f"[ERROR] [PAYOUT ERROR] {e}")

    def _calculate_payout(self, trigger_event: dict, worker: dict) -> dict:
        """Calculate payout amount based on disruption duration and worker income."""
        severity = trigger_event.get('severity', 'moderate')

        # Estimate inactive hours based on severity
        hours_map = {'moderate': 4, 'high': 6, 'critical': 8}
        inactive_hours = hours_map.get(severity, 5)

        hourly_rate = worker.get('avg_hourly_income', 70)
        coverage_pct = worker.get('coverage_percentage', 70) / 100

        amount = round(inactive_hours * hourly_rate * coverage_pct, 2)

        return {
            'inactive_hours': inactive_hours,
            'hourly_rate': hourly_rate,
            'coverage_pct': coverage_pct * 100,
            'amount': amount,
            'formula': f'{inactive_hours}hrs * RS.{hourly_rate}/hr * {int(coverage_pct * 100)}%',
        }

    def _generate_timeline(self, claim: dict, start_time: datetime) -> list:
        """Generate claim processing timeline."""
        timeline = [
            {
                'time': start_time.strftime('%I:%M %p'),
                'event': f'Trigger detected: {claim["trigger_label"]} - {claim["trigger_data"]}',
                'status': 'detected',
            },
            {
                'time': (start_time.replace(second=start_time.second + 30)).strftime('%I:%M %p'),
                'event': 'Auto-claim created',
                'status': 'created',
            },
            {
                'time': (start_time.replace(minute=start_time.minute + 1)).strftime('%I:%M %p'),
                'event': f'Fraud validation: Score {claim["confidence_score"]}/100',
                'status': 'validated',
            },
        ]

        if claim['status'] == 'approved':
            timeline.extend([
                {
                    'time': (start_time.replace(minute=start_time.minute + 2)).strftime('%I:%M %p'),
                    'event': f'Payout calculated: {claim["inactive_hours"]}hrs * RS.{claim["hourly_rate"]}/hr * {int(claim["coverage_pct"])}%',
                    'status': 'calculated',
                },
                {
                    'time': (start_time.replace(minute=start_time.minute + 5)).strftime('%I:%M %p'),
                    'event': f'RS.{claim["payout_amount"]} processed via UPI',
                    'status': 'paid',
                },
            ])
        elif claim['status'] == 'soft_review':
            timeline.append({
                'time': (start_time.replace(minute=start_time.minute + 2)).strftime('%I:%M %p'),
                'event': 'Claim flagged for manual review - additional verification requested',
                'status': 'review',
            })
        else:
            timeline.append({
                'time': (start_time.replace(minute=start_time.minute + 2)).strftime('%I:%M %p'),
                'event': f'Claim rejected: {claim.get("rejection_reason", "Low confidence score")}',
                'status': 'rejected',
            })

        return timeline

    def _get_rejection_reason(self, confidence: dict) -> str:
        """Generate human-readable rejection reason."""
        failed = [k for k, v in confidence.get('signals', {}).items() if not v.get('passed')]
        if failed:
            return f'Failed validation: {", ".join(failed)}. Please file an appeal if you believe this is incorrect.'
        return 'Low overall confidence score. Please file an appeal with additional evidence.'
