# E2E Test: CSV Export Functionality

Test CSV export functionality for both tables and query results in the Natural Language SQL Interface application.

## User Story

As a user
I want to export tables and query results to CSV files with a single click
So that I can analyze the data in external tools like Excel or share it with colleagues

## Test Steps

### Part 1: Setup - Upload Sample Data

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. Click the "Upload Data" button
5. **Verify** the upload modal appears
6. Click the "Users Data" sample data button
7. Wait for the upload to complete
8. **Verify** a success message appears
9. **Verify** the "users" table appears in Available Tables section
10. Take a screenshot of the loaded table

### Part 2: Export Table to CSV

11. **Verify** a download button (↓ symbol) appears next to the × button in the users table header
12. Take a screenshot showing the download button
13. Click the download button on the users table
14. **Verify** a CSV file is downloaded with filename "users.csv"
15. Open the downloaded CSV file in a text editor or spreadsheet
16. **Verify** the CSV contains:
    - A header row with column names (e.g., id, name, email, signup_date)
    - Data rows matching the users table data
    - Proper CSV formatting (commas as delimiters, quoted fields where needed)
17. Take a screenshot of the CSV file opened in a text editor or spreadsheet

### Part 3: Export Query Results to CSV

18. In the query input, enter: "Show me users who signed up in 2024"
19. Take a screenshot of the query input
20. Click the Query button
21. Wait for results to appear
22. **Verify** query results are displayed with SQL translation
23. **Verify** a "Download CSV" button appears next to the "Hide" button in the Query Results section
24. Take a screenshot showing the Download CSV button
25. Click the "Download CSV" button
26. **Verify** a CSV file is downloaded with filename starting with "query_results_" and including a timestamp
27. Open the downloaded CSV file
28. **Verify** the CSV contains:
    - A header row with column names from the query results
    - Only the filtered data (users from 2024)
    - Proper CSV formatting
29. Take a screenshot of the query results CSV file

### Part 4: Edge Cases

30. Execute a query that returns zero results: "Show me users from year 2050"
31. **Verify** "No results found" message appears
32. **Verify** the Download CSV button is still visible
33. Click the Download CSV button
34. **Verify** either:
    - A CSV with only headers is downloaded, OR
    - An appropriate message is shown indicating no data to export

## Success Criteria

- Upload modal works and sample data loads successfully
- Download button (↓) appears in table header next to remove button (×)
- Clicking table download button triggers CSV download
- Downloaded table CSV has correct filename (table_name.csv)
- Table CSV contains all rows and columns with proper formatting
- Download CSV button appears in Query Results section next to Hide button
- Clicking results download button triggers CSV download
- Downloaded results CSV has timestamped filename (query_results_YYYYMMDD_HHMMSS.csv)
- Results CSV contains only the filtered query results
- CSV files can be opened in Excel/text editors
- Special characters in data are properly escaped in CSV
- Empty result sets are handled gracefully
- At least 6 screenshots are taken showing key steps

## Expected CSV Format

### Users Table CSV Example:
```
id,name,email,signup_date
1,Alice Smith,alice@example.com,2024-01-15
2,Bob Jones,bob@example.com,2024-02-20
3,Carol White,carol@example.com,2023-12-10
```

### Query Results CSV Example:
```
id,name,email,signup_date
1,Alice Smith,alice@example.com,2024-01-15
2,Bob Jones,bob@example.com,2024-02-20
```

## Notes

- CSV files should use UTF-8 encoding
- Fields containing commas should be quoted
- Download should trigger automatically (browser download dialog)
- No page refresh should occur during export
- Loading indicators should appear during export operations
