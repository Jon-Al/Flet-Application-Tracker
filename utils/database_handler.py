import sqlite3
from pathlib import Path
from typing import Tuple, Any, Union, Optional, List

from utils.path_utils import PathManager, PathFlag


class DatabaseHandler:
    def __init__(self, db_path: Union[str, Path], creation_script_path: Optional[Union[str, Path]] = None,
                 execute_mode: bool = True, backup_script_path: Optional[Union[str, Path]] = None):
        """
        :param db_path: the path to the database
        :param creation_script_path: the path to the creation script for the database (if needed)
        :param execute_mode: if to use row mode.
        """
        self._database = PathManager.resolve_path(db_path, PathFlag.R | PathFlag.N)
        if not self._database.exists():
            self.execute_script(backup_script_path)
        self._execute_mode = execute_mode
        if not self._database.exists():
            if not creation_script_path:
                raise FileNotFoundError("Database does not exist and path to creation script not specified.")
            creation_script = PathManager.resolve_path(creation_script_path, PathFlag.R)
            if not creation_script.exists():
                raise FileNotFoundError("Database does not exist and path to creation script not specified.")
            self.execute_script(creation_script)
        self.execute_query('PRAGMA case_sensitive_like = FALSE')

    @property
    def database(self) -> Path:
        return self._database

    def execute_mode(self, mode):
        self._execute_mode = bool(mode)

    def execute_script(self, script: Union[str, Path]):
        with sqlite3.connect(self.database) as conn:
            with open(PathManager.resolve_path(script)) as f:
                conn.executescript(f.read())


    def execute_query(self, query: str, params: Tuple[Any, ...] = None, fetch_mode: int = -1):
        """
        Executes an SQL query and returns results based on the query type.
        Raises exceptions on failures instead of returning error status.

        :param query: The SQL query string to execute.
        :param params: Query parameters as a tuple. Defaults to None.
        :param fetch_mode: Controls row fetching behavior:
                        * ``<0``: Fetch all rows (default for SELECT queries).
                        * ``0``: No rows fetched.
                        * ``>0``: Fetch up to the specified number of rows.

        :return: Based on query type:
                * SELECT: List[Dict] of rows, single row, or None based on fetchall
                * INSERT: lastrowid or 0 if no insert occurred
                * UPDATE/DELETE: Number of rows affected
        :raises: sqlite3.Error for database-related errors
        """

        def dict_factory(_cursor, _row):
            fields = [column[0] for column in _cursor.description]
            return {key: value for key, value in zip(fields, _row)}

        conn = None
        try:
            conn = sqlite3.connect(self.database)
            if self._execute_mode:
                conn.row_factory = dict_factory
            else:
                conn.row_factory = None

            conn.execute("BEGIN TRANSACTION")
            cursor = conn.cursor()

            if not params:
                cursor.execute(query)
            else:
                cursor.execute(query, params if params else ())
            query_type = query.lstrip().upper().split()[0]
            if query_type in ("DELETE", "UPDATE"):
                result = cursor.rowcount
            elif query_type.startswith(("INSERT", "REPLACE")):
                result = cursor.lastrowid if cursor.rowcount > 0 else 0
            elif query_type == "SELECT":
                if fetch_mode == 0:
                    result = None
                elif fetch_mode < 0:
                    result = cursor.fetchall()
                elif fetch_mode == 1:
                    row = cursor.fetchone()
                    result = dict(row) if self._execute_mode and row else row
                else:
                    result = cursor.fetchmany(fetch_mode)
            else:
                result = None  # Default return for other query types

            conn.commit()
            conn.close()

            return result

        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            raise e  # Re-raise the exception after rollback


    def insert_bulk_data(self, query: str, data: List[Tuple[Any, ...]]) -> int:
        """
        Insert multiple rows of data with transaction support.
        Returns the last row id inserted.
        """
        with sqlite3.connect(self._database) as conn:
            cursor = conn.cursor()
            cursor.executemany(query, data)
            conn.commit()
            return cursor.lastrowid

    def select_all(self, table_name: str):
        """
        Select all rows from a table.
        """
        return self.execute_query(f'SELECT * FROM {table_name}', fetch_mode=-1)

    def get_table_metadata(self, table_name: str):
        """
        Get table metadata.
        """
        return self.execute_query('SELECT * FROM PRAGMA_TABLE_INFO(?)', (table_name,), fetch_mode=-1)
