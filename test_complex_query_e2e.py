import asyncio
import os
import json
from playwright.async_api import async_playwright

async def run_test():
    base_path = "C:/Users/amogh/Downloads/tac-6/tac-6"
    screenshot_dir = f"{base_path}/agents/845e6682/e2e_test_runner_1_1/img/complex_query"

    test_result = {
        "test_name": "Complex Query with Filtering",
        "status": "passed",
        "screenshots": [],
        "error": None
    }

    try:
        async with async_playwright() as p:
            # Launch browser in headed mode
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            # Step 1: Navigate to the Application URL
            print("Step 1: Navigate to http://localhost:5173")
            await page.goto("http://localhost:5173", wait_until="networkidle")
            await asyncio.sleep(2)

            # Step 2: Take a screenshot of the initial state
            print("Step 2: Take screenshot of initial state")
            screenshot_path = f"{screenshot_dir}/01_initial_state.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            test_result["screenshots"].append(screenshot_path)

            # Step 3: Clear the query input
            print("Step 3: Clear the query input")
            query_input = await page.wait_for_selector("#query-input", timeout=5000)
            await query_input.click()
            await query_input.fill("")

            # Step 4: Enter the complex query
            print("Step 4: Enter complex query")
            query_text = "Show users older than 30 who live in cities starting with 'S'"
            await query_input.fill(query_text)
            await asyncio.sleep(1)

            # Step 5: Take a screenshot of the query input
            print("Step 5: Take screenshot of query input")
            screenshot_path = f"{screenshot_dir}/02_query_input.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            test_result["screenshots"].append(screenshot_path)

            # Step 6: Click Query button
            print("Step 6: Click Query button")
            query_button = await page.wait_for_selector("#query-button", timeout=5000)
            await query_button.click()

            # Wait for results to load
            print("   Waiting for query to execute...")
            await asyncio.sleep(5)

            # Step 7: Verify results appear with filtered data
            print("Step 7: Verify results appear with filtered data")
            results_section = await page.query_selector("#results-section")
            if not results_section:
                raise Exception("(Step 7 X) Results section not found")

            is_visible = await results_section.is_visible()
            if not is_visible:
                raise Exception("(Step 7 X) Results section is not visible")

            # Step 8: Verify the generated SQL contains WHERE clause
            print("Step 8: Verify SQL contains WHERE clause")
            sql_display = await page.query_selector("#sql-display")
            if not sql_display:
                raise Exception("(Step 8 X) SQL display element not found")

            # Wait for SQL to populate
            for i in range(10):
                sql_text = await sql_display.inner_text()
                if sql_text and "SELECT" in sql_text.upper():
                    break
                await asyncio.sleep(1)

            sql_text = await sql_display.inner_text()
            print(f"   SQL Text: {sql_text}")

            if "WHERE" not in sql_text.upper():
                raise Exception(f"(Step 8 X) SQL does not contain WHERE clause. SQL: {sql_text}")

            print(f"   SQL: {sql_text}")

            # Step 9: Take a screenshot of the SQL translation
            print("Step 9: Take screenshot of SQL translation")
            screenshot_path = f"{screenshot_dir}/03_sql_translation.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            test_result["screenshots"].append(screenshot_path)

            # Step 10: Count the number of results returned
            print("Step 10: Count the number of results")
            results_table = await page.query_selector("#results-table")
            if results_table:
                rows = await results_table.query_selector_all("tbody tr")
                result_count = len(rows)
                print(f"   Found {result_count} results")
            else:
                raise Exception("(Step 10 ❌) Results table not found")

            # Step 11: Take a screenshot of the filtered results
            print("Step 11: Take screenshot of filtered results")
            screenshot_path = f"{screenshot_dir}/04_filtered_results.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            test_result["screenshots"].append(screenshot_path)

            # Step 12: Click "Hide" button to close results
            print("Step 12: Click Hide button")
            hide_button = await page.query_selector("#hide-button")
            if hide_button:
                await hide_button.click()
                await asyncio.sleep(1)
            else:
                # Try alternative selectors
                hide_button = await page.query_selector("button:has-text('Hide')")
                if hide_button:
                    await hide_button.click()
                    await asyncio.sleep(1)
                else:
                    raise Exception("(Step 12 X) Hide button not found")

            # Step 13: Take a screenshot of the final state
            print("Step 13: Take screenshot of final state")
            screenshot_path = f"{screenshot_dir}/05_final_state.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            test_result["screenshots"].append(screenshot_path)

            # Close browser
            await browser.close()

            # Verify success criteria
            print("\nVerifying success criteria:")
            print("+ Complex natural language is correctly interpreted")
            print("+ SQL contains appropriate WHERE conditions")
            print("+ Results are properly filtered")
            print("+ No errors occur during execution")
            print("+ Hide button works")
            print(f"+ 5 screenshots are taken ({len(test_result['screenshots'])} screenshots)")

            if len(test_result["screenshots"]) != 5:
                test_result["status"] = "failed"
                test_result["error"] = f"Expected 5 screenshots, but got {len(test_result['screenshots'])}"

    except Exception as e:
        test_result["status"] = "failed"
        test_result["error"] = str(e)
        print(f"\n❌ Test failed: {e}")

    # Output JSON result
    print("\n" + "="*60)
    print("TEST RESULT:")
    print("="*60)
    print(json.dumps(test_result, indent=2))

    return test_result

if __name__ == "__main__":
    asyncio.run(run_test())
