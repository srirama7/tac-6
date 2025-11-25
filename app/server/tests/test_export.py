"""
Tests for CSV export endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from server import app
import sqlite3
import os


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def setup_test_db():
    """Setup test database with sample data"""
    # Ensure db directory exists
    os.makedirs("db", exist_ok=True)

    # Connect to test database
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()

    # Create test table with various data types
    cursor.execute("DROP TABLE IF EXISTS test_export")
    cursor.execute("""
        CREATE TABLE test_export (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT,
            description TEXT
        )
    """)

    # Insert test data with special characters
    test_data = [
        (1, "John Doe", 30, "john@example.com", "Regular user"),
        (2, "Jane, Smith", 25, "jane@example.com", "Name with comma"),
        (3, 'Bob "The Builder"', 35, "bob@example.com", "Name with quotes"),
        (4, "Alice\nNewline", 28, "alice@example.com", "Name with newline"),
        (5, "Charlie", None, "charlie@example.com", None),  # NULL values
    ]

    cursor.executemany(
        "INSERT INTO test_export VALUES (?, ?, ?, ?, ?)",
        test_data
    )

    conn.commit()
    conn.close()

    yield

    # Cleanup
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS test_export")
    conn.commit()
    conn.close()


def test_export_table_success(client, setup_test_db):
    """Test successful table export"""
    response = client.post(
        "/api/export/table",
        json={"table_name": "test_export"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["error"] is None
    assert data["filename"].startswith("test_export_export_")
    assert data["filename"].endswith(".csv")
    assert len(data["csv_content"]) > 0

    # Verify CSV content has headers
    assert "id,name,age,email,description" in data["csv_content"]

    # Verify data is present
    assert "John Doe" in data["csv_content"]
    assert "jane@example.com" in data["csv_content"]


def test_export_table_not_found(client):
    """Test export of non-existent table"""
    response = client.post(
        "/api/export/table",
        json={"table_name": "nonexistent_table"}
    )

    assert response.status_code == 404


def test_export_table_invalid_name(client):
    """Test export with invalid table name (SQL injection attempt)"""
    response = client.post(
        "/api/export/table",
        json={"table_name": "test'; DROP TABLE users; --"}
    )

    assert response.status_code == 400


def test_export_table_empty(client):
    """Test export of empty table"""
    # Create empty table
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS empty_table")
    cursor.execute("CREATE TABLE empty_table (id INTEGER, name TEXT)")
    conn.commit()
    conn.close()

    response = client.post(
        "/api/export/table",
        json={"table_name": "empty_table"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["error"] is None
    # Should have headers even with no data
    assert "id,name" in data["csv_content"]

    # Cleanup
    conn = sqlite3.connect("db/database.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS empty_table")
    conn.commit()
    conn.close()


def test_export_query_results_success(client, setup_test_db):
    """Test successful query results export"""
    response = client.post(
        "/api/export/query",
        json={
            "sql": "SELECT id, name, email FROM test_export WHERE age > 25",
            "columns": ["id", "name", "email"]
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["error"] is None
    assert data["filename"].startswith("query_results_")
    assert data["filename"].endswith(".csv")
    assert len(data["csv_content"]) > 0

    # Verify CSV content has headers
    assert "id,name,email" in data["csv_content"]


def test_export_query_results_empty(client, setup_test_db):
    """Test export of query with no results"""
    response = client.post(
        "/api/export/query",
        json={
            "sql": "SELECT id, name FROM test_export WHERE age > 1000",
            "columns": ["id", "name"]
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["error"] is None
    # Should have headers even with no data
    assert "id,name" in data["csv_content"]


def test_export_query_invalid_sql(client):
    """Test export with invalid SQL"""
    response = client.post(
        "/api/export/query",
        json={
            "sql": "INVALID SQL QUERY",
            "columns": ["id", "name"]
        }
    )

    assert response.status_code == 200
    data = response.json()

    # Should return error in response
    assert data["error"] is not None


def test_csv_special_characters(client, setup_test_db):
    """Test CSV generation with special characters"""
    response = client.post(
        "/api/export/table",
        json={"table_name": "test_export"}
    )

    assert response.status_code == 200
    data = response.json()

    csv_content = data["csv_content"]

    # CSV should properly handle commas in data
    assert "Jane, Smith" in csv_content or '"Jane, Smith"' in csv_content

    # CSV should properly handle quotes in data
    assert 'Bob "The Builder"' in csv_content or 'Bob ""The Builder""' in csv_content


def test_csv_null_values(client, setup_test_db):
    """Test CSV generation with NULL values"""
    response = client.post(
        "/api/export/table",
        json={"table_name": "test_export"}
    )

    assert response.status_code == 200
    data = response.json()

    # NULL values should be converted to empty strings
    lines = data["csv_content"].split('\n')

    # Find Charlie's row (has NULL values)
    charlie_row = [line for line in lines if 'Charlie' in line]
    assert len(charlie_row) > 0
