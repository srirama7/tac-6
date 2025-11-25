# Feature: CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality for both database tables and query results. Users will be able to download data as CSV files directly from the UI with a single button click. This feature includes two new backend endpoints to generate and serve CSV files, and frontend download buttons strategically placed for easy access.

## User Story
As a user
I want to export tables and query results as CSV files
So that I can analyze data in external tools like Excel, Google Sheets, or other data analysis software

## Problem Statement
Currently, users can view data in the web interface but have no way to export it for use in external applications. This limits their ability to perform offline analysis, share data with colleagues, or use the data in other tools. Users need a simple, one-click solution to download both their uploaded tables and query results in a widely-compatible format.

## Solution Statement
Implement two new FastAPI endpoints (`/api/export/table/{table_name}` and `/api/export/results`) that generate CSV files from database tables and query results respectively. Add download buttons with appropriate icons in the UI: one next to the 'x' icon for each table in the Available Tables section, and one next to the 'Hide' button for query results. The solution will use Python's built-in `csv` module to ensure proper CSV formatting and handle edge cases like special characters and null values.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - Main FastAPI application where we'll add the two new export endpoints (`/api/export/table/{table_name}` and `/api/export/results`)
- `app/server/core/data_models.py` - Pydantic models for request/response validation. We'll add new models for export functionality
- `app/server/core/sql_security.py` - SQL security utilities for safe database operations. We'll use these to safely query tables for export
- `app/server/core/sql_processor.py` - SQL execution functions that we'll leverage for data retrieval
- `app/client/src/main.ts` - Main TypeScript file containing all UI logic. We'll add download button event handlers and CSV download functionality
- `app/client/src/types.d.ts` - TypeScript type definitions. We'll add types for export requests/responses
- `app/client/src/api/client.ts` - API client functions. We'll add new methods to call the export endpoints
- `app/client/src/style.css` - Styles for the application. We'll add styles for the download buttons
- `app/client/index.html` - HTML structure where we'll verify the placement of download buttons
- `README.md` - Project documentation to be updated with the new export feature
- `app/server/tests/test_sql_injection.py` - Security tests to ensure export endpoints are secure

### New Files
- `.claude/commands/e2e/test_csv_export.md` - E2E test file to validate CSV export functionality works correctly for both tables and query results
- `app/server/tests/test_export.py` - Unit tests for the export endpoints covering success cases, error handling, and edge cases

## Implementation Plan

### Phase 1: Foundation
First, establish the backend infrastructure for CSV generation. Create the core export functionality that will:
- Accept table names or query results as input
- Query the SQLite database safely using existing security utilities
- Convert database rows to CSV format with proper escaping
- Return CSV files with appropriate headers and content type
- Handle edge cases (empty tables, special characters, null values)

### Phase 2: Core Implementation
Implement the two export endpoints with full error handling and validation:
- `/api/export/table/{table_name}` - Export entire tables with validation that the table exists
- `/api/export/results` - Export query results passed from the frontend
- Add Pydantic models for request/response validation
- Implement comprehensive error handling for missing tables, empty data, and database errors

### Phase 3: Integration
Connect the backend to the frontend by:
- Adding TypeScript API client methods for both export endpoints
- Creating download buttons with appropriate icons in the UI
- Implementing click handlers that trigger CSV downloads
- Ensuring the download buttons are positioned correctly (next to 'x' for tables, next to 'Hide' for results)
- Adding CSS styles to make the buttons visually consistent with the existing UI

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Backend Export Utility Function
- Create a new utility function `convert_to_csv()` in `app/server/core/sql_processor.py`
- Function should accept a list of dictionaries (rows) and list of column names
- Use Python's `csv` module to generate properly formatted CSV content
- Handle edge cases: empty data, null values (convert to empty string), special characters (proper escaping)
- Return CSV content as a string
- Write unit tests in `app/server/tests/test_export.py` for the utility function

### Step 2: Add Export Data Models
- Add `TableExportRequest` model to `app/server/core/data_models.py` (empty model, table name comes from path)
- Add `ResultsExportRequest` model with fields: `sql: str`, `results: List[Dict[str, Any]]`, `columns: List[str]`
- Both endpoints will return CSV files directly with appropriate headers, no response model needed

### Step 3: Implement Table Export Endpoint
- Add `POST /api/export/table/{table_name}` endpoint to `app/server/server.py`
- Validate table name using `validate_identifier()` from `sql_security.py`
- Check table exists using `check_table_exists()` from `sql_security.py`
- Query all data from the table using `execute_query_safely()` with `SELECT * FROM {table}`
- Convert results to CSV using the utility function from Step 1
- Return CSV with headers: `Content-Type: text/csv`, `Content-Disposition: attachment; filename="{table_name}.csv"`
- Handle errors: table not found (404), invalid table name (400), database errors (500)
- Add logging for success and failure cases

### Step 4: Implement Results Export Endpoint
- Add `POST /api/export/results` endpoint to `app/server/server.py`
- Accept `ResultsExportRequest` in request body
- Validate that results and columns are not empty
- Convert results to CSV using the utility function from Step 1
- Generate filename based on timestamp: `query_results_{timestamp}.csv`
- Return CSV with appropriate headers
- Handle errors: empty results (400), conversion errors (500)
- Add logging for success and failure cases

### Step 5: Add Backend Tests
- Create comprehensive unit tests in `app/server/tests/test_export.py`
- Test table export: successful export, table not found, invalid table name, empty table
- Test results export: successful export, empty results, results with null values, special characters in data
- Test CSV formatting: proper headers, proper escaping, proper line endings
- Test security: SQL injection attempts through table names
- Run tests with `cd app/server && uv run pytest tests/test_export.py -v`

### Step 6: Add TypeScript Types
- Add export request/response types to `app/client/src/types.d.ts`
- Add `TableExportRequest` interface (empty)
- Add `ResultsExportRequest` interface with fields matching backend model
- Add types for download functionality

### Step 7: Add API Client Methods
- Add `exportTable(tableName: string)` method to `app/client/src/api/client.ts`
- Add `exportResults(request: ResultsExportRequest)` method to `app/client/src/api/client.ts`
- Both methods should handle the response as a blob
- Include error handling for failed requests
- Return blob URLs that can be used to trigger downloads

### Step 8: Add Download Utility Function
- Create a utility function `downloadCSV(blob: Blob, filename: string)` in `app/client/src/main.ts`
- Function should create a temporary anchor element
- Set the href to a blob URL
- Set the download attribute to the filename
- Programmatically click the anchor to trigger download
- Clean up the blob URL after download

### Step 9: Add Table Export Button UI
- In `displayTables()` function in `app/client/src/main.ts`, add a download button
- Position the download button directly to the left of the 'x' icon in the table header
- Use an appropriate download icon (📥 or use an SVG icon)
- Add class `download-table-button` for styling
- Set title attribute to "Download as CSV"
- Update the table header structure to accommodate three elements: table info, download button, remove button

### Step 10: Add Table Export Click Handler
- In `displayTables()` function, add click event listener to the download button
- Call `api.exportTable(table.name)` when clicked
- Show a loading state on the button during download
- Use `downloadCSV()` utility to trigger the download with filename `{table_name}.csv`
- Handle errors with user-friendly messages
- Show success feedback (optional)

### Step 11: Add Results Export Button UI
- In `displayResults()` function in `app/client/src/main.ts`, add a download button
- Position the download button directly to the left of the 'Hide' button in the results header
- Use the same download icon as the table export button
- Add class `download-results-button` for styling
- Set title attribute to "Download results as CSV"
- Store the current query results in a way that the download handler can access them

### Step 12: Add Results Export Click Handler
- Add click event listener to the results download button
- Store the current query response (sql, results, columns) in a module-level variable when `displayResults()` is called
- Call `api.exportResults()` with the stored data when download button is clicked
- Show a loading state on the button during download
- Use `downloadCSV()` utility to trigger download with filename `query_results_{timestamp}.csv`
- Handle errors with user-friendly messages
- Show success feedback (optional)

### Step 13: Add CSS Styles
- Add styles for `.download-table-button` and `.download-results-button` to `app/client/src/style.css`
- Style should match existing button styles (similar to `.remove-table-button`)
- Ensure proper sizing, spacing, and hover states
- Add transition effects for smooth interactions
- Ensure the download icon is clearly visible
- Make buttons accessible (proper contrast, focus states)

### Step 14: Create E2E Test File
- Create `.claude/commands/e2e/test_csv_export.md` based on the format in `.claude/commands/e2e/test_basic_query.md`
- Test should validate:
  - Upload sample data (users.json)
  - Verify download button appears next to 'x' icon for the table
  - Click the table download button
  - Verify CSV file downloads successfully
  - Execute a query and verify results appear
  - Verify download button appears next to 'Hide' button
  - Click the results download button
  - Verify CSV file downloads successfully
- Include screenshots at key steps
- Validate CSV file contents contain correct data

### Step 15: Update Documentation
- Update `README.md` to document the new export feature
- Add the new API endpoints to the "API Endpoints" section:
  - `POST /api/export/table/{table_name}` - Export table as CSV
  - `POST /api/export/results` - Export query results as CSV
- Update the "Features" section to mention CSV export capability
- Add usage instructions in the "Usage" section

### Step 16: Run Validation Commands
- Execute all commands listed in the "Validation Commands" section below
- Ensure all tests pass with zero regressions
- Verify the application builds successfully
- Run the E2E test to validate end-to-end functionality
- Fix any issues that arise

## Testing Strategy

### Unit Tests
- **CSV Utility Function Tests** (`test_export.py`):
  - Test conversion of simple data to CSV format
  - Test handling of null/None values (should convert to empty string)
  - Test special characters (commas, quotes, newlines) are properly escaped
  - Test empty data returns valid CSV with headers only
  - Test Unicode characters are preserved

- **Table Export Endpoint Tests** (`test_export.py`):
  - Test successful export of existing table
  - Test 404 error when table doesn't exist
  - Test 400 error for invalid table names (SQL injection attempts)
  - Test export of empty table (should return CSV with headers only)
  - Test CSV content type and disposition headers are correct
  - Test filename matches table name

- **Results Export Endpoint Tests** (`test_export.py`):
  - Test successful export of query results
  - Test 400 error for empty results
  - Test 400 error for missing columns
  - Test CSV content and headers are correct
  - Test filename includes timestamp
  - Test large result sets (performance)

- **Security Tests** (`test_sql_injection.py`):
  - Test SQL injection attempts through table name parameter
  - Test path traversal attempts in table names
  - Verify all table names are validated with `validate_identifier()`

### Edge Cases
- Empty tables with no data (should export CSV with headers only)
- Tables with single column
- Tables with many columns (50+)
- Data containing special CSV characters: commas, quotes, newlines, tabs
- Data with null/None values
- Data with Unicode/emoji characters
- Very large tables (10,000+ rows) - should still work but may be slow
- Query results with no rows (should export CSV with headers only)
- Simultaneous downloads (multiple users or multiple tabs)
- Invalid table names (spaces, special characters, SQL keywords)
- Non-existent tables
- Database connection errors during export

## Acceptance Criteria
- ✅ Two new backend endpoints are implemented and functional:
  - `POST /api/export/table/{table_name}` returns CSV file
  - `POST /api/export/results` returns CSV file
- ✅ Download button appears directly to the left of 'x' icon for each table in Available Tables section
- ✅ Download button appears directly to the left of 'Hide' button for query results
- ✅ Both download buttons use appropriate download icons
- ✅ Clicking table download button downloads a CSV file named `{table_name}.csv`
- ✅ Clicking results download button downloads a CSV file named `query_results_{timestamp}.csv`
- ✅ CSV files contain correct data with proper headers and formatting
- ✅ CSV files handle special characters (commas, quotes, newlines) correctly
- ✅ CSV files handle null values correctly (converted to empty strings)
- ✅ Export endpoints validate table names and reject SQL injection attempts
- ✅ Error messages are user-friendly when exports fail
- ✅ Loading states are shown during download operations
- ✅ All existing functionality continues to work (zero regressions)
- ✅ Unit tests pass for all export functionality
- ✅ E2E test validates the complete user workflow
- ✅ Frontend builds without errors
- ✅ Documentation is updated with new feature

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works end-to-end
- `cd app/server && uv run pytest tests/test_export.py -v` - Run new export tests to validate backend functionality
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Manually test the feature:
  - Start the application with `./scripts/start.sh`
  - Upload sample data (users.json)
  - Click the download button next to the 'x' icon for the users table
  - Verify CSV file downloads and contains correct data
  - Execute a query: "Show me all users"
  - Click the download button next to the 'Hide' button
  - Verify CSV file downloads and contains query results
  - Test with different tables and queries
  - Test error cases: try to download a non-existent table

## Notes

### Technical Decisions
- **CSV Module**: Using Python's built-in `csv` module instead of pandas to avoid adding unnecessary dependencies. The csv module provides proper escaping and formatting out of the box.
- **Endpoint Design**: Using POST instead of GET for the results export endpoint because the request body may be large (query results can contain many rows).
- **Filename Format**: Using timestamp in results filename to avoid conflicts when users download multiple query results. Format: `query_results_YYYYMMDD_HHMMSS.csv`.
- **Security**: Leveraging existing `validate_identifier()` and `check_table_exists()` functions to prevent SQL injection and ensure table exports are secure.
- **Download Mechanism**: Using the blob download approach (create blob URL, trigger anchor click, cleanup) which is the standard pattern for client-side downloads and works across all modern browsers.

### Future Enhancements
- Add support for other export formats (JSON, Excel, Parquet)
- Add option to export only selected columns
- Add option to limit number of rows in export
- Add progress indicator for large exports
- Add option to export with or without headers
- Consider streaming large exports instead of loading everything into memory
- Add export history/recent downloads feature
- Add batch export (export multiple tables at once)

### Dependencies
- No new dependencies required. Using only built-in Python `csv` module and standard JavaScript Blob/URL APIs.

### Performance Considerations
- For very large tables (100,000+ rows), exports may take several seconds and consume significant memory
- Consider adding a row limit or pagination for exports in future iterations
- The current implementation loads all data into memory before generating CSV - acceptable for small to medium datasets
- CSV generation is efficient with the built-in csv module

### Browser Compatibility
- Blob download approach works in all modern browsers (Chrome, Firefox, Safari, Edge)
- IE 11 is not supported (but likely not a concern for this modern tech stack)
