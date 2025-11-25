# Feature: One-Click CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality to the Natural Language SQL Interface application, allowing users to export entire tables or query results as CSV files. This feature includes two new FastAPI backend endpoints for secure CSV generation and frontend download buttons placed strategically next to existing UI elements in the Available Tables and Query Results sections.

## User Story
As a user of the Natural Language SQL Interface
I want to export tables and query results as CSV files with a single click
So that I can easily share, analyze, or archive my data outside the application

## Problem Statement
Currently, users can view their data in the application but have no way to export it for external use. Data analysis often requires transferring data to spreadsheet applications, sharing with colleagues, or archiving for records. Without export functionality, users must manually copy data or resort to workarounds, which is inefficient and error-prone for large datasets.

## Solution Statement
Implement a comprehensive CSV export system with:
1. **Backend**: Two secure FastAPI endpoints that leverage existing SQL security infrastructure to generate CSV files from table data and query results
2. **Frontend**: Strategically placed download buttons with appropriate icons that trigger browser-native downloads without page navigation
3. **Security**: Full integration with the existing `sql_security.py` module to prevent SQL injection and validate all identifiers
4. **User Experience**: Seamless one-click downloads with proper filename generation and CSV formatting

## Relevant Files
Use these files to implement the feature:

- **app/server/server.py** (lines 1-280) - Main FastAPI application file where new endpoints will be added. Already contains similar endpoint patterns (`/api/upload`, `/api/query`, `/api/schema`) that can be used as templates. Uses existing security module imports and follows established error handling patterns.

- **app/server/core/sql_security.py** (lines 1-295) - SQL security module that provides `validate_identifier()`, `execute_query_safely()`, and `check_table_exists()` functions. Must be used for all SQL operations in the new export endpoints to maintain security standards.

- **app/server/core/data_models.py** - Contains Pydantic models for request/response validation. Need to add new models for CSV export requests and responses.

- **app/client/src/main.ts** (lines 1-423) - Main frontend TypeScript file containing UI initialization and event handlers. Contains `displayTables()` (lines 189-258) and `displayResults()` (lines 119-154) functions where download buttons need to be added.

- **app/client/src/api/client.ts** (lines 1-79) - API client module with typed request functions. Need to add new export API methods following existing patterns.

- **app/client/src/types.d.ts** (lines 1-80) - TypeScript type definitions matching backend Pydantic models. Need to add types for export requests/responses.

- **app/client/src/style.css** - CSS styles for the application. Need to add styles for download buttons to match existing UI patterns.

- **app/server/tests/test_sql_injection.py** - Existing security tests. Use as reference for creating export endpoint security tests.

### New Files

- **app/server/tests/test_csv_export.py** - New test file for CSV export endpoint functionality including unit tests for both endpoints, edge cases, and security validation.

- **.claude/commands/e2e/test_csv_export.md** - New E2E test file following the pattern of `.claude/commands/e2e/test_basic_query.md` to validate CSV export functionality works end-to-end with user interactions.

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for CSV export by adding new Pydantic models for request/response validation and implementing secure CSV generation functions. This phase establishes the data contracts and security patterns that will be used by both export endpoints.

### Phase 2: Core Implementation
Implement the two FastAPI endpoints (`/api/export/table/{table_name}` and `/api/export/query`) with full SQL security integration, proper CSV generation using Python's `csv` module, and streaming responses with appropriate HTTP headers. Add comprehensive unit tests covering normal operation, edge cases, and security validation.

### Phase 3: Integration
Build the frontend download functionality by adding download buttons to the UI, implementing API client methods, creating click handlers that trigger browser downloads, and validating the entire flow with an E2E test.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Add Backend Data Models
- Open `app/server/core/data_models.py`
- Add `ExportQueryRequest` model with fields: `sql` (str), `columns` (List[str]), `results` (List[Dict[str, Any]])
- Add `ExportResponse` model with fields: `filename` (str), `row_count` (int), `error` (Optional[str])
- Ensure all models use proper Pydantic field validation

### 2. Implement Table Export Endpoint
- Open `app/server/server.py`
- Add `GET /api/export/table/{table_name}` endpoint function
- Use `validate_identifier()` to validate the table name parameter
- Use `check_table_exists()` to verify table exists, return 404 if not
- Use `execute_query_safely()` to fetch all rows: `SELECT * FROM {table}`
- Generate CSV using Python's `csv` module with `io.StringIO`
- Return `StreamingResponse` with headers: `Content-Type: text/csv`, `Content-Disposition: attachment; filename="{table_name}.csv"`
- Add comprehensive error handling with logging following existing patterns
- Test manually by starting server and calling endpoint with curl or browser

### 3. Implement Query Result Export Endpoint
- In `app/server/server.py`, add `POST /api/export/query` endpoint
- Accept `ExportQueryRequest` in request body
- Validate that results are not empty (return 400 if empty)
- Generate CSV from the provided results and columns
- Create filename as `query_results_{timestamp}.csv` using `datetime.now().strftime("%Y%m%d_%H%M%S")`
- Return `StreamingResponse` with same CSV headers as table export
- Add error handling and logging
- Test manually with sample query results

### 4. Create Backend Unit Tests
- Create `app/server/tests/test_csv_export.py`
- Import pytest, test client from FastAPI, and required modules
- Add test for table export with valid table: verify CSV format, headers, content, filename
- Add test for table export with non-existent table: verify 404 response
- Add test for table export with invalid table name (SQL injection attempt): verify 400 response
- Add test for query export with valid results: verify CSV generation and formatting
- Add test for query export with empty results: verify 400 response
- Add test for query export with special characters in data: verify proper CSV escaping
- Add test for large dataset export: verify streaming works correctly
- Run tests with `cd app/server && uv run pytest tests/test_csv_export.py -v`

### 5. Add Frontend TypeScript Types
- Open `app/client/src/types.d.ts`
- Add `ExportQueryRequest` interface matching backend model
- Add `ExportResponse` interface matching backend model
- Ensure types align with Pydantic models exactly

### 6. Add Frontend API Client Methods
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string): Promise<Blob>` method
- Add `exportQueryResults(request: ExportQueryRequest): Promise<Blob>` method
- Both methods should fetch from appropriate endpoint and return blob for download
- Handle errors appropriately

### 7. Add Download Helper Function
- In `app/client/src/main.ts`, create `downloadCSV(blob: Blob, filename: string)` function
- Create object URL from blob: `URL.createObjectURL(blob)`
- Create temporary anchor element with download attribute
- Trigger click programmatically
- Clean up object URL: `URL.revokeObjectURL()`
- Add error handling

### 8. Add Table Export Button to UI
- In `app/client/src/main.ts`, modify `displayTables()` function
- Inside the table header creation (around line 204-230), add download button before remove button
- Create button element with class `download-table-button`
- Set button innerHTML to download icon: `↓` or appropriate SVG icon
- Set button title to "Export as CSV"
- Add click handler that calls `api.exportTable(table.name)` and then `downloadCSV()`
- Ensure button is positioned to the left of the × button
- Add loading state during download

### 9. Add Query Result Export Button to UI
- In `app/client/src/main.ts`, modify `displayResults()` function
- In the results section header (around line 149-153), add download button near toggle button
- Create button element with class `download-results-button`
- Set button innerHTML to download icon
- Set button title to "Export results as CSV"
- Add click handler that prepares `ExportQueryRequest` from current results and calls `api.exportQueryResults()`
- Store current query results in a variable accessible to the handler
- Position button to the left of "Hide" button
- Add loading state during download

### 10. Add CSS Styles for Download Buttons
- Open `app/client/src/style.css`
- Add styles for `.download-table-button` and `.download-results-button`
- Style should match existing button patterns (remove button, query button)
- Ensure proper spacing, hover effects, and icon sizing
- Add loading state styles if needed
- Test visual appearance in browser

### 11. Create E2E Test File
- Create `.claude/commands/e2e/test_csv_export.md`
- Follow the format of `.claude/commands/e2e/test_basic_query.md`
- Define User Story for CSV export feature
- Create Test Steps:
  - Navigate to application
  - Upload sample data (users.json)
  - Verify table appears in Available Tables
  - Verify download button appears next to × button
  - Click download button for table export
  - Verify CSV file is downloaded with correct filename
  - Execute a natural language query
  - Verify results appear
  - Verify download button appears next to Hide button
  - Click download button for query results export
  - Verify CSV file is downloaded
  - Take screenshots at key steps
- Define Success Criteria: both downloads work, files contain correct data, buttons are properly positioned

### 12. Manual Testing and Validation
- Start server: `cd app/server && uv run python server.py`
- Start client: `cd app/client && bun run dev`
- Open browser to http://localhost:5173
- Upload sample data
- Test table export by clicking download button
- Verify CSV file downloads with correct name and content
- Execute a query
- Test query result export by clicking download button
- Verify CSV file downloads with correct content
- Test edge cases: empty results, special characters, large datasets

### 13. Run All Validation Commands
- Execute validation commands listed in "Validation Commands" section below
- Ensure all tests pass with zero failures
- Ensure no regressions in existing functionality
- Fix any issues that arise

### 14. Execute E2E Test
- Read `.claude/commands/test_e2e.md` to understand E2E test execution
- Execute the new E2E test: `.claude/commands/e2e/test_csv_export.md`
- Verify all steps pass
- Review screenshots to confirm UI elements are properly positioned
- Confirm CSV files are downloaded and contain expected data

## Testing Strategy

### Unit Tests
1. **Table Export Endpoint Tests** (test_csv_export.py)
   - Test valid table export returns proper CSV format
   - Test CSV headers match table columns
   - Test CSV data matches table content
   - Test non-existent table returns 404
   - Test invalid table name (SQL injection) returns 400
   - Test filename format matches pattern: `{table_name}.csv`

2. **Query Export Endpoint Tests** (test_csv_export.py)
   - Test valid query results export returns proper CSV
   - Test CSV generation from provided data structure
   - Test empty results returns 400 error
   - Test filename includes timestamp
   - Test special characters are properly escaped in CSV

3. **Security Tests** (test_csv_export.py)
   - Test SQL injection attempts in table name are blocked
   - Test invalid identifiers are rejected
   - Test validation uses `sql_security` module functions
   - Test DDL operations cannot be injected through export

### Edge Cases
1. **Empty Data**: Export endpoints handle tables/results with no rows
2. **Special Characters**: CSV properly escapes quotes, commas, newlines in data
3. **Large Datasets**: Streaming response works for tables with 10,000+ rows
4. **Unicode Content**: CSV export preserves international characters and emojis
5. **Column Names**: Handles column names with spaces, underscores, special characters
6. **Null Values**: Properly represents NULL/None values in CSV (empty string)
7. **Concurrent Downloads**: Multiple simultaneous export requests don't interfere
8. **Invalid Requests**: Malformed requests return appropriate error codes

## Acceptance Criteria
1. Two new backend endpoints (`/api/export/table/{table_name}` and `/api/export/query`) are implemented and functional
2. Both endpoints integrate with `sql_security.py` module for secure SQL operations
3. CSV files are generated correctly with proper headers and data formatting
4. Download button appears in Available Tables section, positioned to the left of the × button
5. Download button appears in Query Results section, positioned to the left of the Hide button
6. Both download buttons use appropriate download icons
7. Clicking table download button exports the entire table as CSV
8. Clicking query result download button exports the current query results as CSV
9. Downloaded CSV files have descriptive filenames (table name or query_results with timestamp)
10. CSV files can be opened in Excel, Google Sheets, and other spreadsheet applications
11. All unit tests pass with 100% success rate
12. E2E test validates the complete user flow with screenshots
13. No regressions in existing functionality (all existing tests still pass)
14. Security validation confirms no SQL injection vulnerabilities in export endpoints

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

```bash
# Test table export endpoint
curl -X GET "http://localhost:8000/api/export/table/users" -o users.csv

# Test query export endpoint
curl -X POST "http://localhost:8000/api/export/query" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT * FROM users","columns":["id","name"],"results":[{"id":1,"name":"test"}]}' \
  -o results.csv

# Run CSV export unit tests
cd app/server && uv run pytest tests/test_csv_export.py -v

# Run all server tests to ensure no regressions
cd app/server && uv run pytest

# Run frontend TypeScript type checking
cd app/client && bun tsc --noEmit

# Run frontend build to ensure no build errors
cd app/client && bun run build

# Execute E2E test
# Read .claude/commands/test_e2e.md first, then execute:
# .claude/commands/e2e/test_csv_export.md with appropriate test runner
```

## Notes

### Implementation Considerations
- Use Python's built-in `csv` module for CSV generation (no additional dependencies needed)
- Use `io.StringIO` for in-memory CSV generation
- Use FastAPI's `StreamingResponse` for efficient file downloads
- Set `Content-Disposition: attachment` header to trigger browser download dialog
- Use UTC timestamps in filenames to avoid timezone confusion

### CSV Format Specifications
- Use comma as delimiter (standard CSV)
- Use double quotes for escaping values containing commas or newlines
- Include header row with column names
- Use UTF-8 encoding for international character support
- Represent NULL values as empty strings (not "NULL" or "None")

### Security Notes
- All table name validation must use `validate_identifier()` from `sql_security.py`
- All SQL queries must use `execute_query_safely()` with proper parameterization
- Never concatenate user input directly into SQL strings
- Query export endpoint validates that provided SQL/results are non-empty but does not re-execute SQL (uses provided results)

### Frontend Best Practices
- Use browser's native download mechanism (no server-side file storage)
- Clean up blob URLs after download to prevent memory leaks
- Show loading indicators during download for better UX
- Handle download errors gracefully with user-friendly messages
- Ensure download buttons match existing UI styling and patterns

### Future Enhancements (Not in Scope)
- Support for other export formats (JSON, Excel, Parquet)
- Configurable CSV delimiters and quote characters
- Export only selected columns or filtered rows
- Export multiple tables at once as ZIP archive
- Download progress indicators for very large exports
