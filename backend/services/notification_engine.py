"""
GigKavach — Notification Engine
Handles outbound alerts to workers for risk scenarios and claim statuses.
"""
from datetime import datetime

class NotificationEngine:
    """Manages real-time alerts for the platform."""
    
    def __init__(self):
        self.active_notifications = []

    def emit_risk_alert(self, worker_id: str, zone: str, hazard_type: str, severity: str):
        """Sends a notification directly related to geometric risk."""
        payload = {
            "type": "geo_risk",
            "worker_id": worker_id,
            "title": f"⚠️ {severity.upper()} Warning in {zone}",
            "message": f"Our Parametric Engine detects {hazard_type} anomalies. Shift to safe zones immediately.",
            "timestamp": datetime.now().isoformat()
        }
        self._broadcast(payload)
    
    def emit_claim_status(self, worker_id: str, claim_id: str, status: str, amount: float):
        """Notifies worker about autonomous claim actions."""
        payload = {
            "type": "claim_update",
            "worker_id": worker_id,
            "title": "💸 Zero-Touch Claim Processed",
            "message": f"Claim {claim_id} processed as {status}. ₹{amount} has been dispatched to your digital wallet via Parametric Auth.",
            "timestamp": datetime.now().isoformat()
        }
        self._broadcast(payload)

    def _broadcast(self, payload: dict):
        """
        In production, this interfaces directly with Supabase Realtime Broadcast or Firebase Cloud Messaging.
        For localized OS, it buffers to an in-memory queue that clients can poll.
        """
        import uuid
        payload['id'] = str(uuid.uuid4())
        self.active_notifications.append(payload)
        # Keep the latest 50 notifications in memory
        if len(self.active_notifications) > 50:
            self.active_notifications.pop(0)

        print(f"\n[BROADCAST NOTIFICATION] To {payload['worker_id']}: {payload['title']} - {payload['message']}\n")

    def get_latest(self):
        return self.active_notifications
        
    def clear(self):
        self.active_notifications = []

# Global singleton
notifier = NotificationEngine()
