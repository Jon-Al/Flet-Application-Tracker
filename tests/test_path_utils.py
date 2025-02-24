import os
from datetime import datetime
from pathlib import Path

import pytest

from utils.path_utils import (normalize_path,
                              find_path_from_project_root,
                              create_folder_if_dne, get_project_root,
                              PathFlag,
                              PathManager)


def test_normalize_path(capsys):
    test_path = "./test_folder/../test_folder/sub_folder"
    expected = os.path.abspath("test_folder/sub_folder")
    assert normalize_path(test_path) == expected


def test_find_path_from_project_root():
    root = get_project_root()
    test_file = "test_file.txt"
    file_path = Path(root) / test_file
    file_path.touch()
    try:
        assert find_path_from_project_root(test_file) == str(file_path.resolve())
    finally:
        file_path.unlink()


def test_find_path_from_project_root_not_found():
    with pytest.raises(FileNotFoundError):
        find_path_from_project_root("non_existent_file.txt")


def test_create_folder_if_dne(tmp_path):
    new_folder = tmp_path / "new_folder"
    create_folder_if_dne(str(new_folder))
    assert new_folder.exists() and new_folder.is_dir()


def test_get_project_root():
    root = get_project_root()
    assert Path(root).exists() and Path(root).is_dir()


def test_path_manager_normalize():
    test_path = "./temp_folder"
    pm = PathManager(test_path, PathFlag.NORMALIZE)
    assert pm.new_path == Path(test_path).resolve()


def test_path_manager_cascade(tmp_path):
    test_path = tmp_path / "storage"
    pm = PathManager(str(test_path), [PathFlag.CASCADE_BY_YEAR, PathFlag.CASCADE_BY_MONTH, PathFlag.CASCADE_BY_DAY])
    expected_path = test_path / datetime.now().strftime("%Y/%m-%b/%d")
    assert Path(pm.new_path) == expected_path


def test_path_manager_create_if_missing(tmp_path):
    test_path = tmp_path.resolve() / "new_storage"
    pm = PathManager(str(test_path), PathFlag.CREATE_FOLDER)
    ex = pm.new_path.exists()
    assert Path(pm.new_path).resolve().exists()
    assert Path(pm.new_path).resolve().is_dir()


def test_path_manager_from_project_root():
    root = get_project_root()
    test_path = "logs"
    pm = PathManager(test_path, PathFlag.FROM_PROJECT_ROOT)
    assert pm.new_path == Path(root) / test_path


def test_path_manager_postfix_flag():
    test_path = "new_storage"
    pm = PathManager(test_path, PathFlag.CHANGED_SUFFIX)
    assert not (pm.flags & PathFlag.CHANGED_SUFFIX)
    pm2 = PathManager(test_path)
    assert not (pm2.flags & PathFlag.CHANGED_SUFFIX)


def test_increment_if_exists():
    test_dir = Path("test_increment")
    test_dir.mkdir(exist_ok=True)
    try:
        test_file = test_dir / "test_file.json"
        test_file.touch()
        pm = PathManager(test_file, PathFlag.INCREMENT_IF_EXISTS)
        incremented_path = pm.resolve_new_path
        assert incremented_path != test_file
        assert incremented_path.suffix == ".json"
        incremented_path.touch()
        pm_next = PathManager(test_file, PathFlag.INCREMENT_IF_EXISTS)
        next_incremented_path = pm_next.resolve_new_path
        assert next_incremented_path != incremented_path
        assert next_incremented_path.suffix == ".json"

    finally:
        for file in test_dir.glob("*"):
            file.unlink()
        test_dir.rmdir()


if __name__ == "__main__":
    pytest.main()
