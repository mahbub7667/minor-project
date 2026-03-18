import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load all environment variables from the .env file
load_dotenv()

# Fetch the credentials using the keys defined in the .env file
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Create the Supabase client instance
# This 'supabase' object will be used in app.py for database operations
if not supabase_url or not supabase_key:
    print("Error: Missing Supabase credentials in environment variables.")
else:
    supabase: Client = create_client(supabase_url, supabase_key)
    print("Connection to Supabase database initialized.")