"""CSV generation utilities for exporting query results and table data."""
import csv
import io
from typing import List, Dict, Any


def generate_csv_from_results(results: List[Dict[str, Any]], columns: List[str]) -> str:
    """
    Generate CSV content from query results.

    Args:
        results: List of dictionaries containing row data
        columns: List of column names for CSV headers

    Returns:
        CSV content as a string

    Note:
        - Handles None/null values by converting them to empty strings
        - Properly escapes special characters (quotes, commas, newlines)
        - Uses RFC 4180 compliant CSV format
        - UTF-8 encoding for international characters
    """
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction='ignore')

    # Write header row
    writer.writeheader()

    # Write data rows
    for row in results:
        # Convert None values to empty strings for CSV compatibility
        cleaned_row = {
            key: '' if value is None else value
            for key, value in row.items()
        }
        writer.writerow(cleaned_row)

    # Get CSV content and return
    csv_content = output.getvalue()
    output.close()

    return csv_content
