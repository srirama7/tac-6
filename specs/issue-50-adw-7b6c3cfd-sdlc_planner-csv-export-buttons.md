# Feature: CSV Export Buttons for Tables and Query Results

## Feature Description
Add one-click CSV export functionality for both database tables and query results. This feature will enable users to download their data as CSV files by clicking a download button. For tables in the "Available Tables" section, a download button will appear directly to the left of the 'x' (remove) icon. For query results, a download button will appear directly to the left of the 'Hide' button. The feature requires two new backend endpoints to generate CSV data: one for exporting entire tables and one for exporting query results.

## User Story
As a data analyst
I want to export tables and query results as CSV files
So that I can use the data in spreadsheet applications or share it with others

## Problem Statement
Currently, users can view data in the web interface but cannot export it for use in other applications. When users need to share insights, perform offline analysis, or backup their query results, they must manually copy data or take screenshots. This is inefficient and error-prone, especially for large datasets. There's no built-in way to persist query results or table data outside the application.

## Solution Statement
Implement downloadable CSV export functionality by adding two new FastAPI endpoints (`/api/export/table/{table_name}` and `/api/export/query-result`) that generate CSV files with proper headers and data formatting. On the client side, add download buttons with appropriate icons positioned next to existing controls. When clicked, these buttons will trigger API calls to fetch CSV data and initiate browser downloads. The implementation will follow existing security patterns to prevent SQL injection and ensure safe data export.

## Relevant Files
Use these files to implement the feature:

**Server-side files:**
- `app/server/server.py` - Add two new endpoints for CSV export (table export and query result export)
- `app/server/core/data_models.py` - Add new Pydantic models for export requests and responses
- `app/server/core/sql_processor.py` - Leverage existing safe query execution for table data retrieval
- `app/server/core/sql_security.py` - Use existing security validation for table names and identifiers

**Client-side files:**
- `app/client/src/main.ts` - Add download button UI elements and event handlers for tables and query results
- `app/client/src/api/client.ts` - Add API methods for CSV export endpoints
- `app/client/src/types.d.ts` - Add TypeScript interfaces for export request/response
- `app/client/src/style.css` - Add styles for download buttons

### New Files
- `.claude/commands/e2e/test_csv_export.md` - E2E test specification for CSV export functionality
- `app/server/core/csv_exporter.py` - New module for CSV generation logic with proper formatting and encoding
- `app/server/tests/core/test_csv_exporter.py` - Unit tests for CSV export functionality

## Implementation Plan
### Phase 1: Foundation
Create the core CSV export module with functions to convert database query results to properly formatted CSV data. Implement security validations using existing patterns to ensure only authorized table names are used. Set up data models for export requests and responses with proper type validation.

### Phase 2: Core Implementation
Implement two new FastAPI endpoints: one for exporting entire tables by name, and another for exporting specific query results. The table export endpoint will validate table names, fetch all rows, and return CSV data. The query result export endpoint will accept SQL query text (from a previous query) and return the results as CSV. Add comprehensive error handling for missing tables, invalid queries, and database errors.

### Phase 3: Integration
Build client-side download buttons with appropriate download icons, positioned exactly as specified in the requirements. Integrate API calls to fetch CSV data and trigger browser downloads with proper filenames (e.g., `{table_name}.csv` or `query_result_{timestamp}.csv`). Ensure the UI updates gracefully with loading states during export operations. Add user feedback for successful downloads and error messages for failures.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Create CSV Exporter Module
- Create `app/server/core/csv_exporter.py` with function `generate_csv_from_data(columns: List[str], rows: List[Dict[str, Any]]) -> str`
- Implement proper CSV formatting with quoted fields, escaped special characters, and UTF-8 encoding
- Handle edge cases: null values, special characters (commas, quotes, newlines), empty datasets
- Add helper function `sanitize_filename(name: str) -> str` to create safe CSV filenames
- Write comprehensive docstrings for all functions

### Add CSV Exporter Tests
- Create `app/server/tests/core/test_csv_exporter.py`
- Test CSV generation with various data types (integers, floats, strings, dates, nulls)
- Test edge cases: empty data, special characters, very long strings, unicode characters
- Test filename sanitization with invalid characters
- Ensure all tests pass with `uv run pytest tests/core/test_csv_exporter.py -v`

### Add Data Models for Export
- Add `TableExportRequest` model to `data_models.py` (empty, table name comes from path parameter)
- Add `QueryResultExportRequest` model with fields: `sql` (str), `columns` (List[str]), `results` (List[Dict[str, Any]])
- Add `CSVExportResponse` model with fields: `csv_data` (str), `filename` (str), `row_count` (int), `error` (Optional[str])
- Ensure all models have proper type annotations and validation

### Implement Table Export Endpoint
- Add `GET /api/export/table/{table_name}` endpoint in `server.py`
- Validate table name using `validate_identifier` from sql_security module
- Check table exists using `check_table_exists` function
- Fetch all table data using secure query execution: `SELECT * FROM {table}`
- Convert results to CSV using `generate_csv_from_data`
- Return CSV as plain text response with proper headers: `Content-Type: text/csv` and `Content-Disposition: attachment; filename="{table_name}.csv"`
- Add error handling for invalid table names, missing tables, and query failures
- Log all export operations for audit trail

### Implement Query Result Export Endpoint
- Add `POST /api/export/query-result` endpoint in `server.py`
- Accept `QueryResultExportRequest` in request body
- Validate that columns and results arrays are not empty
- Generate CSV from provided columns and results data
- Create filename with timestamp: `query_result_{timestamp}.csv`
- Return CSV as plain text response with proper headers
- Add error handling for invalid data formats and CSV generation failures
- Log all export operations

### Add Export API Client Methods
- Add `exportTable(tableName: string): Promise<Blob>` method to `api/client.ts`
- Add `exportQueryResult(sql: string, columns: string[], results: Record<string, any>[]): Promise<Blob>` method
- Both methods should fetch CSV data and return as Blob for browser download
- Add proper error handling with user-friendly error messages
- Add TypeScript interfaces matching the Pydantic models

### Add Download Buttons to Tables UI
- In `displayTables` function in `main.ts`, add a download button before the remove button
- Create download button with class `download-table-button` and appropriate download icon (e.g., `↓` or SVG download icon)
- Position button directly to the left of the 'x' icon in the table header
- Add click handler that calls `downloadTable(tableName)` function
- Implement `downloadTable` function that fetches CSV and triggers browser download using `URL.createObjectURL` and temporary anchor element
- Add loading state to button during download (disable button, show spinner)
- Show success/error feedback after download attempt

### Add Download Button to Query Results UI
- In `displayResults` function in `main.ts`, add a download button before the 'Hide' button
- Create download button with class `download-results-button` and download icon
- Position button directly to the left of the 'Hide' button in the results section header
- Store current query results data in a global variable or data attribute for export
- Add click handler that calls `downloadQueryResults()` function
- Implement `downloadQueryResults` function that fetches CSV from stored results and triggers download
- Add loading state to button during download
- Show success/error feedback after download attempt

### Style Download Buttons
- Add CSS for `.download-table-button` and `.download-results-button` in `style.css`
- Style buttons to match existing UI design (same size and style as remove/hide buttons)
- Add hover effects for better UX
- Add loading spinner animation for download in progress state
- Ensure buttons are visually distinct but cohesive with existing design
- Add appropriate spacing between download button and adjacent buttons

### Create E2E Test for CSV Export
- Create `.claude/commands/e2e/test_csv_export.md` following the pattern from `test_basic_query.md`
- Test scenario: Upload sample data, export table as CSV, verify download occurs
- Test scenario: Execute a query, export results as CSV, verify download occurs
- Verify download buttons appear in correct locations
- Verify CSV files contain expected data with proper headers
- Include screenshots of UI with download buttons visible
- Define clear success criteria for CSV export functionality

### Manual Testing and Validation
- Start the application and upload sample data (users.json, products.csv)
- Click download button on a table in "Available Tables" section
- Verify CSV file downloads with correct filename and contains all table data
- Execute a natural language query that returns results
- Click download button in results section
- Verify CSV file downloads with timestamp filename and contains query results
- Test edge cases: empty tables, special characters in data, very large datasets
- Test error scenarios: download fails, invalid table name, network errors
- Verify all existing functionality still works (no regressions)

### Run All Validation Commands
- Execute all validation commands listed in the Validation Commands section
- Fix any test failures or build errors
- Ensure zero regressions in existing functionality
- Verify CSV export works for all data types and edge cases

## Testing Strategy
### Unit Tests
- Test `generate_csv_from_data` with various data types and edge cases
- Test CSV formatting: proper quoting, escaping, delimiter handling
- Test filename sanitization with special characters and invalid names
- Test empty datasets and null value handling
- Test unicode and international character support
- Test very long strings and large datasets

### Integration Tests
- Test `/api/export/table/{table_name}` endpoint with valid and invalid table names
- Test table export with various data types and sizes
- Test `/api/export/query-result` endpoint with different query results
- Test CSV download triggers correct browser download behavior
- Test concurrent export requests
- Test export operations with existing security validations intact

### Edge Cases
- Empty tables or query results (0 rows)
- Tables with special characters in column names or data
- Very large datasets (10,000+ rows)
- Data with embedded commas, quotes, and newlines
- Unicode and international characters (Chinese, Arabic, emoji)
- Null values and empty strings
- Tables with no columns (edge case, should error gracefully)
- Invalid table names or SQL injection attempts
- Network failures during download
- Browser download restrictions or blocked popups

## Acceptance Criteria
- Download button appears directly to the left of 'x' icon for each table in "Available Tables" section
- Download button appears directly to the left of 'Hide' button in query results section
- Clicking table download button exports entire table as CSV file
- CSV file for tables is named `{table_name}.csv`
- Clicking results download button exports current query results as CSV file
- CSV file for query results is named `query_result_{timestamp}.csv` with readable timestamp
- CSV files have proper headers with column names
- CSV data is properly formatted with quoted fields and escaped special characters
- Download buttons use appropriate download icon (not placeholder text)
- Download buttons have loading states during export operations
- User receives feedback on successful download or error messages on failure
- CSV export respects existing SQL injection protections
- All existing functionality continues to work without regression
- CSV files can be opened in Excel, Google Sheets, and other spreadsheet applications

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/core/test_csv_exporter.py -v` - Run specific CSV exporter tests
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Ensure SQL injection protection still works
- `cd app/client && bun tsc --noEmit` - Run TypeScript type checking to ensure no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works end-to-end

## Notes
- Use Python's built-in `csv` module for robust CSV generation instead of manual string concatenation
- Consider adding Content-Length header for better download progress indication
- Future enhancement: Add option to customize CSV delimiter (comma, semicolon, tab) for international users
- Future enhancement: Add Excel-specific export format (.xlsx) for better formatting support
- Future enhancement: Add export options (select specific columns, filter rows, custom filename)
- The CSV export should handle large datasets efficiently without timing out (consider streaming for very large exports)
- Consider implementing export limits (e.g., max 100,000 rows) to prevent server overload
- UTF-8 with BOM encoding may be needed for proper Excel compatibility with special characters
- Add export operation logging for analytics and debugging purposes
- Consider adding a download history or export queue feature in future iterations
