import sys
from playwright.sync_api import sync_playwright

def download_ginesys_report():
    with sync_playwright() as p:
        # Chromium Browser Start
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("Navigating to Ginesys Reports Portal...")
        page.goto("https://erpreports.ginesys.cloud/Home/index.aspx")

        # Search for report
        page.wait_for_selector("input[placeholder*='Search Report Names']")
        search_input = page.locator("input[placeholder*='Search Report Names']")
        search_input.fill("deli")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

        # Right click on Delivery Challan Pending Report
        report_item = page.locator("text=Delivery challan pending bo...").first
        report_item.click(button="right")
        page.wait_for_timeout(1000)

        # Hover on Export As and Click Excel
        page.locator("text=Export As").hover()
        page.wait_for_timeout(500)

        with page.expect_download() as download_info:
            page.locator("text=Excel").click()
        
        download = download_info.value
        download.save_as("billing_data.xlsx")
        print("Fresh Ginesys Report downloaded successfully!")

        browser.close()

if __name__ == "__main__":
    download_ginesys_report()
