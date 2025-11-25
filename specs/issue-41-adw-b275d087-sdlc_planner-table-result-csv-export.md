# Feature: One-Click CSV Export for Tables and Query Results

## Feature Description
This feature adds one-click CSV export functionality to the Natural Language SQL Interface application, allowing users to export database tables and query results as CSV files with a single click. Two new download buttons will be strategically placed in the UI: one directly to the left of the 'x' icon for exporting entire tables from the Available Tables section, and one directly to the left of the 'Hide' button for exporting query results. The feature includes two new backend endpoints (`/api/export/table/{table_name}` and `/api/export/query`) that handle CSV generation with proper formatting, security validation, and browser-friendly download headers.

## User Story
As a data analyst or user of the Natural Language SQL Interface
I want to export tables and query results as CSV files with a single click
So that I can use the data in other tools like Excel, Google Sheets, or data analysis software without manually copying data

## Problem Statement
Currently, users can view tables and query results in the web interface but have no way to export this data for use in external applications. This limitation forces users to manually copy data or recreate queries in other tools, which is time-consuming and error-prone. Users need a quick, reliable way to download their data in a universally-compatible CSV format for further analysis, reporting, or sharing.

## Solution Statement
Implement two new FastAPI endpoints (`/api/export/table/{table_name}` and `/api/export/query`) that generate CSV files from database tables and query results. Add download buttons with appropriate download icons directly to the left of existing buttons (the 'x' icon for tables and 'Hide' button for results) in the frontend UI that trigger these exports. The solution will use Python's built-in `csv` module for efficient CSV generation, implement proper security validation using the existing `sql_security` module, and return CSV data with appropriate HTTP headers to trigger browser downloads.

## Relevant Files
Use these files to implement the feature:

- **README.md** - Contains project overview, setup instructions, API endpoints documentation, and project structure
- **app/server/server.py** (lines 1-280) - Main FastAPI application file where new export endpoints will be added; contains existing endpoints and patterns for error handling, logging, and response models
- **app/server/core/data_models.py** (lines 1-82) - Defines all Pydantic models for request/response objects; need to add new model for query export request
- **app/server/core/sql_security.py** - Contains security functions for SQL injection protection: `validate_identifier()`, `check_table_exists()`, `execute_query_safely()`
- **app/server/core/sql_processor.py** (lines 1-117) - Contains `get_database_schema()` and safe query execution patterns
- **app/client/src/main.ts** (lines 1-423) - Main TypeScript file containing UI logic; contains `displayTables()` (lines 189-258) and `displayResults()` (lines 119-154) functions where download buttons will be added
- **app/client/src/api/client.ts** (lines 1-79) - API client with backend communication methods; need to add export methods
- **app/client/src/types.d.ts** (lines 1-80) - TypeScript type definitions matching backend Pydantic models
- **app/client/index.html** (lines 1-99) - HTML structure for the application
- **app/client/src/style.css** - CSS styles for buttons and UI components
- **app/server/tests/test_sql_injection.py** - Shows testing patterns for security validation
- **.claude/commands/test_e2e.md** - E2E test runner instructions and format
- **.claude/commands/e2e/test_basic_query.md** - Example E2E test file showing test structure

### New Files

- **app/server/tests/test_csv_export.py** - New test file for CSV export endpoints; will test `/api/export/table/{table_name}` and `/api/export/query` endpoints with validation for CSV generation, security checks, special characters, edge cases, and error handling
- **.claude/commands/e2e/test_csv_export.md** - New E2E test specification validating download buttons appear correctly, clicking download buttons triggers CSV downloads, and CSV file contents are correct

## Implementation Plan

### Phase 1: Foundation
First, establish the backend infrastructure for CSV export functionality. Create new Pydantic models for the query export request that will contain the results data, columns, and SQL query from the frontend. Implement two new FastAPI endpoints that generate CSV files: one for exporting entire tables by querying the database, and one for exporting query results by converting frontend-provided data. Ensure all database operations use the existing `sql_security` module for proper validation and SQL injection protection. This foundation ensures type-safe, secure CSV export operations.

### Phase 2: Core Implementation
Implement the CSV generation logic using Python's built-in `csv` module with proper handling of special characters (commas, quotes, newlines), NULL values, and unicode characters. Add comprehensive error handling for missing tables, invalid table names, empty results, and malformed requests. Configure HTTP response headers with `Content-Type: text/csv` and `Content-Disposition: attachment` to trigger browser downloads with descriptive filenames (table name for table exports, timestamped filename for query results). Add structured logging for all export operations to track usage and debug issues.

### Phase 3: Integration
Update the frontend to add download buttons with appropriate download icons (📥 or ⬇) positioned directly to the left of the 'x' icon in the Available Tables section and directly to the left of the 'Hide' button in the Query Results section. Create API client methods that fetch CSV data from the backend endpoints and trigger browser downloads using blob URLs or direct anchor element clicks. Add visual feedback (loading states, success/error messages) to inform users of export progress. Create comprehensive test suites including unit tests for both endpoints covering security, edge cases, and error conditions, plus E2E tests validating the complete user flow from button click to downloaded CSV file.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Backend Data Models
- Open `app/server/core/data_models.py`
- Add new Pydantic model `QueryExportRequest` with fields:
  - `sql: str` - the SQL query that generated the results (for logging/debugging)
  - `columns: List[str]` - column names for CSV header
  - `results: List[Dict[str, Any]]` - the data rows to export
- Ensure proper imports (`List`, `Dict`, `Any` from `typing`)
- Add docstring explaining the model's purpose for query result exports

### Step 2: Implement Table Export Endpoint
- Open `app/server/server.py`
- Add new GET endpoint `/api/export/table/{table_name}` that:
  - Validates table name using `validate_identifier()` from sql_security module
  - Checks table exists using `check_table_exists()`
  - Queries all rows from the table using `execute_query_safely()`
  - Generates CSV using Python's `csv.writer` with proper escaping
  - Returns CSV with headers: `Content-Type: text/csv; charset=utf-8` and `Content-Disposition: attachment; filename="{table_name}.csv"`
  - Handles errors: 400 for invalid table names, 404 for non-existent tables, 500 for other errors
  - Adds structured logging for success and failure cases
- Import required modules: `csv`, `io.StringIO` for in-memory CSV generation
- Import `Response` from `fastapi` for custom response handling

### Step 3: Implement Query Export Endpoint
- In `app/server/server.py`
- Add new POST endpoint `/api/export/query` that:
  - Accepts `QueryExportRequest` model as request body
  - Validates columns list is not empty
  - Validates results list is not empty (return 400 if empty)
  - Generates CSV from provided results and columns using `csv.DictWriter`
  - Handles missing keys in result dictionaries (treat as NULL/empty string)
  - Returns CSV with headers: `Content-Type: text/csv; charset=utf-8` and `Content-Disposition: attachment; filename="query_results_{timestamp}.csv"` where timestamp is `YYYYMMDD_HHMMSS` format
  - Handles errors: 400 for invalid requests, 500 for generation errors
  - Adds structured logging for all operations
- Use `datetime.now().strftime('%Y%m%d_%H%M%S')` for timestamp generation
- Ensure proper CSV escaping for special characters (commas, quotes, newlines)

### Step 4: Add Frontend Type Definitions
- Open `app/client/src/types.d.ts`
- Add new interface `QueryExportRequest` matching the backend Pydantic model:
  - `sql: string`
  - `columns: string[]`
  - `results: Record<string, any>[]`
- Place the interface near other request/response type definitions

### Step 5: Add API Client Methods
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string)` method that:
  - Calls GET `/export/table/{tableName}`
  - Returns blob response (not JSON)
  - Handles errors appropriately
- Add `exportQuery(request: QueryExportRequest)` method that:
  - Calls POST `/export/query` with JSON body
  - Returns blob response (not JSON)
  - Handles errors appropriately
- Both methods should use `fetch` directly instead of `apiRequest` wrapper since they return blobs not JSON

### Step 6: Add Download Button to Available Tables Section
- Open `app/client/src/main.ts`
- In the `displayTables()` function (around line 189-258):
  - After creating the table header elements and before the remove button (line 223-227)
  - Create a download button element: `const downloadButton = document.createElement('button')`
  - Add class: `downloadButton.className = 'download-table-button'`
  - Add icon: `downloadButton.innerHTML = '⬇'` or `'📥'`
  - Add title: `downloadButton.title = 'Download table as CSV'`
  - Add click handler: `downloadButton.onclick = () => downloadTable(table.name)`
  - Insert download button into tableHeader before the remove button
- Create new function `downloadTable(tableName: string)` that:
  - Calls `api.exportTable(tableName)`
  - Creates a blob URL from the response
  - Creates a temporary anchor element
  - Sets `href` to blob URL and `download` attribute to filename
  - Triggers click to download
  - Revokes blob URL after download
  - Shows success message or error message using existing `displayError()` pattern
  - Handles loading states

### Step 7: Add Download Button to Query Results Section
- In `app/client/src/main.ts`
- In the `displayResults()` function (around line 119-154):
  - Store the query results, columns, and SQL in variables accessible to download handler
  - In the results header section (around line 149-153), before the toggle button:
    - Create a download button element: `const downloadButton = document.createElement('button')`
    - Add class: `downloadButton.className = 'download-results-button'`
    - Add icon: `downloadButton.innerHTML = '⬇'` or `'📥'`
    - Add title: `downloadButton.title = 'Download results as CSV'`
    - Add click handler that calls `downloadQueryResults(response.results, response.columns, response.sql)`
    - Insert download button before toggle button
- Create new function `downloadQueryResults(results: Record<string, any>[], columns: string[], sql: string)` that:
  - Calls `api.exportQuery({ sql, columns, results })`
  - Creates a blob URL from the response
  - Triggers download similar to `downloadTable()`
  - Shows success/error messages
  - Handles loading states

### Step 8: Add CSS Styles for Download Buttons
- Open `app/client/src/style.css`
- Add styles for `.download-table-button` and `.download-results-button`:
  - Match existing button styles (look at `.remove-table-button` and `.toggle-button`)
  - Ensure proper sizing, spacing, and hover effects
  - Use consistent color scheme with rest of UI
  - Add cursor pointer on hover
  - Add subtle hover effect (opacity or background color change)

### Step 9: Create E2E Test Specification
- Create new file `.claude/commands/e2e/test_csv_export.md`
- Follow the format from `test_basic_query.md` and `test_complex_query.md`
- Include test steps:
  1. Navigate to application URL
  2. Upload sample data (users.json)
  3. Verify download button appears next to 'x' icon in Available Tables
  4. Click table download button
  5. Verify CSV file downloads with correct filename
  6. Execute a query to show results
  7. Verify download button appears next to 'Hide' button in Query Results
  8. Click query results download button
  9. Verify CSV file downloads with timestamp in filename
  10. Take screenshots at key steps
- Include success criteria validating both download buttons work correctly

### Step 10: Create Comprehensive Unit Tests
- Create new file `app/server/tests/test_csv_export.py`
- Import required modules: `pytest`, `sqlite3`, `tempfile`, `TestClient` from fastapi
- Create fixtures for test database with sample data (users table with various data types)
- Create test class `TestTableExport` with tests:
  - `test_export_valid_table()` - verify CSV format, headers, data rows
  - `test_export_nonexistent_table()` - verify 404 response
  - `test_export_invalid_table_name()` - verify 400 for SQL injection attempts
  - `test_export_table_with_special_characters()` - verify proper CSV escaping
  - `test_export_empty_table()` - verify CSV with only headers
- Create test class `TestQueryExport` with tests:
  - `test_export_valid_query_results()` - verify CSV format and content
  - `test_export_empty_results()` - verify 400 response
  - `test_export_without_columns()` - verify 400 response
  - `test_export_query_with_special_characters()` - verify proper escaping
  - `test_export_query_filename_has_timestamp()` - verify filename format
  - `test_export_query_with_null_values()` - verify NULL handling
- Create test class `TestExportSecurity` with tests:
  - `test_table_export_validates_identifiers()` - verify sql_security integration
  - `test_table_export_blocks_sql_keywords()` - verify SQL keyword blocking
  - `test_query_export_does_not_execute_sql()` - verify query endpoint only uses provided results
- Create test class `TestExportEdgeCases` with tests:
  - `test_export_table_with_unicode_characters()` - verify UTF-8 encoding
  - `test_export_query_with_missing_column_values()` - verify partial data handling

### Step 11: Run Validation Commands
- Execute all commands in the Validation Commands section below
- Verify zero test failures
- Verify zero type errors
- Verify successful frontend build
- Execute E2E test and verify success
- Fix any issues that arise

## Testing Strategy

### Unit Tests
- **Backend endpoint tests**: Validate both `/api/export/table/{table_name}` and `/api/export/query` endpoints return proper CSV format with correct headers
- **CSV generation tests**: Verify special characters (commas, quotes, newlines) are properly escaped in CSV output
- **Security tests**: Validate SQL injection attempts are blocked, table names are validated, and malicious inputs are rejected
- **Error handling tests**: Test responses for non-existent tables (404), invalid table names (400), empty results (400), and server errors (500)
- **Edge case tests**: Test unicode characters, NULL values, missing column values, empty tables, and large datasets

### Edge Cases
- Table names with SQL injection attempts (e.g., `"users'; DROP TABLE users; --"`)
- Non-existent tables (should return 404 with clear error message)
- Empty tables (should return CSV with only header row)
- Empty query results (should return 400 with helpful error message)
- Results with special characters in data: commas, quotes, newlines, tabs
- Results with NULL values or missing keys in result dictionaries
- Results with unicode characters (Japanese, emoji, accented characters)
- Very large tables or result sets (performance testing)
- Column names with special characters
- Malformed requests (missing required fields, wrong data types)
- Query export endpoint receives malicious SQL (should not execute it)

## Acceptance Criteria
- Two new backend endpoints are implemented: GET `/api/export/table/{table_name}` and POST `/api/export/query`
- Table export endpoint validates table names using sql_security module and blocks SQL injection attempts
- Both endpoints return valid CSV format with proper Content-Type and Content-Disposition headers
- CSV files handle special characters (commas, quotes, newlines) with proper escaping
- CSV files represent NULL values as empty strings
- Download button appears directly to the left of 'x' icon in Available Tables section
- Download button appears directly to the left of 'Hide' button in Query Results section
- Both download buttons use appropriate download icon (📥 or ⬇)
- Clicking table download button downloads CSV file named `{table_name}.csv`
- Clicking query results download button downloads CSV file named `query_results_{timestamp}.csv`
- Download buttons show visual feedback (loading state) during export
- Error messages are displayed if download fails
- All unit tests pass with 100% success rate
- E2E test validates complete user flow from button click to downloaded file
- No regressions in existing functionality (all existing tests still pass)
- Frontend builds without TypeScript errors
- Code follows existing patterns and conventions in the codebase

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_csv_export.md` to validate this functionality works.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Implementation Details
- Use Python's built-in `csv` module for CSV generation (no additional dependencies needed)
- Use `csv.DictWriter` for query results export (handles missing keys gracefully)
- Use `csv.writer` for table export (simpler for database rows)
- Use `io.StringIO` for in-memory CSV generation before returning as response
- Ensure UTF-8 encoding in CSV responses for proper unicode support
- Use appropriate HTTP status codes: 200 (success), 400 (bad request), 404 (not found), 500 (server error)

### Security Considerations
- All table names must be validated using `validate_identifier()` from sql_security module
- Table existence must be checked using `check_table_exists()` before querying
- SQL queries for tables must use `execute_query_safely()` with identifier parameters
- Query export endpoint should NOT execute the provided SQL (only use provided results data)
- Implement rate limiting considerations for large exports in future iterations

### User Experience
- Download buttons should match existing UI design (colors, sizing, spacing)
- Show loading indicators during export operations
- Display clear error messages if export fails
- Use descriptive filenames: table name for table exports, timestamped for query results
- Ensure browser triggers download automatically (no popup blockers)
- Consider adding success notification after download completes

### Future Enhancements
- Add export format options (Excel, JSON, Parquet)
- Add column selection for table exports (export only specific columns)
- Add filtering options for table exports (export only rows matching criteria)
- Add progress indicators for large exports
- Add export history/recent downloads panel
- Add ability to schedule automated exports
- Add export to cloud storage (S3, Google Drive, Dropbox)
- Add data validation and schema export with CSV

### Testing Notes
- The test file `app/server/tests/test_csv_export.py` already exists and appears to have comprehensive tests
- Review and run existing tests first before adding new ones
- Ensure new tests follow existing patterns in `test_csv_export.py`
- E2E test should use Playwright browser automation via MCP server
- Take screenshots at each major step for visual validation
- Test on both development (localhost:5173) and production builds
