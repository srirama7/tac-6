# E2E Test: CSV Export for Tables and Query Results

Test CSV export functionality for both uploaded tables and query results in the Natural Language SQL Interface application.

## User Story

As a user
I want to export my tables and query results as CSV files
So that I can analyze the data in external tools like Excel or perform further processing

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page loads correctly with core UI elements

4. Upload a sample CSV file to create a table:
   - Click the "Upload Data" button
   - Select a CSV file (use test fixtures if available, or create a sample file with at least 3 columns and 5 rows including special characters like quotes and commas)
   - Wait for the upload to complete

5. **Verify** the table appears in the "Available Tables" section
6. **Verify** the export button (⬇) is visible on the table item
7. **Verify** the export button is positioned to the left of the 'x' (remove) button
8. Take a screenshot of the table with export button visible

9. Click the export button on the table item
10. Wait for the download to trigger (check browser downloads)
11. **Verify** a CSV file was downloaded with the table name as filename (e.g., `tablename.csv`)
12. Take a screenshot showing the download triggered

13. Read the downloaded CSV file content
14. **Verify** the CSV file contains:
    - Correct headers matching the table columns
    - All data rows from the table
    - Properly escaped special characters (quotes, commas, newlines)
    - No data corruption

15. Execute a natural language query:
    - Enter query: "Show all records from the uploaded table"
    - Click Query button
    - Wait for results to appear

16. **Verify** query results are displayed
17. **Verify** the export button appears in the query results section (should show "⬇ Export Results")
18. **Verify** the export button is visible and properly positioned
19. Take a screenshot of the query results with export button visible

20. Click the export results button
21. Wait for the download to trigger
22. **Verify** a CSV file was downloaded with a timestamped filename (e.g., `query_results_YYYYMMDD_HHMMSS.csv`)
23. Take a screenshot showing the results download triggered

24. Read the downloaded query results CSV file
25. **Verify** the results CSV file contains:
    - Correct headers matching the query result columns
    - All result rows from the query
    - Properly formatted data
    - Matches the displayed results

26. Test with special characters:
    - If the uploaded data contains special characters (quotes, commas, newlines), verify they are properly escaped in both CSV exports

27. Take a final screenshot of the application state
28. Click "Hide" button to close results

## Success Criteria

- Export buttons are visible and properly positioned:
  - Table export button (⬇) appears to the left of the 'x' button
  - Results export button appears in the results section
- Table export downloads CSV with correct filename format (`tablename.csv`)
- Results export downloads CSV with timestamped filename (`query_results_YYYYMMDD_HHMMSS.csv`)
- Both CSV files contain correct headers
- Both CSV files contain all expected data rows
- Special characters are properly escaped according to RFC 4180
- No JavaScript errors occur during exports
- Downloads are triggered automatically without user intervention beyond clicking the button
- 6 screenshots are taken (initial state, table with export button, table download, results with export button, results download, final state)
