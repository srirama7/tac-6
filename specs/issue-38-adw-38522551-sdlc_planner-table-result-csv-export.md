# Feature: One-Click CSV Export for Tables and Query Results

## Feature Description
This feature adds one-click CSV export functionality to the Natural Language SQL Interface application, allowing users to export database tables and query results as CSV files. Two new download buttons will be strategically placed in the UI: one next to the table removal button for exporting entire tables, and one next to the "Hide" button for exporting query results. The feature includes two new backend endpoints that handle CSV generation and ensure data is properly formatted and secured.

## User Story
As a data analyst or user of the Natural Language SQL Interface
I want to export tables and query results as CSV files with a single click
So that I can use the data in other tools like Excel, Google Sheets, or data analysis software without manually copying data

## Problem Statement
Currently, users can view tables and query results in the web interface but have no way to export this data for use in external applications. This limitation forces users to manually copy data or recreate queries in other tools, which is time-consuming and error-prone. Users need a quick, reliable way to download their data in a universally-compatible CSV format for further analysis, reporting, or sharing.

## Solution Statement
Implement two new FastAPI endpoints (`/api/export/table/{table_name}` and `/api/export/results`) that generate CSV files from database tables and query results. Add download buttons with appropriate icons in the frontend UI that trigger these exports. The solution will use Python's built-in `csv` module for efficient CSV generation, implement proper security validation using the existing `sql_security` module, and return CSV data with appropriate headers to trigger browser downloads.

## Relevant Files
Use these files to implement the feature:

- **app/server/server.py** (lines 1-280)
  - Main FastAPI application file where new export endpoints will be added
  - Contains existing endpoints like `/api/upload`, `/api/query`, `/api/schema`, `/api/table/{table_name}`
  - Shows patterns for error handling, logging, and response models
  - Demonstrates use of sql_security module for table name validation

- **app/server/core/data_models.py** (lines 1-82)
  - Defines all Pydantic models for request/response objects
  - Need to add new models: `ExportResultsRequest` for exporting query results
  - Shows existing patterns for optional error fields and typed responses

- **app/server/core/sql_security.py**
  - Contains security functions: `validate_identifier()`, `check_table_exists()`, `execute_query_safely()`
  - Will be used to validate table names before export
  - Ensures SQL injection protection for all database operations

- **app/server/core/sql_processor.py** (lines 1-117)
  - Contains `get_database_schema()` function that safely queries table information
  - Shows patterns for safe query execution and error handling
  - Demonstrates how to interact with sqlite3 database

- **app/client/src/main.ts** (lines 1-423)
  - Main TypeScript file containing all UI logic and event handlers
  - Contains `displayTables()` function (lines 189-258) where table download button will be added
  - Contains `displayResults()` function (lines 119-154) where results download button will be added
  - Shows patterns for API calls, DOM manipulation, and button event handlers

- **app/client/src/api/client.ts** (lines 1-79)
  - API client with all backend communication methods
  - Need to add two new methods: `exportTable()` and `exportResults()`
  - Shows patterns for apiRequest wrapper and error handling

- **app/client/src/types.d.ts** (lines 1-80)
  - TypeScript type definitions matching backend Pydantic models
  - Need to add `ExportResultsRequest` interface to match backend model

- **app/client/index.html** (lines 1-99)
  - HTML structure showing results section (lines 29-36) and tables section (lines 38-44)
  - Provides context for where download buttons will be placed

- **app/client/src/style.css**
  - Contains existing button styles and UI component styles
  - Will need to add styles for download buttons to match existing design

- **app/server/tests/test_sql_injection.py**
  - Shows testing patterns for the application
  - Will use similar patterns for testing new export endpoints

### New Files

- **app/server/tests/test_export_endpoints.py**
  - New test file for export functionality
  - Will test both `/api/export/table/{table_name}` and `/api/export/results` endpoints
  - Will validate CSV generation, security checks, and error handling

- **.claude/commands/e2e/test_csv_export.md**
  - New E2E test specification for CSV export feature
  - Will validate that download buttons appear correctly in UI
  - Will test clicking download buttons triggers CSV downloads
  - Will verify CSV file contents are correct

## Implementation Plan

### Phase 1: Foundation
First, establish the backend infrastructure for CSV export functionality. Create new Pydantic models for the export results request, and implement a reusable CSV generation utility function that can convert database rows into properly formatted CSV data. Update the sql_security module if needed to ensure table name validation works correctly for export operations. This foundation ensures all subsequent work has a solid, type-safe base.

### Phase 2: Core Implementation
Implement the two new FastAPI endpoints for exporting tables and query results. The `/api/export/table/{table_name}` endpoint will validate the table name, query all rows from the specified table, and generate a CSV file. The `/api/export/results` endpoint will accept a list of rows and column names from the frontend, generate a CSV file from that data, and return it with appropriate headers. Both endpoints will include comprehensive error handling, logging, and security validation.

### Phase 3: Integration
Update the frontend to add download buttons in the appropriate locations with proper icons (using standard download icon: ⬇ or 📥). Wire up the API client methods to call the new backend endpoints. Implement the download logic that triggers the browser's native download mechanism when users click the buttons. Add visual feedback (loading states, success/error messages) to ensure users know their export is processing. Finally, create comprehensive tests including unit tests for the endpoints and E2E tests to validate the complete user flow.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Backend Data Models
- Open `app/server/core/data_models.py`
- Add new Pydantic model `ExportResultsRequest` with fields:
  - `results: List[Dict[str, Any]]` - the data rows to export
  - `columns: List[str]` - column names for CSV header
  - `filename: str` - desired filename for the download

### Step 2: Implement CSV Generation Utility
- Create new function `generate_csv_from_data()` in `app/server/core/sql_processor.py`
- Function should accept rows (list of dicts) and columns (list of strings)
- Use Python's `csv` module with `csv.DictWriter` to generate CSV content
- Return CSV string with proper newline handling
- Add comprehensive error handling

### Step 3: Create Table Export Endpoint
- Open `app/server/server.py`
- Add new endpoint `@app.get("/api/export/table/{table_name}")`
- Validate table_name using `validate_identifier()` from sql_security
- Check table exists using `check_table_exists()`
- Query all rows from the table using `execute_query_safely()`
- Generate CSV using the utility function from Step 2
- Return CSV as Response with headers:
  - `Content-Type: text/csv`
  - `Content-Disposition: attachment; filename="{table_name}.csv"`
- Add logging and error handling following existing patterns

### Step 4: Create Results Export Endpoint
- In `app/server/server.py`, add endpoint `@app.post("/api/export/results")`
- Accept `ExportResultsRequest` model as request body
- Validate that results and columns are not empty
- Generate CSV using the utility function from Step 2
- Return CSV as Response with headers:
  - `Content-Type: text/csv`
  - `Content-Disposition: attachment; filename="{request.filename}.csv"`
- Add logging and error handling following existing patterns

### Step 5: Add Backend Unit Tests
- Create `app/server/tests/test_export_endpoints.py`
- Test table export endpoint:
  - Test successful export with valid table name
  - Test error handling for non-existent table
  - Test security validation for invalid table names
  - Verify CSV format and content
- Test results export endpoint:
  - Test successful export with valid data
  - Test error handling for empty data
  - Test CSV header and row formatting
  - Verify filename handling
- Run tests with `cd app/server && uv run pytest tests/test_export_endpoints.py -v`

### Step 6: Add Frontend Type Definitions
- Open `app/client/src/types.d.ts`
- Add `ExportResultsRequest` interface matching the backend Pydantic model

### Step 7: Add API Client Methods
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string)` method that calls `/api/export/table/{table_name}`
- Add `exportResults(request: ExportResultsRequest)` method that calls `/api/export/results`
- Both methods should handle blob responses for file downloads
- Add helper function `downloadFile(blob: Blob, filename: string)` to trigger browser download

### Step 8: Add Download Button to Table Items
- Open `app/client/src/main.ts`
- In the `displayTables()` function (around line 199-257), locate where the table header is created
- Add a download button element before the remove button (×)
- Use download icon: '⬇' or '↓'
- Add CSS class `download-table-button`
- Set click handler to call `exportTableData(table.name)`
- Create new function `exportTableData(tableName: string)` that:
  - Calls `api.exportTable(tableName)`
  - Handles the blob response
  - Triggers browser download
  - Shows success/error messages

### Step 9: Add Download Button to Query Results
- In `app/client/src/main.ts`, locate `displayResults()` function (line 119-154)
- In the results header section (where "Hide" button is), add a download button before the "Hide" button
- Use download icon: '⬇' or '↓'
- Add CSS class `download-results-button`
- Store the current query results and columns in variables accessible to the download function
- Set click handler to call `exportResultsData()`
- Create new function `exportResultsData()` that:
  - Gets current results and columns from the last query
  - Generates appropriate filename based on timestamp
  - Calls `api.exportResults()` with the data
  - Handles the blob response
  - Triggers browser download
  - Shows success/error messages

### Step 10: Add CSS Styles for Download Buttons
- Open `app/client/src/style.css`
- Add styles for `.download-table-button` and `.download-results-button`
- Style them consistently with existing buttons (like `.remove-table-button`)
- Ensure proper sizing, spacing, and hover effects
- Make sure icons are clearly visible and appropriately sized

### Step 11: Create E2E Test Specification
- Create `.claude/commands/e2e/test_csv_export.md`
- Read `.claude/commands/test_e2e.md` and `.claude/commands/e2e/test_basic_query.md` for reference
- Define test steps:
  1. Navigate to application
  2. Upload sample data (users.json)
  3. Verify table appears with download button
  4. Click table download button
  5. Verify CSV file downloads with correct name
  6. Execute a query
  7. Verify results appear with download button
  8. Click results download button
  9. Verify CSV file downloads
  10. Take screenshots at each major step
- Define success criteria:
  - Download buttons appear in correct locations
  - CSV files download successfully
  - CSV content matches table/query data
  - Buttons have appropriate icons and styling

### Step 12: Run All Validation Commands
- Execute all validation commands listed in the "Validation Commands" section below
- Ensure all tests pass with zero errors
- Fix any issues that arise before considering the feature complete

## Testing Strategy

### Unit Tests
- **Backend endpoint tests** (`test_export_endpoints.py`):
  - Test CSV generation with various data types (strings, numbers, nulls, special characters)
  - Test table export with empty tables
  - Test results export with empty result sets
  - Test security validation (SQL injection attempts, invalid table names)
  - Test error responses and status codes
  - Verify CSV headers are set correctly
  - Verify CSV content format and encoding (UTF-8)

- **Frontend download functionality**:
  - Manual testing of download trigger mechanism
  - Verify blob handling and filename generation
  - Test error states when API calls fail

### Edge Cases
- Empty tables (should generate CSV with headers only)
- Empty query results (should generate CSV with headers only)
- Tables with special characters in column names (quotes, commas, newlines)
- Data containing CSV special characters (quotes, commas, newlines) - should be properly escaped
- Very large tables (test performance and memory usage)
- Tables with mixed data types (ensure proper string conversion)
- Non-existent table names (should return 404 error)
- Invalid table names with SQL injection attempts (should return 400 error)
- Unicode characters in data (should be properly encoded in UTF-8)
- Column names with spaces or special characters
- Null values in data (should export as empty strings)
- Concurrent export requests (ensure thread safety)

## Acceptance Criteria
- Users can click a download button next to any table in the "Available Tables" section to export that table as a CSV file
- Users can click a download button next to the "Hide" button in the "Query Results" section to export query results as a CSV file
- Download buttons use an appropriate download icon (⬇ or 📥)
- CSV files are properly formatted with headers as the first row and data in subsequent rows
- CSV special characters (quotes, commas, newlines) are properly escaped following CSV standards
- File downloads use descriptive filenames (e.g., `users.csv` for tables, `query_results_2025-11-25.csv` for results)
- Both export endpoints validate inputs and reject invalid table names with appropriate error messages
- Security validation prevents SQL injection attempts through table names
- Empty tables and empty result sets generate valid CSV files with headers only
- All existing functionality remains working with zero regressions
- All existing tests continue to pass
- New unit tests achieve >90% code coverage for new export endpoints
- E2E test validates the complete user flow from button click to file download
- Backend logs export operations for monitoring and debugging
- Error messages are user-friendly and informative

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

1. Read `.claude/commands/test_e2e.md` for instructions on running E2E tests
2. Read and execute `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works end-to-end
3. `cd app/server && uv run pytest tests/test_export_endpoints.py -v` - Run new export endpoint tests
4. `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
5. `cd app/client && bun run build` - Validate frontend builds successfully without errors
6. `cd app/client && bun tsc --noEmit` - Validate TypeScript compilation with no type errors

## Notes

### Implementation Considerations
- Use Python's built-in `csv` module rather than pandas to avoid adding a new heavy dependency
- The `csv.DictWriter` class handles CSV escaping automatically (quotes, commas, newlines)
- For the results export endpoint, we need to pass data from frontend to backend because the backend doesn't store query results - each query executes and returns immediately
- CSV files should use UTF-8 encoding to support international characters
- Consider using `io.StringIO` for in-memory CSV generation rather than writing to disk
- FastAPI's `Response` class with custom headers is the best way to return file downloads

### Security Notes
- All table names must be validated using the existing `validate_identifier()` function
- Use `check_table_exists()` before attempting to export to prevent information leakage
- The results export endpoint doesn't need table validation since it works with data passed from frontend
- Do not log actual data contents to avoid leaking sensitive information
- Consider rate limiting in future iterations if export abuse becomes an issue

### UX Considerations
- Download buttons should be visually consistent with existing UI elements
- Use clear, recognizable icons for downloads (⬇ is universally understood)
- Position buttons logically: table export near table management, results export near results controls
- Show loading states while CSV is being generated for large datasets
- Display success confirmation after download initiates
- Handle errors gracefully with user-friendly messages (e.g., "Failed to export table" rather than raw error messages)

### Future Enhancements
- Add export format options (JSON, Excel, Parquet)
- Allow filtering/selecting specific columns before export
- Add progress indicators for large exports
- Implement server-side pagination for very large tables
- Add export history/audit log
- Support compressed exports (zip/gzip) for large datasets
- Add ability to schedule recurring exports
- Email export results for very large datasets
