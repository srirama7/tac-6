# Feature: CSV Export for Tables and Query Results

## Metadata
issue_number: `54`
adw_id: `845e6682`
issue_json: `{"number":54,"title":"tac6six","body":"Using adw_plan_build_review add one click table exports and one click result export feature to get results as csv files.\n\nCreate two new endpoints to support these features. One exporting tables, one for exporting query results.\n\nPlace a download button directly to the left of the 'x' icon for available tables.\nPlace a download button directly to the left of the 'hide' button for query results.\n\nUse the appropriate download icon.","state":"OPEN","author":{"id":"U_kgDOCDKQYA","login":"srirama7","name":"Amogha Bhat M R","is_bot":false},"assignees":[],"labels":[],"milestone":null,"comments":[{"id":"IC_kwDOQXQFdM7VYtgf","author":{"id":null,"login":"srirama7","name":null,"is_bot":false},"body":"## 📊 ADW Workflow Complete - Issue #54\n\n### Summary\nThe CSV export feature has been successfully implemented and tested.\n\n### Artifacts\n- **Branch:** `feature-issue-54-adw-b3a1bde8-csv-export-tables-results`\n- **ADW ID:** `b3a1bde8`\n- **Pull Request:** https://github.com/srirama7/tac-6/pull/55\n\n### Implementation Details\n- **Backend Endpoints:**\n  - `GET /api/table/{table_name}/export` - Export table data as CSV\n  - `POST /api/query/export` - Export query results as CSV\n\n- **Frontend:**\n  - Download buttons for each table in Available Tables section\n  - Download button in Query Results section\n\n### Test Results\n- ✅ 21 unit tests passed\n- ✅ CSV format validation\n- ✅ UTF-8 encoding with BOM\n- ✅ SQL injection protection\n- ✅ Unicode character support\n\n### Phases Completed\n1. ✅ Planning - Implementation plan created\n2. ✅ Building - Code implemented\n3. ✅ Testing - All unit tests passed\n4. ✅ Review - PR created\n\n---\n🤖 *This workflow was automated by ADW (AI Developer Workflow)*","createdAt":"2025-11-26T08:14:56Z","updatedAt":null},{"id":"IC_kwDOQXQFdM7VZdLu","author":{"id":null,"login":"srirama7","name":null,"is_bot":false},"body":"## b3a1bde8_test_runner: 🧪 Test Results\n\n### Unit Tests: ✅ ALL PASSED (88/88)\n\n| Test Category | Tests | Status |\n|---------------|-------|--------|\n| File Processor Tests | 22 | ✅ Passed |\n| LLM Processor Tests | 16 | ✅ Passed |\n| SQL Processor Tests | 11 | ✅ Passed |\n| CSV Export Tests | 21 | ✅ Passed |\n| SQL Injection Tests | 18 | ✅ Passed |\n\n### Frontend Build: ✅ PASSED\n- TypeScript compilation: ✅ No errors\n- Vite production build: ✅ Successful\n\n### API Endpoints Verified: ✅\n- `GET /api/table/{table_name}/export` - Working correctly\n- `POST /api/query/export` - Working correctly\n- CSV files include proper UTF-8 BOM encoding for Excel compatibility\n\n### Summary\nAll tests pass and the CSV export feature is fully implemented and functional.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)","createdAt":"2025-11-26T08:54:30Z","updatedAt":null}],"createdAt":"2025-11-26T07:02:43Z","updatedAt":"2025-11-26T10:01:44Z","closedAt":null,"url":"https://github.com/srirama7/tac-6/issues/54"}`

## Feature Description
This feature adds one-click CSV export functionality to the Natural Language SQL Interface application, allowing users to export both entire database tables and query results as CSV files. The feature includes two new backend API endpoints for generating CSV data and frontend download buttons placed strategically next to table and result controls. CSV files will be properly formatted with UTF-8 encoding (with BOM for Excel compatibility), proper escaping for special characters, and full SQL injection protection.

## User Story
As a data analyst using the Natural Language SQL Interface
I want to export tables and query results as CSV files with a single click
So that I can analyze the data in spreadsheet applications like Excel, perform offline analysis, share data with colleagues, and create reports without manually copying data

## Problem Statement
Currently, users can view data in the web interface but have no way to export it for use in other tools. Users need to manually copy-paste data if they want to use it in spreadsheet applications, perform offline analysis, or share results with colleagues. This manual process is time-consuming, error-prone, and loses data formatting. There's a clear need for a streamlined export mechanism that preserves data integrity and works seamlessly with common spreadsheet applications.

## Solution Statement
Implement a comprehensive CSV export system with two new backend endpoints (`GET /api/table/{table_name}/export` for table export and `POST /api/query/export` for query results export) that generate properly formatted CSV files with UTF-8 encoding and BOM for Excel compatibility. Add download buttons in the frontend: one next to each table's remove button in the Available Tables section, and one next to the Hide button in the Query Results section. Use standard download icons (⬇) to maintain consistent UI. The implementation will leverage the existing SQL security infrastructure to prevent injection attacks and ensure safe data export.

## Relevant Files
Use these files to implement the feature:

- **Backend Core Files:**
  - `app/server/server.py` - Main FastAPI application where new export endpoints will be added
  - `app/server/core/data_models.py` - Pydantic models for request/response validation; will add export-related models
  - `app/server/core/sql_security.py` - SQL security utilities for safe table name validation and query execution
  - `app/server/core/sql_processor.py` - SQL execution functions; will be used to fetch table/query data safely

- **Frontend Files:**
  - `app/client/src/main.ts` - Main TypeScript file containing UI logic; will add download button handlers
  - `app/client/src/api/client.ts` - API client functions; will add export API methods
  - `app/client/src/types.d.ts` - TypeScript type definitions; will add export-related types
  - `app/client/src/style.css` - CSS styles; will add download button styling

- **Testing Files:**
  - `app/server/tests/core/test_sql_processor.py` - SQL processor tests; will add CSV export tests here or in new file
  - `app/server/tests/test_sql_injection.py` - SQL injection tests; will verify export endpoints are secure
  - `.claude/commands/test_e2e.md` - E2E test runner instructions
  - `.claude/commands/e2e/test_basic_query.md` - Example E2E test for reference

- **Documentation:**
  - `README.md` - Project documentation; will add CSV export endpoints to API documentation

### New Files
- `app/server/core/csv_exporter.py` - New module containing CSV generation logic with proper encoding, escaping, and security
- `app/server/tests/core/test_csv_exporter.py` - Comprehensive tests for CSV export functionality
- `.claude/commands/e2e/test_csv_export.md` - E2E test to validate CSV export feature works end-to-end

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for CSV export by building a secure CSV exporter module that handles data serialization, UTF-8 encoding with BOM (for Excel compatibility), proper CSV escaping for special characters (commas, quotes, newlines), and integrates with existing SQL security utilities. This module will be the foundation for both table and query result exports, ensuring consistent CSV formatting and security across both endpoints.

### Phase 2: Core Implementation
Implement the two new API endpoints in the FastAPI server:
1. `GET /api/table/{table_name}/export` - Validates table name, fetches all table data using secure SQL execution, converts to CSV format, and returns as downloadable file with proper headers
2. `POST /api/query/export` - Accepts query results data from frontend, converts to CSV format, and returns as downloadable file

Add comprehensive unit tests covering CSV formatting, encoding, special character handling, SQL injection protection, empty data handling, and Unicode support.

### Phase 3: Integration
Integrate CSV export functionality into the frontend by:
1. Adding download buttons in the UI with appropriate icons next to table remove buttons and query result hide buttons
2. Implementing API client methods for calling export endpoints
3. Adding click handlers that trigger downloads with proper filenames (table_name.csv or query_results.csv)
4. Styling download buttons to match existing UI design patterns
5. Creating an E2E test that validates the complete user flow from uploading data to exporting it as CSV

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create CSV Exporter Module
- Create `app/server/core/csv_exporter.py` with functions:
  - `generate_csv_from_data(data: List[Dict[str, Any]], columns: List[str]) -> str` - Converts data to CSV format with UTF-8 BOM
  - `export_table_to_csv(table_name: str) -> str` - Fetches table data and generates CSV
  - `export_query_results_to_csv(results: List[Dict[str, Any]], columns: List[str]) -> str` - Generates CSV from query results
- Implement proper CSV escaping for commas, quotes, newlines, and special characters
- Add UTF-8 BOM (`\ufeff`) at the start of CSV for Excel compatibility
- Use Python's `csv` module with appropriate quoting and dialect settings
- Integrate with `sql_security` module for safe table name validation and query execution

### Step 2: Add Backend Data Models
- Add to `app/server/core/data_models.py`:
  - `ExportQueryRequest(BaseModel)` - Model for POST /api/query/export with fields: results, columns, filename
  - Update type definitions as needed for export responses

### Step 3: Implement Table Export Endpoint
- Add `GET /api/table/{table_name}/export` endpoint in `app/server/server.py`:
  - Validate table name using `validate_identifier()` from sql_security
  - Check table exists using `check_table_exists()`
  - Fetch all table data using `execute_query_safely()`
  - Generate CSV using csv_exporter module
  - Return CSV as downloadable file with headers:
    - `Content-Type: text/csv; charset=utf-8`
    - `Content-Disposition: attachment; filename="{table_name}.csv"`
- Add comprehensive error handling and logging

### Step 4: Implement Query Export Endpoint
- Add `POST /api/query/export` endpoint in `app/server/server.py`:
  - Accept ExportQueryRequest with results and columns data
  - Generate CSV using csv_exporter module
  - Return CSV as downloadable file with headers:
    - `Content-Type: text/csv; charset=utf-8`
    - `Content-Disposition: attachment; filename="query_results.csv"`
- Add comprehensive error handling and logging

### Step 5: Create Backend Unit Tests
- Create `app/server/tests/core/test_csv_exporter.py` with tests for:
  - Basic CSV generation from simple data
  - CSV formatting with proper headers and rows
  - UTF-8 encoding with BOM verification
  - Special character escaping (commas in values, quotes, newlines)
  - Unicode character support (emojis, international characters)
  - Empty data handling (no rows, no columns)
  - SQL injection attempts in table names
  - Large dataset handling (performance)
  - NULL value handling
- Add tests in `app/server/tests/test_sql_injection.py` to verify:
  - Export endpoints reject malicious table names
  - CSV generation doesn't introduce injection vulnerabilities
- Run tests: `cd app/server && uv run pytest tests/core/test_csv_exporter.py -v`

### Step 6: Add Frontend API Client Methods
- Add to `app/client/src/api/client.ts`:
  - `exportTable(tableName: string): Promise<Blob>` - Calls GET /api/table/{table_name}/export
  - `exportQueryResults(results: any[], columns: string[]): Promise<Blob>` - Calls POST /api/query/export
- Handle blob responses for file download
- Add error handling for failed exports

### Step 7: Add Frontend Type Definitions
- Add to `app/client/src/types.d.ts`:
  - `ExportQueryRequest` interface matching backend model
- Ensure type safety for export operations

### Step 8: Implement Table Download Buttons
- Modify `displayTables()` function in `app/client/src/main.ts`:
  - Add download button before the remove button (×) in each table header
  - Use download icon: `⬇` or appropriate SVG icon
  - Add click handler that calls `api.exportTable(tableName)`
  - Trigger browser download using blob and URL.createObjectURL()
  - Set filename to `{table_name}.csv`
  - Add loading state during export
  - Add success/error feedback to user

### Step 9: Implement Query Results Download Button
- Modify `displayResults()` function in `app/client/src/main.ts`:
  - Add download button next to the Hide button in results section
  - Use download icon: `⬇` or appropriate SVG icon
  - Add click handler that calls `api.exportQueryResults(response.results, response.columns)`
  - Trigger browser download using blob and URL.createObjectURL()
  - Set filename to `query_results_{timestamp}.csv`
  - Add loading state during export
  - Add success/error feedback to user

### Step 10: Style Download Buttons
- Add to `app/client/src/style.css`:
  - Styles for `.download-button` class
  - Hover effects matching existing button styles
  - Loading state styles
  - Proper spacing and alignment next to existing buttons
  - Icon sizing and color (matching theme)

### Step 11: Create E2E Test File
- Create `.claude/commands/e2e/test_csv_export.md` following the format of `test_basic_query.md`:
  - Test steps to upload sample data (users.json)
  - Verify table appears in Available Tables
  - Click download button on table
  - Verify CSV file is downloaded with correct name (users.csv)
  - Execute a query: "Show all users"
  - Verify query results appear
  - Click download button on query results
  - Verify CSV file is downloaded (query_results_*.csv)
  - Success criteria: Both downloads work, CSV files contain proper data with headers

### Step 12: Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Fix any issues that arise
- Verify all tests pass
- Verify frontend builds without errors
- Execute E2E test and verify all steps pass with screenshots

## Testing Strategy

### Unit Tests
- **CSV Generation Tests:**
  - Test basic CSV formatting with headers and rows
  - Test UTF-8 BOM is added at file start
  - Test special character escaping (commas, quotes, newlines)
  - Test Unicode characters (emojis, international alphabets)
  - Test empty datasets (0 rows, 0 columns)
  - Test NULL/None value handling
  - Test large datasets (1000+ rows) for performance

- **Security Tests:**
  - Test SQL injection attempts in table names are rejected
  - Test malicious column names are handled safely
  - Test CSV injection attempts (formulas starting with =, +, -, @)
  - Test path traversal attempts in filenames

- **Integration Tests:**
  - Test table export endpoint with real database
  - Test query export endpoint with various result sets
  - Test error responses for non-existent tables
  - Test concurrent export requests

### Edge Cases
- Empty tables (0 rows)
- Tables with 1 row
- Tables with 1 column
- Results with NULL values
- Column names with special characters
- Very long text values (1000+ characters)
- Unicode characters in data (emojis, Chinese, Arabic, etc.)
- Table names at maximum identifier length
- Malformed requests (missing columns, invalid JSON)
- Very large result sets (10,000+ rows)
- Simultaneous exports from multiple users
- Network interruptions during download
- Special characters in table names (underscores, numbers)

## Acceptance Criteria
1. **Backend Endpoints:**
   - GET /api/table/{table_name}/export returns valid CSV for any existing table
   - POST /api/query/export returns valid CSV for query results
   - Both endpoints return proper CSV Content-Type headers
   - Both endpoints return Content-Disposition headers with appropriate filenames
   - CSV files include UTF-8 BOM for Excel compatibility
   - All CSV values are properly escaped (commas, quotes, newlines)
   - SQL injection attempts are blocked and logged

2. **Frontend UI:**
   - Download button appears next to × button for each table in Available Tables
   - Download button appears next to Hide button in Query Results section
   - Download buttons use appropriate download icon (⬇)
   - Clicking download buttons triggers immediate CSV download
   - Downloaded files have correct names (table_name.csv, query_results.csv)
   - Download buttons show loading state during export
   - User receives feedback on successful/failed exports

3. **Data Quality:**
   - CSV files open correctly in Microsoft Excel
   - CSV files open correctly in Google Sheets
   - Headers match column names exactly
   - Data rows match database/query results exactly
   - Unicode characters display correctly
   - NULL values are represented as empty strings
   - No data corruption or loss during export

4. **Testing:**
   - All unit tests pass (21 new tests for CSV export)
   - All existing tests continue to pass (no regressions)
   - SQL injection tests verify export security
   - E2E test validates complete user workflow
   - Frontend builds without TypeScript errors

5. **Performance:**
   - Table export completes in <2 seconds for tables with <1000 rows
   - Query export completes in <1 second for typical result sets
   - No memory leaks during repeated exports
   - Concurrent exports don't block each other

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/core/test_csv_exporter.py -v` - Run new CSV exporter tests to validate CSV generation works correctly
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Run SQL injection tests to ensure export endpoints are secure
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript compiler to validate no type errors
- `cd app/client && bun run build` - Run frontend build to validate production build works
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` to validate the complete CSV export workflow works end-to-end with visual confirmation via screenshots

## Notes

### CSV Format Specification
- Use UTF-8 encoding with BOM (`\ufeff`) for Excel compatibility
- Use comma (`,`) as delimiter
- Use double quotes (`"`) for quoting fields
- Escape double quotes by doubling them (`""`)
- Use CRLF (`\r\n`) line endings for Windows compatibility
- First row contains column headers
- Subsequent rows contain data

### Security Considerations
- All table names must be validated using `validate_identifier()` before use
- Use `execute_query_safely()` for all database queries
- Prevent CSV injection by escaping values that start with `=`, `+`, `-`, `@` with a single quote prefix
- Sanitize filenames to prevent path traversal attacks
- Rate limit export endpoints if needed for production deployment

### Excel Compatibility
- UTF-8 BOM is critical for Excel to recognize encoding
- CRLF line endings work best with Excel on Windows
- Test with both Excel and Google Sheets to ensure compatibility

### Future Enhancements (Not in Scope)
- Custom filename input from user
- Column selection for partial exports
- Export format options (TSV, JSON, Excel .xlsx)
- Automatic compression for large files (ZIP)
- Email export for large datasets
- Scheduled exports with cron jobs
- Export history and re-download capability

### Python Libraries
- Use built-in `csv` module - no new dependencies needed
- Use `io.StringIO` for in-memory CSV generation
- All required libraries are already available in the project
