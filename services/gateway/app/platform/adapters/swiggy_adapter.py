from datetime import datetime, timedelta
from app.platform.adapters.base import PlatformAdapter
from app.platform.provider import WorkHistory, VerificationResult

class SwiggyAdapter(PlatformAdapter):
    async def get_work_history(self) -> VerificationResult:
        # Swiggy logic: Normal hours, lower income
        history = []
        today = datetime.utcnow().date()
        avg_hours = 8.0
        avg_inc = 600.0
        
        for i in range(14):
            dt = today - timedelta(days=i)
            history.append(WorkHistory(
                date=dt.isoformat(),
                hours_worked=8.0,
                orders_completed=15,
                gross_earnings=600.0
            ))
            
        return VerificationResult(
            verified=True,
            platform="swiggy",
            avg_daily_hours=avg_hours,
            avg_daily_income=avg_inc,
            history=history
        )
