"""
Unit tests for CSV export functionality.
"""

import csv
import io
import sqlite3
import pytest

from app.server.core.csv_exporter import (
    export_table_to_csv,
    export_query_results_to_csv,
    CSVExportError,
)
from app.server.core.sql_security import SQLSecurityError


@pytest.fixture
def db_connection():
    """Create an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()


@pytest.fixture
def sample_table(db_connection):
    """Create a sample table with various data types."""
    cursor = db_connection.cursor()
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            salary REAL,
            active INTEGER
        )
        """
    )
    cursor.execute(
        """
        INSERT INTO users (id, name, age, salary, active)
        VALUES
            (1, 'Alice', 30, 75000.50, 1),
            (2, 'Bob', 25, 60000.00, 1),
            (3, 'Charlie', 35, 85000.75, 0)
        """
    )
    db_connection.commit()
    return db_connection


@pytest.fixture
def special_chars_table(db_connection):
    """Create a table with special characters that need CSV escaping."""
    cursor = db_connection.cursor()
    cursor.execute(
        """
        CREATE TABLE special_data (
            id INTEGER PRIMARY KEY,
            text TEXT
        )
        """
    )
    # Insert data with various special characters
    test_data = [
        (1, 'Normal text'),
        (2, 'Text with, comma'),
        (3, 'Text with "quotes"'),
        (4, 'Text with\nnewline'),
        (5, 'Text with\ttab'),
        (6, 'Text with, comma and "quotes"'),
        (7, 'Multi\nline\ntext'),
        (8, ''),  # Empty string
    ]
    cursor.executemany("INSERT INTO special_data VALUES (?, ?)", test_data)
    db_connection.commit()
    return db_connection


@pytest.fixture
def unicode_table(db_connection):
    """Create a table with Unicode characters."""
    cursor = db_connection.cursor()
    cursor.execute(
        """
        CREATE TABLE unicode_data (
            id INTEGER PRIMARY KEY,
            text TEXT
        )
        """
    )
    test_data = [
        (1, 'Hello 世界'),
        (2, 'Café ☕'),
        (3, 'Emoji 😀🎉'),
        (4, 'Accents: àéîöü'),
    ]
    cursor.executemany("INSERT INTO unicode_data VALUES (?, ?)", test_data)
    db_connection.commit()
    return db_connection


@pytest.fixture
def empty_table(db_connection):
    """Create an empty table."""
    cursor = db_connection.cursor()
    cursor.execute(
        """
        CREATE TABLE empty_table (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        """
    )
    db_connection.commit()
    return db_connection


@pytest.fixture
def null_table(db_connection):
    """Create a table with NULL values."""
    cursor = db_connection.cursor()
    cursor.execute(
        """
        CREATE TABLE null_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            value INTEGER
        )
        """
    )
    cursor.execute(
        """
        INSERT INTO null_data (id, name, value)
        VALUES
            (1, 'Alice', 100),
            (2, NULL, 200),
            (3, 'Charlie', NULL),
            (4, NULL, NULL)
        """
    )
    db_connection.commit()
    return db_connection


class TestExportTableToCSV:
    """Tests for export_table_to_csv function."""

    def test_export_basic_table(self, sample_table):
        """Test exporting a basic table with various data types."""
        csv_output = export_table_to_csv(sample_table, "users")

        # Remove BOM and split into lines
        lines = csv_output.lstrip("\ufeff").strip().split("\r\n")

        # Check header
        assert lines[0] == "id,name,age,salary,active"

        # Check data rows
        assert lines[1] == "1,Alice,30,75000.5,1"
        assert lines[2] == "2,Bob,25,60000.0,1"
        assert lines[3] == "3,Charlie,35,85000.75,0"

    def test_export_nonexistent_table(self, db_connection):
        """Test exporting a table that doesn't exist."""
        with pytest.raises(CSVExportError) as exc_info:
            export_table_to_csv(db_connection, "nonexistent_table")
        assert "does not exist" in str(exc_info.value)

    def test_export_invalid_table_name(self, db_connection):
        """Test exporting with an invalid table name."""
        with pytest.raises(SQLSecurityError):
            export_table_to_csv(db_connection, "users'; DROP TABLE users; --")

    def test_export_empty_table(self, empty_table):
        """Test exporting an empty table (should have headers only)."""
        csv_output = export_table_to_csv(empty_table, "empty_table")

        # Remove BOM and split into lines
        lines = csv_output.lstrip("\ufeff").strip().split("\r\n")

        # Should only have header row
        assert lines[0] == "id,name"
        assert len(lines) == 1

    def test_export_table_with_special_chars(self, special_chars_table):
        """Test exporting table with special characters requiring escaping."""
        csv_output = export_table_to_csv(special_chars_table, "special_data")

        # Parse CSV to verify proper escaping
        csv_reader = csv.DictReader(io.StringIO(csv_output.lstrip("\ufeff")))
        rows = list(csv_reader)

        # Verify special characters are preserved correctly
        assert rows[0]["text"] == "Normal text"
        assert rows[1]["text"] == "Text with, comma"
        assert rows[2]["text"] == 'Text with "quotes"'
        assert rows[3]["text"] == "Text with\nnewline"
        assert rows[4]["text"] == "Text with\ttab"
        assert rows[5]["text"] == 'Text with, comma and "quotes"'
        assert rows[6]["text"] == "Multi\nline\ntext"
        assert rows[7]["text"] == ""

    def test_export_table_with_unicode(self, unicode_table):
        """Test exporting table with Unicode characters."""
        csv_output = export_table_to_csv(unicode_table, "unicode_data")

        # Parse CSV to verify Unicode is preserved
        csv_reader = csv.DictReader(io.StringIO(csv_output.lstrip("\ufeff")))
        rows = list(csv_reader)

        assert rows[0]["text"] == "Hello 世界"
        assert rows[1]["text"] == "Café ☕"
        assert rows[2]["text"] == "Emoji 😀🎉"
        assert rows[3]["text"] == "Accents: àéîöü"

    def test_export_table_with_nulls(self, null_table):
        """Test exporting table with NULL values."""
        csv_output = export_table_to_csv(null_table, "null_data")

        # Parse CSV to verify NULLs are converted to empty strings
        csv_reader = csv.DictReader(io.StringIO(csv_output.lstrip("\ufeff")))
        rows = list(csv_reader)

        assert rows[0]["name"] == "Alice"
        assert rows[0]["value"] == "100"
        assert rows[1]["name"] == ""  # NULL converted to empty string
        assert rows[1]["value"] == "200"
        assert rows[2]["name"] == "Charlie"
        assert rows[2]["value"] == ""  # NULL converted to empty string
        assert rows[3]["name"] == ""  # NULL converted to empty string
        assert rows[3]["value"] == ""  # NULL converted to empty string

    def test_csv_has_utf8_bom(self, sample_table):
        """Test that CSV output includes UTF-8 BOM for Excel compatibility."""
        csv_output = export_table_to_csv(sample_table, "users")

        # Check for UTF-8 BOM at the start
        assert csv_output.startswith("\ufeff")

    def test_csv_uses_crlf_line_endings(self, sample_table):
        """Test that CSV uses CRLF line endings for compatibility."""
        csv_output = export_table_to_csv(sample_table, "users")

        # Remove BOM for easier checking
        csv_content = csv_output.lstrip("\ufeff")

        # Check that lines are separated by CRLF
        assert "\r\n" in csv_content
        # Verify no lone LF
        lines = csv_content.split("\r\n")
        for line in lines[:-1]:  # Exclude last line which may be empty
            assert "\n" not in line or line.count("\n") == line.count("\r\n")


class TestExportQueryResultsToCSV:
    """Tests for export_query_results_to_csv function."""

    def test_export_basic_results(self):
        """Test exporting basic query results."""
        results = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
        ]
        columns = ["id", "name", "age"]

        csv_output = export_query_results_to_csv(results, columns)

        # Remove BOM and split into lines
        lines = csv_output.lstrip("\ufeff").strip().split("\r\n")

        assert lines[0] == "id,name,age"
        assert lines[1] == "1,Alice,30"
        assert lines[2] == "2,Bob,25"

    def test_export_empty_results(self):
        """Test exporting empty results (headers only)."""
        results = []
        columns = ["id", "name", "age"]

        csv_output = export_query_results_to_csv(results, columns)

        # Remove BOM and split into lines
        lines = csv_output.lstrip("\ufeff").strip().split("\r\n")

        # Should only have header
        assert lines[0] == "id,name,age"
        assert len(lines) == 1

    def test_export_results_with_none_values(self):
        """Test exporting results with None values."""
        results = [
            {"id": 1, "name": "Alice", "value": 100},
            {"id": 2, "name": None, "value": 200},
            {"id": 3, "name": "Charlie", "value": None},
        ]
        columns = ["id", "name", "value"]

        csv_output = export_query_results_to_csv(results, columns)

        # Parse CSV to verify None values are converted to empty strings
        csv_reader = csv.DictReader(io.StringIO(csv_output.lstrip("\ufeff")))
        rows = list(csv_reader)

        assert rows[0]["name"] == "Alice"
        assert rows[1]["name"] == ""  # None converted to empty string
        assert rows[2]["value"] == ""  # None converted to empty string

    def test_export_results_with_special_chars(self):
        """Test exporting results with special characters."""
        results = [
            {"id": 1, "text": "Text with, comma"},
            {"id": 2, "text": 'Text with "quotes"'},
            {"id": 3, "text": "Text with\nnewline"},
        ]
        columns = ["id", "text"]

        csv_output = export_query_results_to_csv(results, columns)

        # Parse CSV to verify special characters are preserved
        csv_reader = csv.DictReader(io.StringIO(csv_output.lstrip("\ufeff")))
        rows = list(csv_reader)

        assert rows[0]["text"] == "Text with, comma"
        assert rows[1]["text"] == 'Text with "quotes"'
        assert rows[2]["text"] == "Text with\nnewline"

    def test_export_results_with_unicode(self):
        """Test exporting results with Unicode characters."""
        results = [
            {"id": 1, "text": "Hello 世界"},
            {"id": 2, "text": "Café ☕"},
            {"id": 3, "text": "Emoji 😀🎉"},
        ]
        columns = ["id", "text"]

        csv_output = export_query_results_to_csv(results, columns)

        # Parse CSV to verify Unicode is preserved
        csv_reader = csv.DictReader(io.StringIO(csv_output.lstrip("\ufeff")))
        rows = list(csv_reader)

        assert rows[0]["text"] == "Hello 世界"
        assert rows[1]["text"] == "Café ☕"
        assert rows[2]["text"] == "Emoji 😀🎉"

    def test_export_single_row(self):
        """Test exporting a single row."""
        results = [{"id": 1, "name": "Alice"}]
        columns = ["id", "name"]

        csv_output = export_query_results_to_csv(results, columns)

        lines = csv_output.lstrip("\ufeff").strip().split("\r\n")

        assert lines[0] == "id,name"
        assert lines[1] == "1,Alice"
        assert len(lines) == 2

    def test_export_single_column(self):
        """Test exporting results with a single column."""
        results = [{"id": 1}, {"id": 2}, {"id": 3}]
        columns = ["id"]

        csv_output = export_query_results_to_csv(results, columns)

        lines = csv_output.lstrip("\ufeff").strip().split("\r\n")

        assert lines[0] == "id"
        assert lines[1] == "1"
        assert lines[2] == "2"
        assert lines[3] == "3"

    def test_large_dataset(self):
        """Test exporting a large dataset (performance test)."""
        # Create 1000 rows of data
        results = [
            {"id": i, "name": f"User_{i}", "value": i * 1.5} for i in range(1000)
        ]
        columns = ["id", "name", "value"]

        csv_output = export_query_results_to_csv(results, columns)

        # Verify it completed and has correct number of lines
        lines = csv_output.lstrip("\ufeff").strip().split("\r\n")
        assert len(lines) == 1001  # Header + 1000 data rows

        # Spot check first and last rows
        assert lines[0] == "id,name,value"
        assert lines[1] == "0,User_0,0.0"
        assert lines[1000] == "999,User_999,1498.5"
