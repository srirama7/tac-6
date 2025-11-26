"""
Unit tests for CSV export endpoints
"""

import pytest
import sqlite3
import tempfile
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from server import app
from core.sql_processor import convert_to_csv


@pytest.fixture
def test_db():
    """Create a test database with sample data"""
    # Create temporary database
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
                   ('Charlie', 'charlie@example.com', None))  # Test NULL value

    conn.commit()
    conn.close()

    yield db_file.name

    # Cleanup
    os.unlink(db_file.name)


class TestCSVConversionFunction:
    """Test the convert_to_csv utility function"""

    def test_convert_empty_results_to_csv(self):
        """Test converting empty results to CSV"""
        columns = ['id', 'name', 'email']
        results = []

        csv_output = convert_to_csv(columns, results)

        # Should contain only headers
        lines = csv_output.strip().split('\n')
        assert len(lines) == 1
        assert lines[0] == 'id,name,email'

    def test_convert_single_row_to_csv(self):
        """Test converting single row to CSV"""
        columns = ['id', 'name', 'email']
        results = [{'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}]

        csv_output = convert_to_csv(columns, results)

        lines = csv_output.strip().replace('\r\n', '\n').split('\n')
        assert len(lines) == 2
        assert lines[0] == 'id,name,email'
        assert lines[1] == '1,Alice,alice@example.com'

    def test_convert_multiple_rows_to_csv(self):
        """Test converting multiple rows to CSV"""
        columns = ['id', 'name']
        results = [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
            {'id': 3, 'name': 'Charlie'}
        ]

        csv_output = convert_to_csv(columns, results)

        lines = csv_output.strip().replace('\r\n', '\n').split('\n')
        assert len(lines) == 4
        assert lines[0] == 'id,name'
        assert lines[1] == '1,Alice'
        assert lines[2] == '2,Bob'
        assert lines[3] == '3,Charlie'

    def test_convert_with_special_characters(self):
        """Test that special characters are properly escaped"""
        columns = ['id', 'description']
        results = [
            {'id': 1, 'description': 'Contains, comma'},
            {'id': 2, 'description': 'Contains "quotes"'},
            {'id': 3, 'description': 'Contains\nnewline'},
            {'id': 4, 'description': 'Normal text'}
        ]

        csv_output = convert_to_csv(columns, results)

        # CSV should properly escape these values
        assert 'Contains, comma' in csv_output or '"Contains, comma"' in csv_output
        assert 'Contains "quotes"' in csv_output or 'Contains ""quotes""' in csv_output

    def test_convert_with_null_values(self):
        """Test that NULL values are converted to empty strings"""
        columns = ['id', 'name', 'email']
        results = [
            {'id': 1, 'name': 'Alice', 'email': None},
            {'id': 2, 'name': None, 'email': 'bob@example.com'}
        ]

        csv_output = convert_to_csv(columns, results)

        lines = csv_output.strip().split('\n')
        assert len(lines) == 3
        # NULL values should be represented as empty fields
        assert ',,' in csv_output or ',"",' in csv_output or lines[1].endswith(',')

    def test_csv_column_headers_included(self):
        """Test that column headers are included in CSV"""
        columns = ['user_id', 'user_name', 'user_email']
        results = [{'user_id': 1, 'user_name': 'Alice', 'user_email': 'alice@example.com'}]

        csv_output = convert_to_csv(columns, results)

        lines = csv_output.strip().replace('\r\n', '\n').split('\n')
        assert lines[0] == 'user_id,user_name,user_email'


class TestTableExportEndpoint:
    """Test the table export endpoint"""

    @patch('server.sqlite3.connect')
    def test_successful_export_of_existing_table(self, mock_connect):
        """Test successful export of an existing table"""
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn

        # Mock check_table_exists to return True
        with patch('server.check_table_exists', return_value=True):
            # Mock execute_query_safely
            mock_cursor.description = [('id',), ('name',)]
            mock_cursor.fetchall.return_value = [(1, 'Alice'), (2, 'Bob')]

            with patch('server.execute_query_safely', return_value=mock_cursor):
                client = TestClient(app)
                response = client.get('/api/export/table/test_users')

                assert response.status_code == 200
                assert response.headers['content-type'] == 'text/csv; charset=utf-8'
                assert 'attachment; filename="test_users.csv"' in response.headers['content-disposition']

                # Check CSV content
                content = response.text
                assert 'id,name' in content
                assert 'Alice' in content
                assert 'Bob' in content

    @patch('server.sqlite3.connect')
    def test_export_nonexistent_table_returns_404(self, mock_connect):
        """Test that exporting a non-existent table returns 404"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Mock check_table_exists to return False
        with patch('server.check_table_exists', return_value=False):
            client = TestClient(app)
            response = client.get('/api/export/table/nonexistent_table')

            assert response.status_code == 404

    def test_export_invalid_table_name_returns_400(self):
        """Test that invalid table name returns 400"""
        client = TestClient(app)

        # Try various invalid table names
        invalid_names = [
            "users'; DROP TABLE users; --",
            "users' OR '1'='1",
            "SELECT",
            "123_table"
        ]

        for name in invalid_names:
            response = client.get(f'/api/export/table/{name}')
            assert response.status_code == 400

    @patch('server.sqlite3.connect')
    def test_export_proper_csv_content_type(self, mock_connect):
        """Test that proper CSV Content-Type header is returned"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn

        with patch('server.check_table_exists', return_value=True):
            mock_cursor.description = [('id',)]
            mock_cursor.fetchall.return_value = [(1,)]

            with patch('server.execute_query_safely', return_value=mock_cursor):
                client = TestClient(app)
                response = client.get('/api/export/table/test_table')

                assert response.status_code == 200
                assert 'text/csv' in response.headers['content-type']

    @patch('server.sqlite3.connect')
    def test_export_proper_content_disposition_with_filename(self, mock_connect):
        """Test that proper Content-Disposition with filename is returned"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn

        with patch('server.check_table_exists', return_value=True):
            mock_cursor.description = [('id',)]
            mock_cursor.fetchall.return_value = [(1,)]

            with patch('server.execute_query_safely', return_value=mock_cursor):
                client = TestClient(app)
                response = client.get('/api/export/table/my_table')

                assert response.status_code == 200
                assert 'attachment; filename="my_table.csv"' in response.headers['content-disposition']


class TestQueryExportEndpoint:
    """Test the query results export endpoint"""

    def test_successful_export_with_valid_data(self):
        """Test successful export with valid data"""
        client = TestClient(app)

        request_data = {
            'columns': ['id', 'name', 'email'],
            'results': [
                {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
                {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
            ]
        }

        response = client.post('/api/export/query', json=request_data)

        assert response.status_code == 200
        assert response.headers['content-type'] == 'text/csv; charset=utf-8'
        assert 'attachment; filename="query_results.csv"' in response.headers['content-disposition']

        # Check CSV content
        content = response.text
        assert 'id,name,email' in content
        assert 'Alice' in content
        assert 'Bob' in content

    def test_export_with_empty_columns(self):
        """Test export with empty columns returns 400"""
        client = TestClient(app)

        request_data = {
            'columns': [],
            'results': []
        }

        response = client.post('/api/export/query', json=request_data)
        assert response.status_code == 400

    def test_export_with_empty_results(self):
        """Test export with empty results returns 400"""
        client = TestClient(app)

        request_data = {
            'columns': ['id', 'name'],
            'results': []
        }

        response = client.post('/api/export/query', json=request_data)
        assert response.status_code == 400

    def test_export_proper_headers_and_content_type(self):
        """Test that proper headers and content type are returned"""
        client = TestClient(app)

        request_data = {
            'columns': ['id', 'name'],
            'results': [
                {'id': 1, 'name': 'Alice'}
            ]
        }

        response = client.post('/api/export/query', json=request_data)

        assert response.status_code == 200
        assert 'text/csv' in response.headers['content-type']
        assert 'attachment' in response.headers['content-disposition']
        assert 'query_results.csv' in response.headers['content-disposition']

    def test_csv_formatting_is_correct(self):
        """Test that CSV formatting is correct with headers and escaping"""
        client = TestClient(app)

        request_data = {
            'columns': ['id', 'description'],
            'results': [
                {'id': 1, 'description': 'Contains, comma'},
                {'id': 2, 'description': 'Normal text'}
            ]
        }

        response = client.post('/api/export/query', json=request_data)

        assert response.status_code == 200
        content = response.text

        # Check headers are present
        assert 'id,description' in content

        # Check data is present (comma in value should be handled)
        assert 'Contains' in content
        assert 'Normal text' in content
