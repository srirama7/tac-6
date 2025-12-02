# Feature: CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality to enable users to download table data and query results as CSV files. This feature adds download buttons to both the Available Tables section (for exporting entire tables) and the Query Results section (for exporting query results). The implementation includes two new backend endpoints to handle CSV generation and file streaming, along with frontend UI components to trigger downloads.

## User Story
As a data analyst using the Natural Language SQL Interface
I want to export tables and query results to CSV files with a single click
So that I can analyze the data offline in spreadsheet applications like Excel or perform further processing

## Problem Statement
Currently, users can view data in the web interface but have no way to export it for offline analysis or sharing. Users need to manually copy-paste data or write custom scripts to extract information, which is time-consuming and error-prone. This limits the utility of the application for users who need to work with data in other tools or share results with colleagues.

## Solution Statement
Implement CSV export functionality by creating two new FastAPI endpoints (`/api/export/table/{table_name}` and `/api/export/query`) that generate CSV files from database queries. Add download buttons to the frontend UI positioned directly to the left of existing action buttons (× for tables, Hide for query results) using appropriate download icons. The solution uses Python's built-in CSV module for server-side generation and browser download APIs for client-side file handling.

## Relevant Files
Use these files to implement the feature:

- **app/server/server.py** (lines 1-280) - Main FastAPI server file where we'll add the two new CSV export endpoints
  - Currently has endpoints for upload, query, schema, insights, health, and table deletion
  - Will add `/api/export/table/{table_name}` endpoint for table exports
  - Will add `/api/export/query` endpoint for query result exports

- **app/server/core/data_models.py** (lines 1-82) - Pydantic models for request/response validation
  - Will add `TableExportRequest` model (empty, table_name from path)
  - Will add `QueryExportRequest` model (contains QueryRequest fields: query, llm_provider)
  - Export responses will use FastAPI's `StreamingResponse` with CSV content type

- **app/server/core/sql_security.py** (lines 1-305) - SQL security module for safe database operations
  - Already has `validate_identifier()` for table name validation
  - Already has `check_table_exists()` for table existence verification
  - Already has `execute_query_safely()` for secure query execution
  - Will use these functions to securely generate CSV data

- **app/client/src/api/client.ts** (lines 1-79) - Frontend API client
  - Will add `exportTable(tableName: string)` method
  - Will add `exportQueryResults(request: QueryRequest)` method
  - These methods will trigger browser downloads using blob URLs

- **app/client/src/main.ts** (lines 1-423) - Main frontend TypeScript file
  - Will add download button to `displayTables()` function (line 189) for table exports
  - Will add download button to `displayResults()` function (line 119) for query result exports
  - Will add `downloadTableCSV(tableName: string)` function
  - Will add `downloadQueryResultsCSV(query: string)` function

- **app/client/src/style.css** (lines 1-500+) - CSS styling
  - Will add `.download-button` class similar to `.remove-table-button` (line 303)
  - Will style download icons to match existing UI patterns

- **app/client/src/types.d.ts** (lines 1-80) - TypeScript type definitions
  - Will add `TableExportRequest` interface (empty interface, table name from path)
  - Will add `QueryExportRequest` interface (extends QueryRequest)

- **app/client/index.html** (lines 1-99) - HTML structure
  - No changes needed, buttons will be added dynamically via JavaScript

### New Files

- **.claude/commands/e2e/test_csv_export.md** - E2E test file to validate CSV export functionality
  - Will test table export by clicking download button and verifying CSV file
  - Will test query result export by running query and downloading results
  - Will verify CSV file format and content correctness

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for CSV generation and file streaming. This includes adding new Pydantic models for request validation, implementing secure CSV generation functions that use the existing SQL security module, and creating helper utilities for CSV formatting. The foundation ensures that CSV data is generated safely from the database without SQL injection vulnerabilities.

### Phase 2: Core Implementation
Implement the two new FastAPI endpoints for CSV export. The `/api/export/table/{table_name}` endpoint will export entire tables by validating the table name, querying all rows, and streaming CSV data. The `/api/export/query` endpoint will accept natural language queries, generate SQL, execute the query, and stream results as CSV. Both endpoints will use FastAPI's `StreamingResponse` with appropriate headers for browser downloads.

### Phase 3: Integration
Add frontend UI components and API client methods to trigger downloads. This includes adding download buttons to the table list and query results sections, implementing click handlers that call the new API endpoints, and using browser APIs to trigger file downloads. The integration phase also includes styling the download buttons to match the existing UI design patterns and creating E2E tests to validate the complete workflow.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create Backend Data Models
- Open `app/server/core/data_models.py`
- Add `QueryExportRequest` model that inherits from `QueryRequest` (same fields: query, llm_provider, optional table_name)
- Note: Table export doesn't need a request model (table_name comes from URL path parameter)

### 2. Create CSV Generation Helper Function
- Open `app/server/core/sql_processor.py` or create a new `app/server/core/csv_generator.py` file
- Create `generate_csv_from_results(results: List[Dict[str, Any]], columns: List[str]) -> str` function
- Use Python's `csv` module with `StringIO` to generate CSV content
- Ensure proper escaping of special characters and handling of None values
- Return CSV content as string

### 3. Implement Table Export Endpoint
- Open `app/server/server.py`
- Add `@app.get("/api/export/table/{table_name}")` endpoint
- Validate `table_name` using `validate_identifier()` from `sql_security`
- Check table exists using `check_table_exists()`
- Query all rows: `SELECT * FROM {table_name}` using `execute_query_safely()`
- Generate CSV using helper function from step 2
- Return `StreamingResponse` with:
  - content: CSV string as bytes
  - media_type: "text/csv"
  - headers: `Content-Disposition: attachment; filename="{table_name}.csv"`

### 4. Implement Query Results Export Endpoint
- Open `app/server/server.py`
- Add `@app.post("/api/export/query")` endpoint with `QueryExportRequest` body
- Follow same logic as `/api/query` endpoint (line 110):
  - Get database schema using `get_database_schema()`
  - Generate SQL using `generate_sql()`
  - Execute SQL using `execute_sql_safely()`
- Generate CSV from results using helper function
- Return `StreamingResponse` with:
  - content: CSV string as bytes
  - media_type: "text/csv"
  - headers: `Content-Disposition: attachment; filename="query_results.csv"`

### 5. Add Backend Unit Tests
- Create `app/server/tests/test_csv_export.py`
- Test `generate_csv_from_results()` with:
  - Empty results
  - Single row
  - Multiple rows with various data types
  - Special characters and null values
- Test `/api/export/table/{table_name}` endpoint:
  - Valid table name
  - Invalid table name
  - Non-existent table
- Test `/api/export/query` endpoint:
  - Valid query
  - Invalid query
  - Empty results
- Run tests: `cd app/server && uv run pytest tests/test_csv_export.py -v`

### 6. Add Frontend TypeScript Types
- Open `app/client/src/types.d.ts`
- Add `QueryExportRequest` interface (same as `QueryRequest`)
- Note: Table export doesn't need a request type (just table name string)

### 7. Add Frontend API Client Methods
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string): Promise<Blob>` method
  - Makes GET request to `/api/export/table/{tableName}`
  - Returns response as Blob
- Add `exportQueryResults(request: QueryRequest): Promise<Blob>` method
  - Makes POST request to `/api/export/query` with request body
  - Returns response as Blob

### 8. Add Download Helper Functions
- Open `app/client/src/main.ts`
- Add `downloadCSV(blob: Blob, filename: string)` helper function:
  - Creates blob URL using `URL.createObjectURL(blob)`
  - Creates temporary `<a>` element with href=blobURL and download=filename
  - Triggers click to download
  - Revokes blob URL after download
- Add `downloadTableCSV(tableName: string)` function:
  - Calls `api.exportTable(tableName)`
  - Calls `downloadCSV(blob, `${tableName}.csv`)`
  - Handles errors with `displayError()`
- Add `downloadQueryResultsCSV(query: string, llmProvider: string)` function:
  - Calls `api.exportQueryResults({ query, llm_provider: llmProvider })`
  - Calls `downloadCSV(blob, 'query_results.csv')`
  - Handles errors with `displayError()`

### 9. Add Download Button to Table Headers
- Open `app/client/src/main.ts`
- Find `displayTables()` function (line 189)
- In the table header creation section (line 204-230):
  - Create download button element: `<button class="download-button" title="Download as CSV">⬇</button>`
  - Position it in `tableLeft` div, between table info and remove button
  - Add click handler: `downloadButton.onclick = () => downloadTableCSV(table.name)`
- Update layout to use flexbox with gap for proper spacing

### 10. Add Download Button to Query Results Header
- Open `app/client/src/main.ts`
- Find `displayResults()` function (line 119)
- Modify the results header HTML (line 128-135):
  - Add download button between `<h2>` and toggle button
  - Button HTML: `<button id="download-results" class="download-button" title="Download results as CSV">⬇</button>`
- After setting `resultsSection.style.display = 'block'`:
  - Add click handler for download button
  - Store current query in a global variable or button data attribute
  - Call `downloadQueryResultsCSV(query, 'openai')` on click

### 11. Add CSS Styles for Download Button
- Open `app/client/src/style.css`
- Add `.download-button` class after `.remove-table-button` (around line 322):
  ```css
  .download-button {
    background: none;
    border: none;
    font-size: 1.25rem;
    color: var(--text-secondary);
    cursor: pointer;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    transition: all 0.2s;
  }

  .download-button:hover {
    background: rgba(13, 110, 253, 0.1);
    color: var(--primary-color);
  }
  ```

### 12. Create E2E Test File
- Read `.claude/commands/test_e2e.md` for test file format
- Read `.claude/commands/e2e/test_basic_query.md` for example structure
- Create `.claude/commands/e2e/test_csv_export.md` with:
  - User Story: Test CSV export functionality for tables and query results
  - Test Steps:
    1. Navigate to application
    2. Load sample users data
    3. Verify download button appears in table header (to the left of ×)
    4. Click download button for users table
    5. Verify CSV file downloads with correct filename "users.csv"
    6. Take screenshot of table with download button
    7. Enter query: "Show me all users"
    8. Click Query button
    9. Verify download button appears in results header (to the left of Hide)
    10. Click download button for query results
    11. Verify CSV file downloads with correct filename "query_results.csv"
    12. Take screenshot of results with download button
  - Success Criteria:
    - Download buttons appear in correct positions
    - Table CSV export works and contains correct data
    - Query results CSV export works and contains correct data
    - CSV files have correct filenames
    - No errors occur during export
    - Screenshots show download buttons in correct positions

### 13. Run Manual Testing
- Start the application: `./scripts/start.sh`
- Upload sample data (users.json)
- Test table export:
  - Verify download button appears to the left of × button
  - Click download button
  - Verify users.csv downloads with correct data
- Test query result export:
  - Enter query: "Show me all users"
  - Click Query button
  - Verify download button appears to the left of Hide button
  - Click download button
  - Verify query_results.csv downloads with correct data
- Test edge cases:
  - Empty query results
  - Large tables (if available)
  - Special characters in data

### 14. Run Validation Commands
- Execute all validation commands to ensure zero regressions
- See "Validation Commands" section below

## Testing Strategy

### Unit Tests
- **CSV Generation Function Tests**:
  - Empty results → should return CSV with headers only
  - Single row → should return headers + 1 data row
  - Multiple rows → should return headers + multiple data rows
  - Special characters (quotes, commas, newlines) → should properly escape
  - Null/None values → should render as empty strings
  - Various data types (int, float, string, date) → should format correctly

- **Table Export Endpoint Tests**:
  - Valid table name → should return 200 with CSV content
  - Invalid table name (SQL injection attempt) → should return 400
  - Non-existent table → should return 404
  - Empty table → should return CSV with headers only
  - Response headers → should have correct Content-Disposition and Content-Type

- **Query Export Endpoint Tests**:
  - Valid query → should return 200 with CSV content
  - Invalid query → should return appropriate error
  - Query with no results → should return CSV with headers only
  - Complex query with joins → should export correctly
  - Response headers → should have correct Content-Disposition and Content-Type

### Edge Cases
- Tables or queries with no data (empty CSV with headers only)
- Large result sets (10,000+ rows) - ensure streaming works efficiently
- Column names with special characters
- Data containing quotes, commas, newlines (proper CSV escaping)
- Non-ASCII characters (UTF-8 encoding)
- Very long column values (truncation or wrapping)
- Table names with SQL injection attempts (should be blocked)
- Concurrent export requests (multiple users downloading simultaneously)
- Browser compatibility for download (Chrome, Firefox, Safari, Edge)

## Acceptance Criteria
- Download button appears in table header, directly to the left of × button
- Download button appears in query results header, directly to the left of Hide button
- Clicking table download button exports entire table as CSV file
- Clicking query results download button exports current results as CSV file
- CSV files have correct filenames (table_name.csv, query_results.csv)
- CSV files are properly formatted with headers and data rows
- Special characters in data are properly escaped
- Empty results produce CSV files with headers only
- All backend endpoints return appropriate HTTP status codes and error messages
- Frontend displays error messages if export fails
- No SQL injection vulnerabilities in table or query exports
- All existing functionality continues to work (zero regressions)
- E2E test validates complete workflow end-to-end
- All unit tests pass
- TypeScript compilation succeeds
- Frontend build succeeds

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_csv_export.md` test file to validate this functionality works
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Implementation Details
- Use Python's built-in `csv` module for CSV generation (no external dependencies)
- Use `io.StringIO` to generate CSV in memory before streaming
- FastAPI's `StreamingResponse` efficiently handles file streaming without loading entire file in memory
- Browser download is triggered using blob URLs and temporary anchor elements
- Download icons use Unicode character ⬇ (U+2B07) for consistency without requiring icon libraries

### CSV Format Specification
- RFC 4180 compliant CSV format
- UTF-8 encoding for proper international character support
- Header row contains column names
- Values containing commas, quotes, or newlines are enclosed in double quotes
- Double quotes within values are escaped as two double quotes ("")
- Empty/null values are rendered as empty strings

### Security Considerations
- Table names are validated using existing `validate_identifier()` function to prevent SQL injection
- Query export reuses existing `/api/query` security logic (safe SQL generation and execution)
- All database operations use parameterized queries via `execute_query_safely()`
- No raw SQL concatenation with user input
- File downloads use Content-Disposition header to prevent XSS attacks

### Future Enhancements (Not in Scope)
- Support for other export formats (JSON, Excel, Parquet)
- Configurable filename for query result exports
- Export progress indicator for large datasets
- Pagination for extremely large exports
- Column selection (export subset of columns)
- Export with filters (date range, row limits)
- Scheduled/automated exports
- Compression (zip) for large files

### Dependencies
- No new backend dependencies required (csv module is built-in)
- No new frontend dependencies required (uses native browser APIs)
- Existing dependencies are sufficient for this feature
