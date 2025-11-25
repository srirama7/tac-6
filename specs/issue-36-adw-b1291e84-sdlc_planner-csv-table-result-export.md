# Feature: CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality to the Natural Language SQL Interface application, allowing users to download both entire table data and query results as CSV files. This feature enhances data portability and enables users to perform further analysis or sharing of their data outside the application. The feature includes two new backend endpoints for exporting tables and query results, plus UI download buttons positioned for easy access.

## User Story
As a user of the Natural Language SQL Interface
I want to export table data and query results to CSV files
So that I can analyze the data in spreadsheet applications, share it with colleagues, or maintain local backups

## Problem Statement
Currently, users can view table data and query results in the web interface but have no way to export this data for use in other applications. Users need the ability to download their data in a standard, portable format (CSV) that can be opened in spreadsheet applications, imported into other systems, or archived for record-keeping purposes.

## Solution Statement
Implement two new FastAPI endpoints (`/api/export/table/{table_name}` and `/api/export/query`) that generate CSV files from table data and query results respectively. Add download buttons in the frontend interface: one next to the 'x' icon in the Available Tables section for table exports, and one next to the 'Hide' button in the Query Results section for result exports. The implementation will use Python's csv module for safe CSV generation and ensure proper security validation for all database operations.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` (lines 1-280) - Main FastAPI server file where the two new export endpoints will be added. Contains existing endpoint patterns to follow.
- `app/server/core/data_models.py` (lines 1-82) - Pydantic models for request/response validation. Need to add models for export endpoints.
- `app/server/core/sql_security.py` - SQL security utilities including `validate_identifier`, `execute_query_safely`, and `check_table_exists` for safe database operations.
- `app/server/core/sql_processor.py` - Contains `execute_sql_safely` function used by existing query endpoint.
- `app/client/src/main.ts` (lines 1-423) - Main frontend logic including `displayTables` (line 189) and `displayResults` (line 119) functions that need download button additions.
- `app/client/src/api/client.ts` (lines 1-79) - API client functions where export API methods will be added.
- `app/client/src/types.d.ts` (lines 1-80) - TypeScript type definitions that need export-related types.
- `app/client/src/style.css` - CSS styles where download button styles will be added.
- `app/client/index.html` (lines 1-99) - HTML structure showing existing button patterns.
- `README.md` (lines 129-135) - API endpoints documentation section where new endpoints should be documented.

### New Files
- `app/server/tests/test_export.py` - New test file for testing CSV export endpoints with security validation
- `.claude/commands/e2e/test_csv_export.md` - E2E test specification for validating CSV export functionality

## Implementation Plan

### Phase 1: Foundation
Create the core CSV export functionality in the backend by implementing two new FastAPI endpoints with proper security validation. Define the data models for export requests/responses following existing patterns. Ensure CSV generation uses Python's csv module for safe formatting and proper handling of special characters, newlines, and commas within data.

### Phase 2: Core Implementation
Implement the backend endpoints using the established security patterns (identifier validation, safe query execution). For table exports, retrieve all rows from the specified table after security validation. For query result exports, accept the SQL query that was already validated by the `/api/query` endpoint and re-execute it for export. Add comprehensive error handling and logging following existing patterns.

### Phase 3: Integration
Add frontend API client methods for calling the export endpoints. Update the UI by adding download buttons with appropriate icons in both the Available Tables section (next to the 'x' icon) and Query Results section (next to the 'Hide' button). Implement the download functionality using browser's built-in file download mechanism. Style the buttons to match the existing design system.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Backend - Add Export Data Models
- Open `app/server/core/data_models.py`
- Add `TableExportRequest` model with `table_name: str` field
- Add `QueryExportRequest` model with `sql: str` and `columns: List[str]` fields
- Add `ExportResponse` model with `filename: str`, `csv_content: str`, and `error: Optional[str]` fields
- Ensure all models follow existing Pydantic patterns with proper typing

### Step 2: Backend - Implement CSV Export Helper Function
- Create a new helper function `generate_csv_content` in `app/server/server.py` (or extract to a new `app/server/core/export.py` module)
- Function signature: `generate_csv_content(columns: List[str], rows: List[Dict[str, Any]]) -> str`
- Use Python's `csv` module with `StringIO` to generate CSV content
- Handle special characters, newlines, and proper escaping
- Add comprehensive error handling
- Write unit tests in `app/server/tests/test_export.py` for this function

### Step 3: Backend - Implement Table Export Endpoint
- Add `POST /api/export/table` endpoint in `app/server/server.py`
- Accept `TableExportRequest` in request body
- Validate table name using `validate_identifier` from `core/sql_security`
- Check table exists using `check_table_exists`
- Query all columns using `execute_query_safely` with `SELECT * FROM {table}`
- Generate CSV using the helper function
- Return CSV content with proper filename (e.g., `{table_name}_export_{timestamp}.csv`)
- Add logging following existing patterns
- Handle all errors with appropriate HTTP status codes

### Step 4: Backend - Implement Query Result Export Endpoint
- Add `POST /api/export/query` endpoint in `app/server/server.py`
- Accept `QueryExportRequest` with SQL query and columns
- Re-execute the query using `execute_sql_safely` (query was already validated by `/api/query`)
- Generate CSV using the helper function
- Return CSV content with filename `query_results_{timestamp}.csv`
- Add logging following existing patterns
- Handle all errors with appropriate HTTP status codes

### Step 5: Backend - Write Unit Tests for Export Endpoints
- Create `app/server/tests/test_export.py`
- Test table export with valid table name
- Test table export with invalid/malicious table name (SQL injection attempts)
- Test table export with non-existent table
- Test query result export with valid query
- Test CSV generation with special characters (commas, quotes, newlines)
- Test empty result sets
- Test error handling
- Run tests with `cd app/server && uv run pytest tests/test_export.py -v`

### Step 6: Frontend - Add TypeScript Types
- Open `app/client/src/types.d.ts`
- Add interface `TableExportRequest` matching backend model
- Add interface `QueryExportRequest` matching backend model
- Add interface `ExportResponse` matching backend model
- Ensure types align exactly with Pydantic models

### Step 7: Frontend - Add API Client Methods
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string): Promise<ExportResponse>` method
- Add `exportQueryResults(sql: string, columns: string[]): Promise<ExportResponse>` method
- Follow existing API method patterns for consistency
- Include proper error handling

### Step 8: Frontend - Add Download Helper Function
- Add `downloadCSV(csvContent: string, filename: string)` function in `app/client/src/main.ts`
- Create a Blob from CSV content
- Create temporary anchor element
- Trigger download using `URL.createObjectURL` and click event
- Clean up object URL after download
- Add error handling

### Step 9: Frontend - Add Download Button to Available Tables
- Modify `displayTables` function in `app/client/src/main.ts` (around line 189)
- In the table header section (line 204-230), add a download button before the remove button
- Use appropriate download icon (e.g., '⬇' or '💾')
- Position button directly to the left of the 'x' icon
- Add click handler that calls `exportTable(table.name)`
- Handle the export response and trigger CSV download
- Show success/error messages following existing patterns

### Step 10: Frontend - Add Download Button to Query Results
- Modify `displayResults` function in `app/client/src/main.ts` (around line 119)
- In the results header section (line 144-149), add a download button before the toggle button
- Use same download icon for consistency
- Position button directly to the left of the 'Hide' button
- Add click handler that calls `exportQueryResults(response.sql, response.columns)`
- Store the current query response data in a way that's accessible to the download button
- Handle the export response and trigger CSV download
- Show success/error messages following existing patterns

### Step 11: Frontend - Add CSS Styles for Download Buttons
- Open `app/client/src/style.css`
- Add `.download-button` class with styling matching existing button patterns
- Style for table download button (smaller, fits in header)
- Style for query results download button (matches toggle button size)
- Add hover effects consistent with other buttons
- Ensure buttons are visually distinct but harmonious with existing design
- Test responsive behavior

### Step 12: Update API Documentation
- Open `README.md`
- Add two new endpoints to the API Endpoints section (line 129-135):
  - `POST /api/export/table` - Export table data as CSV
  - `POST /api/export/query` - Export query results as CSV
- Include brief description of each endpoint

### Step 13: Create E2E Test Specification
- Create `.claude/commands/e2e/test_csv_export.md`
- Follow the pattern from `.claude/commands/e2e/test_basic_query.md`
- Include test steps to:
  1. Upload sample data (users.json)
  2. Verify table appears in Available Tables
  3. Click download button for table export
  4. Verify CSV file is downloaded with correct filename pattern
  5. Execute a natural language query
  6. Click download button for query results export
  7. Verify CSV file is downloaded with correct filename pattern
  8. Take screenshots at each major step
- Define success criteria for both export types
- Specify verification that CSV content is valid and contains expected data

### Step 14: Manual Testing
- Start the server and client using `./scripts/start.sh`
- Upload sample data or use existing tables
- Test table export functionality:
  - Click download button on a table
  - Verify CSV downloads with correct filename
  - Open CSV in a spreadsheet app to verify content
  - Test with tables containing special characters
- Test query result export functionality:
  - Execute a query
  - Click download button on results
  - Verify CSV downloads with correct filename
  - Verify exported data matches displayed results
- Test error cases (permissions, non-existent tables, etc.)

### Step 15: Run All Validation Commands
- Execute every validation command listed below to ensure zero regressions
- Fix any issues that arise
- Verify the feature works end-to-end with zero errors

## Testing Strategy

### Unit Tests
- **CSV Generation Tests**: Test CSV generation with various data types (strings, numbers, nulls, special characters including commas, quotes, newlines)
- **Table Export Endpoint Tests**:
  - Valid table name exports successfully
  - Invalid table names rejected with appropriate error
  - Non-existent tables return 404
  - Empty tables export with headers only
  - SQL injection attempts blocked
- **Query Export Endpoint Tests**:
  - Valid query results export successfully
  - Empty results export with headers only
  - Large result sets handle efficiently
  - Special characters in data handled correctly
- **Security Tests**:
  - Table name validation prevents SQL injection
  - Query re-execution uses existing safe patterns
  - Malicious filenames sanitized

### Edge Cases
- Tables/results with zero rows (headers only CSV)
- Tables/results with single row
- Very large tables (performance testing)
- Column names with special characters
- Data containing commas, quotes, newlines, and other CSV special characters
- Unicode characters in data
- NULL values representation in CSV
- Column names that are SQL keywords
- Empty string values vs NULL values
- Very long text fields (thousands of characters)
- Tables with many columns (100+)
- Concurrent export requests
- Network interruption during download

## Acceptance Criteria
- [ ] Two new backend endpoints (`/api/export/table` and `/api/export/query`) successfully generate CSV files
- [ ] Table export endpoint validates table names and prevents SQL injection
- [ ] Query result export endpoint safely re-executes validated queries
- [ ] Download button appears in Available Tables section, positioned to the left of the 'x' icon
- [ ] Download button appears in Query Results section, positioned to the left of the 'Hide' button
- [ ] Both download buttons use consistent, appropriate download icons
- [ ] Clicking table download button triggers CSV file download with filename pattern `{table_name}_export_{timestamp}.csv`
- [ ] Clicking query results download button triggers CSV file download with filename pattern `query_results_{timestamp}.csv`
- [ ] CSV files are properly formatted with headers and data
- [ ] Special characters (commas, quotes, newlines) in data are properly escaped
- [ ] Empty result sets export with headers only
- [ ] Appropriate success/error messages displayed to user
- [ ] All existing functionality remains unchanged (zero regressions)
- [ ] All existing tests pass
- [ ] New unit tests achieve high coverage for export functionality
- [ ] E2E test validates the complete user workflow for both export types
- [ ] Documentation updated with new API endpoints

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/test_export.py -v` - Run new export endpoint tests
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate zero regressions
- `cd app/client && bun run build` - Run frontend build to validate zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` to validate the CSV export functionality works end-to-end

## Notes

### Implementation Considerations
- **Security**: All table names must be validated using existing `validate_identifier` function before any database operations. Re-executing queries for export uses the same security validation as the original `/api/query` endpoint.
- **CSV Format**: Use Python's `csv` module which handles proper escaping of special characters automatically. Ensure consistent CSV dialect (e.g., excel dialect with CRLF line endings).
- **File Naming**: Include timestamp in filenames to avoid collisions: `{table_name}_export_20250125_143022.csv`
- **Response Type**: Return CSV content as string in JSON response for simplicity. Frontend handles creating the downloadable file.
- **Performance**: For very large tables (10k+ rows), consider adding pagination or streaming support in a future enhancement. Current implementation loads all data into memory.
- **Error Handling**: Follow existing error handling patterns with proper logging and user-friendly error messages.
- **Browser Compatibility**: The download approach using Blob and createObjectURL works in all modern browsers.

### Future Enhancements
- Add export format options (Excel, JSON, XML)
- Add column selection for partial exports
- Add filtering/sorting options for table exports
- Implement streaming for large datasets
- Add progress indicators for large exports
- Support for zipped exports of multiple tables
- Export history/logs
- Scheduled exports

### Dependencies
No new dependencies required. Uses existing libraries:
- Python: `csv` module (built-in), existing FastAPI dependencies
- Frontend: Built-in browser APIs (Blob, URL.createObjectURL)

### Icon Suggestions
Use one of these Unicode characters or custom SVG icon for download buttons:
- `⬇` (U+2B07) - Downward arrow
- `↓` (U+2193) - Downward arrow
- `💾` (U+1F4BE) - Floppy disk (save icon)
- `📥` (U+1F4E5) - Inbox tray (download)

Recommend using `↓` for consistency with common download icon conventions.
