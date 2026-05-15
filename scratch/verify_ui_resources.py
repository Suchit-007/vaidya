import asyncio
from playwright.async_api import async_playwright
import os

async def test_ui_resources():
    async with async_playwright() as p:
        # Use a real browser instance if possible, or headless
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to Vaidya.ai...")
        await page.goto("http://localhost:8000")
        
        # Search for yogavahi
        print("Searching for 'yogavahi'...")
        await page.fill("#search-input", "yogavahi")
        await page.click("#search-btn")
        
        # Wait for result
        print("Waiting for results...")
        await page.wait_for_selector("#result-card", state="visible", timeout=10000)
        
        # Check if button exists
        print("Checking for 'Clinical Sources' button...")
        toggle_btn = await page.query_selector("#toggle-resources-btn")
        if toggle_btn:
            print("SUCCESS: 'Clinical Sources' button found.")
            
            # Click it
            print("Clicking 'Clinical Sources' button...")
            await toggle_btn.click()
            
            # Check if sidebar is active
            await page.wait_for_selector("#resources-sidebar.active", state="visible", timeout=5000)
            print("SUCCESS: Resources sidebar is now active.")
            
            # Check for resource items
            items = await page.query_selector_all(".resource-item")
            if len(items) > 0:
                print(f"SUCCESS: Found {len(items)} resource items.")
                text = await items[0].inner_text()
                print(f"First item text: {text[:50]}...")
            else:
                print("FAILURE: No resource items found in sidebar.")
                
            # Close it
            print("Closing sidebar...")
            await page.click("#close-resources")
            await page.wait_for_selector("#resources-sidebar.active", state="hidden", timeout=5000)
            print("SUCCESS: Sidebar closed.")
        else:
            print("FAILURE: 'Clinical Sources' button NOT found.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_ui_resources())
