# E2E Test: CSV Export for Tables and Query Results

Test CSV export functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want to export tables and query results as CSV files
So that I can use my data in external applications like Excel or Google Sheets

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"

### Load Sample Data
4. Click the "Upload Data" button to open modal
5. Click on "Users Data" sample button to load users data
6. Wait for modal to close and table to appear
7. **Verify** a table named "users" appears in Available Tables section
8. Take a screenshot showing the users table with download button

### Test Table Download Button
9. **Verify** a download button (with download icon) appears directly to the left of the × (remove) button for the users table
10. Click the download button for the users table
11. **Verify** a CSV file download is triggered (the download should be named "users.csv")
12. Take a screenshot after clicking table download

### Execute a Query for Results Export
13. Enter the query: "Show me all users"
14. Click the Query button
15. Wait for query results to appear
16. **Verify** the Query Results section is visible
17. Take a screenshot of query results

### Test Results Download Button
18. **Verify** a download button appears directly to the left of the "Hide" button in the results header
19. Click the download button for query results
20. **Verify** a CSV file download is triggered (the download should be named "query_results.csv")
21. Take a screenshot after clicking results download

### Verify Button Positions
22. **Verify** the table download button is positioned immediately to the left of the × button (in the same header row)
23. **Verify** the results download button is positioned immediately to the left of the Hide button

## Success Criteria
- Download button appears next to × icon for each table in Available Tables section
- Download button appears next to Hide button in Query Results section
- Clicking table download button triggers file download
- Clicking results download button triggers file download
- Download buttons use an appropriate download icon
- Button positions match the specification (download left of × for tables, download left of Hide for results)
- All existing functionality continues to work (no regressions)
