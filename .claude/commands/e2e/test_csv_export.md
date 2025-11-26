# E2E Test: CSV Export Functionality

Test CSV export functionality for both table data and query results in the Natural Language SQL Interface application.

## User Story

As a data analyst
I want to export table data and query results as CSV files with a single click
So that I can use the data in other tools like Excel or data analysis scripts

## Prerequisites

- Application must be running (server and client)
- Sample data must be loaded (users table with at least a few rows)

## Test Steps

### Part 1: Table Export

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the "Available Tables" section is visible
4. **Verify** at least one table is displayed (e.g., "users")
5. Take a screenshot of the tables section
6. **Verify** each table has a download button (⬇) displayed to the left of the remove (×) button
7. Hover over the download button
8. **Verify** tooltip shows "Export table as CSV"
9. Click the download button for the users table
10. **Verify** a CSV file is downloaded
11. **Verify** the filename format matches: `users_YYYY-MM-DD_HHMMSS.csv`
12. Take a screenshot after download completes
13. Open the downloaded CSV file in a text editor or Excel
14. **Verify** the CSV contains:
    - Header row with column names (id, name, email, age, etc.)
    - Data rows matching the table content
    - Proper UTF-8 encoding (special characters display correctly)
15. Take a screenshot of the CSV content

### Part 2: Query Results Export

16. In the query input, enter: "Show me all users who are older than 25"
17. Take a screenshot of the query input
18. Click the Query button
19. **Verify** query results appear in the "Query Results" section
20. **Verify** the results header shows:
    - "Query Results" title
    - Download button (⬇) to the left of the Hide button
21. Take a screenshot of the results header
22. Hover over the download button
23. **Verify** tooltip shows "Export results as CSV"
24. Click the download button
25. **Verify** a CSV file is downloaded
26. **Verify** the filename format matches: `query_results_YYYY-MM-DD_HHMMSS.csv`
27. Take a screenshot after download completes
28. Open the downloaded query results CSV file
29. **Verify** the CSV contains:
    - Header row with the query result column names
    - Only the filtered data (users older than 25)
    - Proper CSV formatting (commas, quotes for special characters)
30. Take a screenshot of the query results CSV content

### Part 3: Edge Cases

31. Execute a query that returns no results: "Show me users who are 200 years old"
32. **Verify** results section shows "No results found"
33. Click the download button for the empty result set
34. **Verify** downloaded CSV contains only the header row (no data rows)
35. Take a screenshot

36. Test exporting a table with special characters or NULL values
37. **Verify** CSV handles these cases correctly:
    - NULL values appear as empty cells
    - Special characters (quotes, commas) are properly escaped
    - Unicode characters are preserved

## Success Criteria

- Download button appears next to × icon for each table in Available Tables section
- Download button appears next to Hide button in Query Results section
- Download buttons use the ⬇ icon
- Clicking table download button downloads CSV with all table data
- Clicking query results download button downloads CSV with current query results
- CSV files have descriptive filenames with timestamps
- CSV files are properly formatted with UTF-8 encoding
- CSV files include column headers as first row
- CSV files handle special characters and null values correctly
- Empty result sets download with header row only
- At least 7 screenshots are taken documenting the test flow

## Expected File Outputs

- `users_[timestamp].csv` - Full table export
- `query_results_[timestamp].csv` - Query results export
- Screenshots showing:
  - Initial table view with download buttons
  - Downloaded table CSV content
  - Query results with download button
  - Downloaded query results CSV content
  - Empty results CSV

## Notes

- Test should verify both download functionality and CSV format correctness
- Timestamps in filenames ensure uniqueness for multiple exports
- CSV files should be compatible with Excel, Google Sheets, and other tools
- All exports must use UTF-8 encoding for proper character support
