# E2E Test: CSV Export Functionality

Test CSV export functionality for both database tables and query results in the Natural Language SQL Interface application.

## User Story

As a data analyst
I want to export tables and query results as CSV files
So that I can use the data in spreadsheet applications or share it with others

## Prerequisites

- Application must be running
- Sample data should be loaded (users table)

## Test Steps - Part 1: Table Export

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the "Available Tables" section is visible
4. **Verify** at least one table is displayed (e.g., "users" table)
5. **Verify** each table has a download button (↓) to the left of the remove button (×)
6. Take a screenshot showing the download button in the table header
7. Hover over the download button
8. **Verify** the tooltip displays "Download as CSV"
9. Click the download button for the "users" table
10. **Verify** a success message appears: "Table 'users' downloaded successfully!"
11. **Verify** the file download was initiated (check browser downloads)
12. **Verify** the downloaded file is named "users.csv"
13. Open the downloaded CSV file
14. **Verify** the CSV contains proper headers (column names)
15. **Verify** the CSV contains data rows
16. **Verify** special characters are properly escaped
17. Take a screenshot of the CSV file opened in a text editor or spreadsheet

## Test Steps - Part 2: Query Result Export

18. Enter a natural language query: "Show me all users who signed up in 2024"
19. Click the Query button
20. **Verify** query results are displayed
21. **Verify** a download button (↓) appears to the left of the "Hide" button
22. Take a screenshot showing the download button in the results section
23. Hover over the download button
24. **Verify** the tooltip displays "Download as CSV"
25. Click the download button in the results section
26. **Verify** a success message appears: "Query results downloaded successfully!"
27. **Verify** the file download was initiated
28. **Verify** the downloaded file is named with pattern "query_result_YYYYMMDD_HHMMSS.csv"
29. Open the downloaded CSV file
30. **Verify** the CSV contains query result headers
31. **Verify** the CSV contains the filtered data
32. Take a screenshot of the query result CSV file

## Test Steps - Part 3: Edge Cases

33. Execute a query that returns no results: "Show me users with age over 1000"
34. **Verify** results section shows "No results found"
35. **Verify** the download button does NOT appear (no results to export)
36. Upload a CSV file with special characters in data (commas, quotes, newlines)
37. Export the table
38. **Verify** the exported CSV properly handles special characters
39. Execute a query on a table with many rows (>100)
40. Export the query results
41. **Verify** the CSV export completes successfully
42. **Verify** all rows are included in the export

## Success Criteria

- Download buttons appear in the correct locations (table headers and query results)
- Download buttons have appropriate styling and hover effects
- Clicking table download button exports the entire table as CSV
- CSV files for tables are named "{table_name}.csv"
- Clicking results download button exports query results as CSV
- CSV files for query results are named "query_result_{timestamp}.csv"
- CSV files have proper headers with column names
- CSV data is properly formatted and can be opened in spreadsheet applications
- Special characters (commas, quotes, newlines) are properly escaped
- Empty result sets do not show a download button
- Success messages appear after successful downloads
- All existing functionality continues to work (no regressions)
- At least 4 screenshots are taken

## Error Scenarios to Test

- Export a non-existent table (should fail gracefully)
- Export when server is down (should show error message)
- Export a very large dataset (should complete or timeout gracefully)
- Export with Unicode characters (should preserve encoding)

## Notes

- CSV files should be UTF-8 encoded
- Excel should be able to open the CSV files correctly
- Google Sheets should be able to import the CSV files
- The download should trigger a browser download (not open in a new tab)
- Success messages should disappear after 3 seconds
