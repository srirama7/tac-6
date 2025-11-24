# Feature: CSV Export for Tables and Query Results

## Feature Description
This feature adds one-click CSV export functionality to the Natural Language SQL Interface application, enabling users to download both stored tables and query results as CSV files. The feature includes two new API endpoints for exporting data and intuitive download buttons integrated seamlessly into the existing UI. This empowers users to easily extract and share their data in a universally compatible format for further analysis in spreadsheet applications or other data tools.

## User Story
As a data analyst using the Natural Language SQL Interface
I want to export tables and query results as CSV files with a single click
So that I can analyze the data in external tools, share it with colleagues, or archive it for future reference

## Problem Statement
Currently, users can query and view data within the Natural Language SQL Interface, but there's no way to export this data for use outside the application. Users need to manually copy and paste data from the web interface, which is time-consuming, error-prone, and doesn't preserve data types or handle large datasets well. This limitation prevents users from leveraging external tools like Excel, Google Sheets, or specialized data analysis software, reducing the overall utility of the application.

## Solution Statement
Implement CSV export functionality through two dedicated API endpoints and corresponding UI buttons. The solution will allow users to export entire tables or specific query results directly to CSV files. Export buttons will be strategically placed next to existing UI elements (table remove buttons and results hide button) for intuitive access. The implementation will leverage the existing pandas library on the backend for efficient CSV conversion and use browser-native download mechanisms on the frontend, ensuring a smooth user experience without external dependencies.

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - Add new API endpoints for CSV export
- `app/server/core/data_models.py` - Add new Pydantic models for export requests/responses
- `app/server/core/sql_processor.py` - Use existing functions to fetch table data safely
- `app/server/core/sql_security.py` - Validate table names and prevent SQL injection
- `app/client/src/api/client.ts` - Add new API client methods for CSV export
- `app/client/src/types.d.ts` - Add TypeScript interfaces for export functionality
- `app/client/src/main.ts` - Add download buttons and event handlers to UI
- `app/client/src/style.css` - Style the new download buttons consistently
- `app/client/index.html` - Modify results section structure if needed
- `.claude/commands/test_e2e.md` - Reference for E2E test structure
- `.claude/commands/e2e/test_basic_query.md` - Reference for E2E test example

### New Files
- `.claude/commands/e2e/test_csv_export.md` - E2E test file for validating CSV export functionality

## Implementation Plan
### Phase 1: Foundation
Establish the backend infrastructure for CSV export by creating data models, implementing secure data fetching mechanisms, and setting up the API endpoints. This phase ensures proper security validation and efficient data handling using existing patterns in the codebase.

### Phase 2: Core Implementation
Implement the CSV conversion logic on the backend and create the client-side API integration. This includes building the export functions, handling file responses, and ensuring proper error handling throughout the data export pipeline.

### Phase 3: Integration
Integrate the export functionality into the existing UI by adding download buttons, connecting event handlers, and ensuring the feature works seamlessly with the current user workflow. Style the buttons consistently with the existing design system.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create E2E Test File for CSV Export
- Create `.claude/commands/e2e/test_csv_export.md` following the pattern from `test_basic_query.md`
- Define test steps for both table export and query results export
- Include verification steps for download triggers and file content
- Specify screenshot requirements for UI validation

### 2. Add Data Models for Export Functionality
- Open `app/server/core/data_models.py`
- Add `ExportTableRequest` Pydantic model with table_name field
- Add `ExportQueryResultsRequest` Pydantic model with results, columns, and filename fields
- Ensure models include proper validation and optional fields

### 3. Implement Backend Export Endpoints
- Open `app/server/server.py`
- Import required modules: `StreamingResponse` from fastapi.responses, `StringIO` from io
- Create `GET /api/export/table/{table_name}` endpoint:
  - Validate table_name using sql_security.validate_identifier()
  - Fetch table data using sql_processor.execute_sql_safely()
  - Convert results to CSV using pandas DataFrame
  - Return StreamingResponse with CSV content and appropriate headers
- Create `POST /api/export/results` endpoint:
  - Accept ExportQueryResultsRequest in body
  - Convert results to CSV using pandas DataFrame
  - Return StreamingResponse with CSV content and appropriate headers
- Add proper error handling and logging to both endpoints

### 4. Add TypeScript Types for Export
- Open `app/client/src/types.d.ts`
- Add `ExportTableRequest` interface matching Pydantic model
- Add `ExportQueryResultsRequest` interface matching Pydantic model
- Ensure types align exactly with backend models

### 5. Implement Client API Methods
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string): Promise<Blob>` method to api object:
  - Make GET request to `/api/export/table/${tableName}`
  - Handle response as blob
  - Include error handling
- Add `exportQueryResults(results: any[], columns: string[], filename?: string): Promise<Blob>` method:
  - Make POST request to `/api/export/results`
  - Send results, columns, and filename in body
  - Handle response as blob
  - Include error handling

### 6. Add Download Button for Tables
- Open `app/client/src/main.ts`
- Locate `displayTables()` function (around line 189)
- Before the remove button (× button), add a download button:
  - Create button element with class 'download-button'
  - Use appropriate download icon (⬇ or similar)
  - Add title attribute "Download as CSV"
  - Implement onclick handler that:
    - Calls api.exportTable(table.name)
    - Creates blob URL
    - Triggers download with filename `${table.name}.csv`
    - Handles errors with user feedback
- Position button to the left of the remove button in the table header

### 7. Add Download Button for Query Results
- Continue in `app/client/src/main.ts`
- Locate `displayResults()` function (around line 119)
- Find the results header section with the Hide button
- Add download button before the Hide button:
  - Create button element with class 'download-button'
  - Use same download icon as tables
  - Add title attribute "Download results as CSV"
  - Store current query results in a closure or data attribute
  - Implement onclick handler that:
    - Calls api.exportQueryResults() with stored results
    - Creates blob URL
    - Triggers download with filename 'query_results.csv'
    - Handles errors with user feedback

### 8. Style the Download Buttons
- Open `app/client/src/style.css`
- Add `.download-button` class styling:
  - Use similar styling to `.secondary-button` for consistency
  - Set appropriate size (matching remove button dimensions)
  - Add hover effects with transform
  - Ensure proper spacing in flex containers
  - Consider using a subtle background color to distinguish from destructive actions

### 9. Test Backend Endpoints Manually
- Start the server with `cd app/server && uv run python server.py`
- Upload sample data to create test tables
- Test table export endpoint using curl or browser:
  - `curl http://localhost:8000/api/export/table/users -o test_table.csv`
  - Verify CSV content is correct
- Test query results export endpoint:
  - Use curl with POST request and sample data
  - Verify CSV content matches input

### 10. Test Frontend Integration
- Start the client with `cd app/client && bun run dev`
- Navigate to http://localhost:5173
- Upload sample data or use existing tables
- Test table download button:
  - Click download button next to a table
  - Verify CSV file downloads with correct name and content
- Run a query and test results download:
  - Execute a natural language query
  - Click download button in results header
  - Verify CSV file downloads with query results

### 11. Add Error Handling and Edge Cases
- Handle empty tables/results gracefully
- Add loading states for large exports
- Implement timeout handling for export operations
- Add user feedback for successful downloads
- Handle special characters in table names for filenames
- Test with tables containing various data types

### 12. Run Unit Tests
- Execute `cd app/server && uv run pytest`
- Ensure all existing tests pass
- Add specific tests for export functionality if time permits

### 13. Run Type Checking and Build
- Execute `cd app/client && bun tsc --noEmit`
- Fix any TypeScript errors
- Execute `cd app/client && bun run build`
- Ensure production build completes successfully

### 14. Execute E2E Test for CSV Export
- Read `.claude/commands/test_e2e.md` for test execution instructions
- Execute the new E2E test file `.claude/commands/e2e/test_csv_export.md`
- Verify all test steps pass
- Review screenshots for UI validation
- Fix any issues identified by the test

### 15. Run Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

## Testing Strategy
### Unit Tests
- Test CSV conversion with various data types (strings, numbers, dates, nulls)
- Test export endpoints with valid and invalid table names
- Test security validation for SQL injection attempts
- Test handling of large datasets (pagination/streaming)
- Test special characters in data and filenames

### Edge Cases
- Empty tables with no rows but valid columns
- Tables with special characters in names (spaces, symbols)
- Very large tables (10,000+ rows)
- Tables with many columns (50+)
- Query results with no data
- Concurrent export requests
- Network interruptions during download
- Tables with various data types including JSON fields
- Unicode characters in data content

## Acceptance Criteria
- Download button appears to the left of the × button for each table in the Available Tables section
- Download button appears to the left of the Hide button in Query Results header
- Clicking table download button triggers CSV download with filename matching table name
- Clicking results download button triggers CSV download with filename 'query_results.csv'
- CSV files contain headers matching column names
- CSV files properly escape special characters and handle nulls
- Export works for tables with 0 to 10,000+ rows
- No SQL injection vulnerabilities in export endpoints
- Download buttons have consistent styling with existing UI
- Error messages display when export fails
- All existing functionality continues to work without regression
- E2E test for CSV export passes successfully

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Verify security measures remain intact
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate TypeScript interfaces
- `cd app/client && bun run build` - Run frontend build to validate the feature compiles correctly
- `./scripts/start.sh` - Start the application and manually test both export features
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` test file to validate CSV export functionality works end-to-end
- Test table export: Upload sample data, click download button, verify CSV content
- Test query export: Run a query, click download button, verify CSV content
- Test edge cases: Empty table export, special characters in names, large datasets

## Notes
- Using pandas for CSV conversion leverages existing dependency and ensures robust handling of data types
- StreamingResponse is preferred over FileResponse to avoid creating temporary files on disk
- Download buttons use browser-native download mechanism (blob URLs) for better compatibility
- The feature respects existing security patterns, validating all table names through sql_security module
- CSV format chosen for universal compatibility with Excel, Google Sheets, and data analysis tools
- Future enhancement could include additional export formats (JSON, Excel) using the same infrastructure
- Consider implementing download progress indicators for large exports in future iterations
- The placement of buttons (left of existing buttons) maintains UI consistency and follows common UX patterns