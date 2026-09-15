import requests
from supabase import create_client, Client

SUPABASE_URL = "https://ridnmxfctzfntbfpzjnd.supabase.co"
SUPABASE_KEY = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DHANIWIN_API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

def fetch_and_sync():
    print("🚀 Universal Cloud Scraper Triggered...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(DHANIWIN_API_URL, headers=headers)
        live_data = response.json()
        
        # API response se list extract karne ka universal tareeqa
        latest_rounds = []
        if isinstance(live_data, list):
            latest_rounds = live_data
        elif isinstance(live_data, dict):
            data_field = live_data.get("data", live_data.get("list", live_data.get("records", [])))
            if isinstance(data_field, list):
                latest_rounds = data_field
            elif isinstance(data_field, dict):
                latest_rounds = data_field.get("list", data_field.get("records", []))

        print(f"🔢 Total Rounds Extracted: {len(latest_rounds)}")
        if not latest_rounds:
            print("⚠️ API data format nahi mila. Raw data:", live_data)
            return

        # Supabase se aakhiri saved period nikalna
        db_res = supabase.table("rounds").select("period").order("period", desc=True).limit(1).execute()
        last_saved_period = str(db_res.data[0]["period"]) if db_res.data and len(db_res.data) > 0 else "0"
        print(f"🕒 Last Saved Period in DB: {last_saved_period}")

        new_rounds_to_insert = []
        for item in latest_rounds:
            if not isinstance(item, dict):
                continue
            
            # Period key auto-detect karna
            period = None
            for k in ["period", "issueNumber", "issue", "round", "gameNo", "number", "idx"]:
                if k in item and item[k]:
                    period = str(item[k])
                    break
            
            # Outcome key auto-detect karna
            outcome = "BIG"
            for k in ["outcome", "size", "color", "result", "win"]:
                if k in item and item[k]:
                    val = str(item[k]).upper()
                    if val in ["BIG", "SMALL"]:
                        outcome = val
                        break
                    elif val in ["GREEN", "RED", "VIOLET"]:
                        outcome = "BIG" if val in ["GREEN", "VIOLET"] else "SMALL"
                        break
            
            if period and period > last_saved_period:
                new_rounds_to_iter = {"period": period, "outcome": outcome}
                if new_rounds_to_iter not in new_rounds_to_insert:
                    new_rounds_to_insert.append(new_rounds_to_iter)

        if new_rounds_to_insert:
            # Purane se naye kram mein sort karna
            new_rounds_to_insert.sort(key=lambda x: x["period"])
            supabase.table("rounds").insert(new_rounds_to_insert).execute()
            print(f"✅ {len(new_rounds_to_insert)} naye rounds successfully database mein add ho gaye!")
        else:
            print("⚡ Koi naya round nahi aaya, database pehle se updated hai.")

    except Exception as e:
        print(f"❌ Error in scraper: {e}")

if __name__ == "__main__":
    fetch_and_sync()
