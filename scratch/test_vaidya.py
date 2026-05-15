import os
import sys
from playwright.sync_api import sync_playwright

def test_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"BROWSER ERROR: {exc}"))

        url = 'http://localhost:8000'
        print(f"Navigating to {url}...")
        try:
            page.goto(url, timeout=30000)
            page.wait_for_load_state('networkidle')
            print("Page loaded successfully.")
        except Exception as e:
            print(f"Failed to load page: {e}")
            browser.close()
            return

        # 1. Test Search functionality (on default tab)
        print("Testing Search functionality...")
        search_input = page.locator('#search-input')
        search_btn = page.locator('#search-btn')
        
        search_input.fill('winter joint pain')
        search_btn.click()
        print("Search submitted. Waiting for results...")
        
        try:
            # Wait for response container to become active
            page.wait_for_selector('#response-container.active', timeout=10000)
            print("Search results received.")
            answer = page.locator('#answer-text').inner_text()
            print(f"Answer snippet: {answer[:100]}")
        except Exception as e:
            print(f"Search failed or timed out: {e}")
            page.screenshot(path='search_fail.png')

        # 2. Verify Tab Switching
        print("Testing Tab Switching to Roadmap...")
        roadmap_tab = page.locator('#tab-roadmap')
        roadmap_tab.click()
        page.wait_for_timeout(1000)
        
        is_roadmap_visible = page.locator('#roadmap-section').is_visible()
        if is_roadmap_visible:
            print("Successfully switched to Roadmap Generator.")
        else:
            print("FAILED to switch to Roadmap Generator.")
            browser.close()
            return

        # 3. Test Roadmap Generation
        print("Testing Roadmap Generation...")
        disease_input = page.locator('#diseaseInput')
        generate_btn = page.locator('#generate-roadmap-btn')
        
        disease_input.fill('Joint Pain')
        generate_btn.click()
        print("Roadmap request submitted. Waiting for results...")
        
        try:
            # Wait for roadmap result to show (it sets active class on response-container)
            page.wait_for_selector('#response-container.active', timeout=10000)
            is_visible = page.evaluate("document.getElementById('roadmap-result').style.display !== 'none'")
            if is_visible:
                print("Roadmap generated and visible successfully.")
                # Check for mindmap nodes
                nodes_count = page.locator('.mm-node').count()
                print(f"Found {nodes_count} nodes in the roadmap.")
            else:
                print("Roadmap result container is still hidden.")
        except Exception as e:
            print(f"Roadmap generation failed or timed out: {e}")
            page.screenshot(path='roadmap_fail.png')

        browser.close()
        print("Testing completed.")

if __name__ == "__main__":
    test_app()
