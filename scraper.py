import requests
from supabase import create_client, Client

SUPABASE_URL = "https://ridnmxfctzfntbfpzjnd.supabase.co"
SUPABASE_KEY = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def run_scraper():
    print("🚀 GitHub Action Scraper Triggered...")
    try:
        # Supabase connection check aur data fetch/sync logic
        response = supabase.table("rounds").select("period").order("period", desc=True).limit(1).execute()
        print(f"✅ Supabase Sync Successful! Latest Period in DB: {response.data}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_scraper()