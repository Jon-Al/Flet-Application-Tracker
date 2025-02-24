import json
from pathlib import Path

import pytest
from utils.json_import_export import import_json, save_json
from utils.path_utils import PathManager, PathFlag

TEST_DIR = PathManager.resolve_path("test_data", PathFlag.R)
TEST_JSON_FILE = TEST_DIR / "test_file.json"


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """Setup and cleanup test JSON files before and after each test."""
    TEST_DIR.mkdir(exist_ok=True)  # Ensure test directory exists
    yield
    for file in TEST_DIR.glob("*"):
        file.unlink()
    TEST_DIR.rmdir()


def test_import_json_file_not_found():
    """Test importing from a non-existent file returns an empty dictionary."""
    assert import_json(TEST_JSON_FILE) == {}


def test_import_json_valid():
    """Test importing a valid JSON file."""
    data = {"name": "Alice", "age": 30}
    TEST_JSON_FILE.write_text(json.dumps(data))  # Create JSON file

    loaded_data = import_json(TEST_JSON_FILE)
    assert loaded_data == data


def test_import_json_invalid():
    """Test importing an invalid JSON file logs an error and returns an empty dictionary."""
    TEST_JSON_FILE.write_text("{invalid_json}")  # Corrupt JSON

    loaded_data = import_json(TEST_JSON_FILE)
    assert loaded_data == {}  # Should return an empty dict


def test_save_json_success():
    """Test successfully saving a JSON file."""
    data = {"key": "value"}
    result = save_json(data, TEST_JSON_FILE, overwrite=True)

    assert result == TEST_JSON_FILE
    assert TEST_JSON_FILE.exists()
    assert json.loads(TEST_JSON_FILE.read_text()) == data


def test_save_json_no_overwrite():
    """Test that saving without overwrite does not replace existing file."""
    data1 = {"first": "data"}
    data2 = {"second": "data"}

    save_json(data1, TEST_JSON_FILE, overwrite=True)  # First save
    result = save_json(data2, TEST_JSON_FILE, overwrite=False)  # Second save without overwrite

    assert result is False  # Should not overwrite
    assert json.loads(TEST_JSON_FILE.read_text()) == data1  # File should contain first data


def test_save_json_increment():
    """Test that incrementing filenames works correctly when a file exists."""
    data = {"entry": "test"}

    # First, create an initial JSON file
    save_json(data, TEST_JSON_FILE, overwrite=True)

    # Call save_json() with increment=True
    p = save_json(data, TEST_JSON_FILE, increment=True)  # Should create a new incremented file

    print("\nSTART DEBUGGING")
    print("Returned path from save_json: " + str(p))
    print("Existing files in test directory:", list(TEST_DIR.glob('*')))
    print("END DEBUGGING\n")

    # Ensure save_json() actually returned a valid Path
    assert isinstance(p, Path), "save_json() did not return a Path"
    assert p.exists(), f"Expected file {p} to exist, but it does not."

    # Check if the new incremented file is present in the directory
    incremented_file = None
    for file in TEST_DIR.glob("*"):
        if file.stem.startswith("test_file") and file.suffix == ".json" and file != TEST_JSON_FILE:
            incremented_file = file
            break

    assert incremented_file is not None, "No incremented file was created"
    assert incremented_file.exists()
    assert json.loads(incremented_file.read_text()) == data
