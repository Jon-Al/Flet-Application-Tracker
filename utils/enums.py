from enum import Enum


class ColumnType(Enum):
    """Strict data types for database columns."""
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    REAL = "REAL"
    CURRENCY = "CURRENCY"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    BOOLEAN = "BOOLEAN"
    BLOB = "BLOB"


class PlaceholderType(Enum):
    DEFAULT_PLACEHOLDER = 'default',
    REQUIRED_PLACEHOLDER = 'required',
    INVALID_PLACEHOLDER = 'invalid',
