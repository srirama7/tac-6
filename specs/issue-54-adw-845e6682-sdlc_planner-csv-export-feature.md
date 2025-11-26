# Feature: CSV Export for Tables and Query Results

## Metadata
issue_number: `54`
adw_id: `845e6682`
issue_json: `{"number":54,"title":"tac6six","body":"Using adw_plan_build_review add one click table exports and one click result export feature to get results as csv files.\n\nCreate two new endpoints to support these features. One exporting tables, one for exporting query results.\n\nPlace a download button directly to the left of the 'x' icon for available tables.\nPlace a download button directly to the left of the 'hide' button for query results.\n\nUse the appropriate download icon.","state":"OPEN","author":{"id":"U_kgDOCDKQYA","login":"srirama7","name":"Amogha Bhat M R","is_bot":false},"assignees":[],"labels":[],"milestone":null,"comments":[{"id":"IC_kwDOQXQFdM7VYtgf","author":{"id":null,"login":"srirama7","name":null,"is_bot":false},"body":"## 📊 ADW Workflow Complete - Issue #54\n\n### Summary\nThe CSV export feature has been successfully implemented and tested.\n\n### Artifacts\n- **Branch:** `feature-issue-54-adw-b3a1bde8-csv-export-tables-results`\n- **ADW ID:** `b3a1bde8`\n- **Pull Request:** https://github.com/srirama7/tac-6/pull/55\n\n### Implementation Details\n- **Backend Endpoints:**\n  - `GET /api/table/{table_name}/export` - Export table data as CSV\n  - `POST /api/query/export` - Export query results as CSV\n\n- **Frontend:**\n  - Download buttons for each table in Available Tables section\n  - Download button in Query Results section\n\n### Test Results\n- ✅ 21 unit tests passed\n- ✅ CSV format validation\n- ✅ UTF-8 encoding with BOM\n- ✅ SQL injection protection\n- ✅ Unicode character support\n\n### Phases Completed\n1. ✅ Planning - Implementation plan created\n2. ✅ Building - Code implemented\n3. ✅ Testing - All unit tests passed\n4. ✅ Review - PR created\n\n---\n🤖 *This workflow was automated by ADW (AI Developer Workflow)*","createdAt":"2025-11-26T08:14:56Z","updatedAt":null},{"id":"IC_kwDOQXQFdM7VZdLu","author":{"id":null,"login":"srirama7","name":null,"is_bot":false},"body":"## b3a1bde8_test_runner: 🧪 Test Results\n\n### Unit Tests: ✅ ALL PASSED (88/88)\n\n| Test Category | Tests | Status |\n|---------------|-------|--------|\n| File Processor Tests | 22 | ✅ Passed |\n| LLM Processor Tests | 16 | ✅ Passed |\n| SQL Processor Tests | 11 | ✅ Passed |\n| CSV Export Tests | 21 | ✅ Passed |\n| SQL Injection Tests | 18 | ✅ Passed |\n\n### Frontend Build: ✅ PASSED\n- TypeScript compilation: ✅ No errors\n- Vite production build: ✅ Successful\n\n### API Endpoints Verified: ✅\n- `GET /api/table/{table_name}/export` - Working correctly\n- `POST /api/query/export` - Working correctly\n- CSV files include proper UTF-8 BOM encoding for Excel compatibility\n\n### Summary\nAll tests pass and the CSV export feature is fully implemented and functional.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)","createdAt":"2025-11-26T08:54:30Z","updatedAt":null}],"createdAt":"2025-11-26T07:02:43Z","updatedAt":"2025-11-26T10:16:38Z","closedAt":null,"url":"https://github.com/srirama7/tac-6/issues/54"}`

## Feature Description
This feature adds one-click CSV export functionality to the Natural Language SQL Interface application, enabling users to download complete database tables and query results as properly formatted CSV files. The implementation includes two new backend API endpoints for generating CSV data with security validation, and intuitive download buttons in the frontend interface positioned adjacent to table controls and query result displays. All CSV exports utilize UTF-8 encoding with BOM for Excel compatibility, proper escaping for special characters (commas, quotes, newlines), and comprehensive SQL injection protection using the existing security infrastructure.

## User Story
As a data analyst or business user
I want to export database tables and query results to CSV files with a single click
So that I can perform further analysis in Excel or Google Sheets, share data with colleagues, create reports, and maintain offline copies of query results without manually copying data

## Problem Statement
The current application allows users to view data through the web interface but provides no mechanism to export this data for use in external tools. Users who need to analyze data in spreadsheet applications, share results with team members, or create detailed reports must resort to manual copy-paste operations, which are time-consuming, error-prone, and prone to formatting loss. Additionally, viewing large result sets in the browser is impractical for comprehensive analysis. There is a clear need for a streamlined, one-click export mechanism that preserves data integrity, handles special characters correctly, maintains proper encoding for international characters, and integrates seamlessly with popular spreadsheet applications like Microsoft Excel and Google Sheets.

## Solution Statement
Implement a comprehensive CSV export system consisting of backend API endpoints and frontend UI components. The backend will provide two RESTful endpoints: `GET /api/table/{table_name}/export` for exporting complete tables and `POST /api/query/export` for exporting query results. These endpoints will generate RFC 4180-compliant CSV files with UTF-8 encoding including BOM (Byte Order Mark) for Excel compatibility, proper CSV escaping for commas, quotes, and newlines, and comprehensive security validation using the existing `sql_security` module to prevent SQL injection attacks. The frontend will display download buttons with download icons (⬇) positioned directly to the left of the × icon for each table in the Available Tables section, and to the left of the Hide button in the Query Results section. When clicked, these buttons will trigger instant CSV downloads with descriptive filenames. The implementation will use Python's built-in `csv` module for reliable formatting, the FastAPI Response class with StreamingResponse for efficient file delivery, and blob-based downloads in the browser for proper file handling.

## Relevant Files
Use these files to implement the feature:

- **Backend Core Files:**
  - `app/server/server.py` - Main FastAPI application; will add two new export endpoints (GET /api/table/{table_name}/export and POST /api/query/export) with proper response headers for CSV download
  - `app/server/core/data_models.py` - Pydantic models for request/response validation; will add ExportQueryRequest model for POST endpoint
  - `app/server/core/sql_security.py` - SQL security utilities including validate_identifier, check_table_exists, and execute_query_safely; will be used extensively to secure export operations
  - `app/server/core/sql_processor.py` - SQL execution functions; may use get_database_schema and existing query execution patterns

- **Frontend Files:**
  - `app/client/src/main.ts` - Main TypeScript application file containing UI logic including displayTables() and displayResults() functions; will add download button creation and click handlers
  - `app/client/src/api/client.ts` - API client with functions like uploadFile, processQuery, getSchema; will add exportTable and exportQueryResults methods
  - `app/client/src/types.d.ts` - TypeScript type definitions; will add ExportQueryRequest interface and related types
  - `app/client/src/style.css` - CSS styles for the application; will add styles for download buttons including hover effects and loading states

- **Testing Files:**
  - `app/server/tests/test_sql_injection.py` - Comprehensive SQL injection tests; will add tests for export endpoints to verify table name validation
  - `.claude/commands/test_e2e.md` - E2E test runner that executes Playwright-based tests
  - `.claude/commands/e2e/test_basic_query.md` - Example E2E test showing test format and structure

- **Documentation:**
  - `README.md` - Project documentation with API endpoints section; will document the two new CSV export endpoints

### New Files
- `app/server/core/csv_exporter.py` - New module containing CSV generation logic including generate_csv_from_data, export_table_to_csv, and export_query_results_to_csv functions with proper UTF-8 BOM encoding, CSV escaping, and security integration
- `app/server/tests/core/test_csv_exporter.py` - Comprehensive test suite for CSV export functionality covering formatting, encoding, special characters, Unicode support, empty data handling, and security validation
- `.claude/commands/e2e/test_csv_export.md` - E2E test file validating the complete CSV export workflow from uploading data to downloading both table exports and query result exports with visual verification

## Implementation Plan

### Phase 1: Foundation
Build the core CSV export infrastructure by creating a dedicated `csv_exporter.py` module in the `app/server/core/` directory. This module will handle all CSV generation logic including data serialization from database rows to CSV format, UTF-8 encoding with BOM prepended to the file content for Excel compatibility, proper CSV escaping for special characters (commas require field quoting, double quotes must be doubled, newlines must be preserved within quoted fields), and integration with the existing `sql_security` module for safe table name validation and query execution. The exporter will use Python's built-in `csv` module with csv.QUOTE_MINIMAL quoting strategy and proper delimiter/quotechar configuration. This foundational module will serve both table exports and query result exports, ensuring consistent CSV formatting and security across all export operations. Include comprehensive error handling for edge cases like empty result sets, NULL values, and malformed data.

### Phase 2: Core Implementation
Implement the backend API endpoints in `app/server/server.py` and add necessary data models in `app/server/core/data_models.py`. First, add the `ExportQueryRequest` Pydantic model with fields for results (List[Dict[str, Any]]), columns (List[str]), and optional filename (str). Then implement `GET /api/table/{table_name}/export` which validates the table_name parameter using `validate_identifier()`, checks table existence with `check_table_exists()`, executes a SELECT * query using `execute_query_safely()` to fetch all table data, converts the data to CSV using the csv_exporter module, and returns a Response with media_type="text/csv", charset="utf-8", and Content-Disposition header for file download. Next, implement `POST /api/query/export` which accepts an ExportQueryRequest body, validates the input data, generates CSV from the provided results and columns, and returns the CSV file with appropriate headers. Both endpoints must include comprehensive error handling with appropriate HTTP status codes (400 for validation errors, 404 for non-existent tables, 500 for server errors), detailed logging of export operations, and SQL injection protection through the security module. Create comprehensive unit tests in `app/server/tests/core/test_csv_exporter.py` covering CSV formatting correctness, UTF-8 BOM presence, special character escaping (commas, quotes, newlines, tabs), Unicode support (emojis, Chinese characters, Arabic text), empty data handling, NULL value representation, SQL injection prevention, and performance with large datasets.

### Phase 3: Integration
Integrate CSV export functionality into the frontend by updating the TypeScript code and styles. In `app/client/src/api/client.ts`, add two new API methods: `exportTable(tableName: string): Promise<Blob>` which calls GET /api/table/{tableName}/export and returns the response as a Blob, and `exportQueryResults(results: any[], columns: string[]): Promise<Blob>` which calls POST /api/query/export with the results data. In `app/client/src/types.d.ts`, add the ExportQueryRequest interface matching the backend model. In `app/client/src/main.ts`, modify the `displayTables()` function to add a download button before each table's remove button with the HTML entity ⬇ or SVG download icon, proper CSS class, click handler that calls api.exportTable, creates a blob URL, triggers download via an invisible anchor element, and cleans up the blob URL afterward. Similarly, modify the `displayResults()` function to add a download button before the Hide button with a click handler for exporting query results. In `app/client/src/style.css`, add styles for `.download-button` including dimensions, colors matching the theme, hover effects, active states, and loading states. Create an E2E test file at `.claude/commands/e2e/test_csv_export.md` that tests uploading sample data, verifying download buttons appear, clicking the table download button, verifying a CSV file would be downloaded (check the download initiation), executing a query, and clicking the query results download button. The test should capture screenshots at key steps and validate the UI elements are present and functional.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create CSV Exporter Module with Core Functions
- Create new file `app/server/core/csv_exporter.py`
- Import required modules: `csv`, `io`, `sqlite3`, `typing` (List, Dict, Any), and from `core.sql_security` import `validate_identifier`, `execute_query_safely`, `check_table_exists`, `SQLSecurityError`
- Implement `generate_csv_from_data(data: List[Dict[str, Any]], columns: List[str]) -> str` function:
  - Create StringIO buffer for in-memory CSV generation
  - Prepend UTF-8 BOM character ('\ufeff') to buffer
  - Create csv.DictWriter with columns as fieldnames, quoting=csv.QUOTE_MINIMAL
  - Write header row using writeheader()
  - Write all data rows using writerows(data)
  - Return buffer.getvalue() as string
  - Handle empty data gracefully (if no data, still write headers)
  - Convert None values to empty strings for CSV compatibility
- Implement `export_table_to_csv(table_name: str) -> str` function:
  - Validate table_name using validate_identifier(table_name, "table")
  - Connect to database at "db/database.db"
  - Check table exists using check_table_exists(conn, table_name)
  - If table doesn't exist, raise ValueError with descriptive message
  - Execute SELECT * query using execute_query_safely with identifier_params
  - Fetch all rows and column names from cursor.description
  - Convert rows to list of dictionaries with column names as keys
  - Call generate_csv_from_data with data and columns
  - Close connection and return CSV string
- Implement `export_query_results_to_csv(results: List[Dict[str, Any]], columns: List[str]) -> str` function:
  - Validate that results and columns are provided
  - Simply call generate_csv_from_data(results, columns) and return result
- Add comprehensive docstrings for all functions explaining parameters, return values, and raised exceptions

### Step 2: Create Comprehensive Unit Tests for CSV Exporter
- Create new file `app/server/tests/core/test_csv_exporter.py`
- Import pytest, csv_exporter functions, and test utilities
- Add test `test_generate_csv_basic()` - Test generating CSV from simple data with 3 rows and 3 columns, verify headers and data rows are present
- Add test `test_generate_csv_utf8_bom()` - Verify CSV starts with UTF-8 BOM character ('\ufeff')
- Add test `test_generate_csv_special_characters()` - Test data with commas, double quotes, and newlines in values, verify proper escaping
- Add test `test_generate_csv_unicode()` - Test data with emojis, Chinese characters, Arabic text, verify correct encoding
- Add test `test_generate_csv_empty_data()` - Test with empty list of rows but with column headers, verify headers are still written
- Add test `test_generate_csv_null_values()` - Test data with None values, verify they become empty strings in CSV
- Add test `test_export_table_to_csv()` - Create test table in memory, insert test data, call export_table_to_csv, verify CSV content
- Add test `test_export_table_nonexistent()` - Try to export non-existent table, verify ValueError is raised
- Add test `test_export_table_sql_injection()` - Try to export with malicious table name like "users; DROP TABLE users--", verify SQLSecurityError is raised
- Add test `test_export_query_results()` - Test export_query_results_to_csv with sample query results, verify CSV is generated correctly
- Add test `test_large_dataset_performance()` - Test with 1000 rows, verify export completes in reasonable time (< 2 seconds)
- Run tests: `cd app/server && uv run pytest tests/core/test_csv_exporter.py -v`
- Fix any test failures before proceeding

### Step 3: Add Backend Data Models for Export Endpoints
- Open `app/server/core/data_models.py`
- Add new model after existing models:
```python
class ExportQueryRequest(BaseModel):
    results: List[Dict[str, Any]] = Field(..., description="Query results to export")
    columns: List[str] = Field(..., description="Column names for the results")
    filename: Optional[str] = Field("query_results", description="Base filename for the export")
```
- Ensure all necessary imports are present (List, Dict, Any, Optional, Field from pydantic)

### Step 4: Implement Table Export Endpoint
- Open `app/server/server.py`
- Import required modules at the top: `from fastapi.responses import Response`, and from `core.csv_exporter` import `export_table_to_csv`
- Add new endpoint after the existing DELETE /api/table/{table_name} endpoint:
```python
@app.get("/api/table/{table_name}/export")
async def export_table(table_name: str):
    """Export a database table as CSV file"""
    try:
        # Validate table name (will raise SQLSecurityError if invalid)
        validate_identifier(table_name, "table")

        # Generate CSV
        csv_content = export_table_to_csv(table_name)

        # Return CSV as downloadable file
        response = Response(
            content=csv_content,
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="{table_name}.csv"'
            }
        )

        logger.info(f"[SUCCESS] Table exported: {table_name}")
        return response

    except SQLSecurityError as e:
        logger.error(f"[ERROR] Table export security error: {str(e)}")
        raise HTTPException(400, str(e))
    except ValueError as e:
        logger.error(f"[ERROR] Table export failed: {str(e)}")
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.error(f"[ERROR] Table export failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        raise HTTPException(500, f"Error exporting table: {str(e)}")
```
- Ensure proper error handling and logging for all cases

### Step 5: Implement Query Export Endpoint
- In `app/server/server.py`, import `ExportQueryRequest` from core.data_models and `export_query_results_to_csv` from core.csv_exporter
- Add new endpoint after the table export endpoint:
```python
@app.post("/api/query/export")
async def export_query_results(request: ExportQueryRequest):
    """Export query results as CSV file"""
    try:
        # Validate input
        if not request.results and not request.columns:
            raise HTTPException(400, "No data to export")

        # Generate CSV
        csv_content = export_query_results_to_csv(request.results, request.columns)

        # Generate filename with timestamp for uniqueness
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{request.filename}_{timestamp}.csv"

        # Return CSV as downloadable file
        response = Response(
            content=csv_content,
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )

        logger.info(f"[SUCCESS] Query results exported: {len(request.results)} rows")
        return response

    except Exception as e:
        logger.error(f"[ERROR] Query export failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        raise HTTPException(500, f"Error exporting query results: {str(e)}")
```
- Ensure proper error handling and logging

### Step 6: Add SQL Injection Tests for Export Endpoints
- Open `app/server/tests/test_sql_injection.py`
- Add new test class or section for export endpoint security:
```python
def test_export_table_sql_injection():
    """Test that export endpoint blocks SQL injection in table names"""
    # Test various SQL injection patterns
    malicious_names = [
        "users; DROP TABLE users--",
        "users' OR '1'='1",
        "users'; DELETE FROM users--",
        "../etc/passwd",
        "users UNION SELECT * FROM passwords--"
    ]

    for malicious_name in malicious_names:
        try:
            validate_identifier(malicious_name, "table")
            assert False, f"Should have raised error for: {malicious_name}"
        except SQLSecurityError:
            pass  # Expected
```
- Add similar tests for various attack vectors
- Run tests: `cd app/server && uv run pytest tests/test_sql_injection.py -v`

### Step 7: Add Frontend Type Definitions
- Open `app/client/src/types.d.ts`
- Add the ExportQueryRequest interface:
```typescript
interface ExportQueryRequest {
  results: Array<Record<string, any>>;
  columns: string[];
  filename?: string;
}
```
- Ensure it matches the backend Pydantic model structure

### Step 8: Add Frontend API Client Methods
- Open `app/client/src/api/client.ts`
- Add new methods to the api object before the closing brace:
```typescript
  // Export table as CSV
  async exportTable(tableName: string): Promise<Blob> {
    const url = `${API_BASE_URL}/table/${tableName}/export`;

    try {
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.blob();
    } catch (error) {
      console.error('Table export failed:', error);
      throw error;
    }
  },

  // Export query results as CSV
  async exportQueryResults(results: Array<Record<string, any>>, columns: string[], filename: string = 'query_results'): Promise<Blob> {
    return apiRequest<Blob>('/query/export', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        results,
        columns,
        filename
      })
    }).then(async (response) => {
      // Since apiRequest returns JSON by default, we need to handle blob differently
      const url = `${API_BASE_URL}/query/export`;
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          results,
          columns,
          filename
        })
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      return await res.blob();
    });
  }
```
- Add proper error handling and logging

### Step 9: Implement Table Download Buttons in Frontend
- Open `app/client/src/main.ts`
- Find the `displayTables()` function
- Modify the table header creation section where the removeButton is created
- Add download button before the remove button:
```typescript
// Add download button
const downloadButton = document.createElement('button');
downloadButton.className = 'download-button';
downloadButton.innerHTML = '⬇';
downloadButton.title = 'Download table as CSV';
downloadButton.onclick = async (e) => {
  e.stopPropagation();
  await downloadTableCSV(table.name, downloadButton);
};

const buttonContainer = document.createElement('div');
buttonContainer.style.display = 'flex';
buttonContainer.style.gap = '0.5rem';
buttonContainer.appendChild(downloadButton);
buttonContainer.appendChild(removeButton);

tableHeader.appendChild(tableLeft);
tableHeader.appendChild(buttonContainer);
```
- Add the `downloadTableCSV` helper function before the displayTables function:
```typescript
// Download table as CSV
async function downloadTableCSV(tableName: string, button: HTMLButtonElement) {
  const originalText = button.innerHTML;
  button.innerHTML = '<span class="loading"></span>';
  button.disabled = true;

  try {
    const blob = await api.exportTable(tableName);

    // Create download link
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${tableName}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    // Show success feedback
    button.innerHTML = '✓';
    setTimeout(() => {
      button.innerHTML = originalText;
      button.disabled = false;
    }, 1000);
  } catch (error) {
    displayError(error instanceof Error ? error.message : 'Export failed');
    button.innerHTML = originalText;
    button.disabled = false;
  }
}
```

### Step 10: Implement Query Results Download Button in Frontend
- In `app/client/src/main.ts`, find the `displayResults()` function
- Modify the section where the toggle button is created to add a download button
- Add download button next to the Hide button:
```typescript
// Create button container for Hide and Download buttons
const buttonContainer = document.createElement('div');
buttonContainer.style.display = 'flex';
buttonContainer.style.gap = '0.5rem';

// Add download button
const downloadResultsButton = document.createElement('button');
downloadResultsButton.id = 'download-results';
downloadResultsButton.className = 'download-button';
downloadResultsButton.innerHTML = '⬇';
downloadResultsButton.title = 'Download results as CSV';
downloadResultsButton.onclick = async () => {
  await downloadQueryResultsCSV(response.results, response.columns, downloadResultsButton);
};

buttonContainer.appendChild(downloadResultsButton);
buttonContainer.appendChild(toggleButton);

// Update the results section header to include button container
const resultsHeader = resultsSection.querySelector('.results-header');
if (resultsHeader) {
  resultsHeader.appendChild(buttonContainer);
}
```
- Add the `downloadQueryResultsCSV` helper function:
```typescript
// Download query results as CSV
async function downloadQueryResultsCSV(results: Record<string, any>[], columns: string[], button: HTMLButtonElement) {
  const originalText = button.innerHTML;
  button.innerHTML = '<span class="loading"></span>';
  button.disabled = true;

  try {
    const blob = await api.exportQueryResults(results, columns);

    // Create download link
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
    a.download = `query_results_${timestamp}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    // Show success feedback
    button.innerHTML = '✓';
    setTimeout(() => {
      button.innerHTML = originalText;
      button.disabled = false;
    }, 1000);
  } catch (error) {
    displayError(error instanceof Error ? error.message : 'Export failed');
    button.innerHTML = originalText;
    button.disabled = false;
  }
}
```

### Step 11: Style Download Buttons
- Open `app/client/src/style.css`
- Add styles for download buttons at the end of the file:
```css
/* Download Button Styles */
.download-button {
  padding: 0.5rem 0.75rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 2.5rem;
  height: 2.5rem;
}

.download-button:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.download-button:active {
  transform: translateY(0);
}

.download-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.download-button .loading {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Step 12: Create E2E Test File for CSV Export
- Create new file `.claude/commands/e2e/test_csv_export.md`
- Follow the format of `test_basic_query.md` and structure it as:
```markdown
# E2E Test: CSV Export Functionality

Test CSV export features for tables and query results.

## User Story

As a data analyst
I want to export tables and query results as CSV files
So that I can analyze data in Excel or share it with colleagues

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. Click "Upload Data" button to open the upload modal
4. Click "Users" sample data button to load users table
5. Wait for table to appear in Available Tables section
6. Take a screenshot showing the table with download button
7. **Verify** download button (⬇) appears to the left of the × button
8. Click the download button on the users table
9. **Verify** CSV download is initiated (check browser download indicator)
10. Take a screenshot of the download in progress
11. Enter query: "Show all users"
12. Click Query button
13. Wait for results to appear
14. Take a screenshot of query results with download button
15. **Verify** download button appears to the left of Hide button
16. Click the download button on query results
17. **Verify** CSV download is initiated
18. Take a screenshot of the completed state

## Success Criteria
- Upload modal opens successfully
- Sample data loads and creates users table
- Download button appears for the table
- Clicking table download button initiates CSV download
- Query executes successfully
- Download button appears in query results
- Clicking results download button initiates CSV download
- All UI elements are properly positioned
- 5 screenshots are captured
```

### Step 13: Update README with New API Endpoints
- Open `README.md`
- Find the "## API Endpoints" section
- Add the two new endpoints:
```markdown
- `GET /api/table/{table_name}/export` - Export table data as CSV file
- `POST /api/query/export` - Export query results as CSV file
```

### Step 14: Run All Validation Commands
- Execute all validation commands in sequence to ensure zero regressions:
- Run CSV exporter tests: `cd app/server && uv run pytest tests/core/test_csv_exporter.py -v`
- Run SQL injection tests: `cd app/server && uv run pytest tests/test_sql_injection.py -v`
- Run all server tests: `cd app/server && uv run pytest -v`
- Run TypeScript type check: `cd app/client && bun tsc --noEmit`
- Run frontend build: `cd app/client && bun run build`
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` to validate the CSV export feature works end-to-end
- Fix any failures and re-run validation until all tests pass

## Testing Strategy

### Unit Tests

- **CSV Generation Tests:**
  - Test basic CSV formatting with headers row followed by data rows
  - Test UTF-8 BOM is present at the start of the file (first character is '\ufeff')
  - Test special character escaping: commas in values should trigger field quoting, double quotes should be escaped as "", newlines within fields should be preserved in quoted fields
  - Test Unicode characters: emojis (😀, 🎉), Chinese characters (中文), Arabic text (العربية), Cyrillic (Русский)
  - Test empty datasets: 0 rows with column headers should produce CSV with just header row, 0 columns and 0 rows should produce empty file
  - Test NULL/None value handling: None values should become empty strings in CSV
  - Test large datasets: 1000+ rows should complete in < 2 seconds

- **Security Tests:**
  - Test SQL injection in table names: "users; DROP TABLE users--", "users' OR '1'='1", "users'; DELETE FROM users--" should all raise SQLSecurityError
  - Test path traversal: "../../../etc/passwd", "..\\windows\\system32" should be rejected
  - Test malicious column names: columns with SQL keywords or special characters should be handled safely
  - Test CSV formula injection: values starting with =, +, -, @ should be escaped with single quote prefix

- **Integration Tests:**
  - Test GET /api/table/{table_name}/export with real database table
  - Test POST /api/query/export with various result sets
  - Test error responses: 404 for non-existent tables, 400 for invalid table names, 500 for database errors
  - Test concurrent export requests don't interfere with each other
  - Test response headers: Content-Type should be "text/csv; charset=utf-8", Content-Disposition should include proper filename

### Edge Cases

- Empty tables with 0 rows but defined columns
- Tables with exactly 1 row
- Tables with exactly 1 column
- Results with all NULL values
- Column names with spaces, underscores, numbers
- Column names that are SQL reserved words (handled by query, not export)
- Very long text values: 1000+ character strings
- Unicode in column names (if supported by database)
- Unicode in data values: emoji, Asian languages, right-to-left text
- Table names at maximum identifier length (typically 128 characters)
- Malformed POST request body: missing results, missing columns, invalid JSON
- Very large result sets: 10,000+ rows (should stream or paginate)
- Simultaneous exports from multiple users (load testing)
- Network interruptions during download (handled by browser)
- Special characters in table names: underscores, numbers (valid identifiers)
- Mixed data types in single column (SQLite allows this)
- Binary data in BLOB columns (should convert to string representation or skip)

## Acceptance Criteria

1. **Backend API Endpoints:**
   - GET /api/table/{table_name}/export returns valid CSV for any existing table
   - POST /api/query/export returns valid CSV for provided query results
   - Both endpoints return Content-Type: "text/csv; charset=utf-8"
   - Both endpoints return Content-Disposition: attachment with appropriate filename
   - CSV files start with UTF-8 BOM (U+FEFF) for Excel compatibility
   - All CSV values are properly escaped: commas trigger quoting, quotes are doubled, newlines are preserved
   - SQL injection attempts via table names are blocked and return 400 Bad Request
   - Non-existent tables return 404 Not Found
   - Server errors return 500 Internal Server Error with safe error message
   - All export operations are logged with INFO level on success and ERROR level on failure

2. **Frontend UI Integration:**
   - Download button (⬇) appears directly to the left of × button for each table in Available Tables section
   - Download button (⬇) appears directly to the left of Hide button in Query Results section
   - Download buttons use consistent styling matching the application theme
   - Clicking table download button triggers immediate CSV file download with filename {table_name}.csv
   - Clicking results download button triggers immediate CSV file download with filename query_results_{timestamp}.csv
   - Download buttons show loading state (spinner) while export is in progress
   - Download buttons show success state (✓) briefly after successful export
   - Users see error message in UI if export fails
   - Download buttons are disabled during export to prevent duplicate requests

3. **Data Quality and Compatibility:**
   - CSV files open correctly in Microsoft Excel without encoding issues
   - CSV files open correctly in Google Sheets without encoding issues
   - CSV files open correctly in LibreOffice Calc
   - Headers in CSV match column names from database exactly
   - Data rows in CSV match database/query results exactly
   - Unicode characters (emoji, international text) display correctly in all applications
   - NULL values are represented as empty strings (not "null" or "None")
   - No data corruption or loss during export
   - Numeric values remain numeric (not converted to text with quotes unless necessary)
   - Date/time values maintain their format

4. **Testing Coverage:**
   - All unit tests pass including new CSV export tests (expect 20+ new tests)
   - All existing tests continue to pass (zero regressions)
   - SQL injection tests verify export endpoint security
   - E2E test validates complete user workflow from data upload to CSV export
   - Frontend builds successfully with zero TypeScript errors
   - Test coverage for csv_exporter module is > 90%

5. **Performance Requirements:**
   - Table export completes in < 2 seconds for tables with < 1000 rows
   - Query export completes in < 1 second for typical result sets (< 100 rows)
   - No memory leaks during repeated exports (test with 100 consecutive exports)
   - Concurrent exports (10 simultaneous requests) don't block each other
   - CSV generation is memory-efficient (uses streaming or buffering for large datasets)

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/core/test_csv_exporter.py -v` - Run CSV exporter unit tests to validate CSV generation, encoding, escaping, and security
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Run SQL injection tests to ensure export endpoints block malicious table names
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions in existing functionality
- `cd app/client && bun tsc --noEmit` - Run TypeScript compiler to validate no type errors in frontend code
- `cd app/client && bun run build` - Run frontend production build to validate the application builds successfully
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_csv_export.md` to validate the complete CSV export workflow works end-to-end with visual confirmation via screenshots

## Notes

### CSV Format Specification (RFC 4180 Compliance)
- Use UTF-8 encoding for all text content
- Prepend UTF-8 BOM (Byte Order Mark: U+FEFF or '\ufeff') at the start of file for Excel compatibility
- Use comma (,) as the field delimiter
- Use double quote (") as the quote character for fields
- Use CRLF (\r\n) as the line terminator for maximum compatibility with Windows applications
- First row must contain column headers (field names)
- Subsequent rows contain data values
- Fields containing commas, double quotes, or line breaks must be enclosed in double quotes
- Double quotes within fields must be escaped by doubling them ("")
- Leading and trailing whitespace within fields is significant and preserved
- Empty fields are represented as adjacent delimiters (,,) or empty quoted strings ("")

### Python CSV Module Configuration
```python
import csv
import io

# Create StringIO buffer
buffer = io.StringIO()

# Prepend BOM for Excel
buffer.write('\ufeff')

# Create writer with proper settings
writer = csv.DictWriter(
    buffer,
    fieldnames=columns,
    quoting=csv.QUOTE_MINIMAL,  # Quote only when necessary
    lineterminator='\r\n'  # CRLF for Windows compatibility
)

# Write data
writer.writeheader()
writer.writerows(data)
```

### Security Considerations
- **Table Name Validation:** All table names must pass through `validate_identifier()` from `core.sql_security` before use in any SQL query. This prevents SQL injection attacks via table name parameter.
- **Safe Query Execution:** Use `execute_query_safely()` with identifier_params for all table-related queries to ensure proper escaping and parameterization.
- **Filename Sanitization:** Sanitize filenames in Content-Disposition header to prevent path traversal attacks. Remove or escape characters like: ../, ..\, %, NULL bytes.
- **CSV Formula Injection Prevention:** Values starting with =, +, -, @ can be interpreted as formulas in Excel. Prefix such values with a single quote (') to treat them as text.
- **Rate Limiting:** Consider implementing rate limiting on export endpoints for production deployment to prevent abuse (e.g., max 10 exports per minute per IP).
- **File Size Limits:** For very large tables, consider implementing pagination or streaming to prevent memory exhaustion.
- **Error Message Safety:** Don't expose internal database structure or paths in error messages returned to client.

### Excel Compatibility Requirements
- **UTF-8 BOM is Critical:** Without BOM, Excel may misinterpret UTF-8 as Windows-1252 encoding, causing garbled characters for non-ASCII text.
- **CRLF Line Endings:** Excel on Windows expects \r\n line endings. Unix-style \n may cause issues.
- **Test with Real Excel:** Always test CSV files by opening them in Microsoft Excel (not just LibreOffice or Google Sheets) to verify compatibility.
- **Double-Click Opening:** CSV files should open correctly when double-clicked in Windows Explorer, not just when imported via Excel's "Import" wizard.

### Frontend Download Implementation
```typescript
// Create blob from API response
const blob = await api.exportTable(tableName);

// Create temporary object URL
const url = URL.createObjectURL(blob);

// Create temporary anchor element
const a = document.createElement('a');
a.href = url;
a.download = `${tableName}.csv`;  // Suggested filename

// Trigger download
document.body.appendChild(a);
a.click();

// Cleanup
document.body.removeChild(a);
URL.revokeObjectURL(url);  // Important: free memory
```

### Performance Optimization Opportunities
- For large tables (10,000+ rows), consider implementing streaming response using FastAPI StreamingResponse
- Use database cursor.fetchmany() instead of fetchall() for memory efficiency with large result sets
- Add optional pagination parameter to table export endpoint (e.g., ?limit=1000&offset=0)
- Consider implementing server-side caching for frequently exported tables
- Add compression (gzip) for large CSV files before sending to client

### Future Enhancements (Out of Scope for This Feature)
- Custom filename input: Allow users to specify filename before download
- Column selection: Allow users to choose which columns to export
- Multiple format support: Add TSV (tab-separated), JSON, and Excel .xlsx formats
- Filtering and sorting: Export only filtered/sorted data from UI
- Automatic compression: ZIP large CSV files automatically
- Email delivery: Send large exports via email instead of immediate download
- Scheduled exports: Set up recurring exports via cron jobs
- Export history: Track and allow re-download of previous exports
- Export templates: Save common export configurations
- Batch export: Export multiple tables at once as ZIP archive

### Dependencies
- No new Python dependencies required - use built-in `csv` and `io` modules
- No new npm dependencies required - use built-in Fetch API and Blob
- Leverage existing FastAPI Response class for file downloads
- Leverage existing sql_security module for validation and safe execution

### Testing CSV Files Manually
After implementing the feature, manually test the downloaded CSV files:
1. Download a table CSV and open in Microsoft Excel - verify correct display of all characters including Unicode
2. Download query results CSV and open in Google Sheets - verify correct import and formatting
3. Open CSV in a text editor and verify UTF-8 BOM is present (should see EF BB BF bytes in hex view)
4. Test with tables containing special characters: commas, quotes, newlines, tabs
5. Test with international data: Chinese, Arabic, Hebrew, emoji
6. Test with edge cases: empty table, single row, single column
