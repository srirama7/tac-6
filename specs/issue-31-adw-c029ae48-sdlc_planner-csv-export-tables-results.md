# Feature: CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality to the Natural Language SQL Interface application, allowing users to download both table data and query results as CSV files. This feature adds two new API endpoints - one for exporting entire tables and another for exporting query results - along with download buttons in the UI positioned next to existing controls using appropriate download icons.

## User Story
As a user
I want to export tables and query results to CSV files with a single click
So that I can analyze the data in external tools like Excel or share it with colleagues

## Problem Statement
Currently, users can view data in the web interface but have no way to export it for use in other applications. This limits the utility of the application as users often need to further process, analyze, or share their data. Without export functionality, users would need to manually copy-paste data or recreate queries in other tools.

## Solution Statement
Implement a CSV export feature with two endpoints: `/api/export/table/{table_name}` for exporting entire tables and `/api/export/results` for exporting query results. Add download buttons in the UI that trigger these endpoints and return CSV files with proper content-disposition headers for browser download. The buttons will be positioned directly to the left of the 'x' icon for table exports and directly to the left of the 'Hide' button for query result exports, using a download icon for clear visual indication.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - Main FastAPI server file where new export endpoints will be added
- `app/server/core/data_models.py` - Contains Pydantic models; need to add ExportResponse model
- `app/server/core/sql_security.py` - Security validation functions to ensure safe table name validation
- `app/server/core/sql_processor.py` - Database query execution functions to retrieve data for export
- `app/client/src/main.ts` - Frontend TypeScript code where UI event handlers and download buttons will be added
- `app/client/src/api/client.ts` - API client where export API methods will be added
- `app/client/src/types.d.ts` - TypeScript type definitions for export responses
- `app/client/src/style.css` - Styling for the new download buttons
- `app/client/index.html` - HTML structure (no changes needed, buttons added dynamically)

### New Files
- `.claude/commands/e2e/test_csv_export.md` - E2E test file to validate CSV export functionality works correctly

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for CSV export functionality:
- Add CSV generation utility functions that convert database rows to CSV format
- Define ExportResponse data model for API responses
- Implement security validation for export operations
- Add new API endpoints with proper error handling and logging

### Phase 2: Core Implementation
Build the export endpoints and integrate with existing database operations:
- Implement `/api/export/table/{table_name}` endpoint that validates table existence and exports all rows
- Implement `/api/export/results` endpoint that accepts SQL query and parameters to export filtered data
- Ensure proper CSV formatting with headers, proper escaping, and UTF-8 encoding
- Add appropriate HTTP headers for file downloads (Content-Type, Content-Disposition)

### Phase 3: Integration
Connect the frontend UI to the backend endpoints:
- Add download buttons to the UI in the specified locations with download icons
- Implement API client methods for export operations
- Add event handlers that trigger downloads when buttons are clicked
- Handle loading states and error messages for failed exports
- Update styling to match existing UI patterns

## Step by Step Tasks

### Task 1: Add CSV Export Utility Function
- Create a utility function `convert_to_csv()` in `app/server/core/sql_processor.py` that takes rows and columns, returns CSV string
- Handle proper CSV escaping for special characters (commas, quotes, newlines)
- Include column headers as first row
- Use Python's `csv` module for proper formatting

### Task 2: Add Export Data Models
- Add `ExportRequest` model to `app/server/core/data_models.py` with fields for SQL query and parameters
- Add `ExportResponse` model (if needed for structured responses, though CSV will be returned directly)
- Update TypeScript types in `app/client/src/types.d.ts` to match backend models

### Task 3: Implement Table Export Endpoint
- Add `POST /api/export/table/{table_name}` endpoint in `app/server/server.py`
- Validate table name using `validate_identifier()` from sql_security module
- Check table exists using `check_table_exists()` function
- Retrieve all rows using `execute_query_safely()` with `SELECT * FROM {table}`
- Convert results to CSV format using utility function
- Return StreamingResponse with CSV data, proper headers (Content-Type: text/csv, Content-Disposition: attachment)
- Add comprehensive error handling and logging

### Task 4: Implement Query Results Export Endpoint
- Add `POST /api/export/results` endpoint in `app/server/server.py`
- Accept JSON body with SQL query (or reuse QueryRequest model)
- Validate SQL query using `validate_sql_query()` function
- Execute query using `execute_sql_safely()` function
- Convert results to CSV format
- Return StreamingResponse with CSV data and proper download headers
- Add error handling for invalid queries

### Task 5: Add Frontend API Client Methods
- Add `exportTable(tableName: string)` method to `app/client/src/api/client.ts`
- Add `exportQueryResults(sql: string, results: any[], columns: string[])` method
- Both methods should trigger browser download by creating blob URLs
- Handle API errors and display user-friendly messages

### Task 6: Add Download Button for Tables
- Modify `displayTables()` function in `app/client/src/main.ts`
- Create download button element with download icon (📥 or SVG icon)
- Position button directly to the left of the '×' (remove) button in table header
- Add click handler that calls `api.exportTable(tableName)`
- Add loading state during export
- Style button to match existing UI patterns

### Task 7: Add Download Button for Query Results
- Modify `displayResults()` function in `app/client/src/main.ts`
- Create download button element with download icon
- Position button directly to the left of the 'Hide' button in results header
- Add click handler that calls `api.exportQueryResults()` with current SQL and results
- Add loading state during export
- Ensure button is only visible when results are present

### Task 8: Add CSS Styling for Download Buttons
- Add `.download-button` class in `app/client/src/style.css`
- Style to match existing button styles (secondary-button or remove-table-button)
- Ensure proper hover effects and cursor pointer
- Make icon clearly visible and appropriately sized
- Ensure proper spacing between download button and adjacent buttons

### Task 9: Create E2E Test File
- Create `.claude/commands/e2e/test_csv_export.md` following the format of `test_basic_query.md`
- Test uploading sample data (users table)
- Test clicking download button on table and verify CSV downloads
- Test executing a query, then clicking download button on results and verify CSV downloads
- Verify CSV content has proper headers and data
- Take screenshots at each step

### Task 10: Add Unit Tests for CSV Export
- Create `app/server/tests/test_csv_export.py`
- Test `convert_to_csv()` utility function with various data types
- Test table export endpoint with valid table name
- Test table export endpoint with invalid/non-existent table
- Test results export endpoint with valid query
- Test results export endpoint with SQL injection attempts
- Test CSV special character escaping (commas, quotes, newlines)
- Ensure all tests pass

### Task 11: Validate Implementation
- Run all validation commands listed below
- Execute the E2E test to verify end-to-end functionality
- Fix any issues discovered during testing
- Ensure zero regressions in existing functionality

## Testing Strategy

### Unit Tests
- Test CSV generation with empty result sets
- Test CSV generation with single row
- Test CSV generation with multiple rows
- Test CSV generation with special characters (commas, quotes, newlines, unicode)
- Test CSV generation with NULL values
- Test table export endpoint with valid table names
- Test table export endpoint with non-existent tables
- Test table export endpoint with SQL injection attempts in table name
- Test results export endpoint with valid queries
- Test results export endpoint with malicious SQL
- Test proper HTTP headers in responses (Content-Type, Content-Disposition)
- Test CSV file encoding (UTF-8)

### Edge Cases
- Empty tables (0 rows) - should return CSV with headers only
- Tables with single column
- Tables with many columns (50+)
- Large result sets (1000+ rows) - verify performance
- Column names with special characters
- Data containing commas, quotes, and newlines
- Unicode characters in data (emojis, international characters)
- NULL/None values in data
- Very long string values (500+ characters)
- Concurrent export requests

## Acceptance Criteria
- [ ] Two new API endpoints are implemented and working: `/api/export/table/{table_name}` and `/api/export/results`
- [ ] Both endpoints return properly formatted CSV files with correct HTTP headers
- [ ] Table export downloads all rows from the specified table
- [ ] Query results export downloads the current query results
- [ ] Download button appears directly to the left of 'x' icon for each table in Available Tables section
- [ ] Download button appears directly to the left of 'Hide' button in Query Results section
- [ ] Download buttons use appropriate download icon (📥 or similar)
- [ ] Clicking download buttons triggers immediate CSV file download in browser
- [ ] Downloaded CSV files have appropriate filenames (e.g., `table_name.csv`, `query_results.csv`)
- [ ] CSV files open correctly in Excel and other spreadsheet applications
- [ ] CSV special characters are properly escaped
- [ ] Security validations prevent SQL injection
- [ ] All existing tests pass (no regressions)
- [ ] New unit tests for CSV export functionality pass
- [ ] E2E test validates complete user workflow
- [ ] Error messages are user-friendly when exports fail
- [ ] Loading states are shown during export operations

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works end-to-end
- `cd app/server && uv run python -m py_compile server.py main.py core/*.py` - Validate Python syntax
- `cd app/server && uv run ruff check .` - Run Python linting to ensure code quality
- `cd app/server && uv run pytest tests/test_csv_export.py -v` - Run new CSV export tests
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript type checking
- `cd app/client && bun run build` - Build frontend to ensure no compilation errors

## Notes

### CSV Format Specifications
- Use comma as delimiter
- Use double quotes for text fields containing commas, quotes, or newlines
- Escape internal double quotes by doubling them ("" within fields)
- Use UTF-8 encoding for international character support
- Include header row with column names
- Use CRLF (\r\n) line endings for maximum compatibility

### Security Considerations
- All table names must be validated using `validate_identifier()` to prevent SQL injection
- Query results export should reuse the validated SQL from query execution
- Never trust user-provided SQL directly - always validate
- Limit export size to prevent DoS (consider adding max row limit if needed)
- Rate limiting may be needed for production use (future enhancement)

### Performance Notes
- For large tables (10,000+ rows), consider streaming response to avoid memory issues
- Python's `csv.writer()` with StringIO is efficient for moderate sizes
- FastAPI's `StreamingResponse` allows streaming large files without loading all into memory
- Consider adding pagination or row limits for very large exports (future enhancement)

### User Experience
- Download should start immediately when button is clicked
- Use descriptive filenames: `{table_name}_{timestamp}.csv` for tables, `query_results_{timestamp}.csv` for results
- Show loading indicator (spinner or disabled button state) during export
- Display success message or error message after export completes
- Buttons should have clear hover effects to indicate they're clickable
- Icons should be recognizable as download actions

### Dependencies
- No new Python packages required (csv module is built-in)
- No new JavaScript packages required
- FastAPI's StreamingResponse will be used for file downloads

### Future Enhancements (Out of Scope for This Feature)
- Export to other formats (JSON, Excel, Parquet)
- Select specific columns to export
- Export with filters applied
- Schedule automatic exports
- Email exported files
- Export multiple tables at once
- Compression for large files (zip/gzip)
