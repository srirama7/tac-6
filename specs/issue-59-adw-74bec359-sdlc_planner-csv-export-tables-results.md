# Feature: CSV Export for Tables and Query Results

## Metadata
issue_number: `59`
adw_id: `74bec359`
issue_json: `{"number":59,"title":"ten","body":"Using adw_plan_build_review add one click table exports and one click result export feature to get results as csv files.\n\nCreate two new endpoints to support these features. One exporting tables, one for exporting query results.\n\nPlace a download button directly to the left of the 'x' icon for available tables.\nPlace a download button directly to the left of the 'hide' button for query results.\n\nUse the appropriate download icon.\n"}`

## Feature Description
This feature adds one-click CSV export functionality to the Natural Language SQL Interface application. Users will be able to:
1. Export any available table directly to a CSV file by clicking a download button next to the table's remove (×) button
2. Export query results to a CSV file by clicking a download button next to the "Hide" button in the results section

This provides users with a convenient way to extract their data for use in other applications like Excel, Google Sheets, or other data analysis tools.

## User Story
As a user of the Natural Language SQL Interface
I want to export tables and query results as CSV files with one click
So that I can use my data in external applications and share results easily

## Problem Statement
Currently, users can upload data, query it, and view results, but there is no way to export the data back out of the application. This limits the utility of the tool since users may want to:
- Save query results for reporting
- Share data with colleagues
- Import results into other applications
- Create backups of their table data

## Solution Statement
Implement two new API endpoints and corresponding UI download buttons:
1. `GET /api/export/table/{table_name}` - Exports a full table as CSV
2. `POST /api/export/query-results` - Exports query results as CSV

The frontend will add download icon buttons:
- In the table item header, directly to the left of the × (remove) button
- In the results section header, directly to the left of the "Hide" button

Both buttons will trigger downloads using the browser's native file download functionality via blob URLs.

## Relevant Files
Use these files to implement the feature:

### Server Files
- `app/server/server.py` - Main FastAPI server with existing endpoints; add new export endpoints here
- `app/server/core/data_models.py` - Pydantic models for request/response validation; add new models for export
- `app/server/core/sql_security.py` - Security utilities for safe SQL execution; use for table validation
- `app/server/core/sql_processor.py` - SQL execution utilities; use `execute_sql_safely` for table queries

### Client Files
- `app/client/src/main.ts` - Main TypeScript application; add download button creation and click handlers
- `app/client/src/api/client.ts` - API client module; add export API methods
- `app/client/src/types.d.ts` - TypeScript type definitions; add types for export requests
- `app/client/index.html` - HTML structure; add download button element in results header
- `app/client/src/style.css` - CSS styles; add download button styling

### Test Files
- `app/server/tests/` - Server tests directory; add tests for export endpoints

### Documentation Files
- `.claude/commands/test_e2e.md` - E2E test runner documentation
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test structure

### New Files
- `app/server/tests/test_export.py` - Unit tests for export endpoints
- `.claude/commands/e2e/test_csv_export.md` - E2E test file for CSV export functionality

## Implementation Plan
### Phase 1: Foundation
1. Define Pydantic models for export functionality in `data_models.py`
2. Add TypeScript types for export in `types.d.ts`
3. Create CSS styles for download buttons in `style.css`

### Phase 2: Core Implementation
1. Implement `GET /api/export/table/{table_name}` endpoint in `server.py`
   - Validate table name using security module
   - Query all data from the table
   - Convert to CSV using pandas
   - Return as StreamingResponse with appropriate headers
2. Implement `POST /api/export/query-results` endpoint in `server.py`
   - Accept results array and columns array in request body
   - Convert to CSV using pandas
   - Return as StreamingResponse with appropriate headers
3. Add API client methods in `client.ts`
4. Implement download button creation and handlers in `main.ts`

### Phase 3: Integration
1. Add download button to table items (left of × button)
2. Add download button to results header (left of Hide button)
3. Wire up click handlers to trigger downloads
4. Add unit tests for server endpoints
5. Create E2E test for export functionality

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create E2E Test File
- Create `.claude/commands/e2e/test_csv_export.md` with test steps to validate:
  - Download button appears next to × icon for tables
  - Download button appears next to Hide button for results
  - Clicking table download button triggers file download
  - Clicking results download button triggers file download
  - Downloaded CSV files contain expected data

### Step 2: Add Pydantic Models for Export
- In `app/server/core/data_models.py`:
  - Add `ExportQueryResultsRequest` model with fields:
    - `results: List[Dict[str, Any]]` - The query results to export
    - `columns: List[str]` - Column names for CSV header
    - `filename: Optional[str]` - Optional custom filename (default: "query_results.csv")

### Step 3: Implement Table Export Endpoint
- In `app/server/server.py`:
  - Add import for `StreamingResponse` from `fastapi.responses`
  - Add import for `io` module
  - Add `GET /api/export/table/{table_name}` endpoint:
    - Validate table_name using `validate_identifier()`
    - Check table exists using `check_table_exists()`
    - Execute `SELECT * FROM [table_name]` safely
    - Convert results to pandas DataFrame
    - Export DataFrame to CSV string using `df.to_csv(index=False)`
    - Return `StreamingResponse` with:
      - `media_type="text/csv"`
      - `headers={"Content-Disposition": f"attachment; filename={table_name}.csv"}`

### Step 4: Implement Query Results Export Endpoint
- In `app/server/server.py`:
  - Add `POST /api/export/query-results` endpoint:
    - Accept `ExportQueryResultsRequest` body
    - Create pandas DataFrame from results and columns
    - Export DataFrame to CSV string
    - Return `StreamingResponse` with appropriate headers and filename

### Step 5: Add Server Unit Tests
- Create `app/server/tests/test_export.py`:
  - Test table export with valid table name
  - Test table export with invalid/nonexistent table
  - Test query results export with valid data
  - Test query results export with empty results
  - Test CSV format correctness (headers, data integrity)

### Step 6: Add CSS Styles for Download Button
- In `app/client/src/style.css`:
  - Add `.download-button` class styled similarly to `.remove-table-button`:
    - Same dimensions (2rem × 2rem)
    - No background, no border
    - Color: `var(--text-secondary)`
    - Hover: blue tint with `var(--primary-color)`
    - Cursor: pointer
    - Margin-right for spacing from × button
  - Add `.download-results-button` class for results header button:
    - Similar to `.toggle-button` sizing
    - Appropriate spacing

### Step 7: Add TypeScript Types
- In `app/client/src/types.d.ts`:
  - Add `ExportQueryResultsRequest` interface matching the Pydantic model

### Step 8: Add API Client Methods
- In `app/client/src/api/client.ts`:
  - Add `exportTable(tableName: string): Promise<Blob>` method:
    - Fetch from `/api/export/table/${tableName}`
    - Return response as blob
  - Add `exportQueryResults(request: ExportQueryResultsRequest): Promise<Blob>` method:
    - POST to `/api/export/query-results`
    - Return response as blob

### Step 9: Add Download Helper Function
- In `app/client/src/main.ts`:
  - Add `downloadBlob(blob: Blob, filename: string)` helper function:
    - Create object URL from blob
    - Create temporary anchor element
    - Set href and download attributes
    - Trigger click
    - Revoke object URL

### Step 10: Add Download Button to Table Items
- In `app/client/src/main.ts` in the `displayTables()` function:
  - Create download button element before the remove button:
    - Class: `download-button`
    - Title: `Download as CSV`
    - Inner HTML: Download icon SVG (⬇ or appropriate icon)
  - Add click handler that calls `downloadTableAsCSV(table.name)`
  - Append download button to `tableHeader` before `removeButton`
- Add `downloadTableAsCSV(tableName: string)` async function:
  - Call `api.exportTable(tableName)`
  - Call `downloadBlob()` with result and `${tableName}.csv`
  - Handle errors with `displayError()`

### Step 11: Add Download Button to Results Header
- In `app/client/index.html`:
  - Add a download button element with id `download-results` directly before the `toggle-results` button:
    ```html
    <button id="download-results" class="toggle-button download-results-button" title="Download as CSV">⬇</button>
    ```
- In `app/client/src/main.ts`:
  - Store current query results and columns in module-level variables
  - In `displayResults()` function:
    - Store results and columns for later use
    - Get download button by id
    - Add click handler that calls `downloadQueryResultsAsCSV()`
- Add `downloadQueryResultsAsCSV()` async function:
  - Call `api.exportQueryResults()` with stored results/columns
  - Call `downloadBlob()` with result and `query_results.csv`
  - Handle errors with `displayError()`

### Step 12: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` E2E test

## Testing Strategy
### Unit Tests
- Test `GET /api/export/table/{table_name}`:
  - Returns 200 with valid CSV for existing table
  - Returns 404 or error for nonexistent table
  - Returns error for invalid table name (SQL injection attempt)
  - CSV contains correct headers and data
- Test `POST /api/export/query-results`:
  - Returns 200 with valid CSV for valid request
  - Handles empty results array
  - CSV matches input data exactly
  - Custom filename is respected

### Edge Cases
- Table with special characters in name (should be sanitized)
- Empty table (0 rows)
- Table with many columns
- Query results with null/None values
- Query results with special characters in data
- Very large result sets (streaming should handle efficiently)
- Concurrent export requests

## Acceptance Criteria
- Download button appears directly to the left of the × icon for each table in the Available Tables section
- Download button appears directly to the left of the Hide button in the Query Results section
- Clicking table download button downloads a CSV file named `{table_name}.csv`
- Clicking results download button downloads a CSV file named `query_results.csv`
- Downloaded CSV files are properly formatted with headers and data
- Download buttons use an appropriate download icon
- All existing functionality continues to work (no regressions)
- Server unit tests pass
- E2E tests pass

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/test_export.py -v` - Run export-specific tests
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature compiles correctly
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` E2E test to validate CSV export functionality works

## Notes
- The pandas library is already available in the server dependencies and can export DataFrames to CSV natively with `df.to_csv()`
- FastAPI's `StreamingResponse` is used for efficient file downloads without loading entire file into memory
- The download icon can be a simple Unicode character (⬇) or an SVG icon for better visual consistency
- Consider adding a loading state to download buttons while the export is in progress
- Future enhancements could include:
  - Export to other formats (JSON, Excel)
  - Custom filename input
  - Column selection for partial exports
  - Export format options (delimiter, encoding)
