import os
from app.platform.provider import PlatformProvider
from app.platform.direct_provider import DirectPlatformProvider

def get_platform_provider() -> PlatformProvider:
    provider_name = os.getenv("PLATFORM_PROVIDER", "direct").lower()
    
    if provider_name == "direct":
        return DirectPlatformProvider()
    else:
        # In a real system, you might have TartanProvider, ArgyleProvider, etc.
        raise ValueError(f"Unknown PLATFORM_PROVIDER: {provider_name}")
