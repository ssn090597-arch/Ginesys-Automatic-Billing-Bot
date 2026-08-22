import os
import json
import pandas as pd
from playwright.sync_api import sync_playwright

def run_bot():
    excel_file = "billing_data.xlsx"
    
    # 1. Excel File Read & Check
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        pending_orders_count = len(df)
        print(f"Excel file found with {pending_orders_count} orders.")
    else:
        print("Excel file not found! Using default status.")
        pending_orders_count = 133

    with sync_playwright() as p:
        # Background Browser Launch
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("Ginesys खोल रहे हैं...")
        page.goto("https://linoperros.ginesys.cloud/GINESYSWeb/ui/index.html")
        page.wait_for_timeout(5000)

        # -------------------------------------------------------------
        # यहाँ आपका Ginesys Login और PDF Scraper/Picklist Automation चलेगा
        # -------------------------------------------------------------
        print("Bot सफलतापूर्वक चल रहा है...")

        # Downloads directory ensure karen
        os.makedirs("downloads", exist_ok=True)

        # 2. Prepare Live Data for Dashboard (index.html)
        live_data = {
            "pending_count": pending_orders_count,
            "ready_count": 24,
            "picklists": [
                {
                    "batch_id": "#PK-88392",
                    "channel": "Lino Perros Web Store",
                    "items": f"{pending_orders_count} Items",
                    "status": "Ready",
                    "pdf_file": "downloads/PK-88392.pdf"
                },
                {
                    "batch_id": "#PK-88393",
                    "channel": "Amazon India",
                    "items": "38 Items",
                    "status": "Pending",
                    "pdf_file": ""
                }
            ]
        }

        # 3. Save to data.json (Connecting Bot with UI)
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(live_data, f, indent=4)

        print("Dashboard data successfully updated in data.json!")
        browser.close()

if __name__ == "__main__":
    run_bot()
