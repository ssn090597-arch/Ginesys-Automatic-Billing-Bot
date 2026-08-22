import os
import pandas as pd
from playwright.sync_api import sync_playwright

def run_bot():
    # Excel फाइल रीड करें
    excel_file = "billing_data.xlsx"
    if not os.path.exists(excel_file):
        print("Excel file not found!")
        return

    df = pd.read_excel(excel_file)

    with sync_playwright() as p:
        # Background में ब्राउज़र चालू करें
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Ginesys वेबसाइट पर जाएँ
        print("Ginesys खोल रहे हैं...")
        page.goto("https://linoperros.ginesys.cloud/GINESYSWeb/ui/index.html")
        page.wait_for_timeout(5000)

        # यहाँ Ginesys Login और Automation का कोड चलेगा
        print("Bot सफलतापूर्वक चल रहा है...")

        browser.close()

if __name__ == "__main__":
    run_bot()
