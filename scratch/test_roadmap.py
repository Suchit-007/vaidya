import sys
import os
import time
from playwright.sync_api import sync_playwright

def test_roadmap():
    with sync_playwright() as p:
        # Launch browser with console capture
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Capture console logs with flushing
        def on_console(msg):
            print(f"BROWSER CONSOLE: {msg.type}: {msg.text}", flush=True)
        page.on("console", on_console)
        page.on("pageerror", lambda exc: print(f"BROWSER ERROR: {exc}", flush=True))

        print("Navigating to http://localhost:3000...", flush=True)
        try:
            page.goto("http://localhost:3000", wait_until="networkidle", timeout=30000)
        except Exception as e:
            print(f"Navigation failed: {e}", flush=True)
            browser.close()
            return

        print("Switching to Roadmap tab...", flush=True)
        page.click("#tab-roadmap")
        
        print("Filling form...", flush=True)
        page.fill("#diseaseInput", "Chronic Inflammation")
        page.select_option("#doshaSelect", "Pitta")
        page.select_option("#severitySelect", "Moderate")
        page.select_option("#ageSelect", "Adult")
        
        print("Clicking Generate Roadmap...", flush=True)
        page.click("#generate-roadmap-btn")
        
        # Wait for API response and rendering
        print("Waiting for results...", flush=True)
        try:
            # Wait for the mindmap nodes to be created
            page.wait_for_selector(".mm-node", timeout=20000)
            print("Success: Mindmap nodes found in DOM!", flush=True)
            
            # Inspect the hub node
            hub = page.locator(".mm-node.hub")
            box = hub.bounding_box()
            content = hub.inner_html()
            opacity = hub.evaluate("el => getComputedStyle(el).opacity")
            transform = hub.evaluate("el => getComputedStyle(el).transform")
            
            print(f"Hub Node - Box: {box}", flush=True)
            print(f"Hub Node - Opacity: {opacity}", flush=True)
            print(f"Hub Node - Transform: {transform}", flush=True)
            print(f"Hub Node - Content: {content[:100]}...", flush=True)
            
            # Check container height
            container = page.locator("#mindmap-container")
            c_box = container.bounding_box()
            print(f"Container Box: {c_box}", flush=True)

        except Exception as e:
            print(f"Error during node inspection: {e}", flush=True)
            page.screenshot(path="d:/VSCODE-PROJECTS/VAIDYA/scratch/error_state.png")
            
        # Take a final screenshot
        time.sleep(2) # Wait for animations
        page.screenshot(path="d:/VSCODE-PROJECTS/VAIDYA/scratch/roadmap_test_result.png", full_page=True)
        print("Final screenshot saved to scratch/roadmap_test_result.png", flush=True)
        
        # Close browser
        browser.close()

if __name__ == "__main__":
    test_roadmap()
