from curl_cffi import requests
from supabase import create_client, Client

SUPABASE_URL = "https://ridnmxfctzfntbfpzjnd.supabase.co"
SUPABASE_KEY = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DHANIWIN_API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

def fetch_and_sync():
    print("🚀 Real Browser Impersonation Started...")
    try:
        # Asli jadoo yahan hai: impersonate="chrome110" Cloudflare ko bypass kar dega
        response = requests.get(DHANIWIN_API_URL, impersonate="chrome110", timeout=15)
        
        if response.status_code != 200:
            print(f"❌ API Blocked! Status Code: {response.status_code}")
            return
            
        live_data = response.json()
        
        latest_rounds = []
        if isinstance(live_data, list):
            latest_rounds = live_data
        elif isinstance(live_data, dict):
            data_field = live_data.get("data", {})
            if isinstance(data_field, list):
                latest_rounds = data_field
            elif isinstance(data_field, dict):
                latest_rounds = data_field.get("list", data_field.get("records", []))

        print(f"🔢 API Se Rounds Mile: {len(latest_rounds)}")
        if not latest_rounds:
            print("⚠️ Data empty mila. Raw data:", live_data)
            return

        db_res = supabase.table("rounds").select("period").order("period", desc=True).limit(1).execute()
        last_saved_period = str(db_res.data[0]["period"]) if db_res.data and len(db_res.data) > 0 else "0"
        print(f"🕒 Last Saved Period in DB: {last_saved_period}")

        new_rounds = []
        for item in latest_rounds:
            period = str(item.get("issueNumber", item.get("period", "")))
            outcome_val = str(item.get("size", item.get("outcome", item.get("color", "")))).upper()
            
            outcome = "BIG"
            if outcome_val in ["BIG", "SMALL"]:
                outcome = outcome_val
            elif outcome_val in ["GREEN", "RED", "VIOLET"]:
                outcome = "BIG" if outcome_val in ["GREEN", "VIOLET"] else "SMALL"
                
            if period and period > last_saved_period:
                new_rounds.append({"period": period, "outcome": outcome})

        if new_rounds:
            new_rounds.sort(key=lambda x: x["period"])
            supabase.table("rounds").insert(new_rounds).execute()
            print(f"✅ BINGO! {len(new_rounds)} naye rounds Supabase mein save ho gaye!")
        else:
            print("⚡ Koi naya round nahi aaya.")

    except Exception as e:
        print(f"❌ Error in scraper: {e}")

if __name__ == "__main__":
    fetch_and_sync()
