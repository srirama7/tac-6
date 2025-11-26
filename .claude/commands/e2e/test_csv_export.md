# E2E Test: CSV Export Functionality

Test CSV export functionality for both tables and query results in the Natural Language SQL Interface application.

## User Story

As a user
I want to export tables and query results as CSV files with one click
So that I can use the data in external tools like Excel, Google Sheets, or other data analysis platforms

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Upload Data button
   - Available Tables section

5. Click the "Upload Data" button to open the modal
6. Take a screenshot of the upload modal
7. Click the "Users Data" sample data button to load sample data
8. Wait for the upload to complete
9. **Verify** a success message appears (contains "created successfully")
10. **Verify** the "users" table appears in the Available Tables section
11. Take a screenshot showing the loaded table

12. **Verify** the table has a download button (📥 icon) next to the remove button (×)
13. Click the download button on the "users" table
14. Wait for the download to complete (2 seconds)
15. **Verify** a file named "users.csv" was downloaded to the downloads folder
16. Take a screenshot after clicking download

17. Enter the query: "Show me all users"
18. Take a screenshot of the query input
19. Click the Query button
20. Wait for the query results to appear
21. **Verify** the query results appear with a results table
22. **Verify** a "Download CSV" button appears in the results header (before the Hide button)
23. Take a screenshot of the results with download button

24. Click the "Download CSV" button in the results section
25. Wait for the download to complete (2 seconds)
26. **Verify** a file named "query_results.csv" was downloaded
27. Take a screenshot after clicking the download button

28. **Verify** the CSV files contain the expected data:
    - Check that "users.csv" has headers and data rows
    - Check that "query_results.csv" has headers and data rows
29. Take a final screenshot showing the complete state

## Success Criteria
- Upload Data button works and modal opens
- Sample data loads successfully
- Table appears in Available Tables section with download button
- Table download button triggers CSV export
- CSV file for table is downloaded with correct filename (users.csv)
- Query executes successfully
- Query results display with Download CSV button
- Query results download button triggers CSV export
- CSV file for query results is downloaded (query_results.csv)
- Both CSV files contain valid data with headers
- At least 7 screenshots are taken

## Notes
- The download icon should be 📥 (Unicode 128229)
- The download button should appear to the left of the remove (×) button for tables
- The download button should appear to the left of the Hide button for query results
- Downloaded CSV files should be UTF-8 encoded with proper escaping
- The test should verify that files actually exist in the downloads folder
