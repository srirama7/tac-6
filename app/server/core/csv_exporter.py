"""CSV Export Utility

This module provides utility functions for converting database query results
into properly formatted CSV files.
"""

import csv
import io
from typing import List, Dict, Any


def generate_csv_from_data(data: List[Dict[str, Any]], columns: List[str]) -> str:
    """
    Generate CSV content from data rows and column names.

    Args:
        data: List of dictionaries representing rows
        columns: List of column names (in order)

    Returns:
        CSV-formatted string with proper escaping

    Notes:
        - Uses RFC 4180 standard for CSV formatting
        - UTF-8 encoding for international characters
        - Proper escaping for special characters (quotes, commas, newlines)
        - Handles None values as empty strings
    """
    # Use StringIO to build CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=columns,
        quoting=csv.QUOTE_MINIMAL,
        lineterminator='\r\n'  # CRLF for maximum compatibility
    )

    # Write header row
    writer.writeheader()

    # Write data rows
    for row in data:
        # Convert None values to empty strings
        cleaned_row = {
            col: (row.get(col, '') if row.get(col) is not None else '')
            for col in columns
        }
        writer.writerow(cleaned_row)

    # Get the CSV string
    csv_content = output.getvalue()
    output.close()

    return csv_content
