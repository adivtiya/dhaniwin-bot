import requests
from supabase import create_client, Client

SUPABASE_URL = "https://ridnmxfctzfntbfpzjnd.supabase.co"
SUPABASE_KEY = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DHANIWIN_API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

def fetch_and_sync():
    print("🚀 Debug Scraper Triggered...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(DHANIWIN_API_URL, headers=headers)
        
        # Yahan print karke dekhenge ki API kya data bhej rahi hai
        print(f"📡 API Status Code: {response.status_code}")
        live_data = response.json()
        print(f"📦 Full API Response: {live_data}")
        
        latest_rounds = live_data.get("data", [])
        print(f"🔢 Total Rounds Fetched: {len(latest_rounds)}")
        
        if len(latest_rounds) > 0:
            print(f"📝 Sample Round Data: {latest_rounds[0]}")
            
    except Exception as e:
        print(f"❌ Error caught: {e}")

if __name__ == "__main__":
    fetch_and_sync()
