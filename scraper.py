import cloudscraper
from supabase import create_client, Client

SUPABASE_URL = "https://ridnmxfctzfntbfpzjnd.supabase.co"
SUPABASE_KEY = "sb_publishable_AvI5aU3gVjj2r7PxCcfaWA_L7WOiy7m"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DHANIWIN_API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

def fetch_and_sync():
    print("🚀 Stealth Scraper Triggered...")
    try:
        # Anti-Bot Bypass: Cloudflare ko lagega Chrome browser hai
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        # Timeout add kiya hai taaki request atke nahi
        response = scraper.get(DHANIWIN_API_URL, timeout=15)
        live_data = response.json()
        
        # API Response se asaan tareeqe se records nikalna
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
            print("⚠️ Data empty mila. API response: ", live_data)
            return

        # Supabase se last saved period check karna
        db_res = supabase.table("rounds").select("period").order("period", desc=True).limit(1).execute()
        last_saved_period = str(db_res.data[0]["period"]) if db_res.data and len(db_res.data) > 0 else "0"
        print(f"🕒 Last Saved Period in DB: {last_saved_period}")

        new_rounds = []
        for item in latest_rounds:
            period = str(item.get("issueNumber", item.get("period", "")))
            outcome_val = str(item.get("size", item.get("outcome", item.get("color", "")))).upper()
            
            # Standardize karna: BIG ya SMALL mein convert
            outcome = "BIG"
            if outcome_val in ["BIG", "SMALL"]:
                outcome = outcome_val
            elif outcome_val in ["GREEN", "RED", "VIOLET"]:
                outcome = "BIG" if outcome_val in ["GREEN", "VIOLET"] else "SMALL"
                
            # Sirf naye rounds list mein dalo
            if period and period > last_saved_period:
                new_rounds.append({"period": period, "outcome": outcome})

        if new_rounds:
            # Sahi sequence ke liye order karna
            new_rounds.sort(key=lambda x: x["period"])
            supabase.table("rounds").insert(new_rounds).execute()
            print(f"✅ BINGO! {len(new_rounds)} naye rounds Supabase mein save ho gaye!")
        else:
            print("⚡ Koi naya round nahi aaya. Database pehle se update hai.")

    except Exception as e:
        print(f"❌ Error in stealth scraper: {e}")

if __name__ == "__main__":
    fetch_and_sync()
