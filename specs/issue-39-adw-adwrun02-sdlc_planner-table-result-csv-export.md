# Feature: Table and Query Result CSV Export

## Feature Description
Add one-click CSV export functionality for both database tables and query results. Users can download their data as CSV files with a single button click. This feature adds two download buttons to the UI: one next to the table removal button (×) in the Available Tables section, and another next to the Hide button in the Query Results section. The feature includes two new backend endpoints to handle CSV generation and export for both tables and query results.

## User Story
As a user
I want to export tables and query results as CSV files
So that I can analyze, share, and use my data in external tools like Excel or other data analysis platforms

## Problem Statement
Currently, users can view their data in the web interface but have no way to export it for use in other applications. Users need to manually copy-paste data or take screenshots to extract information, which is inefficient and error-prone. This limits the application's utility for users who need to analyze data in spreadsheet applications, share results with colleagues, or integrate data into other workflows.

## Solution Statement
Implement two new backend API endpoints (`/api/export/table/{table_name}` and `/api/export/query`) that generate CSV files from database tables and query results respectively. Add download buttons with appropriate icons in the UI next to existing controls. The backend will use Python's csv module to safely generate CSV content with proper escaping and return it with appropriate headers for browser download. The frontend will trigger file downloads using the browser's native download mechanism.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - Main FastAPI server file where the two new CSV export endpoints will be added
  - Add `GET /api/export/table/{table_name}` endpoint to export a table as CSV
  - Add `POST /api/export/query` endpoint to export query results as CSV
  - Use `StreamingResponse` with CSV content and appropriate headers for file download

- `app/server/core/data_models.py` - Data models for request/response validation
  - Add `ExportQueryRequest` model for the query export endpoint (contains sql, columns, results)
  - No response model needed as endpoints return StreamingResponse with raw CSV data

- `app/client/src/main.ts` - Main TypeScript file containing UI logic
  - Add download button next to the × button in the `displayTables` function
  - Add download button next to the Hide button in the `displayResults` function
  - Implement `exportTableAsCSV` function to call the table export endpoint
  - Implement `exportQueryResultAsCSV` function to call the query export endpoint
  - Use fetch API with blob response and create download link dynamically

- `app/client/src/api/client.ts` - API client functions
  - Add `exportTable(tableName: string)` method that returns a Blob
  - Add `exportQueryResult(request: ExportQueryRequest)` method that returns a Blob

- `app/client/src/types.d.ts` - TypeScript type definitions
  - Add `ExportQueryRequest` interface matching the backend model

- `app/client/src/style.css` - Styling for the download buttons
  - Add styles for `.download-button` class to match existing button styles
  - Ensure download icon is properly sized and positioned

- `app/server/core/sql_security.py` - SQL security module (reference only)
  - Review existing security functions to ensure CSV export uses safe query execution
  - Use `execute_query_safely` when fetching table data for export

### New Files

- `.claude/commands/e2e/test_csv_export.md` - E2E test file for CSV export functionality
  - Test exporting a table as CSV and verify the downloaded file
  - Test exporting query results as CSV and verify the downloaded file
  - Verify CSV format is correct with proper headers and data

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for CSV generation and export. Add two new FastAPI endpoints that can safely extract data from the database and convert it to CSV format. Implement proper security checks using existing SQL security utilities to ensure only valid tables can be exported. Add appropriate request/response models in the data models file. The CSV generation should handle various data types (strings, numbers, dates) and properly escape special characters.

### Phase 2: Core Implementation
Implement the frontend download functionality by adding download buttons to the UI in the appropriate locations. The table download button should appear in the Available Tables section, positioned directly to the left of the × removal button. The query result download button should appear in the Query Results section header, positioned directly to the left of the Hide button. Implement the JavaScript functions to trigger downloads by calling the backend endpoints and handling the blob responses.

### Phase 3: Integration
Connect the frontend and backend, test the complete flow end-to-end, and create comprehensive E2E tests. Ensure downloads work correctly in different browsers, file names are descriptive (including table/query context), and proper error handling is in place. Verify that CSV files can be opened in Excel and other spreadsheet applications without issues.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Backend Data Models
- Open `app/server/core/data_models.py`
- Add `ExportQueryRequest` Pydantic model with fields: `sql: str`, `columns: List[str]`, `results: List[Dict[str, Any]]`
- This model will be used to pass query results from frontend to backend for CSV generation

### Step 2: Create Table Export Endpoint
- Open `app/server/server.py`
- Add `GET /api/export/table/{table_name}` endpoint
- Validate table name using `validate_identifier` from sql_security module
- Check table exists using `check_table_exists` from sql_security module
- Use `execute_query_safely` to fetch all rows from the table
- Generate CSV content using Python's `csv` module with proper escaping
- Return `StreamingResponse` with CSV content, content-type `text/csv`, and Content-Disposition header for download
- Set filename as `{table_name}.csv`
- Add comprehensive error handling and logging

### Step 3: Create Query Result Export Endpoint
- Open `app/server/server.py`
- Add `POST /api/export/query` endpoint accepting `ExportQueryRequest`
- Generate CSV from the provided results and columns data
- Use Python's `csv.DictWriter` to handle the conversion
- Return `StreamingResponse` with CSV content, content-type `text/csv`, and Content-Disposition header
- Set filename as `query_results_{timestamp}.csv`
- Add comprehensive error handling and logging

### Step 4: Add Unit Tests for Backend Endpoints
- Create or update `app/server/tests/test_export.py`
- Test table export endpoint with valid table name
- Test table export endpoint with invalid table name (should return 400/404)
- Test query result export endpoint with sample data
- Test CSV format correctness (headers, data rows, escaping)
- Verify Content-Disposition headers are set correctly

### Step 5: Add TypeScript Type Definitions
- Open `app/client/src/types.d.ts`
- Add `ExportQueryRequest` interface matching the backend model

### Step 6: Add API Client Methods
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string): Promise<Blob>` method
- Add `exportQueryResult(request: ExportQueryRequest): Promise<Blob>` method
- Both methods should fetch with appropriate options and return blob responses
- Handle errors appropriately

### Step 7: Add Download Button to Available Tables
- Open `app/client/src/main.ts`
- In the `displayTables` function, add a download button in the `tableHeader` section
- Position the download button directly to the left of the × removal button
- Use an appropriate download icon (📥 or SVG icon)
- Add click handler that calls `exportTableAsCSV(table.name)`
- Style with class `download-button`

### Step 8: Add Download Button to Query Results
- Open `app/client/src/main.ts`
- In the `displayResults` function, add a download button in the results header
- Position the download button directly to the left of the Hide button
- Use the same download icon style as the table download button
- Add click handler that calls `exportQueryResultAsCSV(response, query)`
- Store the response data needed for export in the function scope

### Step 9: Implement Table Export Function
- Open `app/client/src/main.ts`
- Create `async function exportTableAsCSV(tableName: string)`
- Call `api.exportTable(tableName)` to get the blob
- Create a temporary anchor element with `href = URL.createObjectURL(blob)`
- Set `download` attribute to `{tableName}.csv`
- Trigger click on anchor element
- Clean up the object URL
- Add error handling with user-friendly error messages

### Step 10: Implement Query Result Export Function
- Open `app/client/src/main.ts`
- Create `async function exportQueryResultAsCSV(response: QueryResponse, query: string)`
- Prepare `ExportQueryRequest` object from response data
- Call `api.exportQueryResult(request)` to get the blob
- Create download link similar to table export
- Set filename as `query_results_{sanitized_query_snippet}.csv`
- Trigger download
- Add error handling

### Step 11: Add CSS Styling for Download Buttons
- Open `app/client/src/style.css`
- Add `.download-button` class styles matching existing button aesthetics
- Ensure proper sizing, spacing, and hover effects
- Make sure the button integrates well with the existing UI layout
- Add icon styling if using SVG icons

### Step 12: Create E2E Test File
- Create `.claude/commands/e2e/test_csv_export.md` following the pattern from `test_basic_query.md`
- Include test steps for:
  1. Upload sample data
  2. Click download button on a table
  3. Verify CSV file is downloaded with correct name
  4. Verify CSV content has correct headers and data
  5. Execute a query
  6. Click download button on query results
  7. Verify query results CSV is downloaded
  8. Verify query results CSV content is correct
- Include screenshots at each major step
- Define clear success criteria

### Step 13: Manual Testing
- Start the server and client applications
- Upload sample data
- Test downloading a table as CSV
- Open the CSV file in a text editor and spreadsheet application
- Verify data integrity and proper CSV formatting
- Execute various queries (simple and complex)
- Test downloading query results as CSV
- Test edge cases: empty results, special characters in data, very long column names
- Verify error handling for invalid table names

### Step 14: Run Validation Commands
- Execute all commands in the Validation Commands section to ensure zero regressions
- Fix any issues that arise
- Ensure all tests pass

## Testing Strategy

### Unit Tests
- Test `GET /api/export/table/{table_name}` endpoint:
  - Valid table name returns 200 with CSV content
  - Invalid table name returns 400 error
  - Non-existent table returns 404 error
  - CSV content has correct headers matching table schema
  - CSV content has correct number of rows matching table row count
  - Special characters in data are properly escaped

- Test `POST /api/export/query` endpoint:
  - Valid request returns 200 with CSV content
  - Empty results array returns valid CSV with headers only
  - Special characters (commas, quotes, newlines) are properly escaped
  - Unicode characters are handled correctly
  - Content-Disposition header has correct filename

- Test frontend functions:
  - `exportTableAsCSV` triggers download with correct filename
  - `exportQueryResultAsCSV` triggers download with correct filename
  - Error handling displays user-friendly messages
  - Blob cleanup happens properly

### Edge Cases
- Empty tables (0 rows) - should export CSV with headers only
- Tables with special characters in column names
- Data containing commas, quotes, newlines, and other CSV special characters
- Very large tables (performance testing)
- Query results with NULL values
- Query results with mixed data types in columns
- Table names with special characters (should be validated)
- Concurrent download requests
- Network errors during download
- Browser compatibility (Chrome, Firefox, Safari, Edge)

## Acceptance Criteria
- Two new API endpoints are created: `GET /api/export/table/{table_name}` and `POST /api/export/query`
- Download button appears directly to the left of × button in Available Tables section
- Download button appears directly to the left of Hide button in Query Results section
- Download buttons use appropriate download icons
- Clicking table download button downloads a CSV file named `{table_name}.csv`
- Clicking query result download button downloads a CSV file with descriptive name
- CSV files contain proper headers matching column names
- CSV files contain all data rows from the table/query
- CSV files can be opened in Excel and other spreadsheet applications without errors
- Special characters in data are properly escaped in CSV format
- NULL values are handled appropriately (empty cells)
- Error messages are displayed if export fails
- Security validation ensures only valid tables can be exported
- All existing tests continue to pass with zero regressions
- New E2E test validates the export functionality end-to-end
- All unit tests for the new endpoints pass
- No TypeScript compilation errors
- Frontend build completes successfully

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` to validate the CSV export functionality works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/test_export.py -v` - Run export-specific tests to validate CSV generation
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate no TypeScript errors
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- Use Python's built-in `csv` module for CSV generation to ensure proper escaping and formatting
- Use `io.StringIO` to build CSV content in memory before streaming
- Consider using `StreamingResponse` from FastAPI with an iterator for very large tables to avoid memory issues
- Use appropriate HTTP headers: `Content-Type: text/csv` and `Content-Disposition: attachment; filename="..."`
- Frontend should use `URL.createObjectURL()` and a temporary anchor element to trigger downloads
- Clean up blob URLs after download using `URL.revokeObjectURL()`
- Sanitize query snippets when creating filenames to avoid invalid filesystem characters
- Consider adding a loading state to download buttons while CSV is being generated
- Ensure UTF-8 encoding is used for CSV files to support international characters
- The CSV export should work with the existing SQL security infrastructure - no new security measures needed
- Future enhancement: Consider adding options for delimiter choice (comma, semicolon, tab) and encoding format
