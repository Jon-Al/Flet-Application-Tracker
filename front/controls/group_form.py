from typing import Union, Dict, Optional, List

from flet import TextField, Text, Container, CupertinoSegmentedButton
from flet.core.button import Button
from flet.core.checkbox import Checkbox
from flet.core.column import Column
from flet.core.cupertino_button import CupertinoButton
from flet.core.cupertino_filled_button import CupertinoFilledButton
from flet.core.cupertino_sliding_segmented_button import CupertinoSlidingSegmentedButton
from flet.core.date_picker import DatePicker
from flet.core.dropdown import Dropdown
from flet.core.elevated_button import ElevatedButton
from flet.core.file_picker import FilePicker
from flet.core.filled_button import FilledButton
from flet.core.filled_tonal_button import FilledTonalButton
from flet.core.floating_action_button import FloatingActionButton
from flet.core.icon_button import IconButton
from flet.core.outlined_button import OutlinedButton
from flet.core.radio import Radio
from flet.core.responsive_row import ResponsiveRow
from flet.core.row import Row
from flet.core.search_bar import SearchBar
from flet.core.switch import Switch
from flet.core.text_button import TextButton
from flet.core.time_picker import TimePicker
from flet.core.types import MainAxisAlignment

from front.controls.datetime_flexible_container import DateTimeFlexibleContainer

FormFields = Union[
    TextField, DateTimeFlexibleContainer, Switch, Checkbox, Radio, SearchBar, Dropdown, FilePicker, DatePicker, TimePicker]
AnyButton = Union[
    Button, ElevatedButton, IconButton, TextButton, FloatingActionButton, FilledButton, FilledTonalButton, OutlinedButton, TextButton, CupertinoButton, CupertinoFilledButton, CupertinoSegmentedButton, CupertinoSlidingSegmentedButton]


class GroupForm:
    def __init__(self, fields: Optional[Dict[str, FormFields]] = None):
        if not fields:
            fields = {}
        self._fields: Dict[str, FormFields] = fields

    def clear_fields(self):
        for field in self._fields.values():
            field.value = ''

    def items(self):
        return self._fields.items()

    def values(self):
        return self._fields.values()

    def keys(self):
        return self._fields.keys()

    @property
    def fields(self) -> Dict[str, FormFields]:
        return self._fields

    @property
    def values(self):
        return {key: field.value for key, field in self.fields.items()}

    def __getitem__(self, index):
        return self.fields[index]

    def get_value(self, key):
        return self.fields[key].value

    def get_field(self, key):
        return self.fields[key]

    def add(self, key, field: FormFields):
        if key not in self._fields:
            self.fields[key] = field
        else:
            raise KeyError(key + " already exists")

    def update_value(self, key, field: FormFields):
        self.fields[key] = field

    def pop(self, key):
        return self.fields.pop(key, None)
