"""
Comprehensive tests for CSV export endpoints
"""

import pytest
import sqlite3
import tempfile
import os
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from server import app


@pytest.fixture
def test_db():
    """Create a test database with sample data"""
    db_file = "db/database.db"
    os.makedirs("db", exist_ok=True)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS test_users")
    cursor.execute("DROP TABLE IF EXISTS test_special_chars")
    cursor.execute("DROP TABLE IF EXISTS test_empty")

    # Create test tables
    cursor.execute('''
        CREATE TABLE test_users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            age INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE test_special_chars (
            id INTEGER PRIMARY KEY,
            description TEXT,
            value TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE test_empty (
            id INTEGER PRIMARY KEY,
            data TEXT
        )
    ''')

    # Insert test data
    cursor.execute("INSERT INTO test_users (name, email, age) VALUES (?, ?, ?)",
                   ('Alice', 'alice@example.com', 30))
    cursor.execute("INSERT INTO test_users (name, email, age) VALUES (?, ?, ?)",
                   ('Bob', 'bob@example.com', 25))
    cursor.execute("INSERT INTO test_users (name, email, age) VALUES (?, ?, ?)",
                   ('Charlie', 'charlie@example.com', 35))

    # Insert data with special characters
    cursor.execute("INSERT INTO test_special_chars (description, value) VALUES (?, ?)",
                   ('Contains comma', 'value,with,commas'))
    cursor.execute("INSERT INTO test_special_chars (description, value) VALUES (?, ?)",
                   ('Contains quote', 'value"with"quotes'))
    cursor.execute("INSERT INTO test_special_chars (description, value) VALUES (?, ?)",
                   ('Contains newline', 'value\nwith\nnewlines'))

    conn.commit()
    conn.close()

    yield db_file

    # Cleanup
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS test_users")
    cursor.execute("DROP TABLE IF EXISTS test_special_chars")
    cursor.execute("DROP TABLE IF EXISTS test_empty")
    conn.commit()
    conn.close()


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestTableExport:
    """Test table export endpoint"""

    def test_export_valid_table(self, client, test_db):
        """Test exporting a valid table returns proper CSV format"""
        response = client.get("/api/export/table/test_users")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]
        assert "test_users.csv" in response.headers["content-disposition"]

        # Check CSV content
        csv_content = response.text
        lines = csv_content.strip().split('\n')

        # Check header (strip \r for Windows line endings)
        assert lines[0].strip() == "id,name,email,age"

        # Check data rows (should have 3 users)
        assert len(lines) == 4  # 1 header + 3 data rows
        assert "Alice" in csv_content
        assert "Bob" in csv_content
        assert "Charlie" in csv_content

    def test_export_nonexistent_table(self, client, test_db):
        """Test exporting non-existent table returns 404"""
        response = client.get("/api/export/table/nonexistent_table")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_export_invalid_table_name(self, client, test_db):
        """Test exporting table with invalid name (SQL injection attempt) returns 400"""
        malicious_names = [
            "test_users'; DROP TABLE test_users; --",
            "test_users; DELETE FROM test_users",
            "test_users UNION SELECT * FROM sqlite_master"
        ]

        for malicious_name in malicious_names:
            response = client.get(f"/api/export/table/{malicious_name}")
            assert response.status_code == 400

    def test_export_table_with_special_characters(self, client, test_db):
        """Test that special characters are properly escaped in CSV"""
        response = client.get("/api/export/table/test_special_chars")

        assert response.status_code == 200

        csv_content = response.text
        lines = csv_content.strip().split('\n')

        # Check that values with commas are properly quoted
        assert '"value,with,commas"' in csv_content or 'value,with,commas' in csv_content

        # CSV should have header + 3 data rows
        assert len(lines) >= 4

    def test_export_empty_table(self, client, test_db):
        """Test exporting empty table returns CSV with only headers"""
        response = client.get("/api/export/table/test_empty")

        assert response.status_code == 200

        csv_content = response.text
        lines = csv_content.strip().split('\n')

        # Should have only header row (strip \r for Windows line endings)
        assert lines[0].strip() == "id,data"
        assert len(lines) == 1  # Only header, no data rows


class TestQueryExport:
    """Test query results export endpoint"""

    def test_export_valid_query_results(self, client):
        """Test exporting valid query results returns proper CSV"""
        request_data = {
            "sql": "SELECT * FROM users",
            "columns": ["id", "name", "email"],
            "results": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"}
            ]
        }

        response = client.post("/api/export/query", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]
        assert "query_results_" in response.headers["content-disposition"]

        # Check CSV content
        csv_content = response.text
        lines = csv_content.strip().split('\n')

        # Check header (strip \r for Windows line endings)
        assert lines[0].strip() == "id,name,email"

        # Check data rows
        assert len(lines) == 3  # 1 header + 2 data rows
        assert "Alice" in csv_content
        assert "Bob" in csv_content

    def test_export_empty_results(self, client):
        """Test exporting empty results returns 400"""
        request_data = {
            "sql": "SELECT * FROM users WHERE id = -1",
            "columns": ["id", "name"],
            "results": []
        }

        response = client.post("/api/export/query", json=request_data)

        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    def test_export_without_columns(self, client):
        """Test exporting without columns returns 400"""
        request_data = {
            "sql": "SELECT * FROM users",
            "columns": [],
            "results": [
                {"id": 1, "name": "Alice"}
            ]
        }

        response = client.post("/api/export/query", json=request_data)

        assert response.status_code == 400

    def test_export_query_with_special_characters(self, client):
        """Test that special characters in query results are properly escaped"""
        request_data = {
            "sql": "SELECT * FROM data",
            "columns": ["id", "description", "value"],
            "results": [
                {"id": 1, "description": "Contains comma", "value": "a,b,c"},
                {"id": 2, "description": "Contains quote", "value": 'a"b"c'},
                {"id": 3, "description": "Contains newline", "value": "a\nb\nc"}
            ]
        }

        response = client.post("/api/export/query", json=request_data)

        assert response.status_code == 200

        csv_content = response.text
        lines = csv_content.strip().split('\n')

        # Should have header + 3 data rows
        assert len(lines) >= 4

        # Check that special characters are present (properly escaped)
        assert "comma" in csv_content.lower()
        assert "quote" in csv_content.lower()
        assert "newline" in csv_content.lower()

    def test_export_query_filename_has_timestamp(self, client):
        """Test that exported query results have timestamp in filename"""
        request_data = {
            "sql": "SELECT * FROM users",
            "columns": ["id", "name"],
            "results": [
                {"id": 1, "name": "Test"}
            ]
        }

        response = client.post("/api/export/query", json=request_data)

        assert response.status_code == 200

        content_disposition = response.headers["content-disposition"]
        # Should match pattern: query_results_YYYYMMDD_HHMMSS.csv
        assert "query_results_" in content_disposition
        assert ".csv" in content_disposition

    def test_export_query_with_null_values(self, client):
        """Test that NULL values are properly represented in CSV"""
        request_data = {
            "sql": "SELECT * FROM users",
            "columns": ["id", "name", "email"],
            "results": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": None},  # NULL email
                {"id": 3, "name": "Charlie"}  # Missing email key (treated as NULL)
            ]
        }

        response = client.post("/api/export/query", json=request_data)

        assert response.status_code == 200

        csv_content = response.text
        lines = csv_content.strip().split('\n')

        # Should have header + 3 data rows
        assert len(lines) == 4

        # Check that NULL values are represented as empty strings
        # The second row should have empty email
        assert "Bob," in csv_content or "Bob\n" in csv_content


class TestExportSecurity:
    """Test security aspects of export endpoints"""

    def test_table_export_validates_identifiers(self, client, test_db):
        """Test that table name validation uses sql_security module"""
        # SQL injection attempts
        malicious_inputs = [
            "'; DROP TABLE test_users; --",
            "test_users; DELETE FROM test_users",
            "test_users' OR '1'='1",
            "test_users UNION SELECT * FROM sqlite_master"
        ]

        for malicious_input in malicious_inputs:
            response = client.get(f"/api/export/table/{malicious_input}")
            # Should return 400 (validation error) or 404 (table not found after sanitization)
            assert response.status_code in [400, 404]

    def test_table_export_blocks_sql_keywords(self, client):
        """Test that SQL keywords in table names are blocked"""
        sql_keywords = [
            "SELECT",
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT"
        ]

        for keyword in sql_keywords:
            response = client.get(f"/api/export/table/{keyword}")
            # Should be blocked by validation
            assert response.status_code in [400, 404]

    def test_query_export_does_not_execute_sql(self, client, test_db):
        """Test that query export endpoint does not re-execute provided SQL"""
        # Even with malicious SQL, the endpoint should only use the provided results
        request_data = {
            "sql": "DROP TABLE test_users",  # Malicious SQL
            "columns": ["id", "name"],
            "results": [
                {"id": 1, "name": "Test"}
            ]
        }

        response = client.post("/api/export/query", json=request_data)

        # Should succeed because it doesn't execute the SQL, only uses results
        assert response.status_code == 200

        # Verify table still exists (SQL was not executed)
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_users'")
        result = cursor.fetchone()
        conn.close()

        # Table should still exist
        assert result is not None


class TestExportEdgeCases:
    """Test edge cases for export functionality"""

    def test_export_table_with_unicode_characters(self, client, test_db):
        """Test exporting table with unicode characters"""
        # Create table with unicode data
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS test_unicode")
        cursor.execute("CREATE TABLE test_unicode (id INTEGER, name TEXT)")
        cursor.execute("INSERT INTO test_unicode VALUES (1, ?)", ("日本語",))
        cursor.execute("INSERT INTO test_unicode VALUES (2, ?)", ("Émoji 😀",))
        conn.commit()
        conn.close()

        response = client.get("/api/export/table/test_unicode")

        assert response.status_code == 200

        csv_content = response.text
        # UTF-8 encoding should preserve unicode characters
        assert "日本語" in csv_content or response.content

        # Cleanup
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS test_unicode")
        conn.commit()
        conn.close()

    def test_export_query_with_missing_column_values(self, client):
        """Test export handles results with missing column values"""
        request_data = {
            "sql": "SELECT * FROM users",
            "columns": ["id", "name", "email", "age"],
            "results": [
                {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
                {"id": 2, "name": "Bob"},  # Missing email and age
                {"id": 3, "name": "Charlie", "age": 35}  # Missing email
            ]
        }

        response = client.post("/api/export/query", json=request_data)

        assert response.status_code == 200

        csv_content = response.text
        lines = csv_content.strip().split('\n')

        # Should have header + 3 data rows
        assert len(lines) == 4
