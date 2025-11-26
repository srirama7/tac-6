# Feature: CSV Export for Tables and Query Results

## Feature Description
This feature adds one-click CSV export functionality to both the available tables section and query results section of the Natural Language SQL Interface application. Users will be able to download their data as CSV files with a single click, making it easy to export data for external analysis, reporting, or data sharing purposes.

The feature includes:
- Export button for each available table (placed directly to the left of the 'x' remove button)
- Export button for query results (placed directly to the left of the 'Hide' button)
- Two new FastAPI endpoints to support these exports
- Proper CSV formatting with UTF-8 encoding
- Appropriate download icon usage

## User Story
As a user of the Natural Language SQL Interface
I want to export tables and query results as CSV files with one click
So that I can use the data in external tools like Excel, Google Sheets, or other data analysis platforms without manually copying and pasting

## Problem Statement
Currently, users can view data in the application but have no way to export it for use in external tools. This limits the utility of the application as users often need to share data, perform additional analysis in spreadsheet applications, or integrate the data with other workflows. Users would need to manually copy and paste data, which is error-prone and time-consuming for large datasets.

## Solution Statement
Implement two CSV export endpoints on the backend that generate CSV files from table data and query results. Add download buttons in the frontend UI that trigger these endpoints and initiate browser downloads. The implementation will use Python's built-in CSV module for reliable formatting, handle special characters and edge cases properly, and provide a seamless user experience with appropriate visual feedback.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - Main FastAPI application where new export endpoints will be added (lines 241-276 show the delete_table endpoint pattern to follow)
- `app/server/core/data_models.py` - Contains Pydantic models for request/response validation; new models for export requests/responses will be added here
- `app/server/core/sql_security.py` - Provides SQL security functions like `validate_identifier()` and `execute_query_safely()` that must be used in the new endpoints
- `app/server/core/sql_processor.py` - Contains `execute_sql_safely()` function for executing queries safely; will be used by the export endpoints
- `app/client/src/main.ts` - Frontend TypeScript code that handles UI interactions; contains `displayTables()` function (lines 189-258) where the table export button will be added, and `displayResults()` function (lines 119-154) where the query results export button will be added
- `app/client/src/api/client.ts` - API client configuration; new export API methods will be added here following the existing pattern (lines 36-79)
- `app/client/src/types.d.ts` - TypeScript type definitions that must match Pydantic models exactly; new export types will be added
- `app/client/index.html` - HTML structure showing the UI layout; helps understand where buttons should be placed (lines 29-36 for results section, lines 38-44 for tables section)
- `app/client/src/style.css` - CSS styles for the application; may need styles for the new download buttons
- `app/server/tests/test_sql_injection.py` - Security tests to ensure export endpoints don't have SQL injection vulnerabilities; new tests will be added

### New Files

- `.claude/commands/e2e/test_csv_export.md` - End-to-end test file to validate the CSV export functionality works correctly with user interactions
- `app/server/tests/test_export_endpoints.py` - Unit tests for the new CSV export endpoints

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure to support CSV exports:
1. Add new Pydantic models for export requests and responses in `data_models.py`
2. Implement utility function to convert database rows to CSV format with proper escaping
3. Add security validation to ensure export operations are safe

### Phase 2: Core Implementation
Build the two export endpoints and frontend integration:
1. Implement `/api/export/table/{table_name}` endpoint that exports an entire table as CSV
2. Implement `/api/export/query` endpoint that exports query results as CSV
3. Add export API methods to the frontend API client
4. Add download buttons to the UI with appropriate icons

### Phase 3: Integration
Connect all pieces and ensure seamless user experience:
1. Wire up frontend buttons to API calls
2. Handle download triggers in the browser
3. Add error handling and user feedback
4. Create E2E tests to validate the complete user flow
5. Run full validation suite to ensure zero regressions

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Backend Data Models and Types
- Add `ExportTableRequest` model to `app/server/core/data_models.py` (no fields needed, table name comes from path)
- Add `ExportQueryRequest` model with fields for SQL query, columns, and results data
- Add corresponding TypeScript interfaces to `app/client/src/types.d.ts` to match the Pydantic models exactly

### 2. Backend CSV Export Utility Function
- Create a utility function in `app/server/core/sql_processor.py` called `convert_to_csv()` that:
  - Takes a list of column names and a list of row dictionaries
  - Returns a CSV string with proper UTF-8 encoding
  - Uses Python's `csv` module with `csv.DictWriter`
  - Handles special characters, quotes, and commas correctly
  - Includes column headers as the first row

### 3. Backend Table Export Endpoint
- Add `GET /api/export/table/{table_name}` endpoint in `app/server/server.py` that:
  - Validates the table name using `validate_identifier()` from `sql_security`
  - Checks if the table exists using `check_table_exists()`
  - Queries all data from the table using `execute_query_safely()`
  - Converts results to CSV using the utility function
  - Returns a streaming response with `Content-Type: text/csv` and `Content-Disposition: attachment; filename="{table_name}.csv"`
  - Includes proper error handling with HTTPException for invalid tables
  - Logs success/failure with the logging pattern used in other endpoints

### 4. Backend Query Results Export Endpoint
- Add `POST /api/export/query` endpoint in `app/server/server.py` that:
  - Accepts a request body with columns and results data
  - Validates the input data is not empty
  - Converts the provided results to CSV using the utility function
  - Returns a streaming response with `Content-Type: text/csv` and `Content-Disposition: attachment; filename="query_results.csv"`
  - Includes proper error handling
  - Logs success/failure

### 5. Backend Security Tests
- Add tests to `app/server/tests/test_sql_injection.py` that verify:
  - Table export endpoint validates table names and rejects SQL injection attempts
  - Table export endpoint rejects invalid identifiers
  - Table names with special characters are properly escaped
- Create `app/server/tests/test_export_endpoints.py` with tests for:
  - Successful table export with valid data
  - Table export with non-existent table returns 404
  - Query results export with valid data
  - Query results export with empty data
  - CSV formatting is correct (headers, escaping, encoding)
- Run `cd app/server && uv run pytest` to ensure all tests pass

### 6. Frontend API Client Methods
- Add `exportTable(tableName: string): Promise<Blob>` method to `app/client/src/api/client.ts` that:
  - Calls `GET /api/export/table/{tableName}`
  - Returns the response as a Blob for download
  - Uses fetch API with proper error handling
- Add `exportQueryResults(columns: string[], results: Record<string, any>[]): Promise<Blob>` method that:
  - Calls `POST /api/export/query` with the data
  - Returns the response as a Blob for download
  - Includes proper Content-Type headers

### 7. Frontend Download Helper Function
- Add a utility function `downloadFile(blob: Blob, filename: string)` in `app/client/src/main.ts` that:
  - Creates a temporary URL for the blob
  - Creates a temporary anchor element
  - Triggers the download
  - Cleans up the temporary URL
- This will be reused for both table and query exports

### 8. Frontend Table Export Button
- Modify the `displayTables()` function in `app/client/src/main.ts` (around line 189-258) to:
  - Add a download button directly to the left of the remove button (× icon)
  - Use an appropriate download icon (📥 or SVG)
  - Add CSS class `download-table-button` for styling
  - Set `title="Download as CSV"` for tooltip
  - Add click handler that calls `exportTable(table.name)` then `downloadFile(blob, \`${table.name}.csv\`)`
  - Show visual feedback during download (disable button, show loading state)
  - Handle errors gracefully with user-visible error messages

### 9. Frontend Query Results Export Button
- Modify the `displayResults()` function in `app/client/src/main.ts` (around line 119-154) to:
  - Add a download button in the `.results-header` div directly to the left of the "Hide" button
  - Use the same download icon for consistency
  - Add CSS class `download-results-button` for styling
  - Set `title="Download as CSV"` for tooltip
  - Add click handler that calls `exportQueryResults(response.columns, response.results)` then `downloadFile(blob, 'query_results.csv')`
  - Store the current query response data in a variable accessible to the button handler
  - Show visual feedback during download
  - Handle errors gracefully

### 10. Frontend Styling for Download Buttons
- Add CSS styles to `app/client/src/style.css` for:
  - `.download-table-button` - should match the style of `.remove-table-button` but with different color (green/blue instead of red)
  - `.download-results-button` - should match the style of `.toggle-button`
  - Hover states for both buttons
  - Disabled states for loading feedback
  - Ensure buttons are properly aligned and spaced

### 11. Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand the E2E test format
- Read `.claude/commands/e2e/test_basic_query.md` to see an example
- Create `.claude/commands/e2e/test_csv_export.md` that validates:
  - User can upload sample data
  - User can click download button on a table and a CSV file is downloaded
  - User can execute a query
  - User can click download button on query results and a CSV file is downloaded
  - Take screenshots at each major step
  - Verify the downloaded CSV files contain the expected data
- Include specific test steps with verification points
- Define success criteria clearly

### 12. Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Fix any issues that arise
- Ensure all tests pass before considering the feature complete

## Testing Strategy

### Unit Tests
1. **CSV Conversion Function Tests** (`test_export_endpoints.py`):
   - Test converting empty results to CSV
   - Test converting single row to CSV
   - Test converting multiple rows to CSV
   - Test special characters are properly escaped (commas, quotes, newlines)
   - Test UTF-8 encoding works correctly
   - Test column headers are included

2. **Table Export Endpoint Tests** (`test_export_endpoints.py`):
   - Test successful export of existing table
   - Test 404 error for non-existent table
   - Test 400 error for invalid table name
   - Test proper CSV Content-Type header
   - Test proper Content-Disposition with filename
   - Test actual CSV content is correctly formatted

3. **Query Export Endpoint Tests** (`test_export_endpoints.py`):
   - Test successful export with valid data
   - Test empty results handling
   - Test large datasets (performance)
   - Test proper headers and content type

4. **Security Tests** (`test_sql_injection.py`):
   - Test SQL injection attempts in table name are blocked
   - Test path traversal attempts are blocked
   - Test special characters in table names are handled safely

### Edge Cases
- Empty tables (0 rows) - should export just headers
- Tables with NULL values - should export as empty strings
- Tables with special characters in data (commas, quotes, newlines) - should be properly escaped
- Very large tables (10,000+ rows) - should not cause timeout or memory issues
- Column names with special characters - should be properly quoted
- Query results with no columns - should fail gracefully
- Network errors during download - should show error message to user
- Multiple rapid clicks on download button - should not trigger multiple downloads
- Unicode characters in data - should be preserved with UTF-8 encoding

## Acceptance Criteria
1. A download button appears directly to the left of the 'x' icon for each table in the Available Tables section
2. A download button appears directly to the left of the 'Hide' button in the Query Results section
3. Clicking the table download button exports all data from that table as a CSV file with the table name as the filename
4. Clicking the query results download button exports the current query results as a CSV file named "query_results.csv"
5. CSV files are properly formatted with:
   - Column headers in the first row
   - UTF-8 encoding
   - Proper escaping of special characters (commas, quotes, newlines)
   - One row per data record
6. Both endpoints use proper SQL security validation (validate_identifier, execute_query_safely)
7. Download buttons show appropriate visual feedback during the export process
8. Errors are handled gracefully with user-friendly error messages
9. All existing tests continue to pass
10. New unit tests and E2E tests validate the feature works correctly
11. The feature works in both Chrome and Firefox browsers
12. Large datasets (1000+ rows) export successfully without timeouts

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new `.claude/commands/e2e/test_csv_export.md` test file to validate this functionality works end-to-end
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/test_export_endpoints.py -v` - Run new export endpoint tests specifically
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Run security tests to ensure export endpoints are secure
- `cd app/client && bun run tsc --noEmit` - Run TypeScript compiler to validate frontend code has no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature works in production mode

## Notes
- **Download Icon**: Use the download emoji 📥 or a proper SVG icon if available in the project. Check existing icon usage patterns in the codebase first.
- **CSV Library**: Use Python's built-in `csv` module with `csv.DictWriter` for reliable CSV generation. Set `quoting=csv.QUOTE_MINIMAL` to minimize unnecessary quoting.
- **Streaming Response**: Use FastAPI's `StreamingResponse` with `media_type='text/csv'` for the export endpoints. This is efficient for large datasets.
- **CORS**: The existing CORS configuration should work since we're adding endpoints under `/api/`
- **File Naming**: Table exports use `{table_name}.csv`, query exports use `query_results.csv`. Consider adding timestamp to query results filename for multiple downloads: `query_results_{timestamp}.csv`
- **Error Messages**: Follow the existing error message patterns in the codebase - use logger.error() for backend, displayError() for frontend
- **Button Positioning**: Use CSS flexbox/grid to ensure proper alignment. The remove button and download button should be in a button group within the table header.
- **Performance**: For very large tables (100K+ rows), consider adding a warning or limit. Most databases and browsers handle up to 100K rows in CSV without issues.
- **Future Enhancement**: Consider adding format selection (CSV, JSON, Excel) in the future. The current implementation focuses on CSV as specified.
- **Security**: NEVER concatenate user input into SQL queries. Always use the `sql_security` module functions for validation and execution.
