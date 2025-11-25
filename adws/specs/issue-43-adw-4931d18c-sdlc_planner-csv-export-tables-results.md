# Feature: CSV Export for Tables and Query Results

## Feature Description
This feature adds one-click CSV export functionality to enable users to download their database tables and query results as CSV files. Two new download buttons will be added to the UI: one for exporting entire tables (placed next to the 'x' removal button), and one for exporting query results (placed next to the 'Hide' button). The feature includes two new backend endpoints to handle the CSV generation and delivery.

## User Story
As a user analyzing data in the Natural Language SQL Interface
I want to export tables and query results as CSV files with a single click
So that I can use the data in external tools like Excel, Google Sheets, or other data analysis applications

## Problem Statement
Currently, users can view their data and query results within the application, but they have no way to export this data for use in external tools or for offline analysis. This limits the utility of the application and creates friction when users need to share or further process their data.

## Solution Statement
Implement a CSV export feature with two download buttons and two corresponding backend endpoints:
1. A table export endpoint (`/api/table/{table_name}/export`) that generates a CSV of all data in a table
2. A query results export endpoint (`/api/query/export`) that generates a CSV of the most recent query results
3. Frontend download buttons with appropriate icons positioned next to existing UI controls
4. CSV generation using Python's csv module with proper escaping and encoding

## Relevant Files
Use these files to implement the feature:

- `app/server/server.py` - Add two new FastAPI endpoints for CSV export
- `app/server/core/data_models.py` - Add new Pydantic models for export requests/responses
- `app/client/src/api/client.ts` - Add API methods for CSV export endpoints
- `app/client/src/types.d.ts` - Add TypeScript type definitions for export functionality
- `app/client/src/main.ts` - Add download button event handlers and CSV download logic
- `app/client/index.html` - Add download button elements to the DOM structure
- `app/client/src/style.css` - Add styling for download buttons

### New Files
- `.claude/commands/e2e/test_csv_export.md` - E2E test file to validate CSV export functionality

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for CSV export:
- Add new data models for export requests and responses
- Implement CSV generation logic for table exports
- Implement CSV generation logic for query result exports
- Add proper error handling and validation

### Phase 2: Core Implementation
Implement the two backend endpoints:
- `/api/table/{table_name}/export` - Returns CSV file of entire table
- `/api/query/export` - Returns CSV file of query results (requires session management or request payload)
- Implement proper HTTP headers for file downloads (Content-Type, Content-Disposition)
- Add table existence validation and security checks

### Phase 3: Integration
Connect the frontend to the new endpoints:
- Add API client methods for both export endpoints
- Add download buttons to the UI with appropriate icons
- Implement client-side download logic to trigger browser file downloads
- Add loading states and error handling
- Update UI styling to accommodate new buttons

## Step by Step Tasks

### Step 1: Backend - Add Data Models
- Open `app/server/core/data_models.py`
- Add `TableExportResponse` model for table CSV exports
- Add `QueryExportRequest` model for query result export requests
- Add `QueryExportResponse` model for query result exports

### Step 2: Backend - Implement Table Export Endpoint
- Open `app/server/server.py`
- Add `GET /api/table/{table_name}/export` endpoint
- Validate table name using existing security functions
- Query all data from the specified table using secure SQL execution
- Generate CSV using Python's csv module with proper escaping
- Return response with appropriate headers: `Content-Type: text/csv`, `Content-Disposition: attachment; filename="{table_name}.csv"`
- Add comprehensive error handling for missing tables and database errors

### Step 3: Backend - Implement Query Results Export Endpoint
- Open `app/server/server.py`
- Add `POST /api/query/export` endpoint
- Accept request body containing the query results data (columns and rows)
- Generate CSV from the provided data using Python's csv module
- Return response with appropriate headers: `Content-Type: text/csv`, `Content-Disposition: attachment; filename="query_results.csv"`
- Add error handling for invalid data formats

### Step 4: Backend - Add Unit Tests
- Open `app/server/tests/core/test_file_processor.py` or create new test file
- Add tests for table export endpoint:
  - Test successful export with valid table
  - Test error handling for non-existent table
  - Test CSV format correctness
  - Test proper escaping of special characters
- Add tests for query results export endpoint:
  - Test successful export with valid data
  - Test CSV format correctness
  - Test handling of empty results

### Step 5: Frontend - Add TypeScript Types
- Open `app/client/src/types.d.ts`
- Add `QueryExportRequest` interface matching backend model
- Add appropriate response types for blob/file downloads

### Step 6: Frontend - Add API Client Methods
- Open `app/client/src/api/client.ts`
- Add `exportTable(tableName: string): Promise<Blob>` method
- Add `exportQueryResults(request: QueryExportRequest): Promise<Blob>` method
- Use fetch with appropriate options to handle binary response (blob)
- Add error handling for failed downloads

### Step 7: Frontend - Add Download Buttons to HTML
- Open `app/client/index.html`
- Add download button in the table header section (line ~223) next to the remove button
- Use an appropriate download icon (e.g., ⬇ or 📥)
- Add download button in the results header section (line ~32) next to the "Hide" button
- Ensure buttons have appropriate IDs for event binding

### Step 8: Frontend - Implement Download Logic
- Open `app/client/src/main.ts`
- Create helper function `downloadCSV(blob: Blob, filename: string)` to trigger browser download
- Update `displayTables()` function to add event listeners to table download buttons
- Update `displayResults()` function to add event listener to query results download button
- Store current query results in a variable accessible to the download handler
- Add loading states for download buttons during export
- Add error handling and user feedback for failed exports

### Step 9: Frontend - Add Styling
- Open `app/client/src/style.css`
- Add styles for download buttons to match existing button design
- Ensure buttons are properly positioned and sized
- Add hover states and loading states
- Ensure responsive design works with new buttons

### Step 10: Create E2E Test
- Create new file `.claude/commands/e2e/test_csv_export.md`
- Follow the format from `test_basic_query.md` and `test_complex_query.md`
- Define test steps to validate:
  - Upload a sample table
  - Click table export button and verify CSV download
  - Execute a query
  - Click query results export button and verify CSV download
  - Verify CSV file contents are correct
- Include screenshots at key steps

### Step 11: Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Run E2E test to validate the feature works end-to-end
- Fix any issues that arise

## Testing Strategy

### Unit Tests
- **Table Export Endpoint**: Test successful exports, error cases (non-existent table, invalid table name), CSV format correctness
- **Query Export Endpoint**: Test successful exports with various data types, empty results, CSV format correctness
- **CSV Generation**: Test proper escaping of quotes, commas, newlines in data
- **Security**: Test that table name validation prevents SQL injection

### Edge Cases
- Empty tables (no data to export)
- Empty query results
- Tables with special characters in column names or data
- Tables with NULL values
- Very large tables (performance and memory considerations)
- Query results with mixed data types
- Concurrent export requests
- Invalid table names in export requests

## Acceptance Criteria
- [ ] Two new backend endpoints are implemented and functional
- [ ] Table export endpoint returns valid CSV for any existing table
- [ ] Query results export endpoint returns valid CSV for provided data
- [ ] Download button appears next to 'x' icon in Available Tables section
- [ ] Download button appears next to 'Hide' button in Query Results section
- [ ] Clicking table download button downloads the complete table as CSV
- [ ] Clicking query results download button downloads current results as CSV
- [ ] CSV files have proper formatting with headers and escaped special characters
- [ ] CSV files are named appropriately (table name or "query_results")
- [ ] Appropriate error messages appear if export fails
- [ ] Download buttons show loading state during export
- [ ] All existing functionality continues to work (zero regressions)
- [ ] Unit tests pass for new endpoints
- [ ] E2E test validates the complete export workflow

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_csv_export.md` to validate CSV export functionality works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Manually test table export by uploading a CSV and clicking the download button
- Manually test query results export by running a query and clicking the download button
- Verify downloaded CSV files can be opened in Excel/Google Sheets

## Notes

### Technical Decisions
1. **CSV Library**: Use Python's built-in `csv` module for robust CSV generation with proper escaping
2. **Response Type**: Use FastAPI's `StreamingResponse` with `media_type="text/csv"` for efficient large file handling
3. **Frontend Download**: Use Blob and `URL.createObjectURL()` to trigger browser downloads
4. **Query Results Strategy**: Accept results as POST body rather than storing in session to keep the implementation stateless

### Security Considerations
- Reuse existing `validate_identifier()` and `check_table_exists()` functions for table name validation
- Ensure CSV export doesn't expose sensitive system information
- Use parameterized queries for all database operations

### Performance Considerations
- For very large tables, consider streaming CSV generation instead of loading all data into memory
- Add appropriate timeouts for export operations
- Consider adding pagination or row limits for extremely large exports in future iterations

### Icon Suggestions
- Use ⬇ (downward arrow) or 📥 (inbox with arrow) as download icon
- Ensure icon is visually distinct but consistent with existing UI design

### Future Enhancements (not in scope for this feature)
- Add export format options (JSON, Excel, etc.)
- Add column selection for partial exports
- Add export scheduling/automation
- Add compression for large exports
