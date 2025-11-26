"""
CSV Export utilities for exporting database tables and query results to CSV format.
Provides functions for safe CSV generation with proper encoding and escaping.
"""

import csv
import io
import sqlite3
from typing import Any, Dict, List

from app.server.core.sql_security import (
    check_table_exists,
    execute_query_safely,
    validate_identifier,
    SQLSecurityError,
)


class CSVExportError(Exception):
    """Raised when CSV export operation fails."""

    pass


def export_table_to_csv(conn: sqlite3.Connection, table_name: str) -> str:
    """
    Export an entire database table to CSV format.

    Args:
        conn: SQLite connection object
        table_name: Name of the table to export

    Returns:
        str: CSV-formatted string with UTF-8 encoding

    Raises:
        CSVExportError: If table doesn't exist or export fails
        SQLSecurityError: If table name is invalid
    """
    # Validate table name
    validate_identifier(table_name, "table")

    # Check if table exists
    if not check_table_exists(conn, table_name):
        raise CSVExportError(f"Table '{table_name}' does not exist")

    try:
        # Query all data from the table
        cursor = execute_query_safely(
            conn, "SELECT * FROM {table}", identifier_params={"table": table_name}
        )

        # Get column names from cursor description
        columns = [description[0] for description in cursor.description]

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries
        results = [dict(zip(columns, row)) for row in rows]

        # Generate CSV
        return export_query_results_to_csv(results, columns)

    except sqlite3.Error as e:
        raise CSVExportError(f"Database error while exporting table: {str(e)}")
    except Exception as e:
        raise CSVExportError(f"Failed to export table '{table_name}': {str(e)}")


def export_query_results_to_csv(
    results: List[Dict[str, Any]], columns: List[str]
) -> str:
    """
    Export query results to CSV format.

    Args:
        results: List of dictionaries representing rows
        columns: List of column names for the CSV header

    Returns:
        str: CSV-formatted string with UTF-8 encoding

    Raises:
        CSVExportError: If export fails
    """
    try:
        # Create a string buffer with UTF-8-sig encoding (includes BOM for Excel compatibility)
        output = io.StringIO()

        # Create CSV writer with proper settings
        # - quoting=csv.QUOTE_MINIMAL: Only quote fields that need it (contain delimiter, quote, or newline)
        # - lineterminator='\r\n': Use CRLF for maximum compatibility
        writer = csv.DictWriter(
            output,
            fieldnames=columns,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\r\n",
        )

        # Write header
        writer.writeheader()

        # Write rows
        for row in results:
            # Convert None values to empty strings for CSV
            cleaned_row = {
                key: "" if value is None else value for key, value in row.items()
            }
            writer.writerow(cleaned_row)

        # Get the CSV string
        csv_string = output.getvalue()
        output.close()

        # Add UTF-8 BOM for Excel compatibility
        return "\ufeff" + csv_string

    except Exception as e:
        raise CSVExportError(f"Failed to generate CSV: {str(e)}")
