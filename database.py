# database.py
from supabase import create_client, Client

SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-public-key"

# Client initialize karein
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)