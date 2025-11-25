# Feature: CSV Export for Tables and Query Results

## Feature Description
This feature adds one-click CSV export functionality for both database tables and query results. Users can download tables and query results as CSV files with a single button click, making data analysis and sharing more convenient. Two new download buttons will be added to the UI:
- A download button next to the 'x' (remove) icon for available tables
- A download button next to the 'Hide' button for query results

Both download buttons will use appropriate download icons to provide clear visual affordance.

## User Story
As a user
I want to export tables and query results as CSV files with one click
So that I can analyze data in spreadsheet applications, share results with colleagues, and preserve query outputs for later reference

## Problem Statement
Currently, users can query data and view results in the browser, but there's no way to export this data for use in external tools. Users need to:
- Export entire database tables for offline analysis
- Save query results for reporting and sharing
- Work with data in familiar spreadsheet applications like Excel, Google Sheets, or data analysis tools

Without export functionality, users are limited to viewing data within the application interface, which restricts collaboration and external analysis workflows.

## Solution Statement
Implement a comprehensive CSV export system with two new FastAPI endpoints:
1. `GET /api/table/{table_name}/export` - Exports entire database tables as CSV
2. `POST /api/query/export` - Exports query results as CSV (accepts the same parameters as the query endpoint)

Add download buttons to the frontend:
1. Table download button - positioned to the left of the 'x' icon in the table header
2. Query result download button - positioned to the left of the 'Hide' button in the results header

The solution uses Python's built-in CSV module for backend CSV generation and browser download APIs for frontend delivery. All exports maintain proper SQL security through the existing `sql_security` module.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` (lines 1-280) - Main FastAPI application where new export endpoints will be added
  - Contains existing endpoint patterns (`/api/upload`, `/api/query`, `/api/schema`, etc.)
  - Shows proper error handling, logging, and response model patterns
  - Uses `sql_security` module for safe SQL operations

- `app/server/core/data_models.py` (lines 1-82) - Pydantic models for request/response validation
  - Need to add new models for export functionality
  - Contains existing patterns for QueryRequest, QueryResponse, etc.

- `app/server/core/sql_security.py` - SQL injection protection module
  - Contains `validate_identifier()` for validating table/column names
  - Contains `execute_query_safely()` for safe SQL execution
  - Contains `check_table_exists()` for table validation

- `app/server/core/sql_processor.py` - SQL execution utilities
  - Contains `execute_sql_safely()` for query execution
  - Contains `get_database_schema()` for schema retrieval

- `app/client/src/main.ts` (lines 1-423) - Main frontend application logic
  - Contains `displayResults()` function (lines 119-154) where query results are rendered
  - Contains `displayTables()` function (lines 189-258) where table items are rendered
  - Contains patterns for API calls and button event handlers

- `app/client/src/api/client.ts` (lines 1-79) - API client for backend communication
  - Contains `api` object with methods for all endpoints
  - Shows pattern for apiRequest helper function
  - Need to add new export API methods

- `app/client/src/types.d.ts` (lines 1-80) - TypeScript type definitions
  - Contains interfaces matching backend Pydantic models
  - Need to add types for export responses

- `app/client/index.html` (lines 1-99) - HTML structure
  - Line 32: Results section with toggle button (where query export button goes)
  - Lines 39-44: Tables section structure (where table export buttons go)

- `app/client/src/style.css` - Styling for the application
  - Contains button styles (`.primary-button`, `.secondary-button`, etc.)
  - Contains layout styles for `.table-header`, `.results-header`

- `README.md` (lines 129-135) - API documentation section
  - Need to document the two new export endpoints

- `app/server/tests/test_sql_injection.py` - Security testing patterns
  - Shows how to write security tests for SQL operations
  - Pattern for testing with malicious inputs

### New Files

- `app/server/core/csv_exporter.py` - CSV export utility module
  - Function to convert query results to CSV format
  - Function to validate and export table data
  - Proper error handling and security validation

- `app/server/tests/test_csv_export.py` - Unit tests for CSV export functionality
  - Test table export with valid table names
  - Test query result export
  - Test error handling (invalid tables, SQL injection attempts)
  - Test CSV format validation
  - Test empty result handling

- `.claude/commands/e2e/test_csv_export.md` - E2E test for CSV export feature
  - Test table export download
  - Test query result export download
  - Verify file downloads work correctly
  - Verify CSV content is properly formatted
  - Should follow patterns from `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_complex_query.md`

## Implementation Plan

### Phase 1: Foundation
Create the core CSV export infrastructure in the backend:
1. Implement CSV generation utilities in a new `csv_exporter.py` module
2. Add Pydantic models for export requests/responses
3. Implement comprehensive unit tests for CSV export logic
4. Ensure all CSV operations use proper SQL security validation

### Phase 2: Core Implementation
Implement the API endpoints and integrate with existing backend:
1. Create `GET /api/table/{table_name}/export` endpoint for table exports
2. Create `POST /api/query/export` endpoint for query result exports
3. Add error handling and logging following existing patterns
4. Test endpoints with various data types and edge cases

### Phase 3: Integration
Build the frontend download functionality and connect to backend:
1. Add download icon buttons to the UI (tables and query results)
2. Implement client-side download logic using browser download APIs
3. Add API client methods for export endpoints
4. Style the download buttons to match existing design
5. Create and execute E2E tests to validate end-to-end functionality

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create CSV Export Utility Module
- Create `app/server/core/csv_exporter.py` with:
  - `export_table_to_csv(table_name: str) -> str` - Validates table and returns CSV string
  - `export_query_results_to_csv(results: List[Dict[str, Any]], columns: List[str]) -> str` - Converts results to CSV string
  - Both functions should use proper error handling and security validation
  - Use Python's `csv` module with `io.StringIO` for CSV generation
  - Validate table names using `validate_identifier()` from `sql_security`
  - Use `execute_query_safely()` for database queries

### Step 2: Add Export Data Models
- Update `app/server/core/data_models.py`:
  - Add `TableExportRequest` model (empty, path parameter only)
  - Add `QueryExportRequest` model (extends QueryRequest for POST body)
  - Both exports return `StreamingResponse` with CSV content, no response model needed

### Step 3: Create Unit Tests for CSV Export
- Create `app/server/tests/test_csv_export.py`:
  - Test `export_table_to_csv()` with valid table
  - Test `export_table_to_csv()` with invalid/nonexistent table
  - Test `export_query_results_to_csv()` with normal results
  - Test `export_query_results_to_csv()` with empty results
  - Test CSV format validation (proper headers, escaping, quoting)
  - Test SQL injection attempts in table names
  - Run tests with `cd app/server && uv run pytest tests/test_csv_export.py -v`

### Step 4: Implement Table Export Endpoint
- Add endpoint to `app/server/server.py`:
  - `GET /api/table/{table_name}/export`
  - Validate table name using `validate_identifier()`
  - Check table exists using `check_table_exists()`
  - Call `export_table_to_csv(table_name)`
  - Return `StreamingResponse` with CSV content
  - Set headers: `Content-Disposition: attachment; filename="{table_name}.csv"`
  - Set `media_type="text/csv"`
  - Add proper error handling and logging

### Step 5: Implement Query Export Endpoint
- Add endpoint to `app/server/server.py`:
  - `POST /api/query/export`
  - Accept `QueryRequest` body (same as `/api/query`)
  - Generate SQL using existing `generate_sql()` logic
  - Execute query using `execute_sql_safely()`
  - Call `export_query_results_to_csv(results, columns)`
  - Return `StreamingResponse` with CSV content
  - Set headers: `Content-Disposition: attachment; filename="query_results_{timestamp}.csv"`
  - Add proper error handling and logging

### Step 6: Test Backend Endpoints
- Run server tests: `cd app/server && uv run pytest -v`
- Verify all tests pass with zero failures
- Manually test endpoints using curl or browser if needed

### Step 7: Add Frontend Export API Methods
- Update `app/client/src/api/client.ts`:
  - Add `exportTable(tableName: string): Promise<Blob>` method
  - Add `exportQueryResults(request: QueryRequest): Promise<Blob>` method
  - Both methods fetch from respective endpoints and return blob data
  - Handle errors appropriately

### Step 8: Add Frontend TypeScript Types
- Update `app/client/src/types.d.ts`:
  - Add any necessary types for export functionality (if needed)
  - Ensure types match backend models

### Step 9: Implement Table Download Button
- Update `app/client/src/main.ts` in the `displayTables()` function:
  - Add download button element to table header
  - Position button to the left of the remove (×) button
  - Use download icon (📥 or use an SVG icon)
  - Add click handler that calls `api.exportTable(tableName)`
  - Create blob URL and trigger browser download
  - Clean up blob URL after download
  - Add error handling with `displayError()`

### Step 10: Implement Query Results Download Button
- Update `app/client/src/main.ts` in the `displayResults()` function:
  - Add download button element to results header
  - Position button to the left of the 'Hide' button
  - Use download icon (📥 or use an SVG icon)
  - Store the current query and request in closure/variable
  - Add click handler that calls `api.exportQueryResults()`
  - Create blob URL and trigger browser download
  - Clean up blob URL after download
  - Add error handling with `displayError()`

### Step 11: Style Download Buttons
- Update `app/client/src/style.css`:
  - Add styles for `.download-button` class
  - Ensure buttons match existing design system
  - Add hover states and transitions
  - Ensure proper spacing with adjacent buttons
  - Make buttons responsive and accessible

### Step 12: Create E2E Test File
- Create `.claude/commands/e2e/test_csv_export.md`:
  - Follow pattern from `test_basic_query.md` and `test_complex_query.md`
  - Include User Story section
  - Add Test Steps:
    1. Navigate to application
    2. Upload sample data or use existing table
    3. Click table download button
    4. Verify CSV file downloads
    5. Execute a query
    6. Click query result download button
    7. Verify CSV file downloads
    8. Take screenshots at key steps
  - Add Success Criteria
  - Specify 4-5 screenshots to validate functionality

### Step 13: Run Validation Commands
- Execute all validation commands as specified in the "Validation Commands" section below
- Read `.claude/commands/test_e2e.md` to understand E2E test execution
- Execute the new E2E test `.claude/commands/e2e/test_csv_export.md`
- Ensure all tests pass with zero failures
- Fix any issues that arise

### Step 14: Update Documentation
- Update `README.md` API Endpoints section:
  - Add `GET /api/table/{table_name}/export` - Export table as CSV
  - Add `POST /api/query/export` - Export query results as CSV
- Verify documentation is clear and accurate

## Testing Strategy

### Unit Tests
1. **CSV Generation Tests** (`test_csv_export.py`)
   - Test CSV formatting with various data types (strings, numbers, dates, nulls)
   - Test proper CSV escaping (quotes, commas, newlines in data)
   - Test CSV headers match column names
   - Test empty results generate valid CSV with headers only

2. **Security Tests** (`test_csv_export.py`)
   - Test SQL injection attempts in table names
   - Test invalid table names (special characters, SQL keywords)
   - Test nonexistent table handling
   - Test unauthorized access patterns

3. **Backend Integration Tests** (`test_csv_export.py`)
   - Test table export endpoint with valid table
   - Test table export endpoint with invalid table (404 error)
   - Test query export endpoint with valid query
   - Test query export endpoint with malicious query
   - Test response headers (Content-Type, Content-Disposition)
   - Test file naming conventions

4. **Frontend Tests**
   - Frontend type checking: `cd app/client && bun tsc --noEmit`
   - Frontend build validation: `cd app/client && bun run build`

### Edge Cases
1. **Empty Data**
   - Export table with zero rows
   - Export query that returns no results
   - Verify CSV has headers but no data rows

2. **Special Characters in Data**
   - Data containing commas
   - Data containing quotes
   - Data containing newlines
   - Unicode characters and emojis
   - Verify proper CSV escaping

3. **Large Datasets**
   - Export table with many rows (stress test)
   - Export table with many columns (wide tables)
   - Verify memory efficiency with streaming

4. **Data Type Handling**
   - NULL values (should be empty string in CSV)
   - Boolean values (TRUE/FALSE representation)
   - Dates and timestamps (proper formatting)
   - Floating point numbers (precision)

5. **Error Scenarios**
   - Table deleted between viewing and exporting
   - Database connection errors during export
   - Malformed query in export request
   - Very long table/column names

6. **Browser Compatibility**
   - Test download in different browsers (if possible)
   - Test blob URL cleanup
   - Test multiple rapid downloads

## Acceptance Criteria
1. ✅ Two new API endpoints created and functional:
   - `GET /api/table/{table_name}/export` returns CSV file
   - `POST /api/query/export` returns CSV file

2. ✅ Download button appears next to 'x' icon for each table in Available Tables section

3. ✅ Download button appears next to 'Hide' button in Query Results section

4. ✅ Both download buttons use appropriate download icons

5. ✅ Clicking table download button triggers immediate CSV download with filename `{table_name}.csv`

6. ✅ Clicking query result download button triggers immediate CSV download with filename `query_results_{timestamp}.csv`

7. ✅ CSV files are properly formatted with:
   - Headers matching column names
   - Proper escaping of special characters (quotes, commas, newlines)
   - UTF-8 encoding

8. ✅ All SQL operations use proper security validation via `sql_security` module

9. ✅ Error handling displays user-friendly messages for:
   - Nonexistent tables
   - Invalid table names
   - Query failures
   - Database errors

10. ✅ All existing functionality remains working (zero regressions)

11. ✅ Unit tests achieve >90% code coverage for CSV export logic

12. ✅ E2E test validates complete user workflow for both export types

13. ✅ Documentation updated with new endpoints in README.md

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md` to understand how to execute E2E tests
- Read and execute `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works end-to-end with screenshots proving the feature works
- `cd app/server && uv run pytest` - Run all server tests including new CSV export tests to validate zero regressions
- `cd app/server && uv run pytest tests/test_csv_export.py -v` - Run CSV export specific tests with verbose output
- `cd app/client && bun tsc --noEmit` - Run TypeScript type checking to validate zero frontend type errors
- `cd app/client && bun run build` - Build frontend to validate the feature builds successfully with zero errors

## Notes

### CSV Library Choice
Use Python's built-in `csv` module with `csv.DictWriter` for robust CSV generation. This handles proper escaping, quoting, and encoding automatically.

### Streaming Response
Use FastAPI's `StreamingResponse` for CSV downloads:
```python
from fastapi.responses import StreamingResponse
import io

csv_content = export_table_to_csv(table_name)
return StreamingResponse(
    io.StringIO(csv_content),
    media_type="text/csv",
    headers={"Content-Disposition": f"attachment; filename={table_name}.csv"}
)
```

### Frontend Download Implementation
Use the browser's download API:
```typescript
const blob = await api.exportTable(tableName);
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = `${tableName}.csv`;
a.click();
window.URL.revokeObjectURL(url);
```

### Security Considerations
- All table names MUST be validated using `validate_identifier()`
- Never concatenate table names directly into SQL
- Use `execute_query_safely()` for all database operations
- Limit export size if needed (future enhancement)

### Icon Recommendations
Use Unicode download emoji (📥) or Material Design Icons:
- Download icon: `⬇` or `📥`
- Alternative: Use SVG icon from a CDN like Heroicons or Lucide

### File Naming Convention
- Tables: `{table_name}.csv`
- Query Results: `query_results_{YYYYMMDD_HHMMSS}.csv`
- Use ISO 8601 format for timestamps

### Future Enhancements
Consider for future iterations (NOT part of this feature):
- Export to JSON format
- Export to Excel (XLSX)
- Pagination for very large exports
- Export with filters/limits
- Scheduled/automated exports
- Email export functionality
