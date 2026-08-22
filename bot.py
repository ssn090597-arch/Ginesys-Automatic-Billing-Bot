import os
import sys
import time
from playwright.sync_api import sync_playwright

# Ginesys Login Credentials & URL
GINESYS_URL = "https://linoperros.ginesys.cloud/GINESYSWeb/ui/index.html"
USERNAME = os.environ.get("GINESYS_USER", "YOUR_USERNAME")
PASSWORD = os.environ.get("GINESYS_PASS", "YOUR_PASSWORD")

def run_ginesys_bot(action_step):
    print(f"--- Starting Ginesys Automation for: {action_step} ---")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Headless = False करने पर ब्राउज़र स्क्रीन पर दिखेगा
        context = browser.new_context()
        page = context.new_page()

        # Step 0: Login to Ginesys
        print("Navigating to Ginesys...")
        page.goto(GINESYS_URL)
        page.wait_for_load_state("networkidle")

        # Fill credentials if login page is presented
        if page.locator("input[name='username']").is_visible():
            page.fill("input[name='username']", USERNAME)
            page.fill("input[type='password']", PASSWORD)
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")

        print("Login completed successfully!")

        # -------------------------------------------------------------
        # STEP 1: DOWNLOAD SALE ORDER REPORT
        # -------------------------------------------------------------
        if action_step == "step1":
            print("Executing Step 1: Downloading Sale Order Report...")
            # 1. GO TO REPORT
            page.click("text=REPORT")
            # 2. SELECT SALE ORDER WISE REPORT
            page.click("text=Sale Order Wise Report")
            # 3. SELECT EXPORT IN EXCEL & SELECT DATE (LAST 15-20 DAYS)
            page.click("text=Export")
            
            with page.expect_download() as download_info:
                page.click("text=Excel")
            
            download = download_info.value
            download_path = os.path.join(os.getcwd(), "billing_data.xlsx")
            download.save_as(download_path)
            print(f"Step 1 Complete! Saved report to: {download_path}")

        # -------------------------------------------------------------
        # STEP 2: PICKLIST GENERATE & REPORT DOWNLOAD
        # -------------------------------------------------------------
        elif action_step == "step2":
            print("Executing Step 2: Generating Pick List...")
            # 1. GO TO INVENTORY
            page.click("text=INVENTORY")
            # 2. GO TO WMS AND SELECT NEW PICK LIST
            page.click("text=WMS")
            page.click("text=New Pick List")
            
            # Select Order & Fill Remark
            page.click("input[type='checkbox']") # Select first available order
            page.fill("textarea[name='remark']", "AUTO_PICKLIST_BOT")
            page.click("button:has-text('Generate')")
            time.sleep(3)

            # GO TO REPORT -> PICK PACK LIST & DOWNLOAD PDF
            page.click("text=REPORT")
            page.click("text=Pick Pack List")
            
            with page.expect_download() as download_info:
                page.click("text=Download PDF")
            
            download = download_info.value
            os.makedirs("downloads", exist_ok=True)
            pdf_path = os.path.join("downloads", "PK-88392.pdf")
            download.save_as(pdf_path)
            print(f"Step 2 Complete! Saved Picklist PDF to: {pdf_path}")

        # -------------------------------------------------------------
        # STEP 3: B2B PACKING PROCESS
        # -------------------------------------------------------------
        elif action_step == "step3":
            print("Executing Step 3: B2B Packing Process...")
            # 1. SALES & DISTRIBUTION
            page.click("text=SALES & DISTRIBUTION")
            # 2. DELIVERY - AGAINST RESERVATION
            page.click("text=Delivery - Against Reservation")
            # 3. CLICK ADD & SEARCH DESTINATION SITE
            page.click("text=Add")
            page.fill("input[placeholder*='Search']", "S")
            print("Step 3 Complete! B2B Packing Initialized.")

        browser.close()

if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "step2"
    run_ginesys_bot(step)
