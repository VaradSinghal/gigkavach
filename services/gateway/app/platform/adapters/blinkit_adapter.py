from datetime import datetime, timedelta
from app.platform.adapters.base import PlatformAdapter
from app.platform.provider import WorkHistory, VerificationResult

class BlinkitAdapter(PlatformAdapter):
    async def get_work_history(self) -> VerificationResult:
        # Blinkit logic: Very high hours (fatigue risk!), high frequency 10-minute deliveries
        history = []
        today = datetime.utcnow().date()
        avg_hours = 15.0
        avg_inc = 1200.0
        
        for i in range(14):
            dt = today - timedelta(days=i)
            history.append(WorkHistory(
                date=dt.isoformat(),
                hours_worked=15.0,
                orders_completed=35,
                gross_earnings=1200.0
            ))
            
        return VerificationResult(
            verified=True,
            platform="blinkit",
            avg_daily_hours=avg_hours,
            avg_daily_income=avg_inc,
            history=history
        )
