import requests
from supabase import create_client, Client

SUPABASE_URL = "https://ridnmxfctzfntbfpzjnd.supabase.co"
SUPABASE_KEY = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DHANIWIN_API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

def fetch_and_sync():
    print("🚀 Debug Cloud Scraper Triggered...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(DHANIWIN_API_URL, headers=headers)
        live_data = response.json()
        
        print(f"📦 Raw API Response: {live_data}")
        
        # Data extract karke pehla round print karwayenge
        data_field = live_data.get("data", [])
        if isinstance(data_field, dict):
            latest_rounds = data_field.get("list", data_field.get("records", []))
        else:
            latest_rounds = data_field
            
        print(f"🔢 Total Rounds Extracted: {len(latest_rounds)}")
        if len(latest_rounds) > 0:
            print(f"📝 First Item Keys & Values: {latest_rounds[0]}")
            
    except Exception as e:
        print(f"❌ Error caught: {e}")

if __name__ == "__main__":
    fetch_and_sync()
