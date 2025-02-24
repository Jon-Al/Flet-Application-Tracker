import os

import pytest
from utils.database_handler import DatabaseHandler
from utils.path_utils import PathManager, PathFlag

DB_NAME = r"tests/data/test_database.db"
CREATION_SCRIPT = r"tests/data/dummy_data.sql"


@pytest.fixture(scope="module")
def db_handler():
    try:
        p = PathManager.resolve_path(DB_NAME, PathFlag.R)
        os.remove(p.resolve())
    except FileNotFoundError:
        pass
    """Fixture to create a fresh database for each test."""
    handler = DatabaseHandler(DB_NAME, CREATION_SCRIPT)
    handler.execute_mode(False)
    return handler


# ---- Database Query Tests ----

def test_execute_query_fetchall(db_handler):
    result = db_handler.execute_query("SELECT * FROM users", fetch_mode=-1)
    assert len(result) == 5
    assert result[0] == (1, 'Alice', 30, 'alice@example.com')


def test_execute_query_fetchone(db_handler):
    result = db_handler.execute_query("SELECT id FROM users ", ( ), 1)
    assert len(result) == 1
    assert result[0] == 1


def test_execute_query_fetch_some(db_handler):
    result = db_handler.execute_query("SELECT * FROM users ", (  ), 2)
    assert len(result) == 2
    assert result[0] == (1, 'Alice', 30, 'alice@example.com')


def test_insert_bulk_data(db_handler):
    db_handler.execute_query("DELETE FROM users WHERE name = ? and age = ? and email = ?",
                             ("Grace", 123, "grace@example.com"))
    db_handler.execute_query("DELETE FROM users WHERE name = ? and age = ? and email = ?",
                             ("Garry", 45, "garry@example.com"))
    db_handler.insert_bulk_data("INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
                                [("Grace", 123, "grace@example.com"), ("Garry", 45, "garry@example.com")])
    result = db_handler.execute_query("SELECT name, age, email FROM users ORDER BY id DESC", fetch_mode=2)

    assert result[1] == ("Grace", 123, "grace@example.com")
    assert result[0] == ("Garry", 45, "garry@example.com")
    db_handler.execute_query("DELETE FROM users WHERE name = ? and age = ? and email = ?",
                             ("Grace", 123, "grace@example.com"))
    db_handler.execute_query("DELETE FROM users WHERE name = ? and age = ? and email = ?",
                             ("Garry", 45, "garry@example.com"))


def test_select_all(db_handler):
    result = db_handler.select_all("users")
    assert len(result) == 5
    assert result[0] == (1, 'Alice', 30, 'alice@example.com')


# ---- Table Metadata Tests ----

def test_get_table_metadata(db_handler):
    metadata = db_handler.get_table_metadata("users")
    column_names = [column[1] for column in metadata]
    assert column_names == ["id", "name", "age", "email"]


# ---- Row Factory Tests ----
@pytest.mark.parametrize("factory, expected_type", [
    (False, tuple),
    (True, dict),
])
def test_use_row_factory(db_handler, factory, expected_type):
    db_handler.execute_mode(factory)
    result = db_handler.execute_query("SELECT * FROM users", fetch_mode=-1)
    assert isinstance(result[0], expected_type)
