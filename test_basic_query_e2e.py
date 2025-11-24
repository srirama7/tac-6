#!/usr/bin/env python3
"""
E2E Test: Basic Query Execution
Test basic query functionality in the Natural Language SQL Interface application.
"""
import json
import os
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, expect
except ImportError:
    print("Error: Playwright not installed. Installing now...")
    os.system("pip install playwright")
    os.system("playwright install chromium")
    from playwright.sync_api import sync_playwright, expect

# Configuration
APPLICATION_URL = "http://localhost:5173"
ADW_ID = "00620b88"
AGENT_NAME = "e2e_test_runner_0_0"
TEST_NAME = "basic_query"
CODEBASE_PATH = os.getcwd()
SCREENSHOT_DIR = os.path.join(CODEBASE_PATH, "agents", ADW_ID, AGENT_NAME, "img", TEST_NAME)

# Create screenshot directory
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def run_test():
    """Execute the E2E test steps"""
    test_result = {
        "test_name": "Basic Query Execution",
        "status": "passed",
        "screenshots": [],
        "error": None
    }

    try:
        with sync_playwright() as p:
            # Launch browser in headed mode for visibility
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()

            # Step 1: Navigate to the Application URL
            print(f"Step 1: Navigating to {APPLICATION_URL}")
            page.goto(APPLICATION_URL)
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            # Step 2: Take a screenshot of the initial state
            print("Step 2: Taking screenshot of initial state")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "01_initial_state.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 3: Verify the page title
            print("Step 3: Verifying page title")
            title = page.title()
            if title != "Natural Language SQL Interface":
                raise AssertionError(f"(Step 3 [FAIL]) Expected page title 'Natural Language SQL Interface', but got '{title}'")
            print(f"[OK] Page title verified: {title}")

            # Step 4: Verify core UI elements are present
            print("Step 4: Verifying core UI elements")

            # Query input textbox
            query_input = page.locator("textarea[placeholder*='query' i], input[placeholder*='query' i], textarea")
            if not query_input.first.is_visible(timeout=5000):
                raise AssertionError("(Step 4 [FAIL]) Query input textbox not found")
            print("[OK] Query input textbox found")

            # Query button
            query_button = page.locator("button:has-text('Query'), button:has-text('Submit'), button[type='submit']")
            if not query_button.first.is_visible(timeout=5000):
                raise AssertionError("(Step 4 [FAIL]) Query button not found")
            print("[OK] Query button found")

            # Upload Data button
            upload_button = page.locator("button:has-text('Upload Data'), button:has-text('Upload')")
            if not upload_button.first.is_visible(timeout=5000):
                raise AssertionError("(Step 4 [FAIL]) Upload Data button not found")
            print("[OK] Upload Data button found")

            # Available Tables section
            try:
                tables_section = page.locator("text=/Available Tables/i")
                if not tables_section.first.is_visible(timeout=2000):
                    tables_section = page.locator("text=/Tables/i")
                    if not tables_section.first.is_visible(timeout=2000):
                        tables_section = page.locator("[class*='table']")
                        if not tables_section.first.is_visible(timeout=1000):
                            raise AssertionError("(Step 4 [FAIL]) Available Tables section not found")
                print("[OK] Available Tables section found")
            except:
                raise AssertionError("(Step 4 [FAIL]) Available Tables section not found")

            # Step 4.5: Upload sample users data
            print("Step 4.5: Uploading sample users data")
            upload_button.first.click()
            time.sleep(1)

            # Click on "Sample Users" button
            sample_users_btn = page.locator("button:has-text('Sample Users'), button:has-text('Users')")
            if sample_users_btn.first.is_visible(timeout=3000):
                sample_users_btn.first.click()
                print("[OK] Sample users data uploaded")
                time.sleep(2)
            else:
                print("[WARN] Sample users button not found, continuing anyway")

            # Step 5: Enter the query
            print("Step 5: Entering query text")
            query_text = "Show me all users from the users table"
            query_input.first.fill(query_text)
            time.sleep(1)

            # Step 6: Take a screenshot of the query input
            print("Step 6: Taking screenshot of query input")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "02_query_input.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 7: Click the Query button
            print("Step 7: Clicking Query button")
            query_button.first.click()

            # Step 8: Verify the query results appear
            print("Step 8: Verifying query results appear")
            # Wait for results to load (look for results container, table, or loading indicator)
            page.wait_for_timeout(5000)  # Give time for API call

            results_container = page.locator("[class*='result'], [class*='output'], table, .table")
            if not results_container.first.is_visible(timeout=10000):
                raise AssertionError("(Step 8 [FAIL]) Query results did not appear")
            print("[OK] Query results appeared")

            # Take a debugging screenshot
            screenshot_path = os.path.join(SCREENSHOT_DIR, "debug_before_step9.png")
            page.screenshot(path=screenshot_path)

            # Step 9: Verify the SQL translation is displayed
            print("Step 9: Verifying SQL translation")
            sql_found = False
            try:
                # Try different selectors
                if page.locator("text=/SELECT/i").first.is_visible(timeout=2000):
                    sql_found = True
                elif page.locator("code").filter(has_text="SELECT").first.is_visible(timeout=2000):
                    sql_found = True
                elif page.locator("pre").filter(has_text="SELECT").first.is_visible(timeout=2000):
                    sql_found = True
                elif page.locator("*").filter(has_text="SELECT").first.is_visible(timeout=2000):
                    sql_found = True
            except:
                pass

            if not sql_found:
                # Take a screenshot for debugging
                screenshot_path = os.path.join(SCREENSHOT_DIR, "debug_no_sql.png")
                page.screenshot(path=screenshot_path)
                raise AssertionError("(Step 9 [FAIL]) SQL translation not displayed (should contain 'SELECT * FROM users')")

            print("[OK] SQL translation displayed")

            # Step 10: Take a screenshot of the SQL translation
            print("Step 10: Taking screenshot of SQL translation")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "03_sql_translation.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 11: Verify the results table contains data
            print("Step 11: Verifying results table contains data")
            table_rows = page.locator("table tr, [role='row']")
            row_count = table_rows.count()
            if row_count < 2:  # At least header + 1 data row
                raise AssertionError(f"(Step 11 [FAIL]) Results table should contain data, but found only {row_count} rows")
            print(f"[OK] Results table contains {row_count} rows")

            # Step 12: Take a screenshot of the results
            print("Step 12: Taking screenshot of results")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "04_results_table.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 13: Click Hide button to close results
            print("Step 13: Clicking Hide button")
            hide_button = page.locator("button:has-text('Hide'), button:has-text('Close')")
            if hide_button.first.is_visible(timeout=3000):
                hide_button.first.click()
                time.sleep(1)
                print("[OK] Hide button clicked")
            else:
                print("[WARN] Hide button not found (optional step)")

            print("\n[SUCCESS] All test steps completed successfully!")

            # Close browser
            browser.close()

    except AssertionError as e:
        test_result["status"] = "failed"
        test_result["error"] = str(e)
        print(f"\n[FAIL] Test failed: {e}")
        return test_result
    except Exception as e:
        test_result["status"] = "failed"
        test_result["error"] = f"Unexpected error: {str(e)}"
        print(f"\n[FAIL] Unexpected error: {e}")
        return test_result

    return test_result

if __name__ == "__main__":
    print("=" * 80)
    print("E2E Test: Basic Query Execution")
    print("=" * 80)
    print()

    result = run_test()

    print("\n" + "=" * 80)
    print("TEST REPORT")
    print("=" * 80)
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["status"] == "passed" else 1)
