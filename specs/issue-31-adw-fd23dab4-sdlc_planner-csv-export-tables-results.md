# Feature: CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality to the Natural Language SQL Interface application, allowing users to download both database table data and query results as CSV files. This feature includes two new backend endpoints for generating CSV exports and UI enhancements with download buttons positioned next to existing controls in the tables list and results sections.

## User Story
As a user of the Natural Language SQL Interface
I want to export tables and query results as CSV files with a single click
So that I can analyze data offline, share it with colleagues, or use it in other applications like Excel or data analysis tools

## Problem Statement
Currently, users can view data in the application but have no way to export it for use outside the interface. This limits data portability and forces users to manually copy data or take screenshots when they need to share results or perform additional analysis in external tools.

## Solution Statement
Implement a comprehensive CSV export feature with:
- Two new FastAPI endpoints (`/api/export/table/{table_name}` and `/api/export/results`) that generate CSV files from database tables and query results
- Download buttons in the UI positioned strategically next to existing controls (tables list and query results)
- Proper CSV formatting with headers, escaped values, and UTF-8 encoding
- Security validation using existing SQL security module to prevent injection attacks
- Responsive design that maintains the current UI aesthetic

## Relevant Files

### Backend Files

- **app/server/server.py** - Main FastAPI application file
  - Add two new export endpoints
  - Integrate with CSV generation utilities
  - Use existing security validation patterns

- **app/server/core/data_models.py** - Pydantic data models
  - Add new request/response models for CSV export endpoints
  - Define ExportResultsRequest model for query results export

- **app/server/core/sql_security.py** - SQL injection protection module
  - Use existing `validate_identifier()` and `check_table_exists()` functions
  - Ensure secure table name validation for exports

### Frontend Files

- **app/client/src/main.ts** - Main TypeScript application logic
  - Add download button click handlers for tables and results
  - Implement CSV download logic using blob URLs
  - Update `displayTables()` to include download buttons
  - Update `displayResults()` to include download button

- **app/client/src/types.d.ts** - TypeScript type definitions
  - Add ExportResultsRequest interface
  - Document expected API response types

- **app/client/src/style.css** - Application styles
  - Add styles for download buttons
  - Ensure proper positioning and icon display

- **app/client/src/api/client.ts** - API client module
  - Add `exportTable()` method
  - Add `exportResults()` method

### New Files

- **app/server/core/csv_exporter.py** - New CSV generation utility module
  - Implement `generate_table_csv()` function to export entire tables
  - Implement `generate_results_csv()` function to export query results
  - Handle CSV formatting, escaping, and UTF-8 encoding
  - Use Python's built-in `csv` module for proper RFC 4180 compliance

- **.claude/commands/e2e/test_csv_export.md** - E2E test specification
  - Test table export functionality
  - Test query results export functionality
  - Verify CSV file format and content
  - Validate download button placement and functionality

### Testing Files

- **app/server/tests/test_csv_export.py** - New backend test file
  - Unit tests for CSV generation functions
  - Integration tests for export endpoints
  - Security validation tests (malicious table names, SQL injection attempts)
  - Edge case tests (empty tables, special characters, large datasets)

## Implementation Plan

### Phase 1: Foundation
Create the core CSV generation utility module and add necessary data models. This provides the foundation for both backend endpoints to use consistent CSV generation logic.

- Create `app/server/core/csv_exporter.py` with functions to convert database results to properly formatted CSV strings
- Add CSV export request/response models to `app/server/core/data_models.py`
- Ensure CSV generation handles edge cases (null values, special characters, quotes)

### Phase 2: Core Implementation
Implement the two backend API endpoints and their corresponding frontend API client methods. This creates the complete data flow from user action to CSV download.

- Add `/api/export/table/{table_name}` endpoint to `app/server/server.py`
- Add `/api/export/results` endpoint to `app/server/server.py`
- Implement security validation using existing `sql_security` module
- Add API client methods in `app/client/src/api/client.ts`
- Create comprehensive backend tests in `app/server/tests/test_csv_export.py`

### Phase 3: Integration
Integrate download buttons into the UI at the specified locations and implement the client-side download functionality.

- Add download button next to 'x' icon in table header (main.ts:displayTables)
- Add download button next to 'Hide' button in results section (main.ts:displayResults)
- Implement blob-based CSV download in frontend
- Add appropriate download icon styling in style.css
- Create E2E test specification in `.claude/commands/e2e/test_csv_export.md`

## Step by Step Tasks

### Task 1: Create CSV Exporter Utility Module
- Create `app/server/core/csv_exporter.py` with the following functions:
  - `generate_table_csv(table_name: str) -> str`: Query table and convert to CSV
  - `generate_results_csv(results: List[Dict[str, Any]], columns: List[str]) -> str`: Convert query results to CSV
- Use Python's `csv` module with `csv.writer` for proper escaping
- Handle null values as empty strings
- Include column headers as the first row
- Use UTF-8 encoding
- Write unit tests for edge cases (empty data, special characters, null values)

### Task 2: Add Data Models for CSV Export
- Add to `app/server/core/data_models.py`:
  - `ExportResultsRequest` model with fields for results, columns, and filename
  - Import these in server.py for endpoint validation

### Task 3: Implement Backend Export Endpoints
- Add to `app/server/server.py`:
  - `GET /api/export/table/{table_name}` endpoint:
    - Validate table name using `validate_identifier()`
    - Check table exists using `check_table_exists()`
    - Call `generate_table_csv()` from csv_exporter
    - Return CSV as downloadable file with `Response` and `media_type='text/csv'`
    - Set `Content-Disposition` header with filename
  - `POST /api/export/results` endpoint:
    - Accept `ExportResultsRequest` with results and columns
    - Call `generate_results_csv()` from csv_exporter
    - Return CSV as downloadable file with proper headers
- Add comprehensive logging for both endpoints
- Handle errors gracefully with appropriate HTTP status codes

### Task 4: Create Backend Tests
- Create `app/server/tests/test_csv_export.py`:
  - Test `generate_table_csv()` with sample data
  - Test `generate_results_csv()` with various data types
  - Test export endpoints with valid requests
  - Test security validation (invalid table names, SQL injection attempts)
  - Test edge cases (empty tables, special characters, large datasets)
  - Test CSV format compliance (headers, escaping, UTF-8)
- Run tests to ensure all pass: `cd app/server && uv run pytest tests/test_csv_export.py -v`

### Task 5: Add Frontend API Client Methods
- Add to `app/client/src/api/client.ts`:
  - `exportTable(tableName: string): Promise<Blob>` - Calls `/api/export/table/{tableName}`
  - `exportResults(results: any[], columns: string[], filename: string): Promise<Blob>` - Calls `/api/export/results`
- Both methods should return blob data for download
- Handle errors appropriately

### Task 6: Add TypeScript Type Definitions
- Add to `app/client/src/types.d.ts`:
  - `ExportResultsRequest` interface matching backend model
  - Document the expected structure for CSV export requests

### Task 7: Implement Download Button for Tables
- Update `displayTables()` function in `app/client/src/main.ts`:
  - Add download button element before the remove button ('×')
  - Use download icon (📥 or appropriate SVG/icon font)
  - Add click handler that calls `api.exportTable(table.name)`
  - Create blob URL and trigger download with filename `{table_name}.csv`
  - Clean up blob URL after download
  - Add appropriate CSS class for styling

### Task 8: Implement Download Button for Query Results
- Update `displayResults()` function in `app/client/src/main.ts`:
  - Add download button element before the 'Hide' button
  - Use download icon (📥 or appropriate SVG/icon font)
  - Add click handler that calls `api.exportResults(response.results, response.columns, 'query_results.csv')`
  - Create blob URL and trigger download
  - Clean up blob URL after download
  - Add appropriate CSS class for styling

### Task 9: Add Button Styles
- Update `app/client/src/style.css`:
  - Add `.download-button` class with appropriate styling
  - Ensure download buttons match the application's design aesthetic
  - Add hover effects for better UX
  - Ensure proper spacing between download and existing buttons
  - Make buttons responsive

### Task 10: Create E2E Test Specification
- Create `.claude/commands/e2e/test_csv_export.md`:
  - Read `.claude/commands/test_e2e.md` and `.claude/commands/e2e/test_basic_query.md` to understand E2E test format
  - Create test steps to:
    - Upload sample data
    - Verify download button appears next to table 'x' icon
    - Click download button and verify CSV file downloads
    - Execute a query
    - Verify download button appears next to 'Hide' button in results
    - Click download button and verify query results CSV downloads
    - Take screenshots at each step
  - Include success criteria focused on button placement and CSV download functionality

### Task 11: Validation - Run All Tests
- Execute validation commands to ensure zero regressions:
  - `cd app/server && uv run pytest` - Run all server tests
  - `cd app/client && bun tsc --noEmit` - Validate TypeScript types
  - `cd app/client && bun run build` - Ensure frontend builds successfully
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works end-to-end

## Testing Strategy

### Unit Tests
- **CSV Generation**: Test `generate_table_csv()` and `generate_results_csv()` with:
  - Various data types (integers, floats, strings, dates, null values)
  - Special characters requiring escaping (quotes, commas, newlines)
  - Empty datasets
  - Single row/column datasets
  - Large datasets (performance testing)

- **API Endpoints**: Test export endpoints with:
  - Valid table names and results
  - Invalid table names (should return 404)
  - Malicious table names (should return 400 with validation error)
  - Empty tables/results
  - Non-existent tables

### Integration Tests
- Test full export flow from endpoint to CSV generation
- Verify CSV content matches database content exactly
- Verify HTTP headers are set correctly for file download
- Test concurrent export requests

### E2E Tests
- Upload sample data via UI
- Verify download buttons appear in correct locations
- Click table download button and verify CSV downloads
- Execute query and verify results download button appears
- Click results download button and verify CSV downloads
- Verify downloaded CSV files contain correct data and formatting

### Edge Cases
- Tables with no rows (should return CSV with headers only)
- Query results with no rows (should return CSV with headers only)
- Column names with special characters
- Data values with quotes, commas, and newlines
- Unicode characters in data (ensure UTF-8 encoding works)
- Very long column names or values
- Tables with many columns (>50)
- Large result sets (>10,000 rows) - performance testing

## Acceptance Criteria
- Two new backend endpoints (`/api/export/table/{table_name}` and `/api/export/results`) successfully generate and return CSV files
- Download button appears directly to the left of the 'x' icon in the Available Tables section for each table
- Download button appears directly to the left of the 'Hide' button in the Query Results section
- Clicking a table download button downloads a CSV file containing all table data with correct headers
- Clicking a results download button downloads a CSV file containing the query results with correct headers
- CSV files use proper formatting with RFC 4180 compliance (escaped quotes, comma delimiters, headers)
- Downloaded CSV files use UTF-8 encoding and can be opened in Excel, Google Sheets, and text editors
- CSV filenames are descriptive (e.g., `users.csv` for tables, `query_results.csv` for results)
- All existing functionality remains intact (no regressions)
- Security validation prevents SQL injection through table names
- Download buttons use appropriate download icon (📥 or SVG equivalent)
- All backend tests pass (including new CSV export tests)
- All frontend tests pass (TypeScript compilation and build)
- E2E test validates complete download workflow for both tables and results

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/test_csv_export.py -v` - Run CSV export tests specifically
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript validation
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works end-to-end

## Notes

### Implementation Details
- Use Python's built-in `csv` module for CSV generation to ensure RFC 4180 compliance
- FastAPI's `Response` class with `media_type='text/csv'` is the standard way to return downloadable files
- Set `Content-Disposition: attachment; filename="..."` header to trigger browser download
- Use `blob:` URLs in the frontend for downloads to avoid opening files in new tabs

### Security Considerations
- Reuse existing `validate_identifier()` from `sql_security.py` to prevent injection attacks
- Table names must pass security validation before any database operations
- Query results come from already-executed queries, so they're inherently safe

### Performance Considerations
- For large tables (>100,000 rows), consider implementing pagination or streaming responses
- CSV generation is memory-efficient using Python's csv.writer with StringIO
- Frontend blob URLs are automatically garbage collected by the browser

### Future Enhancements (Out of Scope)
- Add format options (CSV, JSON, Excel)
- Add column selection for partial exports
- Add row limit/pagination for very large tables
- Add export progress indicator for large datasets
- Add batch export (multiple tables at once)

### Design Decisions
- Download buttons positioned to the left of existing control buttons as specified
- Using 📥 emoji or SVG download icon for consistency with modern web UX
- Table exports use table name as filename, results use generic "query_results.csv"
- POST endpoint for results export (not GET) because results data is sent in request body
- CSV is the initial format due to universal compatibility (Excel, Google Sheets, all databases)
