"""Tests for CSV export functionality."""
import pytest
from fastapi.testclient import TestClient
import sys
import os
import sqlite3
import csv
import io

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app
from core.csv_generator import generate_csv_from_results


client = TestClient(app)


class TestCSVGenerator:
    """Test CSV generation helper function."""

    def test_empty_results(self):
        """Test CSV generation with empty results."""
        columns = ["id", "name", "email"]
        results = []
        csv_content = generate_csv_from_results(results, columns)

        # Parse CSV to verify structure
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        assert len(rows) == 0
        assert csv_reader.fieldnames == columns

    def test_single_row(self):
        """Test CSV generation with single row."""
        columns = ["id", "name", "email"]
        results = [{"id": 1, "name": "John", "email": "john@example.com"}]
        csv_content = generate_csv_from_results(results, columns)

        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        assert len(rows) == 1
        assert rows[0]["id"] == "1"
        assert rows[0]["name"] == "John"
        assert rows[0]["email"] == "john@example.com"

    def test_multiple_rows(self):
        """Test CSV generation with multiple rows."""
        columns = ["id", "name", "age"]
        results = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
            {"id": 3, "name": "Charlie", "age": 35}
        ]
        csv_content = generate_csv_from_results(results, columns)

        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        assert len(rows) == 3
        assert rows[0]["name"] == "Alice"
        assert rows[1]["name"] == "Bob"
        assert rows[2]["name"] == "Charlie"

    def test_special_characters(self):
        """Test CSV generation with special characters (quotes, commas, newlines)."""
        columns = ["id", "description"]
        results = [
            {"id": 1, "description": 'Contains "quotes" here'},
            {"id": 2, "description": "Contains, comma, here"},
            {"id": 3, "description": "Contains\nnewline\nhere"}
        ]
        csv_content = generate_csv_from_results(results, columns)

        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        assert len(rows) == 3
        assert rows[0]["description"] == 'Contains "quotes" here'
        assert rows[1]["description"] == "Contains, comma, here"
        assert rows[2]["description"] == "Contains\nnewline\nhere"

    def test_null_values(self):
        """Test CSV generation with None/null values."""
        columns = ["id", "name", "optional_field"]
        results = [
            {"id": 1, "name": "Alice", "optional_field": None},
            {"id": 2, "name": "Bob", "optional_field": "value"},
            {"id": 3, "name": None, "optional_field": None}
        ]
        csv_content = generate_csv_from_results(results, columns)

        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        assert len(rows) == 3
        assert rows[0]["optional_field"] == ""
        assert rows[1]["optional_field"] == "value"
        assert rows[2]["name"] == ""

    def test_various_data_types(self):
        """Test CSV generation with various data types."""
        columns = ["id", "name", "age", "score", "active"]
        results = [
            {"id": 1, "name": "Alice", "age": 30, "score": 95.5, "active": True},
            {"id": 2, "name": "Bob", "age": 25, "score": 87.3, "active": False}
        ]
        csv_content = generate_csv_from_results(results, columns)

        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        assert len(rows) == 2
        assert rows[0]["score"] == "95.5"
        assert rows[1]["active"] == "False"


class TestTableExportEndpoint:
    """Test table export endpoint."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self):
        """Setup test database with sample data."""
        # Create test database
        os.makedirs("db", exist_ok=True)
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()

        # Create test table
        cursor.execute("DROP TABLE IF EXISTS test_users")
        cursor.execute("""
            CREATE TABLE test_users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                age INTEGER
            )
        """)

        # Insert test data
        cursor.executemany(
            "INSERT INTO test_users (id, name, email, age) VALUES (?, ?, ?, ?)",
            [
                (1, "Alice", "alice@example.com", 30),
                (2, "Bob", "bob@example.com", 25),
                (3, "Charlie", "charlie@example.com", 35)
            ]
        )

        conn.commit()
        conn.close()

        yield

        # Cleanup
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS test_users")
        conn.commit()
        conn.close()

    def test_export_valid_table(self):
        """Test exporting a valid table."""
        response = client.get("/api/export/table/test_users")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]
        assert "test_users.csv" in response.headers["content-disposition"]

        # Parse CSV content
        csv_content = response.text
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        assert len(rows) == 3
        assert rows[0]["name"] == "Alice"
        assert rows[1]["name"] == "Bob"
        assert rows[2]["name"] == "Charlie"

    def test_export_nonexistent_table(self):
        """Test exporting a non-existent table."""
        response = client.get("/api/export/table/nonexistent_table")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_export_invalid_table_name(self):
        """Test exporting with invalid table name (SQL injection attempt)."""
        response = client.get("/api/export/table/users; DROP TABLE users;")

        assert response.status_code == 400

    def test_export_empty_table(self):
        """Test exporting an empty table."""
        # Create empty table
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS empty_table")
        cursor.execute("CREATE TABLE empty_table (id INTEGER, name TEXT)")
        conn.commit()
        conn.close()

        response = client.get("/api/export/table/empty_table")

        assert response.status_code == 200

        # Parse CSV content - should have headers but no data rows
        csv_content = response.text
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        assert len(rows) == 0
        assert "id" in csv_reader.fieldnames
        assert "name" in csv_reader.fieldnames

        # Cleanup
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS empty_table")
        conn.commit()
        conn.close()


class TestQueryExportEndpoint:
    """Test query export endpoint."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self):
        """Setup test database with sample data."""
        # Create test database
        os.makedirs("db", exist_ok=True)
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()

        # Create test table
        cursor.execute("DROP TABLE IF EXISTS test_products")
        cursor.execute("""
            CREATE TABLE test_products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                stock INTEGER
            )
        """)

        # Insert test data
        cursor.executemany(
            "INSERT INTO test_products (id, name, price, stock) VALUES (?, ?, ?, ?)",
            [
                (1, "Widget", 19.99, 100),
                (2, "Gadget", 29.99, 50),
                (3, "Doohickey", 9.99, 200)
            ]
        )

        conn.commit()
        conn.close()

        yield

        # Cleanup
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS test_products")
        conn.commit()
        conn.close()

    def test_export_valid_query(self):
        """Test exporting valid query results."""
        response = client.post(
            "/api/export/query",
            json={"query": "Show all products", "llm_provider": "openai"}
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]
        assert "query_results.csv" in response.headers["content-disposition"]

        # Parse CSV content
        csv_content = response.text
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        # Should have results
        assert len(rows) > 0

    def test_export_query_with_no_results(self):
        """Test exporting query with no results."""
        response = client.post(
            "/api/export/query",
            json={"query": "Show products where price > 1000", "llm_provider": "openai"}
        )

        assert response.status_code == 200

        # Parse CSV content - should have headers but possibly no data rows
        csv_content = response.text
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)

        # Empty results are valid
        assert len(rows) >= 0

    def test_export_invalid_query(self):
        """Test exporting with invalid query."""
        response = client.post(
            "/api/export/query",
            json={"query": "INVALID SQL SYNTAX HERE", "llm_provider": "openai"}
        )

        # Should return error
        assert response.status_code == 500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
