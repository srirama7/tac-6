# Feature: CSV Export for Tables and Query Results

## Feature Description
Add CSV export functionality to the Natural Language SQL Interface application, enabling users to download both uploaded tables and query results as properly formatted CSV files. This feature will provide export buttons in the UI that trigger downloads of CSV files with proper handling of special characters, quotes, and edge cases. The backend infrastructure is already in place, so this implementation focuses on adding the UI export buttons and integrating them with the existing export endpoints.

## User Story
As a user of the Natural Language SQL Interface
I want to export tables and query results to CSV format
So that I can analyze data in external tools like Excel, Google Sheets, or perform further processing

## Problem Statement
Users can upload data and query it using natural language, but they have no way to export the results or tables back out of the application. This creates a one-way data flow that limits the utility of the application. Users need the ability to:
- Export uploaded tables for backup or external analysis
- Download query results for reporting or further data processing
- Share data insights with colleagues who don't have access to the application

## Solution Statement
Leverage the existing backend CSV export infrastructure (endpoints and CSV generation utility already implemented) and add UI export functionality. The solution will add export buttons to:
1. Each table in the "Available Tables" section with a download icon button
2. The query results section with an "Export Results" button

Both will trigger downloads of properly formatted CSV files using the existing `/api/export/table/{table_name}` and `/api/export/results` endpoints that handle special characters, quotes, and edge cases according to RFC 4180 standards.

## Relevant Files
Use these files to implement the feature:

- **app/server/server.py** (lines 282-365) - Contains the already-implemented CSV export endpoints:
  - `GET /api/export/table/{table_name}` - Exports a table as CSV
  - `POST /api/export/results` - Exports query results as CSV
  - Both endpoints use SQL security validation and return downloadable CSV files

- **app/server/core/csv_exporter.py** - CSV generation utility that:
  - Follows RFC 4180 CSV formatting standards
  - Handles special characters (quotes, commas, newlines) with proper escaping
  - Converts None values to empty strings
  - Uses UTF-8 encoding for international characters

- **app/server/core/data_models.py** (lines 84-92) - Contains the data models:
  - `ResultsExportRequest` - Request model for exporting query results
  - `ExportResponse` - Response model for export operations

- **app/server/tests/test_csv_export.py** - Comprehensive unit tests covering:
  - Basic CSV generation
  - Special character handling
  - Null value handling
  - Empty data scenarios
  - Table export endpoint validation
  - Query results export validation
  - SQL injection protection

- **app/client/src/api/client.ts** (lines 80-108) - API client with already-implemented export methods:
  - `exportTable(tableName: string): Promise<Blob>` - Calls GET endpoint for table export
  - `exportResults(columns: string[], results: Record<string, any>[]): Promise<Blob>` - Calls POST endpoint for results export
  - Both methods return Blob objects suitable for triggering downloads

- **app/client/src/types.d.ts** (lines 82-92) - TypeScript type definitions:
  - `ResultsExportRequest` interface
  - `ExportResponse` interface

- **app/client/src/main.ts** - Main application logic:
  - `displayTables()` function (lines 189-258) - Renders table items; needs export button added
  - `displayResults()` function (lines 119-154) - Renders query results; needs export button added
  - `createResultsTable()` function (lines 157-186) - Creates results table HTML

- **app/client/index.html** - HTML structure:
  - Tables section (lines 38-44) - Container for table items
  - Results section (lines 28-36) - Container for query results

### New Files

- **.claude/commands/e2e/test_csv_export.md** - E2E test specification to validate CSV export functionality works end-to-end in the browser

## Implementation Plan

### Phase 1: Foundation
The backend infrastructure is already complete with working endpoints, CSV generation utility, security validation, and comprehensive unit tests. No foundational backend work is needed.

### Phase 2: Core Implementation
Add UI export buttons to trigger CSV downloads:
1. Add export button to each table item in the "Available Tables" section
2. Add export button to the query results display
3. Implement download trigger functions that use the existing API client methods
4. Add proper error handling and user feedback for export operations

### Phase 3: Integration
Integrate export functionality with existing UI patterns:
1. Match styling and interaction patterns used for existing buttons (remove table button)
2. Ensure downloads work correctly with proper filenames
3. Add loading states during export operations
4. Create E2E test to validate the complete export workflow

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Table Export Button to UI
- Read `app/client/src/main.ts` and locate the `displayTables()` function (around line 189)
- In the table header section (around line 204-230), add an export button next to the remove button
- The export button should have a download icon (⬇) and appropriate styling
- Add click handler that calls a new `exportTable()` function

### Step 2: Implement Table Export Download Function
- In `app/client/src/main.ts`, create a new function `exportTable(tableName: string)`
- Use `api.exportTable(tableName)` to get the CSV blob
- Create a download link using `URL.createObjectURL(blob)` and trigger download
- Add error handling with `displayError()` function
- Show loading state during export (optional but recommended)

### Step 3: Add Query Results Export Button to UI
- Read the `displayResults()` function in `app/client/src/main.ts` (around line 119)
- Add an "Export Results" button to the results header section (around line 128-135)
- Position it next to the SQL display or in the results header
- Style it consistently with existing buttons

### Step 4: Implement Query Results Export Download Function
- Create a new function `exportQueryResults(columns: string[], results: Record<string, any>[])`
- Use `api.exportResults(columns, results)` to get the CSV blob
- Trigger download with proper timestamped filename
- Add error handling and loading states

### Step 5: Update Results Display to Include Export Button
- Modify the `displayResults()` function to store the current results and columns in a way accessible to the export button
- Add click handler to the export button that calls `exportQueryResults()` with current data
- Ensure the export button is only shown when results are available

### Step 6: Add Download Helper Utility Function
- Create a reusable `downloadBlob(blob: Blob, filename: string)` helper function
- This function should create a temporary anchor element, set href to blob URL, trigger click, and cleanup
- Use this in both `exportTable()` and `exportQueryResults()` to avoid code duplication

### Step 7: Run Backend Tests
- Execute `cd app/server && uv run pytest tests/test_csv_export.py -v` to ensure all CSV export unit tests pass
- Verify all tests pass with zero failures
- Fix any issues if tests fail

### Step 8: Run Full Backend Test Suite
- Execute `cd app/server && uv run pytest` to run all backend tests
- Ensure zero regressions in the test suite
- Verify all tests pass

### Step 9: Run Frontend Build
- Execute `cd app/client && bun tsc --noEmit` to check TypeScript compilation
- Fix any TypeScript errors
- Execute `cd app/client && bun run build` to verify production build works
- Ensure build completes successfully with zero errors

### Step 10: Create E2E Test Specification
- Read `.claude/commands/test_e2e.md` to understand the E2E test format
- Read `.claude/commands/e2e/test_basic_query.md` as an example E2E test
- Create `.claude/commands/e2e/test_csv_export.md` following the same structure
- The test should validate:
  - Exporting an uploaded table downloads a CSV file with correct data
  - Exporting query results downloads a CSV file with correct data
  - CSV files have proper headers and content
  - Special characters are handled correctly
- Include specific verification steps and screenshot requirements
- Define clear success criteria

### Step 11: Execute Validation Commands
- Run all validation commands listed in the "Validation Commands" section below
- Ensure every command executes without errors
- Verify zero regressions across the application

## Testing Strategy

### Unit Tests
All unit tests are already implemented in `app/server/tests/test_csv_export.py`:
- CSV generation with basic data
- Special character handling (quotes, commas, newlines)
- Null value handling
- Empty data scenarios
- Table export endpoint validation (valid table, nonexistent table, invalid table name)
- Query results export endpoint validation (basic results, empty results, special characters)
- SQL injection protection

### Edge Cases
The following edge cases are already covered by existing tests:
- Empty result sets (should return CSV with headers only)
- Null values in data (converted to empty strings)
- Special characters that need escaping (quotes, commas, newlines)
- SQL injection attempts in table names (validated and rejected)
- Nonexistent tables (404 error)
- Large datasets (CSV format handles efficiently with streaming)

Additional edge cases to validate during E2E testing:
- Browser download behavior works correctly
- Multiple consecutive exports
- Export while query is running
- Export with no tables loaded

## Acceptance Criteria
- Export button appears on each table item in "Available Tables" section
- Export button appears in query results display when results are shown
- Clicking table export button downloads a CSV file named `{table_name}.csv`
- Clicking results export button downloads a CSV file named `query_results_{timestamp}.csv`
- Downloaded CSV files contain correct headers and data
- Special characters (quotes, commas, newlines) are properly escaped in CSV files
- Null values appear as empty cells in CSV files
- Export works for both small and large datasets
- Export shows appropriate loading state during download
- Error handling displays user-friendly messages if export fails
- All existing tests continue to pass (zero regressions)
- E2E test validates export functionality works end-to-end in browser
- Frontend TypeScript compilation succeeds with no errors
- Frontend production build succeeds with no errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_csv_export.md` test file to validate CSV export functionality works in the browser
- `cd app/server && uv run pytest tests/test_csv_export.py -v` - Run CSV export tests specifically
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Backend Implementation Status
The backend implementation is 100% complete and fully tested:
- Both export endpoints are implemented and working (`/api/export/table/{table_name}` and `/api/export/results`)
- CSV generation utility handles all edge cases correctly
- Security validation prevents SQL injection
- Unit tests provide comprehensive coverage
- Error handling and logging are in place

### Frontend API Client Status
The frontend API client methods are already implemented:
- `api.exportTable()` - Ready to use for table exports
- `api.exportResults()` - Ready to use for results exports
- Both return Blob objects suitable for triggering downloads

### Implementation Focus
This implementation focuses exclusively on:
1. Adding export buttons to the UI
2. Wiring up the buttons to existing API client methods
3. Implementing download trigger logic (create blob URL, trigger download, cleanup)
4. Adding appropriate error handling and user feedback
5. Creating E2E test to validate end-to-end functionality

### CSV Format Standards
The CSV export follows RFC 4180 standards:
- CRLF line endings (`\r\n`) for maximum compatibility
- Minimal quoting (only when necessary)
- Proper escaping of special characters
- UTF-8 encoding for international characters

### Testing Approach
- Backend is already fully tested with unit tests
- Focus E2E testing on browser integration and download behavior
- Validate that downloads work correctly in headed browser mode
- Verify CSV file content matches expected data

### Future Enhancements
Potential future improvements (not part of this implementation):
- Export format selection (CSV, JSON, Excel)
- Custom column selection for exports
- Export progress indicator for large datasets
- Batch export of multiple tables
- Scheduled/automated exports
