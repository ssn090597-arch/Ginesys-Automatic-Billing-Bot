import sys
from playwright.sync_api import sync_playwright

def download_ginesys_report():
    with sync_playwright() as p:
        # 1. Chromium Browser Start
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("Navigating to Ginesys Reports Portal...")
        page.goto("https://erpreports.ginesys.cloud/Home/index.aspx")

        # 2. Search for the specific report
        page.wait_for_selector("input[placeholder*='Search Report Names']")
        search_input = page.locator("input[placeholder*='Search Report Names']")
        search_input.fill("deli")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

        # 3. Locate 'Delivery challan pending bo...' Report
        report_item = page.locator("text=Delivery challan pending bo...").first
        report_item.click(button="right")  # Right click to open menu
        page.wait_for_timeout(1000)

        # 4. Hover on 'Export As' and Click 'Excel'
        page.locator("text=Export As").hover()
        page.wait_for_timeout(500)

        # Handle file download
        with page.expect_download() as download_info:
            page.locator("text=Excel").click()
        
        download = download_info.value
        # Save fresh file directly as billing_data.xlsx
        download.save_as("billing_data.xlsx")
        print("Fresh Ginesys Report downloaded and updated successfully!")

        browser.close()

if __name__ == "__main__":
    download_ginesys_report()
