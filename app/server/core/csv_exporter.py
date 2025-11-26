"""CSV Export Module

This module provides functionality to convert database query results into CSV format
with proper formatting, escaping, and UTF-8 encoding.
"""

import csv
import io
import re
from typing import Any, Dict, List


def generate_csv_from_data(columns: List[str], rows: List[Dict[str, Any]]) -> str:
    """Generate CSV string from column names and row data.

    This function converts database query results into a properly formatted CSV string.
    It handles special characters (commas, quotes, newlines), null values, and ensures
    UTF-8 encoding for international character support.

    Args:
        columns: List of column names to use as CSV headers
        rows: List of dictionaries representing data rows, where keys are column names

    Returns:
        CSV-formatted string with headers and data rows

    Examples:
        >>> columns = ['id', 'name', 'email']
        >>> rows = [
        ...     {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
        ...     {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
        ... ]
        >>> csv_data = generate_csv_from_data(columns, rows)
        >>> print(csv_data)
        id,name,email
        1,John Doe,john@example.com
        2,Jane Smith,jane@example.com
    """
    # Create an in-memory string buffer
    output = io.StringIO()

    # Create CSV writer with proper quoting and escaping
    writer = csv.writer(
        output,
        quoting=csv.QUOTE_MINIMAL,
        lineterminator='\n'
    )

    # Write header row
    writer.writerow(columns)

    # Write data rows
    for row in rows:
        # Extract values in the same order as columns
        # Convert None to empty string for CSV compatibility
        row_values = [
            _format_csv_value(row.get(col))
            for col in columns
        ]
        writer.writerow(row_values)

    # Get the CSV string and return
    csv_string = output.getvalue()
    output.close()

    return csv_string


def _format_csv_value(value: Any) -> str:
    """Format a single value for CSV output.

    Converts various data types to their string representation suitable for CSV.
    Handles None/NULL values, booleans, numbers, and strings.

    Args:
        value: The value to format

    Returns:
        String representation of the value
    """
    if value is None:
        return ''
    elif isinstance(value, bool):
        return str(value)
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        # Convert to string (handles dates, timestamps, etc.)
        return str(value)


def sanitize_filename(name: str) -> str:
    """Sanitize a string to create a safe filename.

    Removes or replaces characters that are invalid in filenames across different
    operating systems (Windows, macOS, Linux). Ensures the filename is safe to use
    for CSV export downloads.

    Args:
        name: The original filename or table name

    Returns:
        Sanitized filename safe for use across operating systems

    Examples:
        >>> sanitize_filename('my_table')
        'my_table'
        >>> sanitize_filename('user/data<2024>')
        'user_data_2024_'
        >>> sanitize_filename('table:name|with*special?chars')
        'table_name_with_special_chars'
    """
    # Define invalid filename characters for Windows, macOS, and Linux
    # Windows: < > : " / \ | ? *
    # Also remove control characters and leading/trailing spaces/dots
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'

    # Replace invalid characters with underscore
    sanitized = re.sub(invalid_chars, '_', name)

    # Remove leading/trailing spaces and dots (problematic on Windows)
    sanitized = sanitized.strip('. ')

    # If the result is empty or only underscores, provide a default
    if not sanitized or sanitized.replace('_', '') == '':
        sanitized = 'export'

    # Limit length to 255 characters (common filesystem limit)
    sanitized = sanitized[:255]

    return sanitized
