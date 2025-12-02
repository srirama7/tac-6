# E2E Test: CSV Export for Tables and Query Results

Test CSV export functionality for both table data and query results in the Natural Language SQL Interface application.

## User Story

As a data analyst using the Natural Language SQL Interface
I want to export tables and query results to CSV files with a single click
So that I can analyze the data offline in spreadsheet applications like Excel or perform further processing

## Test Steps

### Part 1: Table Export

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. Click "Upload Data" button
5. Click the "Users Data" sample button to load sample users data
6. Wait for upload to complete
7. **Verify** the users table appears in the "Available Tables" section
8. **Verify** the download button (⬇) appears in the table header, to the left of the × button
9. Take a screenshot of the table with download button
10. Click the download button (⬇) for the users table
11. Wait 2 seconds for file download
12. **Verify** a file named "users.csv" was downloaded
13. Take a screenshot confirming the download

### Part 2: Query Results Export

14. Enter the query: "Show me all users"
15. Take a screenshot of the query input
16. Click the Query button
17. Wait for query results to appear
18. **Verify** the query results section is displayed
19. **Verify** the download button (⬇) appears in the results header, to the left of the "Hide" button
20. Take a screenshot of the results with download button
21. Click the download button (⬇) in the results header
22. Wait 2 seconds for file download
23. **Verify** a file named "query_results.csv" was downloaded
24. Take a screenshot confirming the download

### Part 3: Verify CSV Content (Manual verification after test)

25. Open users.csv in a text editor or spreadsheet application
26. **Verify** the CSV contains:
    - Header row with column names
    - Data rows with user information
    - Proper CSV formatting (quoted values with commas)
    - No errors or malformed data

27. Open query_results.csv in a text editor or spreadsheet application
28. **Verify** the CSV contains:
    - Header row with column names
    - Data rows matching the query results
    - Proper CSV formatting
    - Same data as shown in the web interface

## Success Criteria

- Download button appears in table header (to the left of × button)
- Download button appears in query results header (to the left of Hide button)
- Clicking table download button exports users.csv
- Clicking query results download button exports query_results.csv
- CSV files have correct filenames
- CSV files are properly formatted with headers and data rows
- CSV content matches the data shown in the web interface
- No errors occur during export
- At least 6 screenshots are taken documenting the test
- Both download buttons are visible and functional

## Notes

- The download button uses the ⬇ (U+2B07) character
- CSV files should be RFC 4180 compliant
- Special characters in data should be properly escaped
- Empty values should be rendered as empty strings in CSV
- File downloads should trigger browser's native download mechanism
