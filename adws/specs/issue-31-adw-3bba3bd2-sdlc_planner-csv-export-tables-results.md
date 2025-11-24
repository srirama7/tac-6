# Feature: One-Click CSV Export for Tables and Query Results

## Feature Description
Add one-click CSV export functionality to the Natural Language SQL Interface application, enabling users to download both database tables and query results as CSV files. This feature provides two new export buttons strategically placed in the UI: one for exporting entire tables (next to the table's remove button) and one for exporting query results (next to the hide button in the results section). The backend already has the necessary CSV export endpoints implemented; this feature focuses on integrating the UI download functionality.

## User Story
As a user of the Natural Language SQL Interface
I want to export tables and query results as CSV files with a single click
So that I can easily analyze, share, or backup my data in a standard format without manually copying results

## Problem Statement
Users currently have no way to export their data from the application. When users query data or view available tables, they can only view the results in the browser. To analyze data in external tools (Excel, Google Sheets, data analysis software) or share results with others, users must manually copy and paste data, which is error-prone and time-consuming. There is a need for a simple, reliable way to download data in a universally compatible CSV format.

## Solution Statement
Implement one-click CSV export buttons in the UI that leverage the existing backend CSV export endpoints (`/api/export/table/{table_name}` and `/api/export/results`). Add download buttons with appropriate icons positioned directly to the left of existing action buttons: next to the 'x' icon for table exports and next to the 'hide' button for query results exports. When clicked, these buttons will fetch CSV data from the backend and trigger browser downloads with appropriate filenames. The solution uses the existing `api.exportTable()` and `api.exportResults()` methods already implemented in `client.ts`.

## Relevant Files
Use these files to implement the feature:

- `app/client/src/main.ts` (lines 188-258) - Contains the `displayTables()` function where table items are rendered. Need to add download button next to the remove button for each table.
- `app/client/src/main.ts` (lines 118-154) - Contains the `displayResults()` function where query results are displayed. Need to add download button next to the hide button in the results section.
- `app/client/src/api/client.ts` (lines 80-108) - Already implements `exportTable()` and `exportResults()` methods that handle the backend API calls and return Blob objects.
- `app/client/index.html` (lines 28-36) - Results section structure showing where the download button for results should be placed.
- `app/client/index.html` (lines 38-44) - Tables section structure showing where table download buttons should be placed.
- `app/client/src/style.css` - Will need to add styles for the new download buttons to match the existing UI design.
- `app/server/server.py` (lines 282-365) - Backend endpoints already implemented for both table and results export.
- `app/server/core/csv_exporter.py` - Backend CSV generation utility already implemented.
- `app/server/core/data_models.py` (lines 84-92) - Backend data models for CSV export already defined.
- `app/server/tests/test_csv_export.py` - Existing backend tests for CSV export functionality.

### New Files

- `../.claude/commands/e2e/test_csv_export.md` - E2E test file to validate the CSV export feature works correctly in the browser. This test will verify both table export and query results export functionality.

## Implementation Plan

### Phase 1: Foundation
Before implementing the main feature, ensure understanding of:
1. Existing CSV export backend endpoints and their response formats
2. Current UI layout and button styling patterns
3. Browser download mechanics using Blob objects
4. Error handling patterns in the existing codebase

### Phase 2: Core Implementation
Add download functionality to the frontend:
1. Implement download button for table exports in the `displayTables()` function
2. Implement download button for query results exports in the `displayResults()` function
3. Create utility function to trigger browser downloads from Blob objects
4. Add appropriate download icons using HTML entities or SVG
5. Add CSS styling for download buttons to match existing UI design
6. Implement error handling for failed downloads

### Phase 3: Integration
Integrate the feature with existing functionality:
1. Ensure download buttons work seamlessly with existing table removal and result hiding features
2. Test download functionality with various data types and sizes
3. Verify CSV files download with correct filenames
4. Create E2E test to validate the feature works end-to-end
5. Run full test suite to ensure no regressions

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create E2E Test File
- Create a new E2E test file at `../.claude/commands/e2e/test_csv_export.md`
- Follow the pattern from `test_basic_query.md` and `test_complex_query.md`
- Include test steps for:
  1. Uploading sample data to create a table
  2. Clicking the download button next to a table to export it
  3. Verifying the CSV file downloads with correct filename
  4. Running a query to get results
  5. Clicking the download button next to the hide button to export results
  6. Verifying the query results CSV downloads
- Include screenshots at each major step
- Define clear success criteria for both export types

### Step 2: Implement Utility Function for Browser Downloads
- Read `app/client/src/main.ts` to understand existing utility functions
- Add a new utility function `triggerDownload(blob: Blob, filename: string)` that:
  - Creates an object URL from the Blob
  - Creates a temporary anchor element
  - Sets the download attribute with the filename
  - Programmatically clicks the anchor to trigger download
  - Cleans up by revoking the object URL
- Place this function near other utility functions like `getTypeEmoji()`

### Step 3: Add Download Button to Table Items
- Locate the `displayTables()` function in `app/client/src/main.ts` (around line 188)
- Find where the remove button is created (around line 223-227)
- Add a download button just before the remove button:
  - Create button element with class `download-table-button`
  - Use download icon (Unicode: ⬇ or ↓ or HTML entity: &darr; or ⬇️)
  - Set title attribute to "Download table as CSV"
  - Add onclick handler that calls `exportTableAsCSV(table.name)`
  - Position it in the tableHeader between tableLeft and removeButton
- Create the `exportTableAsCSV(tableName: string)` async function that:
  - Calls `api.exportTable(tableName)`
  - Handles the returned Blob
  - Triggers download with filename `{tableName}.csv`
  - Shows error message on failure using existing `displayError()` function

### Step 4: Add Download Button to Query Results
- Locate the `displayResults()` function in `app/client/src/main.ts` (around line 118)
- Find where the toggle button is created and displayed (around line 149-153)
- Update the results header section to include a download button:
  - Modify the results-header div structure to include the download button
  - Create button element with class `download-results-button`
  - Use download icon (same as table download button for consistency)
  - Set title attribute to "Download results as CSV"
  - Add onclick handler that calls `exportResultsAsCSV(response.columns, response.results)`
  - Position it directly to the left of the toggle button
- Create the `exportResultsAsCSV(columns: string[], results: Record<string, any>[])` async function that:
  - Calls `api.exportResults(columns, results)`
  - Handles the returned Blob
  - Triggers download with filename `query_results_{timestamp}.csv`
  - Shows error message on failure using existing `displayError()` function

### Step 5: Update HTML Structure for Results Header
- Read `app/client/index.html` to understand the results section structure (lines 28-36)
- Update the results-header div in the `displayResults()` function to properly accommodate both download and toggle buttons
- Ensure buttons are aligned properly with flexbox or existing layout patterns

### Step 6: Add CSS Styling for Download Buttons
- Read `app/client/src/style.css` to understand existing button styles
- Add styles for `.download-table-button` and `.download-results-button`:
  - Match the style of the remove button (`.remove-table-button`)
  - Use appropriate sizing (similar to existing buttons)
  - Add hover effects for better UX
  - Ensure proper spacing between buttons
  - Consider using a download icon or Unicode character
  - Make buttons visually distinct but consistent with overall design

### Step 7: Test Download Functionality Manually
- Start the development server and client
- Upload a test CSV file to create a table
- Click the download button next to a table
- Verify the CSV file downloads with the correct table name
- Run a natural language query
- Click the download button next to the hide button
- Verify the results CSV downloads with a timestamped filename
- Test with different data types and special characters
- Verify error handling when downloads fail

### Step 8: Run Validation Commands
- Execute all validation commands listed in the "Validation Commands" section below
- Fix any issues that arise during validation
- Ensure all tests pass with zero errors

## Testing Strategy

### Unit Tests
- Backend CSV export functionality is already tested in `app/server/tests/test_csv_export.py`
- No new backend unit tests needed as endpoints are already implemented and tested
- Frontend testing will be done through E2E tests since the feature is primarily UI-focused

### Edge Cases
- Empty tables (should download CSV with headers only)
- Empty query results (should download CSV with headers only)
- Tables with special characters in names (should sanitize filenames)
- Very large tables (should handle blob size appropriately)
- Tables with NULL values (should export as empty strings)
- Tables with special characters in data (quotes, commas, newlines - already handled by backend)
- Query results with missing columns (should handle gracefully)
- Network failures during download (should show error message)
- Multiple rapid downloads (should handle concurrent downloads)

## Acceptance Criteria
- Download button appears next to the 'x' icon for each table in the Available Tables section
- Download button appears next to the 'hide' button in the Query Results section
- Clicking table download button downloads the entire table as a CSV file with filename `{table_name}.csv`
- Clicking results download button downloads query results as a CSV file with filename `query_results_{timestamp}.csv`
- Download buttons use appropriate download icons (⬇ or similar)
- Download buttons match the visual style of existing buttons in the UI
- CSV files contain properly formatted data with headers
- Special characters in data are properly escaped in CSV files
- Error messages appear if downloads fail
- Downloads work in Chrome, Firefox, Safari, and Edge browsers
- No regressions in existing functionality (table removal, result hiding, etc.)
- E2E test passes validating both export types work correctly
- All existing unit tests and integration tests pass

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `../.claude/commands/test_e2e.md`, then read and execute the new E2E test file `../.claude/commands/e2e/test_csv_export.md` to validate this functionality works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript compilation to validate no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature builds correctly with zero errors

## Notes

### Implementation Notes
- The backend CSV export endpoints are already fully implemented and tested (`/api/export/table/{table_name}` and `/api/export/results`)
- The API client methods (`api.exportTable()` and `api.exportResults()`) are already implemented in `app/client/src/api/client.ts`
- Focus implementation on UI integration and browser download triggering
- Use the existing error handling patterns from the codebase (`displayError()` function)
- Maintain consistency with existing UI patterns and styling

### Download Icon Options
- Unicode characters: ⬇ (U+2B07), ↓ (U+2193), ⬇️ (U+2B07 U+FE0F)
- HTML entities: `&darr;`, `&#8595;`, `&#11015;`
- Or use an SVG icon if preferred for better styling control

### Browser Compatibility
- The Blob download approach works in all modern browsers
- Object URL cleanup prevents memory leaks
- Consider adding a brief success toast notification (optional enhancement)

### Future Considerations
- Add export format options (CSV, JSON, Excel) in a future iteration
- Add option to export multiple tables at once
- Add progress indicator for large exports
- Add ability to customize column selection before export
- Consider adding export history or recent downloads section
