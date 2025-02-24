from flet import (
    FilePickerResultEvent,
)
from flet.core.colors import Colors
from flet.core.elevated_button import ElevatedButton
from flet.core.file_picker import FilePicker
from flet.core.icons import Icons
from flet.core.text import Text
from flet.core.text_button import TextButton
from flet.core.text_style import TextThemeStyle
from flet.core.textfield import TextField

from utils.json_import_export import import_json, save_json
from utils.path_utils import PathManager, PathFlag


def create_file_picker_controls(picker_name: str) -> tuple[Text, TextButton, ElevatedButton, TextField, FilePicker]:
    """
    keys: ``file_picker``, ``pick_file_button``, ``title_text``, ``path_result_text``, ``"copy_path_button":``

    :param picker_name: The picker's name, will also be used for keeping the last used file.
    :return: A dictionary containing the file picker, button, and related UI elements.
    """

    def on_path_tap(e):
        if path_string:
            e.control.page.set_clipboard(path_string)

    def pick_files_result(e: FilePickerResultEvent):
        nonlocal path_string
        if e.files:
            path_string = e.files[0].path  # Store the last selected file
            doc_data[picker_name] = path_string  # Update stored path
            p = save_json(doc_data, PathManager.resolve_path('data/documents.json', PathFlag.R), overwrite=True)
        path_field.value = path_string
        path_field.update()

    doc_data = import_json(PathManager.resolve_path('data/documents.json', PathFlag.R))
    path_string = doc_data.get(picker_name, "")
    pick_file = FilePicker(on_result=pick_files_result)
    path_field = TextField(value=path_string, tooltip='Input or Pick File')
    title = Text(picker_name, style=TextThemeStyle.BODY_MEDIUM)

    open_picker_button = ElevatedButton(
        "Pick files",
        icon=Icons.FILE_OPEN,
        on_click=lambda _: pick_file.pick_files(allow_multiple=False),
    )
    copy_path = TextButton(
        icon=Icons.COPY,
        text="Copy Path",
        icon_color=Colors.PRIMARY,
        on_click=on_path_tap,
    )

    return title, copy_path, open_picker_button, path_field, pick_file
