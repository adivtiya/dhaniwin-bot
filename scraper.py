import requests
from supabase import create_client, Client

SUPABASE_URL = "https://ridnmxfctzfntbfpzjnd.supabase.co"
SUPABASE_KEY = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DHANIWIN_API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

def fetch_and_sync():
    print("🚀 Cloud Scraper Triggered...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(DHANIWIN_API_URL, headers=headers)
        live_data = response.json()
        
        # 1. Safe extraction: handle both list or nested dictionary formats
        latest_rounds = []
        data_field = live_data.get("data", [])
        
        if isinstance(data_field, list):
            latest_rounds = data_field
        elif isinstance(data_field, dict):
            latest_rounds = data_field.get("list", data_field.get("records", []))
            
        print(f"🔢 Total Rounds Found from API: {len(latest_rounds)}")
        
        # 2. Supabase se aakhiri saved period check karna
        db_res = supabase.table("rounds").select("period").order("period", desc=True).limit(1).execute()
        last_saved_period = db_res.data[0]["period"] if db_res.data and len(db_res.data) > 0 else "0"
        print(f"🕒 Last Saved Period in DB: {last_saved_period}")
        
        # 3. Naye rounds filter karna aur format set karna
        new_rounds_to_insert = []
        for round_info in latest_rounds:
            current_period = str(round_info.get("issueNumber", round_info.get("period", "")))
            
            # Outcome extract karna (size, outcome, ya color se)
            outcome = str(round_info.get("size", round_info.get("outcome", round_info.get("color", "BIG")))).upper()
            
            # Agar outcome color format mein ho toh BIG/SMALL mein map karna
            if outcome not in ["BIG", "SMALL"]:
                outcome = "BIG" if outcome in ["GREEN", "VIOLET"] else "SMALL"
                
            if current_period and current_period > str(last_saved_period):
                new_rounds_to_insert.append({
                    "period": current_period,
                    "outcome": outcome
                })
        
        # 4. Database mein insert karna (Oldest to newest order mein)
        if new_rounds_to_insert:
            new_rounds_to_insert.reverse()
            supabase.table("rounds").insert(new_rounds_to_insert).execute()
            print(f"✅ {len(new_rounds_to_insert)} naye rounds successfully database mein add ho gaye!")
        else:
            print("⚡ Koi naya round nahi aaya, database pehle se updated hai.")
            
    except Exception as e:
        print(f"❌ Error caught during scraping: {e}")

if __name__ == "__main__":
    fetch_and_sync()
