import os
from dotenv import load_dotenv
from supabase import create_client, Client

# load the .env variables
load_dotenv()

# take the keys form the environment
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# initialize c;ient
if not url or not key:
    print("Galti: .env file mein keys nahi mili!")
else:
    supabase: Client = create_client(url, key)
    print("Supabase connection set ho gaya!")