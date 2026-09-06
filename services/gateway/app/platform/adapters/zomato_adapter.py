from datetime import datetime, timedelta
from app.platform.adapters.base import PlatformAdapter
from app.platform.provider import WorkHistory, VerificationResult

class ZomatoAdapter(PlatformAdapter):
    async def get_work_history(self) -> VerificationResult:
        # Zomato logic: High hours, stable income
        history = []
        today = datetime.utcnow().date()
        avg_hours = 12.5
        avg_inc = 950.0
        
        for i in range(14):
            dt = today - timedelta(days=i)
            history.append(WorkHistory(
                date=dt.isoformat(),
                hours_worked=12.5,
                orders_completed=25,
                gross_earnings=950.0
            ))
            
        return VerificationResult(
            verified=True,
            platform="zomato",
            avg_daily_hours=avg_hours,
            avg_daily_income=avg_inc,
            history=history
        )
