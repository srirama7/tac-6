# Feature: CSV Export for Tables and Query Results

## Feature Description
This feature adds one-click CSV export functionality to the Natural Language SQL Interface application. Users will be able to export both:
1. **Table data**: Download complete table contents as CSV files with a download button next to each table's remove (×) button
2. **Query results**: Download query results as CSV files with a download button next to the "Hide" button in the results section

The feature enhances data portability and allows users to easily extract and share their data or analysis results.

## User Story
As a user of the Natural Language SQL Interface
I want to export table data and query results as CSV files
So that I can analyze the data in external tools, share results with others, or create backups

## Problem Statement
Currently, users can view data in the web interface but have no way to export it for use in other applications. When users need to:
- Perform advanced analysis in Excel, Python, or R
- Share query results with colleagues
- Create backups of their uploaded data
- Generate reports from query results

They must manually copy-paste data or take screenshots, which is inefficient and error-prone, especially for large datasets.

## Solution Statement
We will implement two new API endpoints (`/api/export/table/{table_name}` and `/api/export/results`) that generate CSV files from database tables and query results. Download buttons will be strategically placed in the UI:
- Next to each table's remove (×) button for table exports
- Next to the "Hide" button in query results for result exports

The endpoints will use Python's built-in `csv` module to generate properly formatted CSV files with appropriate headers and Content-Disposition headers for browser downloads. The frontend will trigger downloads using blob URLs.

## Relevant Files
Use these files to implement the feature:

- **app/server/server.py** - Main FastAPI server file where new export endpoints will be added. Contains existing endpoints like `/api/upload`, `/api/query`, and `/api/table/{table_name}` that provide patterns for database interaction and response handling.

- **app/server/core/sql_security.py** - Security module for safe SQL execution. Must be used to validate table names and execute queries safely to prevent SQL injection attacks.

- **app/server/core/data_models.py** - Pydantic data models. May need new models for export requests/responses if we want structured responses with metadata.

- **app/client/src/main.ts** - Main client TypeScript file. Contains `displayTables()` function (line 189) where table UI is rendered and `displayResults()` function (line 119) where query results are displayed. Download buttons will be added to these sections.

- **app/client/src/api/client.ts** - API client with fetch helpers. New export API methods will be added here following the existing pattern.

- **app/client/src/types.d.ts** - TypeScript type definitions. May need types for export functionality if using structured responses.

- **app/client/src/style.css** - Application styles. Will need CSS for download button styling to match the existing design system.

- **app/client/index.html** - Main HTML structure. Shows the layout of tables (line 38-44) and results sections (line 28-36) where buttons will be added.

### New Files

- **.claude/commands/e2e/test_csv_export.md** - E2E test file to validate CSV export functionality for both tables and query results. Should follow the pattern of `.claude/commands/e2e/test_basic_query.md`.

## Implementation Plan

### Phase 1: Foundation
1. **Research CSV export patterns**: Review how Python's `csv` module works with SQLite data and how to properly set HTTP headers for file downloads
2. **Identify security requirements**: Ensure table name validation and safe query execution using existing `sql_security.py` patterns
3. **Design API contracts**: Define endpoint paths, request parameters, response formats, and error handling
4. **Select appropriate download icon**: Choose a download icon (e.g., ↓ or 📥) that matches the application's design aesthetic

### Phase 2: Core Implementation
1. **Backend endpoints**:
   - Implement `/api/export/table/{table_name}` endpoint to export entire table contents
   - Implement `/api/export/results` POST endpoint to export query results (accepts SQL query and returns CSV)
   - Use `execute_query_safely()` from `sql_security.py` for all database operations
   - Generate CSV content using Python's `csv` module with proper formatting
   - Set appropriate HTTP headers: `Content-Type: text/csv` and `Content-Disposition: attachment; filename="<name>.csv"`

2. **Frontend API client**:
   - Add `exportTable(tableName: string)` method to `api` object
   - Add `exportResults(sql: string)` method to `api` object
   - Handle blob creation and download triggering in the browser

3. **Frontend UI components**:
   - Add download button to table header (next to × button) in `displayTables()` function
   - Add download button to results header (next to "Hide" button) in `displayResults()` function
   - Style buttons to match existing UI design
   - Wire up click handlers to call export API methods

### Phase 3: Integration
1. **Test with existing data**: Verify exports work with all three sample data types (users.json, products.csv, events.jsonl)
2. **Test with query results**: Verify exports work with various query types (SELECT, aggregations, JOINs)
3. **Error handling**: Ensure graceful failures for non-existent tables, invalid queries, and network errors
4. **Cross-browser testing**: Verify download functionality works in Chrome, Firefox, Safari, and Edge
5. **E2E test creation**: Develop comprehensive E2E test to validate the feature end-to-end

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create E2E Test File
- Read `.claude/commands/test_e2e.md` and `.claude/commands/e2e/test_basic_query.md` to understand the E2E test format
- Create `.claude/commands/e2e/test_csv_export.md` with test steps to:
  - Upload sample data (users table)
  - Export the users table as CSV
  - Verify the CSV file downloads correctly with proper headers and data
  - Execute a query ("Show me all users")
  - Export the query results as CSV
  - Verify the query results CSV downloads correctly
  - Include success criteria and screenshot requirements

### Step 2: Backend - Add Table Export Endpoint
- Open `app/server/server.py`
- Import necessary modules: `csv`, `io`, and `StreamingResponse` from `fastapi.responses`
- Add `GET /api/export/table/{table_name}` endpoint after the existing `/api/table/{table_name}` DELETE endpoint (around line 277)
- Validate `table_name` using `validate_identifier()` from `sql_security.py`
- Check table exists using `check_table_exists()`
- Query all data using `execute_query_safely()` with SQL: `SELECT * FROM {table}`
- Generate CSV content using Python's `csv.DictWriter`
- Return `StreamingResponse` with:
  - `media_type="text/csv"`
  - `headers={"Content-Disposition": f"attachment; filename={table_name}.csv"}`
- Add comprehensive error handling with logging

### Step 3: Backend - Add Query Results Export Endpoint
- Open `app/server/server.py`
- Add new Pydantic model in `app/server/core/data_models.py`:
  ```python
  class ExportResultsRequest(BaseModel):
      sql: str
      filename: Optional[str] = "query_results"
  ```
- Add `POST /api/export/results` endpoint after the table export endpoint
- Accept `ExportResultsRequest` with SQL query and optional filename
- Execute SQL using `execute_sql_safely()` (reuse existing logic from `/api/query`)
- Generate CSV from results using `csv.DictWriter`
- Return `StreamingResponse` with appropriate headers
- Add error handling and logging

### Step 4: Frontend - Add Export API Methods
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string): Promise<Blob>` method to the `api` object
- Add `exportResults(sql: string, filename?: string): Promise<Blob>` method
- Both methods should:
  - Call respective backend endpoints
  - Return response as Blob
  - Handle errors appropriately

### Step 5: Frontend - Add Helper Function for Download Triggering
- Open `app/client/src/main.ts`
- Add utility function `downloadFile(blob: Blob, filename: string)` that:
  - Creates a blob URL using `URL.createObjectURL()`
  - Creates a temporary anchor element
  - Sets `href` to blob URL and `download` attribute to filename
  - Triggers click programmatically
  - Cleans up by revoking the blob URL

### Step 6: Frontend - Add Download Button to Tables
- Open `app/client/src/main.ts`
- Locate the `displayTables()` function (around line 189)
- In the table header section where the remove button is created (around line 223-227), add a download button
- Position it immediately to the left of the × button using flexbox
- Use download icon: "↓" or "⬇"
- Style with class `download-table-button`
- Add click handler that:
  - Calls `api.exportTable(table.name)`
  - Uses `downloadFile()` helper to trigger download
  - Shows loading state during export
  - Displays error message on failure
  - Success message optional (download starting is sufficient feedback)

### Step 7: Frontend - Add Download Button to Query Results
- Open `app/client/src/main.ts`
- Locate the `displayResults()` function (around line 119)
- Find where the results are displayed in the HTML template (around line 128-135)
- Add a download button to the results header, positioned to the left of the "Hide" button
- Store the SQL query in a data attribute or variable accessible to the download handler
- Style with class `download-results-button`
- Add click handler that:
  - Calls `api.exportResults(response.sql)` (SQL is available in the `response` parameter)
  - Uses `downloadFile()` helper to trigger download
  - Shows loading state during export
  - Displays error message on failure

### Step 8: Frontend - Add CSS Styling for Download Buttons
- Open `app/client/src/style.css`
- Add styles for `.download-table-button` and `.download-results-button`:
  - Match the style of existing buttons (use same border-radius, padding, transitions)
  - Use subtle background color (var(--border-color) or similar)
  - Add hover effects
  - Ensure proper spacing between download and adjacent buttons
  - Make buttons same height as adjacent buttons for visual consistency
  - Add cursor: pointer
  - Consider adding a tooltip on hover

### Step 9: Manual Testing - Backend Endpoints
- Start the server: `cd app/server && uv run python server.py`
- Test `/api/export/table/{table_name}` endpoint:
  - Upload sample users.json data via UI or API
  - Use curl or browser to access `http://localhost:8000/api/export/table/users`
  - Verify CSV downloads with correct headers and all data
  - Test with non-existent table (should return 404)
  - Test with invalid table name (should return 400)
- Test `/api/export/results` endpoint:
  - Use curl or Postman to POST to `http://localhost:8000/api/export/results`
  - Body: `{"sql": "SELECT * FROM users LIMIT 5"}`
  - Verify CSV downloads with query results
  - Test with invalid SQL (should return error)

### Step 10: Manual Testing - Frontend Integration
- Start both server and client: `./scripts/start.sh`
- Navigate to `http://localhost:5173`
- Upload sample data (users, products, events)
- Test table export:
  - Click download button on each table
  - Verify CSV files download with correct names
  - Open CSV files in Excel/text editor to verify content
  - Check for proper headers, data integrity, and formatting
- Test query results export:
  - Execute query: "Show me all users"
  - Click download button in results section
  - Verify CSV downloads with query results
  - Test with different query types (aggregations, filters, etc.)
- Test error handling:
  - Check console for any JavaScript errors
  - Verify error messages display appropriately

### Step 11: Run E2E Test
- Read `.claude/commands/test_e2e.md`
- Execute your E2E test: Follow the instructions to run `.claude/commands/e2e/test_csv_export.md`
- Verify all test steps pass
- Review screenshots to confirm UI elements are correctly positioned
- Address any failures by fixing the implementation and re-running the test

### Step 12: Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Fix any issues discovered during validation
- Re-run tests until all pass

## Testing Strategy

### Unit Tests
- **Backend Tests** (add to existing test files or create `app/server/tests/test_export.py`):
  - Test `/api/export/table/{table_name}` endpoint:
    - Valid table export returns CSV with correct format
    - Non-existent table returns 404
    - Invalid table name returns 400 with security error
    - CSV contains correct headers matching table schema
    - CSV contains all rows from table
  - Test `/api/export/results` endpoint:
    - Valid query returns CSV with results
    - Invalid SQL returns error response
    - Empty results return CSV with headers only
    - CSV formatting matches query column names
  - Test CSV generation:
    - Special characters (commas, quotes, newlines) are properly escaped
    - NULL values are handled correctly
    - Unicode characters are properly encoded

- **Frontend Tests** (if applicable):
  - Test download helper function creates and triggers downloads correctly
  - Test API client methods handle blob responses
  - Test error handling for failed exports

### Edge Cases
- **Empty tables**: Export should produce CSV with headers only
- **Large tables**: Test with 1000+ rows to ensure performance is acceptable and no memory issues
- **Special characters**: Table/column names and data containing commas, quotes, newlines, Unicode
- **NULL values**: Ensure NULLs are represented appropriately in CSV (empty string or "NULL")
- **SQL injection attempts**: Validate that security measures prevent injection through table names
- **Network failures**: Frontend should handle failed API calls gracefully
- **Concurrent downloads**: Multiple simultaneous downloads should work without conflicts
- **Browser compatibility**: Test download triggering in different browsers
- **Long filenames**: Ensure table names with maximum length don't break downloads
- **Query errors**: Invalid queries in export results should return appropriate errors

## Acceptance Criteria
- ✅ Two new backend endpoints (`/api/export/table/{table_name}` and `/api/export/results`) are implemented and functional
- ✅ Download button appears next to the × button for each table in the Available Tables section
- ✅ Download button appears next to the "Hide" button in the Query Results section
- ✅ Clicking a table's download button exports the complete table data as a CSV file
- ✅ Clicking the query results download button exports the current query results as a CSV file
- ✅ Downloaded CSV files have appropriate filenames (table name or "query_results.csv")
- ✅ CSV files contain proper headers matching column names
- ✅ CSV files contain all data rows with correct formatting
- ✅ Special characters in data (commas, quotes, newlines) are properly escaped
- ✅ Export functionality works for all sample data types (users, products, events)
- ✅ Error handling works correctly (non-existent tables, invalid queries, network errors)
- ✅ Download buttons are styled consistently with the existing UI
- ✅ SQL injection protection is maintained using existing security patterns
- ✅ All existing tests continue to pass (zero regressions)
- ✅ New E2E test validates the complete workflow
- ✅ CSV files open correctly in Excel, Google Sheets, and text editors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_csv_export.md` test file to validate this functionality works
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Implementation Details
- Use Python's built-in `csv` module with `csv.DictWriter` for reliable CSV generation
- Use `io.StringIO` to create in-memory CSV content before streaming
- Frontend blob downloads use `URL.createObjectURL()` and programmatic anchor clicks (standard pattern)
- Filename sanitization may be needed to prevent path traversal issues (stick to table name validation)

### Security Considerations
- All table name parameters must be validated using `validate_identifier()` before use
- Use `execute_query_safely()` and `check_table_exists()` from `sql_security.py`
- Never concatenate user input directly into SQL queries
- Validate that export results endpoint only accepts SELECT queries (read-only)
- Consider rate limiting for export endpoints to prevent abuse

### Performance Considerations
- For very large tables (10,000+ rows), consider:
  - Streaming response to avoid loading entire result set into memory
  - Adding pagination or row limits to exports
  - Progress indicators on the frontend
- Current implementation should handle typical datasets (<10,000 rows) efficiently

### Future Enhancements (Not in Scope)
- Export format options (JSON, Excel, Parquet)
- Column selection for partial exports
- Export history/download manager
- Batch export multiple tables
- Scheduled/automated exports
- Compression for large exports (gzip)

### Browser Compatibility
- The blob download approach works in all modern browsers (Chrome, Firefox, Safari, Edge)
- IE11 is not supported (application uses modern JavaScript)

### CSV Format Standards
- Use RFC 4180 CSV standard (handled by Python's csv module)
- UTF-8 encoding for Unicode support
- CRLF line endings
- Quoted fields for values containing commas, quotes, or newlines
