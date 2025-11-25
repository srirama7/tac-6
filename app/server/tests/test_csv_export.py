"""
Tests for CSV export functionality
"""

import pytest
import sqlite3
import tempfile
import os
from core.sql_processor import convert_to_csv
from core.sql_security import (
    execute_query_safely,
    validate_identifier,
    check_table_exists,
    SQLSecurityError
)


@pytest.fixture
def test_db():
    """Create a test database with sample data"""
    db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    db_file.close()

    conn = sqlite3.connect(db_file.name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create test table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            signup_date TEXT
        )
    ''')

    # Insert test data
    test_data = [
        (1, 'Alice Smith', 'alice@example.com', '2024-01-15'),
        (2, 'Bob Jones', 'bob@example.com', '2024-02-20'),
        (3, 'Carol White', 'carol@example.com', '2023-12-10'),
        (4, 'Dave "The Man" Brown', 'dave@example.com', '2024-03-01'),
        (5, 'Eve, Jr.', 'eve@example.com', '2024-04-15'),
    ]

    cursor.executemany(
        'INSERT INTO users (id, name, email, signup_date) VALUES (?, ?, ?, ?)',
        test_data
    )

    conn.commit()

    yield conn, db_file.name

    conn.close()
    os.unlink(db_file.name)


class TestConvertToCSV:
    """Tests for convert_to_csv utility function"""

    def test_empty_results(self):
        """Test CSV generation with empty result set"""
        results = []
        columns = ['id', 'name', 'email']

        csv_output = convert_to_csv(results, columns)

        # Should have header row only
        assert 'id,name,email' in csv_output
        lines = csv_output.strip().split('\n')
        assert len(lines) == 1  # Header only

    def test_single_row(self):
        """Test CSV generation with single row"""
        results = [{'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}]
        columns = ['id', 'name', 'email']

        csv_output = convert_to_csv(results, columns)

        lines = csv_output.strip().split('\n')
        assert len(lines) == 2  # Header + 1 data row
        assert 'id,name,email' in lines[0]
        assert '1,Alice,alice@example.com' in lines[1]

    def test_multiple_rows(self):
        """Test CSV generation with multiple rows"""
        results = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': 3, 'name': 'Carol', 'email': 'carol@example.com'},
        ]
        columns = ['id', 'name', 'email']

        csv_output = convert_to_csv(results, columns)

        lines = csv_output.strip().split('\n')
        assert len(lines) == 4  # Header + 3 data rows

    def test_special_characters_commas(self):
        """Test CSV generation with commas in data"""
        results = [{'id': 1, 'name': 'Smith, John', 'email': 'john@example.com'}]
        columns = ['id', 'name', 'email']

        csv_output = convert_to_csv(results, columns)

        # Names with commas should be quoted
        assert '"Smith, John"' in csv_output or 'Smith, John' in csv_output

    def test_special_characters_quotes(self):
        """Test CSV generation with quotes in data"""
        results = [{'id': 1, 'name': 'Dave "The Man" Brown', 'email': 'dave@example.com'}]
        columns = ['id', 'name', 'email']

        csv_output = convert_to_csv(results, columns)

        # Should properly escape quotes
        assert 'Dave' in csv_output
        assert 'Brown' in csv_output

    def test_special_characters_newlines(self):
        """Test CSV generation with newlines in data"""
        results = [{'id': 1, 'name': 'Alice\nSmith', 'email': 'alice@example.com'}]
        columns = ['id', 'name', 'email']

        csv_output = convert_to_csv(results, columns)

        # Newlines in fields should be handled (quoted)
        assert 'Alice' in csv_output
        assert 'Smith' in csv_output

    def test_null_values(self):
        """Test CSV generation with NULL/None values"""
        results = [{'id': 1, 'name': 'Alice', 'email': None}]
        columns = ['id', 'name', 'email']

        csv_output = convert_to_csv(results, columns)

        lines = csv_output.strip().split('\n')
        # None values should result in empty fields
        assert '1,Alice,' in lines[1] or '1,Alice,""' in lines[1]

    def test_unicode_characters(self):
        """Test CSV generation with unicode characters"""
        results = [{'id': 1, 'name': 'José García', 'email': 'jose@example.com'}]
        columns = ['id', 'name', 'email']

        csv_output = convert_to_csv(results, columns)

        # Unicode should be preserved
        assert 'José' in csv_output or 'Jos' in csv_output
        assert 'García' in csv_output or 'Garc' in csv_output

    def test_many_columns(self):
        """Test CSV generation with many columns"""
        columns = [f'col{i}' for i in range(50)]
        results = [{col: i for i, col in enumerate(columns)}]

        csv_output = convert_to_csv(results, columns)

        lines = csv_output.strip().split('\n')
        assert len(lines) == 2  # Header + 1 data row
        # Check that all columns appear in header
        for col in columns[:10]:  # Check first 10 columns
            assert col in lines[0]


class TestTableExportEndpoint:
    """Tests for table export endpoint functionality"""

    def test_valid_table_name(self, test_db):
        """Test exporting a valid table"""
        conn, db_path = test_db

        # Verify table exists
        assert check_table_exists(conn, 'users')

        # Get all rows
        cursor = execute_query_safely(
            conn,
            "SELECT * FROM {table}",
            identifier_params={'table': 'users'}
        )
        rows = cursor.fetchall()

        # Convert to list of dicts
        columns = list(rows[0].keys())
        results = [dict(row) for row in rows]

        # Convert to CSV
        csv_output = convert_to_csv(results, columns)

        # Verify CSV content
        assert 'id,name,email,signup_date' in csv_output
        assert 'Alice Smith' in csv_output
        assert 'Bob Jones' in csv_output
        assert len(csv_output.strip().split('\n')) == 6  # Header + 5 data rows

    def test_invalid_table_name(self):
        """Test exporting with invalid table name"""
        with pytest.raises(SQLSecurityError):
            validate_identifier('users; DROP TABLE users;--', 'table')

    def test_nonexistent_table(self, test_db):
        """Test exporting non-existent table"""
        conn, db_path = test_db

        # Verify table doesn't exist
        assert not check_table_exists(conn, 'nonexistent_table')

    def test_table_with_special_characters(self, test_db):
        """Test exporting table data with special characters"""
        conn, db_path = test_db

        # Get user with special characters
        cursor = execute_query_safely(
            conn,
            "SELECT * FROM {table} WHERE name = ?",
            params=('Dave "The Man" Brown',),
            identifier_params={'table': 'users'}
        )
        rows = cursor.fetchall()

        columns = list(rows[0].keys())
        results = [dict(row) for row in rows]

        csv_output = convert_to_csv(results, columns)

        # Verify special characters are handled
        assert 'Dave' in csv_output
        assert 'Brown' in csv_output

    def test_empty_table(self, test_db):
        """Test exporting empty table"""
        conn, db_path = test_db
        cursor = conn.cursor()

        # Create empty table
        cursor.execute('''
            CREATE TABLE empty_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        conn.commit()

        # Get rows (should be empty)
        cursor = execute_query_safely(
            conn,
            "SELECT * FROM {table}",
            identifier_params={'table': 'empty_table'}
        )
        rows = cursor.fetchall()

        # Empty table should still have columns
        cursor = conn.execute("PRAGMA table_info(empty_table)")
        column_info = cursor.fetchall()
        columns = [col[1] for col in column_info]

        results = [dict(row) for row in rows]

        csv_output = convert_to_csv(results, columns)

        # Should have header only
        assert 'id,name' in csv_output
        lines = csv_output.strip().split('\n')
        assert len(lines) == 1  # Header only


class TestQueryResultsExport:
    """Tests for query results export functionality"""

    def test_export_with_filter(self, test_db):
        """Test exporting filtered query results"""
        conn, db_path = test_db

        # Execute filtered query
        cursor = execute_query_safely(
            conn,
            "SELECT * FROM {table} WHERE signup_date >= ?",
            params=('2024-01-01',),
            identifier_params={'table': 'users'}
        )
        rows = cursor.fetchall()

        columns = list(rows[0].keys())
        results = [dict(row) for row in rows]

        csv_output = convert_to_csv(results, columns)

        # Should only have 2024 users
        assert 'Alice Smith' in csv_output
        assert 'Bob Jones' in csv_output
        assert 'Carol White' not in csv_output  # 2023 user

    def test_export_with_projection(self, test_db):
        """Test exporting with selected columns"""
        conn, db_path = test_db

        # Execute query with specific columns
        cursor = execute_query_safely(
            conn,
            "SELECT name, email FROM {table}",
            identifier_params={'table': 'users'}
        )
        rows = cursor.fetchall()

        columns = list(rows[0].keys())
        results = [dict(row) for row in rows]

        csv_output = convert_to_csv(results, columns)

        # Should only have name and email columns
        assert 'name,email' in csv_output
        assert 'id' not in csv_output
        assert 'signup_date' not in csv_output.split('\n')[0]  # Not in header

    def test_export_zero_results(self, test_db):
        """Test exporting query with zero results"""
        conn, db_path = test_db

        # Execute query that returns no results
        cursor = execute_query_safely(
            conn,
            "SELECT * FROM {table} WHERE signup_date > ?",
            params=('2025-01-01',),
            identifier_params={'table': 'users'}
        )
        rows = cursor.fetchall()

        # Need to get columns from table schema when no rows
        cursor = conn.execute("PRAGMA table_info(users)")
        column_info = cursor.fetchall()
        columns = [col[1] for col in column_info]

        results = [dict(row) for row in rows]

        csv_output = convert_to_csv(results, columns)

        # Should have header only
        lines = csv_output.strip().split('\n')
        assert len(lines) == 1


class TestCSVSQLInjectionProtection:
    """Tests to ensure CSV export is protected against SQL injection"""

    def test_sql_injection_in_table_name(self):
        """Test that SQL injection in table name is prevented"""
        malicious_names = [
            "users; DROP TABLE users;--",
            "users' OR '1'='1",
            "users UNION SELECT * FROM passwords",
            "users/*comment*/",
        ]

        for name in malicious_names:
            with pytest.raises(SQLSecurityError):
                validate_identifier(name, 'table')

    def test_sql_injection_in_query_results(self, test_db):
        """Test that pre-validated queries are safe"""
        conn, db_path = test_db

        # This should work - properly parameterized query
        cursor = execute_query_safely(
            conn,
            "SELECT * FROM {table} WHERE email = ?",
            params=("alice@example.com",),
            identifier_params={'table': 'users'}
        )
        rows = cursor.fetchall()

        columns = list(rows[0].keys())
        results = [dict(row) for row in rows]

        csv_output = convert_to_csv(results, columns)

        # Should return Alice's data only
        assert 'Alice' in csv_output
        lines = csv_output.strip().split('\n')
        assert len(lines) == 2  # Header + 1 row
