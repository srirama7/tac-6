"""Tests for CSV export functionality"""

import pytest
from core.csv_exporter import (
    generate_csv_from_data,
    sanitize_filename,
    _format_csv_value
)


class TestGenerateCSVFromData:
    """Test CSV generation from data"""

    def test_basic_csv_generation(self):
        """Test basic CSV generation with simple data"""
        columns = ['id', 'name', 'email']
        rows = [
            {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
            {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
        ]

        csv_data = generate_csv_from_data(columns, rows)

        expected = (
            "id,name,email\n"
            "1,John Doe,john@example.com\n"
            "2,Jane Smith,jane@example.com\n"
        )
        assert csv_data == expected

    def test_empty_dataset(self):
        """Test CSV generation with empty dataset"""
        columns = ['id', 'name', 'email']
        rows = []

        csv_data = generate_csv_from_data(columns, rows)

        # Should only contain headers
        expected = "id,name,email\n"
        assert csv_data == expected

    def test_null_values(self):
        """Test CSV generation with null values"""
        columns = ['id', 'name', 'email']
        rows = [
            {'id': 1, 'name': 'John Doe', 'email': None},
            {'id': 2, 'name': None, 'email': 'jane@example.com'}
        ]

        csv_data = generate_csv_from_data(columns, rows)

        expected = (
            "id,name,email\n"
            "1,John Doe,\n"
            "2,,jane@example.com\n"
        )
        assert csv_data == expected

    def test_special_characters_in_data(self):
        """Test CSV generation with special characters (commas, quotes, newlines)"""
        columns = ['id', 'description']
        rows = [
            {'id': 1, 'description': 'Contains, comma'},
            {'id': 2, 'description': 'Contains "quotes"'},
            {'id': 3, 'description': 'Contains\nnewline'}
        ]

        csv_data = generate_csv_from_data(columns, rows)

        # CSV writer should properly quote fields with special characters
        lines = csv_data.split('\n')
        assert lines[0] == 'id,description'
        assert 'Contains, comma' in csv_data
        assert '"Contains ""quotes"""' in csv_data  # Quotes should be escaped
        assert 'Contains\nnewline' in csv_data

    def test_various_data_types(self):
        """Test CSV generation with different data types"""
        columns = ['int_col', 'float_col', 'bool_col', 'str_col']
        rows = [
            {'int_col': 42, 'float_col': 3.14, 'bool_col': True, 'str_col': 'text'},
            {'int_col': 0, 'float_col': -2.5, 'bool_col': False, 'str_col': ''}
        ]

        csv_data = generate_csv_from_data(columns, rows)

        expected = (
            "int_col,float_col,bool_col,str_col\n"
            "42,3.14,True,text\n"
            "0,-2.5,False,\n"
        )
        assert csv_data == expected

    def test_unicode_characters(self):
        """Test CSV generation with unicode and international characters"""
        columns = ['id', 'name', 'description']
        rows = [
            {'id': 1, 'name': '李明', 'description': 'Chinese characters'},
            {'id': 2, 'name': 'José', 'description': 'Spanish accents'},
            {'id': 3, 'name': 'محمد', 'description': 'Arabic text'},
            {'id': 4, 'name': 'Emoji😊', 'description': 'Contains emoji'}
        ]

        csv_data = generate_csv_from_data(columns, rows)

        # Should preserve unicode characters
        assert '李明' in csv_data
        assert 'José' in csv_data
        assert 'محمد' in csv_data
        assert 'Emoji😊' in csv_data

    def test_very_long_strings(self):
        """Test CSV generation with very long strings"""
        columns = ['id', 'long_text']
        long_string = 'A' * 10000  # 10,000 character string
        rows = [
            {'id': 1, 'long_text': long_string}
        ]

        csv_data = generate_csv_from_data(columns, rows)

        assert long_string in csv_data
        assert len(csv_data) > 10000

    def test_missing_column_in_row(self):
        """Test CSV generation when row is missing a column"""
        columns = ['id', 'name', 'email']
        rows = [
            {'id': 1, 'name': 'John Doe'},  # Missing 'email'
            {'id': 2, 'email': 'jane@example.com'}  # Missing 'name'
        ]

        csv_data = generate_csv_from_data(columns, rows)

        # Missing values should be treated as None/empty
        expected = (
            "id,name,email\n"
            "1,John Doe,\n"
            "2,,jane@example.com\n"
        )
        assert csv_data == expected

    def test_large_dataset(self):
        """Test CSV generation with large dataset"""
        columns = ['id', 'value']
        rows = [{'id': i, 'value': f'value_{i}'} for i in range(1000)]

        csv_data = generate_csv_from_data(columns, rows)

        # Should have header + 1000 data rows
        lines = csv_data.strip().split('\n')
        assert len(lines) == 1001  # 1 header + 1000 rows


class TestFormatCSVValue:
    """Test individual value formatting"""

    def test_none_value(self):
        """Test formatting None values"""
        assert _format_csv_value(None) == ''

    def test_boolean_values(self):
        """Test formatting boolean values"""
        assert _format_csv_value(True) == 'True'
        assert _format_csv_value(False) == 'False'

    def test_integer_values(self):
        """Test formatting integer values"""
        assert _format_csv_value(0) == '0'
        assert _format_csv_value(42) == '42'
        assert _format_csv_value(-100) == '-100'

    def test_float_values(self):
        """Test formatting float values"""
        assert _format_csv_value(3.14) == '3.14'
        assert _format_csv_value(0.0) == '0.0'
        assert _format_csv_value(-2.5) == '-2.5'

    def test_string_values(self):
        """Test formatting string values"""
        assert _format_csv_value('hello') == 'hello'
        assert _format_csv_value('') == ''
        assert _format_csv_value('with spaces') == 'with spaces'


class TestSanitizeFilename:
    """Test filename sanitization"""

    def test_valid_filename(self):
        """Test that valid filenames are unchanged"""
        assert sanitize_filename('my_table') == 'my_table'
        assert sanitize_filename('users_2024') == 'users_2024'
        assert sanitize_filename('data-export') == 'data-export'

    def test_invalid_characters(self):
        """Test removal of invalid filename characters"""
        assert sanitize_filename('user/data') == 'user_data'
        assert sanitize_filename('table<name>') == 'table_name_'
        assert sanitize_filename('file:name') == 'file_name'
        assert sanitize_filename('data|export') == 'data_export'
        assert sanitize_filename('table*name') == 'table_name'
        assert sanitize_filename('file?name') == 'file_name'
        assert sanitize_filename('path\\to\\file') == 'path_to_file'
        assert sanitize_filename('quote"name') == 'quote_name'

    def test_multiple_invalid_characters(self):
        """Test removal of multiple invalid characters"""
        result = sanitize_filename('user/data<2024>|file*.csv')
        assert result == 'user_data_2024__file_.csv'

    def test_leading_trailing_spaces(self):
        """Test removal of leading/trailing spaces and dots"""
        assert sanitize_filename('  filename  ') == 'filename'
        assert sanitize_filename('.hidden') == 'hidden'
        assert sanitize_filename('file.') == 'file'
        assert sanitize_filename('  .file.  ') == 'file'

    def test_empty_or_invalid_result(self):
        """Test handling of empty or only-invalid-chars input"""
        assert sanitize_filename('') == 'export'
        assert sanitize_filename('   ') == 'export'
        assert sanitize_filename('...') == 'export'
        assert sanitize_filename('___') == 'export'
        assert sanitize_filename('<>:|?*') == 'export'

    def test_unicode_filenames(self):
        """Test that unicode characters are preserved"""
        assert sanitize_filename('文件名') == '文件名'
        assert sanitize_filename('données') == 'données'

    def test_length_limit(self):
        """Test that very long filenames are truncated"""
        long_name = 'a' * 300
        result = sanitize_filename(long_name)
        assert len(result) == 255

    def test_preserves_extensions(self):
        """Test that file extensions are preserved"""
        assert sanitize_filename('myfile.csv') == 'myfile.csv'
        assert sanitize_filename('data.export.csv') == 'data.export.csv'
