import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

# Load credentials and URLs
load_dotenv()
COOKIE = os.getenv('SESSION_COOKIE')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
BASE_URL = "https://agent.callpay.com"

def notify_slack(message):
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={'text': message})
        response.raise_for_status()
    except Exception as e:
        print(f"[Slack Error] {str(e)}")

def switch_back_to_root(session):
    try:
        resp = session.get(BASE_URL + "/payouts")
        soup = BeautifulSoup(resp.text, 'html.parser')
        if soup.select_one("li.settings a[href='/user/switchback']"):
            session.get(BASE_URL + "/user/switchback")
            notify_slack("🔄 Switched back to root user automatically.")
    except Exception as e:
        notify_slack(f"⚠️ Error switching back to root: {str(e)}")

def has_real_payout_rows(soup):
    table = soup.select_one("#w1 table")
    if not table:
        print("[Debug] Table not found.")
        return False

    rows = table.select("tbody tr")
    for idx, row in enumerate(rows):
        cols = row.find_all("td")

        if not cols:
            print(f"[Debug] Row {idx} has no <td> columns.")
            continue

        if row.select_one("td div.empty"):
            print(f"[Debug] Row {idx} is a 'no results' placeholder.")
            continue

        # Show raw column text for debugging
        print(f"[Debug] Row {idx} column count: {len(cols)}")
        for i, col in enumerate(cols):
            print(f"  Col {i}: '{col.get_text(strip=True)}'")

        # If you want to preserve the current logic:
        if len(cols) >= 6:
            bank = cols[1].get_text(strip=True)
            account = cols[3].get_text(strip=True)
            amount = cols[4].get_text(strip=True)

            if bank and account and amount:
                print(f"[Debug] Detected valid row at {idx}.")
                return True

    print("[Debug] No valid payout rows found.")
    return False



def check_processing_payouts():
    today = datetime.today().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')

    payouts_url = (
        f"{BASE_URL}/payouts?"
        f"PayoutQuery%5Bfrom_date%5D={today}+00%3A00&"
        f"PayoutQuery%5Bto_date%5D={today}+23%3A59&"
        f"PayoutQuery%5Bpayout_status%5D=1"
    )

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0',
        'Cookie': COOKIE
    })

    switch_back_to_root(session)

    try:
        response = session.get(payouts_url)
        response.raise_for_status()
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')

        if has_real_payout_rows(soup):
            notify_slack(f"🚨 *Processing Payouts* detected for `{today}` at `{current_time}`.\n<{payouts_url}|View Payouts>")
        else:
            notify_slack(f"✅ No processing payouts for `{today}` at `{current_time}`.")
            print(f"[{today} {current_time}] No processing payouts.")

    except Exception as e:
        notify_slack(f"❌ Error checking payouts at `{current_time}`: {str(e)}")

if __name__ == "__main__":
    check_processing_payouts()
