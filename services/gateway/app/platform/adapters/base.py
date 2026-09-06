from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
from app.platform.provider import WorkHistory, VerificationResult

class PlatformAdapter(ABC):
    @abstractmethod
    async def get_work_history(self) -> VerificationResult:
        """Fetch and return formatted work history from the specific platform."""
        pass
