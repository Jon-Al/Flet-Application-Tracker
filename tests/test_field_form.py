from datetime import datetime, time

import pytest
from flet import TextField, Switch, Dropdown
from flet.core.checkbox import Checkbox
from flet.core.date_picker import DatePicker
from flet.core.radio import Radio
from flet.core.search_bar import SearchBar
from flet.core.time_picker import TimePicker

from core.placeholder_parsing import FieldData
from front.controls.datetime_flexible_container import DateTimeFlexibleContainer
from front.controls.form_field_manager import FormFieldManager


@pytest.fixture
def sample_fields():
    return {
        "text1":     TextField(value="text1"),
        "dropdown1": Dropdown(value="dropdown1"),
        "radio1":    Radio(value="radio1"),
        "search1":   SearchBar(value="search1"),
        "switch1":   Switch(value=True),
        "checkbox1": Checkbox(value=False),
        "date1":     DatePicker(value=datetime(2020, 1, 1).date()),
        "time1":     TimePicker()
    }


@pytest.fixture
def form_manager(sample_fields):
    return FormFieldManager(sample_fields)


def test_add_field():
    manager = FormFieldManager()
    text_field = TextField(value="Hello")
    manager.add_field("new_text", text_field)
    assert len(manager) == 1
    assert manager.get_field("new_text") is text_field


def test_get_field(form_manager):
    assert form_manager.get_field("text1") is not None
    assert form_manager.get_field("non_existent") is None


def test_clear_field(form_manager):
    assert form_manager.clear_field("text1") is True
    assert form_manager.get_value("text1") == ""


def test_clear_all(form_manager, sample_fields):
    form_manager.clear_all()
    for key, field in form_manager.fields.items():
        if key in ["text1", "dropdown1", "radio1", "search1"]:
            assert sample_fields[key].value == field.value
        elif key == "checkbox1":
            assert sample_fields[key].value == False
        elif key == "radio1":
            assert sample_fields[key].value == True
        elif key == "date1":
            assert sample_fields[key].value in [datetime(2020, 1, 1).date(), None]
        elif key == "time1":
            assert isinstance(sample_fields[key].value, time)


def test_set_value(form_manager):
    assert form_manager.set_value("text1", "New Value") is True
    assert form_manager.get_value("text1") == "New Value"
    assert form_manager.set_value("non_existent", "Value") is False


def test_set_value_none(form_manager):
    assert form_manager.set_value("text1", None) is True
    assert form_manager.get_value("text1") == ""


def test_get_value(form_manager):
    assert form_manager.get_value("text1") == "text1"
    assert form_manager.get_value("non_existent") is None


def test_get_all_data(form_manager):
    data = form_manager.get_all_data()
    v = {"text1":     "text1",
         "dropdown1": "dropdown1",
         "radio1":    "radio1",
         "search1":   "search1",
         "switch1":   True,
         "checkbox1": False}
    for key in v.keys():
        assert data[key] == v[key]


def test_default_values():
    field_data = FieldData(original_text="placeholder", label="Test Tooltip", default_value="Default Value",
                           type=None, groups=[])
    text_field = TextField(value="", data=field_data)
    manager = FormFieldManager({"default_text": text_field})
    assert manager.get_value("default_text") == "Default Value"


def test_fill_if_tooltip():
    field_data = FieldData(original_text="placeholder", label="Target Tooltip", default_value="", type=None,
                           groups=[])
    text_field = TextField(value="", data=field_data)
    manager = FormFieldManager({"field1": text_field})

    manager.fill_if_tooltip("Target Tooltip", "Filled Value")
    assert manager.get_value("field1") == "Filled Value"


def test_len(form_manager, sample_fields):
    assert len(form_manager) == len(sample_fields)  # Should match the number of fields


def test_iteration(form_manager, sample_fields):
    fields = list(form_manager)
    assert len(fields) == len(sample_fields)
    assert all(isinstance(field, (TextField, Switch, Dropdown, Checkbox, DatePicker,
                                  Radio, SearchBar, TimePicker, DateTimeFlexibleContainer)) for field in fields)


def test_getitem(form_manager, sample_fields):
    assert form_manager["text1"].value == sample_fields["text1"].value
    with pytest.raises(KeyError):
        form_manager["non_existent"]
