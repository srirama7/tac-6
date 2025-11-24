"""
Unit tests for CSV export functionality
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path to import server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app
from core.csv_exporter import generate_csv_from_data

client = TestClient(app)


class TestCSVExporter:
    """Tests for the CSV exporter utility function"""

    def test_generate_csv_basic(self):
        """Test basic CSV generation"""
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "San Francisco"}
        ]
        columns = ["name", "age", "city"]

        csv = generate_csv_from_data(data, columns)

        # Check header
        assert "name,age,city" in csv
        # Check data
        assert "Alice,30,New York" in csv
        assert "Bob,25,San Francisco" in csv

    def test_generate_csv_special_characters(self):
        """Test CSV generation with special characters (quotes, commas, newlines)"""
        data = [
            {"name": 'O\'Brien', "note": "Has a comma, in text"},
            {"name": "Smith", "note": "Line 1\nLine 2"}
        ]
        columns = ["name", "note"]

        csv = generate_csv_from_data(data, columns)

        # Special characters should be properly escaped
        assert "O'Brien" in csv
        assert "comma" in csv
        # Newline should be in quoted field
        assert "Line 1" in csv

    def test_generate_csv_null_values(self):
        """Test CSV generation with null values"""
        data = [
            {"name": "Alice", "age": 30, "email": None},
            {"name": "Bob", "age": None, "email": "bob@example.com"}
        ]
        columns = ["name", "age", "email"]

        csv = generate_csv_from_data(data, columns)

        # Null values should be empty strings
        lines = csv.strip().split('\r\n')
        assert len(lines) == 3  # header + 2 rows

    def test_generate_csv_empty_data(self):
        """Test CSV generation with empty data"""
        data = []
        columns = ["name", "age"]

        csv = generate_csv_from_data(data, columns)

        # Should have header only
        assert "name,age" in csv
        lines = csv.strip().split('\r\n')
        assert len(lines) == 1  # header only


class TestTableExport:
    """Tests for table export endpoint"""

    def setup_method(self):
        """Set up test data before each test"""
        # Upload a test CSV file
        test_data = "name,age\nAlice,30\nBob,25\n"
        files = {"file": ("test.csv", test_data, "text/csv")}
        response = client.post("/api/upload", files=files)
        assert response.status_code == 200

    def test_export_valid_table(self):
        """Test exporting a valid table"""
        response = client.get("/api/export/table/test")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]
        assert "test.csv" in response.headers["content-disposition"]

        # Check CSV content
        csv_content = response.text
        assert "name,age" in csv_content
        assert "Alice,30" in csv_content
        assert "Bob,25" in csv_content

    def test_export_nonexistent_table(self):
        """Test exporting a table that doesn't exist"""
        response = client.get("/api/export/table/nonexistent")

        assert response.status_code == 404

    def test_export_invalid_table_name(self):
        """Test exporting with invalid table name (SQL injection attempt)"""
        response = client.get("/api/export/table/test; DROP TABLE test--")

        assert response.status_code == 400


class TestResultsExport:
    """Tests for query results export endpoint"""

    def test_export_results_basic(self):
        """Test exporting basic query results"""
        request_data = {
            "columns": ["name", "age", "city"],
            "results": [
                {"name": "Alice", "age": 30, "city": "New York"},
                {"name": "Bob", "age": 25, "city": "San Francisco"}
            ]
        }

        response = client.post("/api/export/results", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]
        assert "query_results_" in response.headers["content-disposition"]
        assert ".csv" in response.headers["content-disposition"]

        # Check CSV content
        csv_content = response.text
        assert "name,age,city" in csv_content
        assert "Alice,30,New York" in csv_content

    def test_export_results_empty(self):
        """Test exporting empty results"""
        request_data = {
            "columns": ["name", "age"],
            "results": []
        }

        response = client.post("/api/export/results", json=request_data)

        assert response.status_code == 200

        # Should have header only
        csv_content = response.text
        assert "name,age" in csv_content

    def test_export_results_special_characters(self):
        """Test exporting results with special characters"""
        request_data = {
            "columns": ["name", "note"],
            "results": [
                {"name": "O'Brien", "note": "Has a comma, here"},
                {"name": "Smith", "note": "Quote: \"test\""}
            ]
        }

        response = client.post("/api/export/results", json=request_data)

        assert response.status_code == 200
        csv_content = response.text
        assert "O'Brien" in csv_content
        assert "comma" in csv_content
