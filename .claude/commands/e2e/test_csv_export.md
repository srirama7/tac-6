# E2E Test: CSV Export Functionality

Test CSV export functionality for both tables and query results in the Natural Language SQL Interface application.

## User Story

As a user
I want to export tables and query results as CSV files
So that I can share, analyze, or archive my data outside the application

## Test Steps

### Part 1: Table Export

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the Available Tables section is visible

4. Click "Upload Data" button to open the upload modal
5. Click the "Users Data" sample data button
6. **Verify** the users table appears in Available Tables section
7. Take a screenshot of the Available Tables section

8. **Verify** the download button (↓) appears next to the × (remove) button
9. **Verify** the download button is positioned to the left of the × button
10. Take a screenshot showing the download button placement

11. Click the download button for the users table
12. **Verify** the button shows a loading state briefly
13. **Verify** a CSV file named "users.csv" is downloaded
14. **Verify** the downloaded file can be opened
15. **Verify** the CSV contains:
    - Header row with column names
    - Data rows with user information
    - Proper CSV formatting (comma-separated, quoted values where needed)

### Part 2: Query Results Export

16. In the query input textbox, enter: "Show me all users who signed up in 2024"
17. Click the Query button
18. **Verify** the query results appear
19. Take a screenshot of the results section

20. **Verify** the download button (↓) appears in the results header
21. **Verify** the download button is positioned to the left of the "Hide" button
22. **Verify** the download button is enabled (not grayed out)
23. Take a screenshot showing the download button in results header

24. Click the download button in the results section
25. **Verify** the button shows a loading state briefly
26. **Verify** a CSV file with name pattern "query_results_YYYYMMDD_HHMMSS.csv" is downloaded
27. **Verify** the downloaded file can be opened
28. **Verify** the CSV contains:
    - Header row matching the query result columns
    - Data rows matching the query results
    - Proper CSV formatting

### Part 3: Edge Cases

29. Execute a query that returns no results (e.g., "Show me users older than 200")
30. **Verify** the download button in results section is disabled
31. Take a screenshot showing the disabled download button

32. Upload a second sample dataset (Products)
33. **Verify** both tables now show download buttons
34. Click the download button for the products table
35. **Verify** a CSV file named "products.csv" is downloaded
36. **Verify** the file contains product data

### Part 4: Data Integrity

37. Open the "users.csv" file in a spreadsheet application (Excel, Google Sheets, etc.)
38. **Verify** all columns are properly separated
39. **Verify** data with special characters (commas, quotes) is properly escaped
40. **Verify** no data corruption occurred during export
41. Take a screenshot of the CSV opened in a spreadsheet application

42. Open the "query_results_*.csv" file in a spreadsheet application
43. **Verify** the data matches what was displayed in the query results
44. Take a screenshot of the query results CSV in a spreadsheet application

## Success Criteria

- Download button appears in Available Tables section for each table
- Download button appears in Query Results section when results are present
- Download buttons are properly positioned (left of × button for tables, left of Hide button for results)
- Table export downloads CSV with correct filename format: `{table_name}.csv`
- Query results export downloads CSV with timestamp: `query_results_YYYYMMDD_HHMMSS.csv`
- CSV files contain proper headers and data
- CSV files are properly formatted and can be opened in spreadsheet applications
- Download buttons show loading state during export
- Download button is disabled when query results are empty
- Special characters in data are properly escaped in CSV
- At least 6 screenshots are taken documenting the test flow

## Expected Behavior

- Clicking table download button exports entire table as CSV
- Clicking query results download button exports current results as CSV
- Downloads happen instantly without page refresh
- No error messages appear during normal operation
- CSV files follow standard CSV format (RFC 4180)
- Filenames are descriptive and include table name or timestamp

## Error Cases to Test

- Attempting to export non-existent table (should fail gracefully)
- Exporting empty table (should produce CSV with only headers)
- Network errors during export (should display error message)
- Concurrent exports (should handle multiple simultaneous downloads)
