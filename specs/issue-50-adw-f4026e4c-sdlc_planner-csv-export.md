# Feature: CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality to the Natural Language SQL Interface application, allowing users to download both entire tables and query results as CSV files. This feature enhances data portability and enables users to work with their data in external tools like Excel, Google Sheets, or other analytics platforms.

## User Story
As a user of the Natural Language SQL Interface
I want to export tables and query results as CSV files with a single click
So that I can analyze, share, or manipulate the data in external applications

## Problem Statement
Users currently can view data in the web interface but have no way to export it for use in other tools. This limits the application's utility for data analysis workflows that require integration with spreadsheet software, reporting tools, or other data processing systems.

## Solution Statement
Implement two new backend API endpoints (`/api/export/table/{table_name}` and `/api/export/results`) that generate CSV files from table data and query results. Add download buttons with appropriate icons in the UI: one next to the 'x' icon for each table in the Available Tables section, and one next to the 'Hide' button in the Query Results section. These buttons will trigger CSV downloads directly in the browser.

## Relevant Files
Use these files to implement the feature:

### Backend Files
- `app/server/server.py` - Main FastAPI application where the new export endpoints will be added
  - Contains existing endpoints pattern to follow
  - Handles CORS and error handling consistently
  - Uses proper logging format

- `app/server/core/sql_security.py` - SQL security module for safe query execution
  - Provides `validate_identifier()` for table name validation
  - Provides `check_table_exists()` to verify tables exist
  - Provides `execute_query_safely()` for secure database operations

- `app/server/core/data_models.py` - Pydantic models for request/response validation
  - Define new request/response models for export endpoints
  - Follow existing patterns for error handling

### Frontend Files
- `app/client/index.html` - HTML structure with table and results sections
  - Contains table-header and results-header sections where download buttons will be added
  - Uses consistent button styling classes

- `app/client/src/main.ts` - Main TypeScript application logic
  - Contains `displayTables()` function that renders the Available Tables section
  - Contains `displayResults()` function that renders Query Results section
  - Handles all UI interactions and API calls

- `app/client/src/api/client.ts` - API client for backend communication
  - Add new methods for export endpoints
  - Follow existing pattern for API requests

- `app/client/src/types.d.ts` - TypeScript type definitions
  - Add types for new export request/response models

- `app/client/src/style.css` - Application styles
  - Add styles for download buttons to match existing UI patterns

### Test Files
- `app/server/tests/core/test_csv_exporter.py` - Unit tests for CSV export functionality
  - Test CSV generation from table data
  - Test CSV generation from query results
  - Test error handling and edge cases

### New Files

#### E2E Test File
- `.claude/commands/e2e/test_csv_export.md` - E2E test to validate CSV export functionality
  - Upload sample data
  - Execute a query
  - Test downloading table export
  - Test downloading query result export
  - Verify CSV file contents and formatting

#### Backend Core Module
- `app/server/core/csv_exporter.py` - CSV export utility module
  - Function to convert table data to CSV format
  - Function to convert query results to CSV format
  - Handle UTF-8 encoding for proper character support
  - Implement proper CSV escaping for special characters

## Implementation Plan

### Phase 1: Foundation
Create the core CSV export utility module that will be used by both export endpoints. This module will handle converting database results into properly formatted CSV data with UTF-8 encoding, proper escaping of special characters (commas, quotes, newlines), and correct header generation. Follow Python's `csv` module best practices.

### Phase 2: Core Implementation
Implement the two backend API endpoints following the existing FastAPI patterns in `server.py`. Add frontend download buttons with appropriate icons (use download icon `↓` or similar) positioned as specified. Implement client-side CSV download handling using browser's built-in download mechanism (Blob + temporary anchor element). Update TypeScript types and API client methods.

### Phase 3: Integration
Add comprehensive unit tests to validate CSV generation with various data types (strings, numbers, nulls, special characters). Create E2E test to validate the complete user workflow. Ensure security measures are in place (table name validation, SQL injection protection). Test with the existing sample data files (users.json, products.csv, events.jsonl).

## Step by Step Tasks

### Task 1: Create CSV Exporter Utility Module
- Create `app/server/core/csv_exporter.py` with two main functions:
  - `export_table_to_csv(table_name: str) -> str` - Exports entire table as CSV string
  - `export_query_results_to_csv(results: List[Dict[str, Any]], columns: List[str]) -> str` - Exports query results as CSV string
- Use Python's `csv` module with `csv.DictWriter` for proper escaping
- Set UTF-8 encoding with BOM (`utf-8-sig`) for Excel compatibility
- Handle edge cases: empty results, null values, special characters in data
- Include proper error handling and logging

### Task 2: Create Unit Tests for CSV Exporter
- Create `app/server/tests/core/test_csv_exporter.py`
- Test CSV generation from table data with various data types
- Test CSV generation from query results
- Test handling of special characters (commas, quotes, newlines)
- Test handling of null values
- Test empty results
- Test UTF-8 encoding with special characters (emoji, accents)
- Run tests with `cd app/server && uv run pytest tests/core/test_csv_exporter.py -v`

### Task 3: Add Backend Export Endpoints
- In `app/server/server.py`, add two new endpoints:
  - `GET /api/export/table/{table_name}` - Export entire table as CSV
  - `POST /api/export/results` - Export query results as CSV
- Use `Response` with `media_type="text/csv"` and appropriate `Content-Disposition` header
- Validate table names using `validate_identifier()` from `sql_security.py`
- Check table existence using `check_table_exists()` from `sql_security.py`
- Use `execute_query_safely()` for database queries
- Add proper error handling and logging following existing patterns
- Set filename in `Content-Disposition` header as `attachment; filename="{table_name}.csv"`

### Task 4: Add Pydantic Models for Export
- In `app/server/core/data_models.py`, add:
  - `ExportResultsRequest` model with fields: `results: List[Dict[str, Any]]` and `columns: List[str]`
- Follow existing model patterns with proper type hints and Field descriptions

### Task 5: Add TypeScript Types
- In `app/client/src/types.d.ts`, add:
  - `ExportResultsRequest` interface matching the backend model

### Task 6: Add API Client Methods
- In `app/client/src/api/client.ts`, add two methods:
  - `exportTable(tableName: string): Promise<Blob>` - Returns CSV Blob
  - `exportResults(request: ExportResultsRequest): Promise<Blob>` - Returns CSV Blob
- Use `fetch()` with proper headers
- Return response as Blob for file download

### Task 7: Add Download Utility Function
- In `app/client/src/main.ts`, create helper function:
  - `downloadCSV(blob: Blob, filename: string)` - Triggers browser download
  - Create temporary anchor element with Blob URL
  - Trigger click to download
  - Clean up Blob URL after download

### Task 8: Add Table Export Button to UI
- In `app/client/src/main.ts`, modify `displayTables()` function:
  - Add download button in `table-header` section, positioned directly to the left of the remove (×) button
  - Use download icon (↓ or ⬇) with proper styling
  - Add click handler to call `api.exportTable(table.name)` and then `downloadCSV()`
  - Handle errors with user-friendly messages
  - Add loading state during download

### Task 9: Add Query Results Export Button to UI
- In `app/client/src/main.ts`, modify `displayResults()` function:
  - Add download button in `results-header` section, positioned directly to the left of the 'Hide' button
  - Use download icon (↓ or ⬇) with proper styling
  - Add click handler to call `api.exportResults()` with current results and columns
  - Handle errors with user-friendly messages
  - Add loading state during download
  - Store current query results in a closure or global variable so export button has access to them

### Task 10: Add CSS Styles for Download Buttons
- In `app/client/src/style.css`, add styles for:
  - `.download-button` class with consistent styling matching existing buttons
  - Hover and active states
  - Loading state indicator
  - Icon sizing and spacing
  - Position the button appropriately in the header layout

### Task 11: Create E2E Test File
- Create `.claude/commands/e2e/test_csv_export.md` following the pattern from `test_basic_query.md`
- Test steps should include:
  1. Navigate to application
  2. Upload sample data (users.json)
  3. Verify table appears in Available Tables
  4. Click download button on table
  5. Verify browser download is triggered (check for download element creation)
  6. Execute a natural language query
  7. Verify query results appear
  8. Click download button on query results
  9. Verify browser download is triggered
  10. Take screenshots at key steps
- Include success criteria for both table and result exports
- Document expected CSV format and content

### Task 12: Run All Validation Commands
- Execute all validation commands listed in the "Validation Commands" section below
- Fix any issues that arise
- Ensure zero test failures and zero regressions
- Verify E2E test passes completely

## Testing Strategy

### Unit Tests
- Test CSV generation with various SQLite data types (TEXT, INTEGER, REAL)
- Test CSV escaping for special characters: commas, quotes, newlines, tabs
- Test null value handling (should output empty string)
- Test empty results (should output headers only)
- Test UTF-8 encoding with emoji and accented characters
- Test table export with non-existent table (should return 404)
- Test table name validation (should reject invalid identifiers)
- Test query results export with empty results
- Test large datasets (1000+ rows) for performance

### Edge Cases
- Table name contains special characters (already prevented by validation)
- Column names contain special characters (commas, quotes)
- Data values contain CSV-sensitive characters (commas, quotes, newlines)
- Data contains null/None values
- Data contains Unicode characters (emoji, non-ASCII)
- Empty table (0 rows)
- Query returns no results
- Query returns single row
- Query returns single column
- Very long text fields (> 1000 characters)

## Acceptance Criteria
- Two new backend endpoints are implemented: `/api/export/table/{table_name}` and `/api/export/results`
- Download button appears directly to the left of 'x' icon for each table in Available Tables section
- Download button appears directly to the left of 'Hide' button in Query Results section
- Both download buttons use appropriate download icon
- Clicking table download button downloads entire table as CSV
- Clicking results download button downloads current query results as CSV
- CSV files are properly formatted with headers and UTF-8 encoding
- CSV files handle special characters correctly (commas, quotes, newlines)
- CSV files are named appropriately (e.g., "users.csv", "query_results.csv")
- All existing functionality remains intact (no regressions)
- Security measures prevent SQL injection via table names
- Error handling provides clear user feedback
- Unit tests achieve > 90% coverage for new code
- E2E test validates complete user workflow
- All validation commands pass with zero errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works end-to-end
- `cd app/server && uv run python -m py_compile server.py main.py core/*.py` - Validate Python syntax
- `cd app/server && uv run ruff check .` - Run Python linting
- `cd app/server && uv run pytest tests/core/test_csv_exporter.py -v` - Run CSV exporter unit tests
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript type checking
- `cd app/client && bun run build` - Run frontend build to validate zero regressions

## Notes

### CSV Format Specification
- Use CSV RFC 4180 standard
- UTF-8 encoding with BOM (`utf-8-sig`) for Excel compatibility
- Headers in first row
- Fields enclosed in quotes if they contain: comma, quote, newline, or carriage return
- Quotes within fields escaped by doubling (`""`)
- Null values represented as empty string
- Line endings: CRLF (`\r\n`) for maximum compatibility

### Download Filename Conventions
- Table exports: `{table_name}.csv` (e.g., "users.csv")
- Query results exports: `query_results_{timestamp}.csv` (e.g., "query_results_20250126_143022.csv")

### Security Considerations
- Table names are validated using existing `validate_identifier()` function
- SQL injection protection via `execute_query_safely()`
- No user-provided SQL in export endpoints
- Rate limiting considerations (may add in future if needed)

### Browser Compatibility
- Download mechanism works in modern browsers (Chrome, Firefox, Safari, Edge)
- Uses Blob API and temporary anchor element click
- Proper cleanup of Blob URLs to prevent memory leaks

### Future Enhancements (Out of Scope)
- Export format selection (CSV, JSON, Excel)
- Column selection for partial exports
- Export with custom delimiter (tab, semicolon)
- Streaming for very large datasets
- Export history/recent downloads
- Scheduled exports
