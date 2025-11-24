# Feature: CSV Export for Tables and Query Results

## Feature Description
This feature adds one-click CSV export functionality to the Natural Language SQL Interface application. Users can export both available tables (from the tables list) and query results to CSV files with a single click. Download buttons will be placed strategically next to existing UI controls for intuitive access.

## User Story
As a user of the Natural Language SQL Interface
I want to export tables and query results as CSV files
So that I can analyze data offline, share it with others, or import it into other tools

## Problem Statement
Currently, users can view data in the application but have no way to export it for use in other tools or offline analysis. This limits the utility of the application as a data exploration and analysis tool. Users need a simple, intuitive way to download their data and query results.

## Solution Statement
Implement a CSV export feature with two new backend endpoints (`/api/export/table/{table_name}` and `/api/export/results`) and corresponding frontend download buttons. The buttons will be positioned directly to the left of existing controls (the 'x' button for tables and the 'Hide' button for query results) using a download icon for visual clarity. The CSV export will maintain proper formatting, handle special characters correctly, and provide appropriate file names based on the table name or query.

## Relevant Files
Use these files to implement the feature:

- **app/server/server.py** - Main FastAPI server where the two new endpoints will be added
  - Contains existing endpoints for upload, query, schema, insights, and table deletion
  - Uses FastAPI response models and proper error handling patterns
  - Already has sql_security imports for safe database operations

- **app/server/core/data_models.py** - Contains Pydantic models for request/response validation
  - Need to add new response models for CSV export endpoints
  - Follows consistent pattern with existing models (FileUploadResponse, QueryResponse, etc.)

- **app/server/core/sql_processor.py** - Contains database query execution logic
  - Has execute_sql_safely() and get_database_schema() functions
  - Uses sql_security module for safe query execution
  - Will be used to fetch table data for export

- **app/server/core/sql_security.py** - SQL injection protection and safe query execution
  - Contains validate_identifier(), check_table_exists(), and execute_query_safely()
  - Must be used for all database operations to maintain security

- **app/client/src/main.ts** - Main frontend application logic
  - Contains displayResults() function that shows query results
  - Contains displayTables() function that renders available tables
  - Need to add download button handlers and CSV generation logic

- **app/client/src/api/client.ts** - API client for backend communication
  - Contains api object with methods for all backend endpoints
  - Need to add two new methods for CSV export endpoints

- **app/client/src/types.d.ts** - TypeScript type definitions
  - Contains interfaces matching Pydantic models
  - Need to add types for CSV export responses

- **app/client/src/style.css** - CSS styling for the application
  - Contains button styles (.primary-button, .secondary-button, .remove-table-button)
  - Need to add styles for download buttons

- **app/client/index.html** - HTML structure
  - Shows results-header structure with toggle button
  - Shows table-header structure with remove button
  - Download buttons will be added adjacent to these existing controls

### New Files

- **app/server/tests/test_csv_export.py** - Unit tests for CSV export endpoints
  - Test table export with various data types
  - Test query results export
  - Test error handling (invalid table names, empty results, etc.)
  - Test CSV formatting and special characters

- **.claude/commands/e2e/test_csv_export.md** - E2E test for CSV export feature
  - User story: export tables and query results as CSV
  - Test steps: upload data, export table, run query, export results
  - Validate downloaded files and content
  - Screenshots showing download buttons and successful exports

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for CSV export by implementing two new API endpoints that safely retrieve data from the database and convert it to CSV format. This includes adding proper data models, implementing secure database queries using the existing sql_security module, and handling edge cases like empty tables and special characters in data.

### Phase 2: Core Implementation
Implement the frontend download buttons and CSV generation logic. Add download icons to the UI positioned directly to the left of existing controls (the 'x' button for tables and 'Hide' button for query results). Implement client-side CSV file download handling and ensure proper file naming conventions.

### Phase 3: Integration
Connect frontend and backend, add comprehensive tests (unit and E2E), validate security measures, and ensure the feature works seamlessly with existing functionality without introducing regressions.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add CSV Export Data Models
- Open `app/server/core/data_models.py`
- Add new Pydantic models for CSV export:
  - `TableExportResponse` - response model for table export endpoint
  - `ResultsExportRequest` - request model for results export (contains query results data)
  - `ExportResponse` - generic response model with CSV content and filename
- Follow existing model patterns with proper type hints and optional error field

### Step 2: Implement Backend CSV Export Utility
- Create `app/server/core/csv_exporter.py` with helper functions:
  - `generate_csv_from_data(data: List[Dict], columns: List[str]) -> str` - converts data rows to CSV string
  - Handle special characters (quotes, commas, newlines) using proper CSV escaping
  - Use Python's `csv` module for proper formatting
  - Add unit tests in `app/server/tests/test_csv_exporter.py` to validate CSV generation with various edge cases

### Step 3: Create Table Export Endpoint
- Open `app/server/server.py`
- Add new endpoint: `GET /api/export/table/{table_name}`
- Validate table name using `validate_identifier()` from sql_security
- Check table exists using `check_table_exists()`
- Query all data from the table using `execute_query_safely()`
- Generate CSV using the csv_exporter utility
- Return CSV content with appropriate headers (Content-Type: text/csv, Content-Disposition)
- Add proper error handling for invalid table names and empty tables

### Step 4: Create Results Export Endpoint
- Open `app/server/server.py`
- Add new endpoint: `POST /api/export/results`
- Accept request body with results data (columns and rows)
- Generate CSV using the csv_exporter utility
- Return CSV content with appropriate headers
- Use filename pattern: `query_results_YYYYMMDD_HHMMSS.csv`

### Step 5: Add Backend Unit Tests
- Create `app/server/tests/test_csv_export.py`
- Test table export endpoint:
  - Valid table with various data types (strings, numbers, dates, nulls)
  - Invalid table name (should return 400/404)
  - Empty table (should return CSV with headers only)
  - Special characters in data (quotes, commas, newlines)
  - SQL injection attempts in table name (should be rejected)
- Test results export endpoint:
  - Various data types in results
  - Empty results
  - Special characters
- Run tests: `cd app/server && uv run pytest tests/test_csv_export.py -v`

### Step 6: Add TypeScript Types for CSV Export
- Open `app/client/src/types.d.ts`
- Add interface for export response matching backend model
- Add any additional types needed for CSV export feature

### Step 7: Add API Client Methods for CSV Export
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string)` method - calls GET /api/export/table/{table_name}
- Add `exportResults(columns: string[], results: Record<string, any>[])` method - calls POST /api/export/results
- Both methods should handle Blob responses for file downloads

### Step 8: Add Download Button Styles
- Open `app/client/src/style.css`
- Add `.download-button` class styled similar to existing buttons
- Ensure button aligns properly next to existing controls
- Add hover effects and download icon styling
- Make it visually distinct but consistent with existing UI

### Step 9: Implement Table Export Download Button
- Open `app/client/src/main.ts`
- In the `displayTables()` function, add a download button for each table
- Position it directly to the left of the 'x' (remove) button
- Use download icon (⬇ or similar)
- Add click handler that:
  - Calls `api.exportTable(tableName)`
  - Creates a Blob from the CSV response
  - Triggers browser download using the filename from response headers
  - Shows success/error message
- Title attribute: "Download table as CSV"

### Step 10: Implement Query Results Export Download Button
- Open `app/client/src/main.ts`
- In the `displayResults()` function, add a download button to the results header
- Position it directly to the left of the 'Hide' button
- Use download icon (⬇ or similar)
- Add click handler that:
  - Calls `api.exportResults(response.columns, response.results)`
  - Creates a Blob from the CSV response
  - Triggers browser download
  - Shows success/error message
- Title attribute: "Download results as CSV"

### Step 11: Create E2E Test Plan
- Read `.claude/commands/test_e2e.md` to understand E2E test format
- Read `.claude/commands/e2e/test_basic_query.md` as an example
- Create `.claude/commands/e2e/test_csv_export.md` with:
  - User story: export tables and query results as CSV
  - Test steps:
    1. Navigate to application
    2. Upload sample users data
    3. Verify download button appears next to table 'x' button
    4. Click table download button
    5. Verify CSV file downloads successfully
    6. Run a query
    7. Verify download button appears next to 'Hide' button in results
    8. Click results download button
    9. Verify CSV file downloads successfully
    10. Take screenshots at key steps
  - Success criteria:
    - Download buttons appear in correct positions
    - CSV files download successfully
    - CSV content is properly formatted
    - File names are appropriate

### Step 12: Run Validation Commands
Execute all validation commands to ensure the feature works correctly with zero regressions:
- Read `.claude/commands/test_e2e.md`
- Execute the E2E test defined in `.claude/commands/e2e/test_csv_export.md`
- Run backend unit tests: `cd app/server && uv run pytest`
- Run frontend type check: `cd app/client && bun tsc --noEmit`
- Run frontend build: `cd app/client && bun run build`
- Verify no errors or regressions

## Testing Strategy

### Unit Tests
1. **CSV Generation Tests** (`test_csv_exporter.py`)
   - Test CSV formatting with various data types (strings, integers, floats, nulls)
   - Test special character escaping (quotes, commas, newlines, tabs)
   - Test empty data and single row/column edge cases
   - Test Unicode characters and international text

2. **Table Export Endpoint Tests** (`test_csv_export.py`)
   - Test successful export of valid table with data
   - Test export of empty table (headers only)
   - Test invalid table name returns appropriate error
   - Test non-existent table returns 404
   - Test SQL injection attempts are blocked
   - Test CSV response headers are correct (Content-Type, Content-Disposition)

3. **Results Export Endpoint Tests** (`test_csv_export.py`)
   - Test successful export with sample query results
   - Test empty results export
   - Test results with special characters
   - Test CSV response format and headers

### Edge Cases
1. **Data Edge Cases**
   - Null values in data (should render as empty string in CSV)
   - Empty strings vs null values
   - Very long text values (thousands of characters)
   - Numeric data (integers, floats, scientific notation)
   - Date/time values in various formats
   - Boolean values

2. **Security Edge Cases**
   - Table names with SQL injection attempts (e.g., "users; DROP TABLE users--")
   - Table names with special characters
   - Malformed request bodies in results export

3. **Performance Edge Cases**
   - Large tables (10,000+ rows)
   - Tables with many columns (100+)
   - Query results with large result sets
   - Concurrent export requests

4. **UI Edge Cases**
   - Button positioning with long table names
   - Multiple simultaneous downloads
   - Download in progress when page is refreshed
   - No tables available (button should not appear)
   - Error responses from backend

## Acceptance Criteria
1. Two new backend endpoints are implemented and properly secured:
   - `GET /api/export/table/{table_name}` - exports a table as CSV
   - `POST /api/export/results` - exports query results as CSV

2. Download buttons are visible and properly positioned:
   - Table download button appears directly to the left of 'x' button for each table
   - Results download button appears directly to the left of 'Hide' button in results section
   - Both buttons use appropriate download icon

3. CSV files are generated correctly:
   - Proper CSV formatting with quoted fields where necessary
   - Special characters (quotes, commas, newlines) are escaped properly
   - Column headers are included as first row
   - Null values are handled correctly

4. File downloads work correctly:
   - Browser initiates download automatically
   - Filenames are descriptive (table name or query_results with timestamp)
   - Files have .csv extension
   - Downloaded files can be opened in Excel/Google Sheets

5. Error handling is robust:
   - Invalid table names show appropriate error message
   - Empty tables/results export successfully (headers only)
   - Network errors are caught and displayed to user

6. Security is maintained:
   - All table names are validated using sql_security module
   - SQL injection attempts are blocked
   - No new security vulnerabilities introduced

7. Tests pass successfully:
   - All unit tests pass
   - E2E test validates the feature end-to-end
   - No regressions in existing functionality
   - Frontend build succeeds without errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_csv_export.md` test file to validate this functionality works
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type check to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### CSV Format Specifications
- Use RFC 4180 standard for CSV formatting
- UTF-8 encoding for international character support
- CRLF line endings for maximum compatibility
- Quoted fields when containing special characters (comma, quote, newline)
- Double-quote escaping for quotes within quoted fields

### File Naming Conventions
- Tables: `{table_name}.csv` (e.g., `users.csv`, `products.csv`)
- Query results: `query_results_{YYYYMMDD}_{HHMMSS}.csv` (e.g., `query_results_20250124_143022.csv`)

### HTTP Response Headers for Downloads
```
Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename="{filename}.csv"
```

### Frontend Download Implementation
Use the Blob API and temporary anchor element technique:
```typescript
const blob = new Blob([csvContent], { type: 'text/csv' });
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = filename;
a.click();
window.URL.revokeObjectURL(url);
```

### Security Considerations
- All table names MUST be validated with `validate_identifier()` before use
- Use `check_table_exists()` to verify table exists before querying
- Use `execute_query_safely()` for all database queries
- Never concatenate user input into SQL queries
- Validate request body size to prevent memory exhaustion with large result exports
- Consider adding rate limiting for export endpoints in production

### Future Enhancements (Not in Scope)
- Excel format export (.xlsx)
- JSON/XML export formats
- Export with custom column selection
- Export large datasets in chunks (streaming)
- Schedule automated exports
- Export to cloud storage (S3, Google Drive, etc.)
