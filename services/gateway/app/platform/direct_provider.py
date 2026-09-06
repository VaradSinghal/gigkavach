import uuid
from datetime import datetime
from typing import Dict, Any

from app.platform.provider import PlatformProvider, PlatformLinkSession, VerificationResult
from app.platform.adapters.zomato_adapter import ZomatoAdapter
from app.platform.adapters.swiggy_adapter import SwiggyAdapter
from app.platform.adapters.blinkit_adapter import BlinkitAdapter

class DirectPlatformProvider(PlatformProvider):
    # Store temporary session state (using in-memory dict for demo)
    _sessions: Dict[str, PlatformLinkSession] = {}

    def _get_adapter(self, platform_name: str):
        name = platform_name.lower()
        if name == "zomato":
            return ZomatoAdapter()
        elif name == "swiggy":
            return SwiggyAdapter()
        elif name == "blinkit":
            return BlinkitAdapter()
        else:
            raise ValueError(f"Unsupported platform: {platform_name}")

    async def initiate_link(self, user_id: str, platform_name: str) -> PlatformLinkSession:
        # Validate that the platform is supported
        self._get_adapter(platform_name)
        
        session = PlatformLinkSession(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            platform_name=platform_name.lower(),
            status="PENDING",
            created_at=datetime.utcnow()
        )
        self._sessions[session.session_id] = session
        return session

    async def verify_login(self, session_id: str, phone: str, otp: str) -> bool:
        if session_id not in self._sessions:
            return False
            
        # In a real direct integration, we would forward the OTP to the provider's API.
        # Here we mock the success condition for the demo.
        if otp == "123456":
            self._sessions[session_id].status = "VERIFIED"
            return True
            
        return False

    async def fetch_work_history(self, session_id: str) -> VerificationResult:
        if session_id not in self._sessions:
            raise ValueError("Invalid session")
            
        session = self._sessions[session_id]
        if session.status != "VERIFIED":
            raise ValueError("Session not verified")
            
        adapter = self._get_adapter(session.platform_name)
        return await adapter.get_work_history()
