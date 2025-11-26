# Feature: CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality to the Natural Language SQL Interface application, enabling users to download both entire table data and query result sets as CSV files. This feature includes two new backend endpoints for generating CSV exports and frontend download buttons with appropriate icons positioned next to existing UI controls. The implementation follows best practices for data export, including proper CSV encoding, content-type headers, and filename generation.

## User Story
As a data analyst
I want to export table data and query results as CSV files with a single click
So that I can use the data in other tools like Excel, data analysis scripts, or share results with colleagues without manual copying

## Problem Statement
Currently, users can view data in the web interface but have no way to export it for use in other applications. This limits the usefulness of query results and prevents users from performing offline analysis or sharing data efficiently. Users must manually copy-paste data, which is error-prone and time-consuming for large datasets.

## Solution Statement
Implement comprehensive CSV export functionality by:
1. Creating two new FastAPI endpoints: `/api/table/{table_name}/export` for full table exports and `/api/query/export` for query result exports
2. Adding download buttons to the frontend UI positioned directly to the left of existing controls (× icon for tables, Hide button for query results)
3. Using appropriate download icons with accessible styling
4. Generating proper CSV files with UTF-8 encoding and correct content-type headers
5. Creating descriptive filenames with timestamps for easy identification
6. Including comprehensive tests and E2E validation to ensure the feature works correctly

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - Main FastAPI server where new CSV export endpoints will be added (lines 241-277 show existing table deletion endpoint pattern to follow)
- `app/server/core/data_models.py` - Contains Pydantic models; may need new models for export requests/responses
- `app/server/core/sql_processor.py` - Contains `execute_sql_safely()` and `get_database_schema()` functions needed for data retrieval
- `app/server/core/sql_security.py` - Contains security validation functions like `validate_identifier()` and `check_table_exists()` to be used in export endpoints
- `app/client/src/main.ts` - Frontend logic where download buttons and export handlers will be added (lines 188-258 show table display function, lines 119-154 show results display function)
- `app/client/src/api/client.ts` - API client where new export methods will be added following existing patterns
- `app/client/src/types.d.ts` - TypeScript type definitions where export-related types will be added
- `app/client/src/style.css` - Styles for the download buttons to ensure consistent appearance
- `app/client/index.html` - HTML structure showing where buttons will be placed (lines 28-36 for results section, lines 38-44 for tables section)
- `app/server/tests/test_sql_injection.py` - Security tests to ensure export endpoints are secure

### New Files
- `.claude/commands/e2e/test_csv_export.md` - E2E test file to validate CSV export functionality works correctly
- `app/server/tests/test_csv_export.py` - Unit tests for the CSV export endpoints

## Implementation Plan
### Phase 1: Foundation
Create the backend infrastructure for CSV generation including new endpoints, data retrieval logic, and proper CSV formatting with headers. This establishes the core functionality that the frontend will consume.

### Phase 2: Core Implementation
Implement the frontend download buttons with proper icons and positioning, add API client methods, and wire up the download handlers to trigger CSV exports from the backend endpoints.

### Phase 3: Integration
Add comprehensive testing including unit tests for endpoints, security validation, E2E tests for user workflows, and ensure the feature integrates seamlessly with existing table management and query execution features.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add CSV Export Data Models
- Open `app/server/core/data_models.py`
- Add `QueryExportRequest` model with fields: `sql` (str), `filename` (Optional[str])
- These models will structure the API request/response for CSV exports
- Follow existing patterns in the file for consistency

### Step 2: Create Table Export Endpoint
- Open `app/server/server.py`
- Create new endpoint `@app.get("/api/table/{table_name}/export")`
- Use `validate_identifier()` to validate table name for security
- Use `check_table_exists()` to verify table exists
- Use `execute_query_safely()` to retrieve all table data with `SELECT * FROM {table}`
- Convert results to CSV format using Python's `csv` module with proper UTF-8 encoding
- Return CSV as StreamingResponse with headers: `Content-Type: text/csv; charset=utf-8`, `Content-Disposition: attachment; filename="{table_name}_{timestamp}.csv"`
- Add comprehensive error handling and logging following existing patterns
- Use `allow_ddl=False` for safe query execution

### Step 3: Create Query Results Export Endpoint
- In `app/server/server.py`
- Create new endpoint `@app.post("/api/query/export")`
- Accept `QueryExportRequest` model as request body
- Validate that SQL query is safe (no DDL operations)
- Use `execute_sql_safely()` to execute the provided SQL query
- Convert results to CSV format using Python's `csv` module
- Return CSV as StreamingResponse with headers similar to table export
- Generate filename from timestamp if not provided: `query_results_{timestamp}.csv`
- Add error handling and logging

### Step 4: Add CSV Export Unit Tests
- Create `app/server/tests/test_csv_export.py`
- Test table export endpoint with valid table name
- Test table export endpoint with invalid/non-existent table name
- Test query export endpoint with valid SQL
- Test query export endpoint with invalid/malicious SQL
- Test CSV format correctness (headers, encoding, line breaks)
- Test error responses and status codes
- Test security validation is enforced
- Run tests: `cd app/server && uv run pytest tests/test_csv_export.py -v`

### Step 5: Add Export Methods to API Client
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string): Promise<Blob>` method
- Add `exportQueryResults(sql: string, filename?: string): Promise<Blob>` method
- Both methods should use fetch with appropriate headers
- Handle blob responses for file download
- Follow existing API client patterns

### Step 6: Add Download Icon and Styles
- Open `app/client/src/style.css`
- Add styles for `.download-button` class
- Style should match existing button patterns but with download icon (⬇ or 📥)
- Ensure button is properly sized and positioned
- Add hover states for better UX
- Ensure accessibility with proper contrast

### Step 7: Add Table Export Download Button
- Open `app/client/src/main.ts`
- Locate `displayTables()` function (around line 188-258)
- In the table header section (around line 203-230), add download button
- Position download button directly to the left of the remove (×) button
- Add click handler that calls `api.exportTable(table.name)`
- Handle blob response and trigger browser download using URL.createObjectURL
- Add error handling and user feedback for download failures
- Use download icon: ⬇ or 📥

### Step 8: Add Query Results Export Download Button
- In `app/client/src/main.ts`
- Locate `displayResults()` function (around line 119-154)
- In the results header section (around line 130-135), add download button
- Position download button directly to the left of the Hide button
- Store the current SQL and results in a way that can be accessed by the download handler
- Add click handler that calls `api.exportQueryResults(currentSql, filename)`
- Generate filename from query or timestamp
- Handle blob response and trigger browser download
- Add error handling and user feedback

### Step 9: Add TypeScript Type Definitions
- Open `app/client/src/types.d.ts`
- Add type definitions for export-related types if needed
- Add `ExportRequest` interface if required
- Ensure all new API methods have proper types

### Step 10: Create E2E Test File
- Create `.claude/commands/e2e/test_csv_export.md`
- Follow the pattern from `.claude/commands/e2e/test_basic_query.md`
- Include test steps:
  1. Load sample data (users table)
  2. Verify table download button appears next to × icon
  3. Click table download button
  4. Verify CSV file downloads with correct filename format
  5. Execute a query and verify results appear
  6. Verify results download button appears next to Hide button
  7. Click results download button
  8. Verify query results CSV downloads
  9. Validate both CSV files contain correct data and headers
- Include success criteria for all download operations
- Take screenshots at key steps

### Step 11: Integration Testing
- Start server and client: `./scripts/start.sh`
- Load sample data through UI
- Test table export button for multiple tables
- Verify CSV files download with correct format and data
- Execute various queries and test results export
- Verify filenames are descriptive and include timestamps
- Test error cases (export non-existent table)
- Verify security: cannot export with SQL injection attempts
- Ensure no regressions in existing functionality

### Step 12: Run Validation Commands
- Execute all validation commands below to ensure feature works correctly with zero regressions
- Review E2E test results and screenshots
- Verify all tests pass before marking feature complete

## Testing Strategy
### Unit Tests
- Test CSV export endpoints return correct content-type headers
- Test CSV format is valid with proper headers and UTF-8 encoding
- Test filename generation includes timestamps
- Test table export retrieves all table data
- Test query export executes provided SQL correctly
- Test error handling for invalid table names
- Test error handling for malicious SQL queries
- Test security validation is enforced on all inputs
- Test large dataset exports (performance testing)

### Integration Tests
- Test complete user flow: upload data → export table
- Test complete user flow: execute query → export results
- Test downloaded CSV files can be opened in Excel/other tools
- Test concurrent export requests
- Test exports work with different data types (strings, numbers, dates, nulls)

### Edge Cases
- Exporting empty tables
- Exporting tables with special characters in column names
- Exporting tables with very long column values
- Exporting query results with no rows
- Exporting tables with null values
- Exporting tables with Unicode characters
- Attempting to export non-existent tables
- Attempting to export with SQL injection in table name
- Very large table exports (memory/streaming considerations)
- Concurrent export requests from multiple users

## Acceptance Criteria
- Two new endpoints exist: `/api/table/{table_name}/export` and `/api/query/export`
- Download button appears to the left of × icon for each table in Available Tables section
- Download button appears to the left of Hide button in Query Results section
- Download buttons use appropriate download icon (⬇ or 📥)
- Clicking table download button downloads CSV file with all table data
- Clicking query results download button downloads CSV file with current query results
- CSV files have descriptive filenames with timestamps (e.g., `users_2025-11-26_143022.csv`)
- CSV files are properly formatted with UTF-8 encoding
- CSV files include column headers as first row
- CSV files handle special characters and null values correctly
- Export endpoints validate table names and SQL queries for security
- Error messages are clear when exports fail
- All existing functionality continues to work without regression
- E2E test validates the complete export workflow
- All unit tests pass
- No SQL injection vulnerabilities in export endpoints

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/test_csv_export.py -v` - Run CSV export unit tests
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Ensure export endpoints are secure
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript compiler to check for type errors
- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_csv_export.md` test file to validate this functionality works

## Notes
- Use Python's built-in `csv` module for CSV generation - no additional dependencies needed
- Use `StreamingResponse` from FastAPI for efficient large file downloads
- Generate timestamps using `datetime.now().strftime('%Y-%m-%d_%H%M%S')` for filename uniqueness
- Follow CSV RFC 4180 standard for maximum compatibility
- Use UTF-8 encoding with BOM for Excel compatibility
- Consider memory usage for large exports - stream data if needed
- Reuse existing security validation functions from `sql_security.py`
- Download icons options: ⬇ (U+2B07) or 📥 (U+1F4E5) or use SVG icon
- Use `URL.createObjectURL()` and `URL.revokeObjectURL()` in frontend for blob downloads
- Add proper ARIA labels to download buttons for accessibility
- Test CSV exports in Excel, Google Sheets, and text editors to ensure compatibility
- Consider adding a loading state to download buttons during export
- Future enhancement: Add option to export as other formats (JSON, Excel)
