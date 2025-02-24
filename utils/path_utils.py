import enum
import os
import re
from datetime import datetime
from functools import cache
from pathlib import Path
from typing import Union, List, Optional


def normalize_path(input_path: str) -> str:
    return os.path.abspath(os.path.normpath(input_path))


def find_path_from_project_root(relative_path: str) -> str:
    """
    Finds the absolute normalized path of a file or directory given its path
    relative to the root of the project.

    :param relative_path: The path relative to the root of the project.
    :return: The normalized absolute path of the target.
    :raises FileNotFoundError: If the file or directory is not found.
    """

    target_path = normalize_path(os.path.join(get_project_root(), relative_path))
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Path '{relative_path}' not found in project root.")
    return target_path


def create_folder_if_dne(path: str):
    """

    :param path: needs to include the complete path (including the project root's absolute path).
    :return:
    """
    target_path = normalize_path(path)
    os.makedirs(target_path, exist_ok=True)
    return target_path


def resume_or_cover_letter(option_name: str) -> Path | None:
    path = ''
    if 'cover' in option_name.lower():
        if 'logo' in option_name.lower():
            path = '/docs/templates/Jonathan Alexander - Cover Letter - With Logos.docx'
        path = '/docs/templates/Jonathan Alexander - Cover Letter.docx'
    elif 'resume' in option_name.lower():
        if 'logo' in option_name.lower():
            path = '/docs/templates/Jonathan Alexander - Resume - With Logos.docx'
        path = '/docs/templates/Jonathan Alexander - Resume.docx'
    if path:
        return PathManager.resolve_path(path, PathFlag.FROM_PROJECT_ROOT)
    else:
        return None


@cache
def get_project_root() -> str:
    """
    :function: get_project_root()
    Returns the root folder of the project by traversing upwards from the current
    working directory until a folder containing ``main.py`` is found.

    """
    current_dir = normalize_path(os.getcwd())

    while True:
        if 'main.py' in os.listdir(current_dir):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Reached the filesystem root
            raise FileNotFoundError("Project root containing 'main.py' not found.")
        current_dir = parent_dir


class PathFlag(enum.IntFlag):
    """
    Note: Using auto with IntFlag results in integers that are powers of two, starting with 1.

    See `IntFlag <https://docs.python.org/3/library/enum.html#enum.IntFlag>`_
    """
    NORMALIZE = N = enum.auto()
    """``path.resolve``. Currently always active."""
    CREATE_FOLDER = C = enum.auto()
    """creates the path if it doesn't exist. Creates the parent folder to the file if a file."""
    CASCADE_BY_YEAR = Y = enum.auto()
    """Creates folder named 'yyyy'."""
    CASCADE_BY_MONTH = M = enum.auto()
    """Creates two levels - year and month."""
    CASCADE_BY_DAY = D = enum.auto()
    """Adds subdirectory with day value."""
    FROM_PROJECT_ROOT = R = enum.auto()
    """Resolves from project's root."""
    VALIDATE = V = enum.auto()
    """Validates the path exists"""
    INCREMENT_IF_EXISTS = I = enum.auto()
    """Will add a postfix with the next number if file exists. Files only."""
    CHANGED_SUFFIX = S = enum.auto()
    """Used internally."""
    CHANGED_FILENAME = F = enum.auto()
    """Used internally."""
    CASCADE_BY_MONTH_AND_YEAR = X = enum.auto()
    """Creates folder named 'yyyy-mm'. Will be removed if CASCADE_BY_YEAR or CASCADE_BY_MONTH."""
    CASCADE_BY_DATE = Z = Y | M | D
    """Creates folder named 'yyyy-mm-dd'."""


class PathManager:
    def __init__(self, path: Union[str, Path], flags: Union[List[PathFlag] | PathFlag] = None,
                 new_postfix: Optional[str] = None) -> None:
        self._original_path = Path(path)
        self._flags = self._parse_flags(flags)
        self._new_path = self._apply_flags(self._original_path, self._flags)
        if new_postfix:
            self.with_suffix(new_postfix)

    @staticmethod
    def resolve_path(path: Union[str, Path], flags: Union[List[PathFlag] | PathFlag] = PathFlag.N) -> Path:
        path = Path(path)
        flags = PathManager._parse_flags(flags | PathFlag.N)
        return PathManager._apply_flags(path, flags).resolve()


    @staticmethod
    def create_dir_path(path: Union[str, Path]):
        """Creates the path for the new path. Stops at parent if path is a file."""
        path = PathManager.resolve_path(path)
        if PathManager._is_intended_directory(path):
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)


    @staticmethod
    def _is_intended_directory(path: Path) -> bool:
        """
        Determines if a path is intended to be a directory, even if it doesn't exist yet.

        The logic is:
        1. If path exists → use is_dir()
        2. If path doesn't exist:
           - Check if it ends with a separator
           - Check if it has no suffix (extension)
           - Check if it's exactly '.' or '..'
        """
        if path.exists():
            return path.is_dir()
        if path.suffix == '':
            path.mkdir(parents=True, exist_ok=True)
        path_str = str(path)
        if path_str.endswith(os.path.sep):
            return True
        # Check for no extension and not being just a dot
        no_extension = path.suffix == ''
        simple_dot = path.name in {'.', '..'}
        return no_extension or simple_dot

    @staticmethod
    def _parse_flags(flags: Union[List[PathFlag], PathFlag], initial: bool = True) -> PathFlag:
        """Converts input flags into a valid PathFlag value."""
        if not flags:
            return PathFlag.NORMALIZE
        if isinstance(flags, list):
            flags = PathFlag(sum(flags))
        if PathFlag.CASCADE_BY_MONTH_AND_YEAR in flags and \
                (PathFlag.CASCADE_BY_YEAR in flags or
                 PathFlag.CASCADE_BY_MONTH in flags):
            flags = flags ^ PathFlag.CASCADE_BY_MONTH_AND_YEAR
        if initial:
            if PathFlag.CHANGED_SUFFIX in flags:
                flags = flags ^ PathFlag.CHANGED_SUFFIX
            if PathFlag.CHANGED_FILENAME in flags:
                flags = flags ^ PathFlag.CHANGED_FILENAME
        return flags | PathFlag.NORMALIZE

    def _check_date_pattern(self, path: Path) -> bool:
        """Check if path already follows a date pattern."""
        if not self.flags & PathFlag.CREATE_FOLDER:
            return False

        name = path.name
        year_pattern = r'^\d{4}$'
        year_month_pattern = r'^\d{4}-\d{2}$'
        full_date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(year_pattern, name) or
                    re.match(year_month_pattern, name) or
                    re.match(full_date_pattern, name))

    @staticmethod
    def get_next_available_name(path: Path) -> Path:
        """Get the next available filename by adding incremental number."""
        if not path.exists() or PathManager._is_intended_directory(path):
            return path
        parent = path.parent
        stem = path.stem
        suffix = path.suffix
        counter = 0
        while True:
            new_name = f"{stem} - {'{:002d}'.format(counter + 1)}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1

    @staticmethod
    def _apply_flags(path: Union[str, Path], flags: Union[List[PathFlag] | PathFlag]) -> Path:
        """Applies the selected flags in a defined order."""

        if PathFlag.FROM_PROJECT_ROOT in flags:
            path = Path(get_project_root()) / path
        else:
            path = Path(path)

        if PathFlag.CASCADE_BY_DAY in flags or PathFlag.CASCADE_BY_MONTH in flags or PathFlag.CASCADE_BY_YEAR in flags:
            path = path / datetime.now().strftime("%Y")

        if PathFlag.CASCADE_BY_DAY in flags or PathFlag.CASCADE_BY_MONTH in flags:
            path = path / datetime.now().strftime("%m-%b")

        if PathFlag.CASCADE_BY_MONTH_AND_YEAR in flags:
            path = path / datetime.now().strftime("%Y-%m")

        if PathFlag.CASCADE_BY_DAY in flags:
            path = path / datetime.now().strftime("%d")

        if PathFlag.NORMALIZE in flags:
            path = path.resolve()

        if (not path.is_dir()) and (PathFlag.INCREMENT_IF_EXISTS in flags):
            path = PathManager.get_next_available_name(path)

        if PathFlag.CREATE_FOLDER in flags:
            if PathManager._is_intended_directory(path):
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
        if PathFlag.VALIDATE in flags:
            if not path.exists():
                raise NotADirectoryError(f"Path '{path}' does not exist.")

        return Path(path)


    @property
    def original_exists(self) -> bool:
        return self._original_path.exists()

    @property
    def new_exists(self) -> bool:
        return self._new_path.exists()


    @property
    def new_path(self) -> Path:
        """Returns the processed path as a Path object."""
        return self._new_path

    @property
    def original_path(self) -> Path:
        """Returns the original path as a Path object."""
        return self._original_path

    @property
    def flags(self) -> PathFlag:
        """Returns the flags as a PathFlag object."""
        return self._flags

    def original_is_dir(self) -> bool:
        """Checks if the original path is a directory or intended to be one"""
        return self._is_intended_directory(self.original_path)

    def new_is_dir(self) -> bool:
        """Checks if the new path is a directory or intended to be one"""
        return self._is_intended_directory(self.new_path)

    @property
    def new_path_stem(self) -> str:
        """Returns only the filename without its suffix."""
        return self._new_path.stem

    @property
    def original_path_name(self) -> str:
        """Returns only the filename with its suffix."""
        return self._original_path.name

    @property
    def new_path_name(self) -> str:
        """Returns only the filename with its suffix."""
        return self._new_path.name

    @property
    def original_path_stem(self) -> str:
        """Returns only the filename without its suffix."""
        return self._original_path.stem

    @property
    def resolve_new_path(self) -> Path:
        """Returns only the filename with its suffix."""
        return self.new_path.resolve()

    @property
    def resolve_original_path(self) -> Path:
        """Returns only the filename without its suffix."""
        return self.original_path.resolve()

    def add_flags(self, flags: Union[List[PathFlag | int] | PathFlag | int]):
        """Sets the flags as a PathFlag object."""
        self._flags = self._parse_flags(self._flags | flags, False)
        self._new_path = self._apply_flags(self._original_path, flags)

    def with_suffix(self, new_suffix: str) -> Path:
        """
        Changes the file's extension of the path. Does not rename actual files. Works only with files.

        :param new_suffix: The new file extension. Will add a dot if not included.
        :return: The updated path as a Path object.
        """
        if not new_suffix:
            return self.new_path
        elif not new_suffix.startswith("."):
            new_suffix = f".{new_suffix}"
        if self.new_is_dir():
            return self._new_path
        if new_suffix == self._new_path.suffix:
            return self._new_path
        else:
            self._new_path.with_suffix(new_suffix)
            self._flags |= PathFlag.CHANGED_SUFFIX
        return self._new_path

    def set_filename(self, new_filename: str) -> Path:
        """
        Either appends a filename to a directory path or changes the file's name.\n
        Does **not** affect the actual filesystem.

        :param new_filename: The new filename (with or without a suffix)
        :return: The updated path as a Path object
        """
        if self.new_is_dir():
            # If it's a directory, append the new filename
            self._new_path = self._new_path / new_filename
        elif self.new_path.name == new_filename:
            return self._new_path
        self._new_path = self._new_path.with_name(new_filename)
        if PathFlag.INCREMENT_IF_EXISTS in self._flags and self._new_path.exists():
            self._new_path = self.get_next_available_name(self._new_path)
        self._flags |= PathFlag.CHANGED_FILENAME
        return self._new_path


def rename_file_by_creation(path: Path) -> None:
    """
    Renames a file in the specified path if it exists, prefixing it with its creation timestamp.

    :param path: The directory path where the file is located.
    """
    if not path.exists():
        return
    file_name = path.name
    if os.path.exists(path):
        creation_time = os.path.getatime(path)
        dt_m = datetime.fromtimestamp(creation_time)
        formatted_time = dt_m.strftime("%Y-%m-%d %H-%M")
        new_file_name = f"[{formatted_time}] {file_name}"
        new_file_path = os.path.join(path, new_file_name)
        try:
            os.rename(path, new_file_path)
        except OSError:
            print('Rename failed')
        print('Renamed to ' + new_file_name)
