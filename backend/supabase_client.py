import os
import sys

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    pass

try:
    from supabase import create_client, Client
except ImportError:
    print("Warning: supabase package not installed. Run `pip install supabase`")
    Client = None
    create_client = None


class SupabaseConnection:
    """Singleton connection to Supabase backend."""
    _instance = None
    client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")

        if not url or not key or url == "YOUR_SUPABASE_PROJECT_URL":
            print("⚠ SUPABASE_URL or SUPABASE_KEY not configured in backend/.env")
            print("  Running in LOCAL MOCK mode (No remote sync).")
            self.client = None
            return

        if create_client:
            try:
                self.client = create_client(url, key)
                print("✓ Connected to Supabase backend.")
            except Exception as e:
                print(f"⚠ Failed to connect to Supabase: {e}")
                self.client = None


# Global singleton client
db = SupabaseConnection()
