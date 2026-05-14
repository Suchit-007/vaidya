import sys
from playwright.sync_api import sync_playwright

def run_automation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Navigating to local Vaidya.ai application server...")
        page.goto('http://localhost:8000')
        page.wait_for_load_state('networkidle')
        
        # Verify initial rendering title bounds
        assert "Vaidya.ai" in page.title()
        
        # Select the 'Joint Pain (Winter)' sample chip
        print("Triggering query input via tactile preset chip...")
        page.locator('.preset-chip').first.click()
        
        # Assert response card display
        page.wait_for_selector('#result-card', state='visible', timeout=10000)
        
        # Extract returned UI payload strings
        answer = page.locator('#answer-text').inner_text()
        citation = page.locator('#citation-text').inner_text()
        print(f"Verified UI Summary:\n{answer[:150]}...\n")
        print(f"Verified Source Pin:\n{citation[:100]}...\n")
        
        assert len(answer) > 20
        assert len(citation) > 10
        print("Web application frontend UI integration automation PASSED successfully!")
        browser.close()

if __name__ == '__main__':
    run_automation()
