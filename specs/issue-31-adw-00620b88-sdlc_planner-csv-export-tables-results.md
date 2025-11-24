# Feature: CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality to the Natural Language SQL Interface application, enabling users to download both uploaded tables and query results as properly formatted CSV files. This feature provides download buttons integrated directly into the UI: one button to the left of the 'x' icon for available tables, and one button to the left of the 'hide' button for query results. The feature leverages backend infrastructure that has already been implemented, focusing on completing the UI integration and validation.

## User Story
As a user of the Natural Language SQL Interface
I want to export tables and query results to CSV format with a single click
So that I can analyze data in external tools like Excel, Google Sheets, or perform further processing without manual data copying

## Problem Statement
Users can upload data and query it using natural language, but they lack a convenient way to export the results or tables back out of the application. This creates a one-way data flow that limits the utility of the application. Users need the ability to:
- Export uploaded tables for backup, sharing, or external analysis
- Download query results for reporting or further data processing
- Share data insights with colleagues who may not have access to the application
- Integrate application data with other tools in their workflow

Without export functionality, users must resort to manual copying and pasting, which is error-prone and time-consuming for large datasets.

## Solution Statement
Implement one-click CSV export functionality by adding download buttons at specific UI locations and connecting them to existing backend endpoints. The solution adds:

1. **Table Export Button**: A download icon button placed directly to the left of the 'x' icon in each table item in the "Available Tables" section
2. **Results Export Button**: An export button placed in the query results section, positioned for easy access

Both buttons trigger immediate downloads of properly formatted CSV files using the existing `/api/export/table/{table_name}` and `/api/export/results` endpoints. The backend handles special characters, quotes, and edge cases according to RFC 4180 standards, ensuring data integrity and compatibility with spreadsheet applications.

## Relevant Files
Use these files to implement the feature:

### Backend Files (Already Implemented)

- **app/server/server.py** (lines 282-365) - Contains the working CSV export endpoints:
  - `GET /api/export/table/{table_name}` - Exports a complete table as CSV with security validation
  - `POST /api/export/results` - Exports query results as CSV with proper formatting
  - Both endpoints include SQL injection protection and return Response objects with proper headers for browser downloads

- **app/server/core/csv_exporter.py** - CSV generation utility providing:
  - RFC 4180 compliant CSV formatting
  - Proper escaping for special characters (quotes, commas, newlines)
  - UTF-8 encoding for international characters
  - Conversion of None/null values to empty strings
  - CRLF line endings for maximum compatibility

- **app/server/core/data_models.py** (lines 84-92) - Pydantic data models:
  - `ResultsExportRequest` - Request model with columns and results fields
  - `ExportResponse` - Response model with filename, content, and error fields

- **app/server/tests/test_csv_export.py** - Comprehensive test suite covering:
  - CSV generation with various data types
  - Special character handling and escaping
  - Null/None value handling
  - Empty dataset scenarios
  - Table export endpoint (valid, nonexistent, invalid names)
  - Query results export endpoint
  - SQL injection protection

### Frontend Files (Need Updates)

- **app/client/src/api/client.ts** (lines 80-108) - API client with implemented export methods:
  - `exportTable(tableName: string): Promise<Blob>` - Calls table export endpoint and returns Blob
  - `exportResults(columns: string[], results: Record<string, any>[]): Promise<Blob>` - Calls results export endpoint
  - Both methods handle HTTP requests and return Blob objects for download triggers

- **app/client/src/main.ts** - Main application logic requiring updates:
  - `displayTables()` function (lines 210-292) - Renders table items; ALREADY HAS export button implementation at lines 248-252
  - `displayResults()` function (lines 120-175) - Renders query results; ALREADY HAS export button implementation at lines 136-156
  - `exportTable()` function (lines 471-479) - ALREADY IMPLEMENTED
  - `exportQueryResults()` function (lines 482-499) - ALREADY IMPLEMENTED
  - `downloadBlob()` helper function (lines 459-468) - ALREADY IMPLEMENTED

- **app/client/src/types.d.ts** - TypeScript type definitions:
  - `ResultsExportRequest` interface
  - `ExportResponse` interface
  - Other API response types

- **app/client/index.html** - HTML structure:
  - Tables section container for table items
  - Results section container for query results

### New Files

- **.claude/commands/e2e/test_csv_export.md** - E2E test specification to validate CSV export functionality works end-to-end in the browser with Playwright automation

## Implementation Plan

### Phase 1: Foundation
The backend infrastructure is 100% complete with working endpoints (`/api/export/table/{table_name}` and `/api/export/results`), CSV generation utility, security validation, and comprehensive unit tests. The frontend API client methods are also implemented. No foundational work is needed.

**STATUS**: ✅ Complete

### Phase 2: Core Implementation
The frontend UI implementation is also already complete based on the current code review. The export buttons are present in the UI at the correct locations, and the download functionality is implemented.

**STATUS**: ✅ Complete - Requires validation only

### Phase 3: Integration
Final integration and validation phase to ensure the complete feature works correctly end-to-end.

**FOCUS**: Validation, testing, and E2E test creation

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Verify Backend Implementation
- Read `app/server/server.py` and verify the export endpoints are implemented correctly
- Confirm `GET /api/export/table/{table_name}` endpoint exists and handles table exports
- Confirm `POST /api/export/results` endpoint exists and handles query results exports
- Verify both endpoints use proper security validation (SQL injection protection)
- Verify endpoints return Response objects with correct MIME types and headers
- Review `app/server/core/csv_exporter.py` to understand CSV generation logic

### Step 2: Verify Frontend API Client
- Read `app/client/src/api/client.ts`
- Confirm `exportTable()` method is implemented and calls the correct endpoint
- Confirm `exportResults()` method is implemented and calls the correct endpoint
- Verify both methods return Promise<Blob> for download triggers
- Check error handling in API methods

### Step 3: Verify Frontend UI Implementation
- Read `app/client/src/main.ts` thoroughly
- Verify the `displayTables()` function includes export button in table headers
- Verify the export button is positioned to the left of the 'x' (remove) button
- Verify the `displayResults()` function includes export button for query results
- Verify the export button uses appropriate download icon
- Check that `exportTable()` function is implemented
- Check that `exportQueryResults()` function is implemented
- Check that `downloadBlob()` helper function is implemented

### Step 4: Test Backend CSV Export Unit Tests
- Execute `cd app/server && uv run pytest tests/test_csv_export.py -v`
- Verify all tests pass with zero failures
- Review test output to confirm coverage of:
  - Basic CSV generation
  - Special character handling
  - Null value handling
  - Empty data scenarios
  - Table export endpoint validation
  - Query results export endpoint validation
  - SQL injection protection
- If any tests fail, investigate and fix the issues

### Step 5: Run Full Backend Test Suite
- Execute `cd app/server && uv run pytest -v`
- Ensure zero regressions in the complete test suite
- Verify all tests pass without errors
- Check for any warnings or deprecation notices
- Document any issues found

### Step 6: Test Frontend TypeScript Compilation
- Execute `cd app/client && bun tsc --noEmit`
- Fix any TypeScript compilation errors
- Verify no type errors related to export functionality
- Ensure all interfaces and types are correctly defined

### Step 7: Test Frontend Production Build
- Execute `cd app/client && bun run build`
- Verify production build completes successfully
- Check build output for any errors or warnings
- Ensure build artifacts are generated correctly

### Step 8: Create E2E Test Specification
- Read `.claude/commands/test_e2e.md` to understand the E2E test framework and format requirements
- Read `.claude/commands/e2e/test_basic_query.md` as a reference example for structuring the test
- Read `.claude/commands/e2e/test_complex_query.md` for additional test patterns
- Create `.claude/commands/e2e/test_csv_export.md` following the established format with:
  - **User Story**: Define what the test validates from a user perspective
  - **Test Steps**: Detailed numbered steps including:
    1. Starting the application and uploading sample data
    2. Verifying table export button appears and is clickable
    3. Clicking table export button and verifying CSV download
    4. Running a query to generate results
    5. Verifying results export button appears
    6. Clicking results export button and verifying CSV download
    7. Validating CSV content has correct headers and data
    8. Testing special characters handling in exports
  - **Success Criteria**: Clear criteria for test pass/fail including:
    - Export buttons are visible and properly positioned
    - Downloads are triggered correctly
    - CSV files contain expected data
    - Special characters are properly escaped
    - File naming follows expected patterns
  - Include screenshot requirements at key steps (initial state, buttons visible, download triggered, results)

### Step 9: Manual Validation Testing
- Start the application using `./scripts/start.sh`
- Upload a sample CSV file to create a table
- Verify the export button (⬇) appears to the left of the 'x' button on the table item
- Click the table export button and verify:
  - A CSV file downloads with the table name
  - The CSV content matches the uploaded data
  - Headers are correct
- Execute a natural language query that returns results
- Verify the export button appears in the query results section
- Click the results export button and verify:
  - A CSV file downloads with a timestamp in the filename
  - The CSV content matches the query results
  - Headers match the result columns
- Test with data containing special characters (quotes, commas, newlines)
- Test with queries returning empty results
- Document any issues found

### Step 10: Execute All Validation Commands
- Run all validation commands listed in the "Validation Commands" section below
- Ensure every command executes successfully without errors
- Verify zero regressions across the application
- Document test results

## Testing Strategy

### Unit Tests
All backend unit tests are implemented in `app/server/tests/test_csv_export.py` and cover:

**CSV Generation Tests** (`TestCSVExporter` class):
- `test_generate_csv_basic` - Basic CSV generation with simple data
- `test_generate_csv_special_characters` - Handling of quotes, commas, newlines
- `test_generate_csv_null_values` - Null/None value conversion to empty strings
- `test_generate_csv_empty_data` - Empty dataset with header only

**Table Export Tests** (`TestTableExport` class):
- `test_export_valid_table` - Export existing table successfully
- `test_export_nonexistent_table` - 404 error for missing tables
- `test_export_invalid_table_name` - SQL injection protection

**Results Export Tests** (`TestResultsExport` class):
- `test_export_results_basic` - Basic query results export
- `test_export_results_empty` - Empty results with header only
- `test_export_results_special_characters` - Special character handling

### Edge Cases
The following edge cases are covered by existing tests and should be validated:

**Backend Edge Cases**:
- Empty result sets → CSV with headers only
- Null/None values → Converted to empty strings
- Special characters requiring escaping → Properly quoted and escaped
- SQL injection attempts → Validated and rejected with 400 error
- Nonexistent tables → 404 error with clear message
- Large datasets → Efficient CSV generation with streaming

**Frontend Edge Cases** (validate during manual/E2E testing):
- Export with no tables loaded → Button should not appear or be disabled
- Export while query is running → Should queue or show loading state
- Multiple consecutive exports → Each should trigger correctly
- Browser download blocking → Handle gracefully with user feedback
- Network errors during export → Display error message
- Large file downloads → Show progress or loading indication

### E2E Testing
The E2E test should validate the complete workflow:
1. Application loads correctly
2. Sample data can be uploaded
3. Export buttons appear at correct positions
4. Table export triggers download with correct filename
5. Query execution generates results
6. Results export triggers download with timestamped filename
7. Downloaded CSV files contain correct data and headers
8. Special characters are properly handled in CSV files

## Acceptance Criteria
The feature is complete when ALL of the following criteria are met:

**UI Requirements**:
- ✅ Export button (download icon ⬇) appears on each table item in "Available Tables" section
- ✅ Export button is positioned directly to the left of the 'x' (remove) icon
- ✅ Export button appears in query results section when results are available
- ✅ Export button is positioned appropriately in the results header area
- ✅ Buttons use appropriate download icon (⬇) for clear visual indication

**Functional Requirements**:
- ✅ Clicking table export button triggers immediate CSV download
- ✅ Downloaded table CSV file is named `{table_name}.csv`
- ✅ Clicking results export button triggers immediate CSV download
- ✅ Downloaded results CSV file is named `query_results_{timestamp}.csv`
- ✅ Downloaded CSV files contain correct headers matching column names
- ✅ Downloaded CSV files contain all expected data rows
- ✅ Special characters (quotes, commas, newlines) are properly escaped
- ✅ Null/None values appear as empty cells in CSV files

**Error Handling**:
- ✅ Export errors display user-friendly error messages
- ✅ Network failures are handled gracefully
- ✅ SQL injection attempts in table names are blocked

**Testing Requirements**:
- ✅ All backend unit tests pass (CSV generation, table export, results export)
- ✅ All backend integration tests pass (no regressions)
- ✅ Frontend TypeScript compilation succeeds with no errors
- ✅ Frontend production build succeeds with no errors
- ✅ E2E test specification is created and validates complete workflow
- ✅ Manual validation confirms buttons work in actual browser

**Performance Requirements**:
- ✅ Export works efficiently for small datasets (< 100 rows)
- ✅ Export works efficiently for medium datasets (100-1000 rows)
- ✅ Export shows appropriate loading state for large operations

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

**E2E Testing**:
```bash
# Read the E2E test documentation and execute the CSV export E2E test
# This validates the complete feature works end-to-end in a browser
```
Read `.claude/commands/test_e2e.md`, then read and execute your new E2E test file `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works in the browser with Playwright automation.

**Backend Testing**:
```bash
# Run CSV export specific tests
cd app/server && uv run pytest tests/test_csv_export.py -v

# Run complete server test suite to ensure zero regressions
cd app/server && uv run pytest -v
```

**Frontend Testing**:
```bash
# Validate TypeScript compilation
cd app/client && bun tsc --noEmit

# Validate production build
cd app/client && bun run build
```

## Notes

### Current Implementation Status

**Backend**: ✅ 100% Complete
- Export endpoints fully implemented and tested
- CSV generation utility handles all edge cases
- Security validation prevents SQL injection
- Comprehensive unit test coverage
- Proper error handling and logging

**Frontend API Client**: ✅ 100% Complete
- `api.exportTable()` method implemented
- `api.exportResults()` method implemented
- Both methods return Blob objects for download triggers

**Frontend UI**: ✅ ALREADY IMPLEMENTED (Requires Validation)
Based on code review of `app/client/src/main.ts`:
- Export buttons are implemented in `displayTables()` (lines 248-252)
- Export buttons are implemented in `displayResults()` (lines 136-156)
- `exportTable()` function implemented (lines 471-479)
- `exportQueryResults()` function implemented (lines 482-499)
- `downloadBlob()` helper function implemented (lines 459-468)

### Implementation Focus for This ADW Run

Since the implementation appears to be complete, this ADW run focuses on:
1. ✅ Validating all backend tests pass
2. ✅ Validating frontend builds without errors
3. ✅ Creating comprehensive E2E test specification
4. ✅ Executing E2E test to validate end-to-end functionality
5. ✅ Manual validation of UI button positions and download behavior
6. ✅ Documenting any issues found and fixing them

### CSV Format Standards

The implementation follows RFC 4180 CSV standards:
- **Line Endings**: CRLF (`\r\n`) for maximum compatibility across platforms
- **Quoting**: Minimal quoting (only when necessary for special characters)
- **Escaping**: Proper escaping of quotes, commas, and newlines
- **Encoding**: UTF-8 for international character support
- **Null Handling**: None/null values converted to empty strings

### Button Positioning Requirements

**Table Export Button**:
- Icon: ⬇ (download arrow)
- Position: Directly to the left of the 'x' (remove) button
- Container: Button group in table header
- Styling: Consistent with remove button styling

**Results Export Button**:
- Icon: ⬇ Export Results or similar clear indicator
- Position: In the query results header area, near the "Hide" button
- Visibility: Only shown when results are available (not on errors or empty results)
- Styling: Consistent with other action buttons

### Future Enhancements
Potential improvements for future iterations (not part of this implementation):
- Export format selection (CSV, JSON, Excel, Parquet)
- Custom column selection for exports (choose which columns to export)
- Export preview before download
- Export progress indicator for very large datasets
- Batch export of multiple tables simultaneously
- Scheduled/automated exports on a timer
- Export history tracking
- Compression options (ZIP for large files)
- Direct export to cloud storage (Google Drive, Dropbox)
