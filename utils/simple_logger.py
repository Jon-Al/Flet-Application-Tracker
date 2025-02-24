import os
import traceback
from abc import ABCMeta, abstractmethod
from datetime import datetime

from utils.path_utils import PathManager, PathFlag


class BaseLogger(metaclass=ABCMeta):
    def __init__(self, log_file_name="log.txt"):
        self.log_file = PathManager.resolve_path(f'logging/{log_file_name}', PathFlag.R | PathFlag.C)
        if not self.log_file.exists():
            self.log_file.write_text("")

    @abstractmethod
    def log(self, message):
        pass

    def _log(self, log_message):
        with open(self.log_file, "a") as log:
            log.write(log_message + "\n")


class SimpleLogger(BaseLogger):
    def log(self, message=""):
        caller = traceback.extract_stack()[-2]  # Get caller information
        file_name = os.path.basename(caller.filename)
        method_name = caller.name
        line_number = caller.lineno

        if isinstance(message, Exception):
            message = str(message)
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {file_name}, {method_name}, {line_number}, {message}"
        self._log(log_entry)


class DocumentLogger(BaseLogger):
    def log(self, doc_path=""):
        self._log(doc_path)


class LogReader:
    def __init__(self, log_file_name="log.txt"):
        path_manager = PathManager.resolve_path(f'logging/{log_file_name}', PathFlag.R | PathFlag.C)
        self.log_file = log_file_name

    def read_log(self, split_lines=True):
        with open(self.log_file, "r") as log:
            if split_lines:
                return log.readlines()
            return log.read()
