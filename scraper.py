import requests
from supabase import create_client, Client

SUPABASE_URL = "https://ridnmxfctzfntbfpzjnd.supabase.co"
SUPABASE_KEY = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DHANIWIN_API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

def fetch_and_sync():
    print("🚀 Cloud Bulk-Scraper Triggered...")
    try:
        # 1. API se latest data uthana (GET Request)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(DHANIWIN_API_URL, headers=headers)
        live_data = response.json()
        
        # API response se list extract karna (assume kar rahe hain 'data' key mein hai)
        latest_rounds = live_data.get("data", [])
        
        # 2. Supabase se aakhiri saved round check karna
        db_res = supabase.table("rounds").select("period").order("period", desc=True).limit(1).execute()
        last_saved_period = db_res.data[0]["period"] if db_res.data else "0"
        
        # 3. Naye rounds filter karna
        new_rounds_to_insert = []
        for round_info in latest_rounds:
            # API structure ke hisaab se key 'issueNumber' ya 'period' ho sakti hai
            current_period = str(round_info.get("issueNumber", round_info.get("period", "")))
            
            if current_period and current_period > str(last_saved_period):
                new_rounds_to_insert.append({
                    "period": current_period,
                    # Result ke liye API mein 'color', 'outcome' ya 'size' ho sakta hai
                    "outcome": str(round_info.get("color", round_info.get("size", "")))
                })
        
        # 4. Data Supabase mein push karna
        if new_rounds_to_insert:
            supabase.table("rounds").insert(new_rounds_to_insert).execute()
            print(f"✅ {len(new_rounds_to_insert)} naye rounds successfully add ho gaye!")
        else:
            print("⚡ Koi naya round nahi aaya.")
            
    except Exception as e:
        print(f"❌ Error aayi: {e}")

if __name__ == "__main__":
    fetch_and_sync()
