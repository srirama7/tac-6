# E2E Test: CSV Export Functionality

Test CSV export functionality for both table data and query results in the Natural Language SQL Interface application.

## User Story

As a user
I want to export table data and query results to CSV files
So that I can analyze the data in spreadsheet applications or share it with colleagues

## Prerequisites

- Application is running at the Application URL
- Sample data (users.json) is available

## Test Steps

### Part 1: Table Export

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. Click the "Upload Data" button
5. Click on "Users Data" sample data button
6. **Verify** a success message appears showing the table was created
7. Take a screenshot of the success message
8. **Verify** the "users" table appears in the "Available Tables" section
9. **Verify** a download button (↓) is visible in the table header, to the left of the remove (×) button
10. Take a screenshot of the table with the download button
11. Click the download button on the users table
12. **Verify** a CSV file is downloaded
13. **Verify** the filename matches the pattern `users_export_YYYYMMDD_HHMMSS.csv`
14. Open the downloaded CSV file
15. **Verify** the CSV contains:
    - Header row with column names (id, name, email, signup_date, etc.)
    - Data rows matching the users table content
    - Proper CSV formatting (commas, quotes where needed)
16. Take a screenshot of the CSV file opened in a text editor or spreadsheet application

### Part 2: Query Results Export

17. Return to the application in the browser
18. Enter the query: "Show me users who signed up after 2023"
19. Click the Query button
20. **Verify** query results are displayed
21. Take a screenshot of the query results
22. **Verify** a download button (↓) appears in the Query Results header, to the left of the "Hide" button
23. Click the download button in the Query Results section
24. **Verify** a CSV file is downloaded
25. **Verify** the filename matches the pattern `query_results_YYYYMMDD_HHMMSS.csv`
26. Open the downloaded CSV file
27. **Verify** the CSV contains:
    - Header row with the query result column names
    - Data rows matching the displayed query results
    - Proper CSV formatting
28. Take a screenshot of the query results CSV file

### Part 3: Edge Cases

29. Execute a query that returns zero results: "Show me users with age over 1000"
30. **Verify** results section shows "No results found"
31. Click the download button in the Query Results section
32. **Verify** the downloaded CSV contains only headers (no data rows)
33. Take a screenshot

### Part 4: Special Characters

34. Upload a test file or table containing data with special characters (commas, quotes, newlines)
35. Export the table to CSV
36. Open the CSV file
37. **Verify** special characters are properly escaped:
    - Commas in data are handled correctly
    - Quotes are properly escaped (doubled quotes)
    - Newlines within fields are preserved
38. Take a screenshot of the CSV with special characters

## Success Criteria

- [ ] Download button appears in Available Tables section for each table
- [ ] Download button appears in Query Results section after executing a query
- [ ] Both download buttons use the ↓ icon
- [ ] Download buttons are positioned to the left of their respective control buttons
- [ ] Clicking table download button triggers CSV file download
- [ ] Table export filename follows pattern: `{table_name}_export_{timestamp}.csv`
- [ ] Clicking query results download button triggers CSV file download
- [ ] Query results export filename follows pattern: `query_results_{timestamp}.csv`
- [ ] CSV files contain proper headers and data
- [ ] Special characters (commas, quotes, newlines) are properly escaped in CSV
- [ ] Empty result sets export with headers only
- [ ] All CSV files can be opened in spreadsheet applications (Excel, Google Sheets, etc.)
- [ ] At least 6 screenshots are taken documenting the test flow

## Expected Outcomes

- Users can easily export table data with a single click
- Users can export query results to continue analysis offline
- CSV files are properly formatted and compatible with standard spreadsheet applications
- Filenames include timestamps to prevent conflicts
- No errors occur during export operations
- UI remains responsive during export operations
