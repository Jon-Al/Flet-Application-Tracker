import os
import pytest
from utils.simple_logger import SimpleLogger
LOG_FILE = "test_log.txt"


@pytest.fixture
def logger():
    """Fixture to create and clean up a logger instance."""
    log = SimpleLogger(LOG_FILE)
    yield log
    log_file_path = log.log_file  # Ensure we delete the exact log file used
    if os.path.exists(log_file_path):
        os.remove(log_file_path)


def test_init(logger):
    assert os.path.exists(logger.log_file)


def test_log_message(logger):
    """Test logging a normal message."""
    logger.log("Test message")
    with open(logger.log_file, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "Test message" in lines[0]


def test_log_exception(logger):
    """Test logging an exception."""
    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.log(e)

    with open(logger.log_file, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    assert "ValueError: Test exception" in lines[0] or "Test exception" in lines[0]


def test_log_format(logger):
    """Test the format of the log entry."""
    logger.log("Format test")
    with open(logger.log_file, "r") as f:
        line = f.readline()

    parts = line.strip().split(", ")
    assert len(parts) == 5  # Should have exactly 5 parts: time, file name, method name, line number, message
    assert "Format test" in parts[-1]


def test_log_multiple_entries(logger):
    """Test logging multiple entries."""
    logger.log("First entry")
    logger.log("Second entry")

    with open(logger.log_file, "r") as f:
        lines = f.readlines()

    assert len(lines) == 2
    assert "First entry" in lines[0]
    assert "Second entry" in lines[1]
