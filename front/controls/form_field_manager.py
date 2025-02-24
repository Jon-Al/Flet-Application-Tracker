from datetime import datetime
from typing import Union, Optional, Dict, Any
from dateutil.parser import parse as date_parse
from flet import TextField
from flet.core.checkbox import Checkbox
from flet.core.date_picker import DatePicker
from flet.core.dropdown import Dropdown
from flet.core.radio import Radio
from flet.core.search_bar import SearchBar
from flet.core.switch import Switch
from flet.core.time_picker import TimePicker

from core.placeholder_parsing import FieldData

FormFields = Union[
    TextField, Switch, Checkbox,
    Radio, SearchBar, Dropdown, DatePicker, TimePicker
]


class FormFieldManager:
    def __init__(self, fields: Optional[Dict[str, FormFields]] = None):
        """
        Initialize the form field manager with optional fields

        Args:
            fields: Single field or list of fields to manage
        """
        self._fields: Dict[str, FormFields] = {}

        if fields:
            if isinstance(fields, dict):
                self._fields.update(fields)

        # Set default values during initialization
        self._set_default_values()

    @property
    def fields(self) -> Dict[str, FormFields]:
        return self._fields

    def add_field(self, key: str, field: FormFields) -> None:
        """Add a field to the manager"""
        self._fields[key] = field

    def get_field(self, name: str) -> Optional[FormFields]:
        """Get a field by name"""
        return self._fields.get(name, None)

    def clear_field(self, name: str) -> bool:
        """Clear the value of a specific field"""
        field = self.get_field(name)
        if field:
            if hasattr(field, 'value'):
                field.value = ""
                return True
        return False

    def clear_all(self) -> None:
        """Clear all field values intelligently based on type."""
        for field in self._fields.values():
            if isinstance(field, TimePicker):
                field.value = datetime.now().time()
            elif isinstance(field, DatePicker):
                if isinstance(field.data, FieldData):
                    default_value = str(field.data.default_value).lower()
                    if default_value == 'today':
                        field.value = datetime.today().date()
                    else:
                        try:
                            parsed_date = date_parse(field.data.default_value, fuzzy=True).date()
                            field.value = parsed_date
                        except (ValueError, TypeError):
                            field.value = None
                else:
                    field.value = None
            elif hasattr(field, 'value') and isinstance(field.data, FieldData):
                field.value = field.data.default_value

    def set_value(self, name: str, value) -> bool:
        """Set the value of a specific field"""
        if value is None or value == "":
            return self.clear_field(name)
        field = self.get_field(name)
        if field:
            if hasattr(field, 'value'):
                field.value = value
                return True
        return False

    def get_value(self, name: str) -> Optional[str]:
        """Get the value of a specific field"""
        field = self.get_field(name)
        if field:
            return getattr(field, 'value', None)
        return None

    def get_all_data(self) -> Dict[str, Any]:
        """
        Get a dictionary containing ``original_text`` and current value from each control
        Returns:
            Dict with field names as keys and dict of ``original_text`` and value as values
        """
        result = {}
        for name, field in self._fields.items():
            result[name] = getattr(field, 'value', '')
        return result

    def _set_default_values(self) -> None:
        """Set default values for fields if they exist"""
        for field in self._fields.values():
            if isinstance(field.data, FieldData):
                field.value = field.data.default_value

    def fill_if_tooltip(self, tooltip: str, fill_value: str) -> None:
        for field in self._fields.values():
            if isinstance(field.data, FieldData):
                d = field.data
                if d.tooltip == tooltip:
                    field.value = fill_value

    def __len__(self) -> int:
        """Return the number of fields"""
        return len(self._fields)

    def __iter__(self):
        """Make the manager iterable"""
        return iter(self._fields.values())

    def __getitem__(self, name: str) -> FormFields:
        """Allow dictionary-style access to fields"""
        return self._fields[name]
