import json
from pathlib import Path
from typing import Union, Dict, Any

from utils.path_utils import PathManager, PathFlag
from core.global_handlers import LOGGER


def import_json(path: Union[str, Path]) -> Dict[Any, Any]:
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        LOGGER.log(e)
        return {}  # Return an empty dictionary if the JSON file doesn't exist
    except Exception as e:
        LOGGER.log(e)
        return {}


def save_json(data: Dict[Any, Any],
              path: Union[str, Path],
              overwrite=False,
              increment=False) -> Union[Path, bool]:
    """
    Save the extracted placeholders to a JSON file. If the path is a directory, behaves like all 3 flags are ``True``. File name will be ``untitled.json`` (or increment of it).

    If the path leads to a non-JSON file, will change the suffix to ``.json``.

    :param data: data to save
    :param path: Path to the JSON file to save.
    :param overwrite: If True, file will overwrite the existing file, if it exists. Will create the file if it doesn't. Irrelevant if ``increment`` is ``True`` (the file's name will be incremented if needed).
    :param increment: File will increment the file's name, if it exists.
    """
    if not path or not data:
        return False
    pm = PathManager(path, PathFlag.CREATE_FOLDER)
    if pm.new_is_dir():
        increment = overwrite = True
        pm.add_flags(PathFlag.I)
        pm.set_filename('untitled.json')
    if pm.new_path.suffix != '.json':
        pm.with_suffix('.json')
        overwrite = True
    if increment:
        pm.add_flags(PathFlag.I)
    if not overwrite and pm.new_exists:
        return False
    json_path = pm.resolve_new_path
    try:
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        return json_path
    except Exception as e:
        LOGGER.log(e)
        return False
