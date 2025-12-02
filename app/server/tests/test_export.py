"""
Tests for CSV export functionality
"""

import pytest
import sqlite3
import tempfile
import os
from fastapi.testclient import TestClient


# Create a temporary database for testing
@pytest.fixture
def test_db():
    """Create a test database with sample data"""
    db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    db_file.close()

    conn = sqlite3.connect(db_file.name)
    cursor = conn.cursor()

    # Create test table
    cursor.execute('''
        CREATE TABLE test_users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            age INTEGER
        )
    ''')

    # Insert test data
    cursor.execute("INSERT INTO test_users (name, email, age) VALUES (?, ?, ?)",
                   ('Alice', 'alice@example.com', 30))
    cursor.execute("INSERT INTO test_users (name, email, age) VALUES (?, ?, ?)",
                   ('Bob', 'bob@example.com', 25))
    cursor.execute("INSERT INTO test_users (name, email, age) VALUES (?, ?, ?)",
                   ('Charlie', 'charlie@example.com', 35))

    conn.commit()
    conn.close()

    yield db_file.name

    # Cleanup
    os.unlink(db_file.name)


def normalize_csv(content: str) -> list:
    """Normalize CSV content by stripping whitespace and handling CRLF"""
    return [line.strip() for line in content.strip().replace('\r\n', '\n').split('\n')]


class TestTableExport:
    """Test table export endpoint"""

    def test_export_table_success(self, test_db, monkeypatch):
        """Test exporting a valid table"""
        # Store the original sqlite3.connect
        original_connect = sqlite3.connect

        # Create a wrapper that redirects to test db
        def patched_connect(database, *args, **kwargs):
            if database == "db/database.db":
                return original_connect(test_db, *args, **kwargs)
            return original_connect(database, *args, **kwargs)

        monkeypatch.setattr(sqlite3, 'connect', patched_connect)

        from server import app
        client = TestClient(app)

        response = client.get("/api/export/table/test_users")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment; filename=test_users.csv" in response.headers["content-disposition"]

        # Verify CSV content
        lines = normalize_csv(response.text)

        # Check header
        assert lines[0] == "id,name,email,age"

        # Check data rows
        assert len(lines) == 4  # 1 header + 3 data rows
        assert "Alice" in lines[1]
        assert "Bob" in lines[2]
        assert "Charlie" in lines[3]

    def test_export_nonexistent_table(self, test_db, monkeypatch):
        """Test exporting a table that doesn't exist"""
        original_connect = sqlite3.connect

        def patched_connect(database, *args, **kwargs):
            if database == "db/database.db":
                return original_connect(test_db, *args, **kwargs)
            return original_connect(database, *args, **kwargs)

        monkeypatch.setattr(sqlite3, 'connect', patched_connect)

        from server import app
        client = TestClient(app)

        response = client.get("/api/export/table/nonexistent_table")

        assert response.status_code == 404

    def test_export_table_invalid_name(self):
        """Test exporting with an invalid table name (SQL injection attempt)"""
        from server import app
        client = TestClient(app)

        response = client.get("/api/export/table/users'; DROP TABLE users; --")

        assert response.status_code == 400

    def test_export_empty_table(self, test_db, monkeypatch):
        """Test exporting an empty table"""
        # Create an empty table
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE empty_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        conn.commit()
        conn.close()

        original_connect = sqlite3.connect

        def patched_connect(database, *args, **kwargs):
            if database == "db/database.db":
                return original_connect(test_db, *args, **kwargs)
            return original_connect(database, *args, **kwargs)

        monkeypatch.setattr(sqlite3, 'connect', patched_connect)

        from server import app
        client = TestClient(app)

        response = client.get("/api/export/table/empty_table")

        assert response.status_code == 200
        lines = normalize_csv(response.text)

        # Should only have header
        assert len(lines) == 1
        assert lines[0] == "id,name"


class TestQueryResultsExport:
    """Test query results export endpoint"""

    def test_export_query_results_success(self):
        """Test exporting valid query results"""
        from server import app
        client = TestClient(app)

        request_data = {
            "results": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"}
            ],
            "columns": ["id", "name", "email"],
            "filename": "test_results.csv"
        }

        response = client.post("/api/export/query-results", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment; filename=test_results.csv" in response.headers["content-disposition"]

        # Verify CSV content
        lines = normalize_csv(response.text)

        assert lines[0] == "id,name,email"
        assert len(lines) == 3  # 1 header + 2 data rows

    def test_export_query_results_empty(self):
        """Test exporting empty query results"""
        from server import app
        client = TestClient(app)

        request_data = {
            "results": [],
            "columns": ["id", "name", "email"]
        }

        response = client.post("/api/export/query-results", json=request_data)

        assert response.status_code == 200
        lines = normalize_csv(response.text)

        # Should only have header
        assert len(lines) == 1
        assert lines[0] == "id,name,email"

    def test_export_query_results_default_filename(self):
        """Test that default filename is used when not provided"""
        from server import app
        client = TestClient(app)

        request_data = {
            "results": [{"id": 1, "name": "Test"}],
            "columns": ["id", "name"]
        }

        response = client.post("/api/export/query-results", json=request_data)

        assert response.status_code == 200
        assert "attachment; filename=query_results.csv" in response.headers["content-disposition"]

    def test_export_query_results_with_null_values(self):
        """Test exporting query results with null values"""
        from server import app
        client = TestClient(app)

        request_data = {
            "results": [
                {"id": 1, "name": "Alice", "email": None},
                {"id": 2, "name": None, "email": "bob@example.com"}
            ],
            "columns": ["id", "name", "email"]
        }

        response = client.post("/api/export/query-results", json=request_data)

        assert response.status_code == 200
        # CSV should handle null values gracefully

    def test_export_query_results_with_special_characters(self):
        """Test exporting query results with special characters"""
        from server import app
        client = TestClient(app)

        request_data = {
            "results": [
                {"id": 1, "name": "Alice, Jr.", "notes": 'Quote: "Hello"'},
                {"id": 2, "name": "Bob\nSmith", "notes": "Line1\nLine2"}
            ],
            "columns": ["id", "name", "notes"]
        }

        response = client.post("/api/export/query-results", json=request_data)

        assert response.status_code == 200
        # CSV should properly escape special characters


class TestCSVFormatCorrectness:
    """Test CSV format correctness"""

    def test_csv_headers_match_columns(self):
        """Test that CSV headers match the provided columns"""
        from server import app
        client = TestClient(app)

        columns = ["column_a", "column_b", "column_c"]
        request_data = {
            "results": [{"column_a": 1, "column_b": 2, "column_c": 3}],
            "columns": columns
        }

        response = client.post("/api/export/query-results", json=request_data)

        assert response.status_code == 200
        lines = normalize_csv(response.text)

        assert lines[0] == ",".join(columns)

    def test_csv_data_integrity(self):
        """Test that CSV data matches input data exactly"""
        from server import app
        client = TestClient(app)

        request_data = {
            "results": [
                {"id": 1, "value": 100.5},
                {"id": 2, "value": 200.75},
                {"id": 3, "value": 300.25}
            ],
            "columns": ["id", "value"]
        }

        response = client.post("/api/export/query-results", json=request_data)

        assert response.status_code == 200
        lines = normalize_csv(response.text)

        # Check data integrity
        assert "1,100.5" in lines[1]
        assert "2,200.75" in lines[2]
        assert "3,300.25" in lines[3]
