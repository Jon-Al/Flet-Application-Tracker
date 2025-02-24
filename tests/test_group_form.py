import pytest
from flet import TextField, Text, ElevatedButton, Checkbox
from flet.core.column import Column
from front.controls import GroupForm


def test_group_form_initialization():
    fields = {
        "name":      TextField(label="Name"),
        "age":       TextField(label="Age"),
        "subscribe": Checkbox(label="Subscribe"),
    }
    result_text = Text()
    action_buttons = [ElevatedButton(text="Submit")]

    form = GroupForm(fields, action_buttons, result_text)

    assert form.fields == fields
    assert form._action_buttons == action_buttons
    assert form._result_text == result_text
    assert isinstance(form.content, Column)


def test_group_form_values():
    fields = {
        "name": TextField(value="John"),
        "age":  TextField(value="30"),
    }
    form = GroupForm(fields)

    assert form.values == ["John", "30"]


def test_group_form_get_value():
    fields = {
        "name": TextField(value="Alice"),
        "age":  TextField(value="25"),
    }
    form = GroupForm(fields)

    assert form.get_value("name") == "Alice"
    assert form.get_value("age") == "25"


def test_group_form_clear_fields():
    fields = {
        "name": TextField(value="Alice"),
        "age":  TextField(value="25"),
    }
    form = GroupForm(fields)
    form.clear_fields()
    assert all(field.value == '' for field in form.fields.values())


def test_group_form_add_field():
    fields = {
        "name": TextField(label="Name"),
    }
    form = GroupForm(fields)

    new_field = TextField(label="Age")
    form.add("age", new_field)

    assert "age" in form.fields
    assert form.fields["age"] == new_field


def test_group_form_add_existing_field():
    fields = {
        "name": TextField(label="Name"),
    }
    form = GroupForm(fields)

    with pytest.raises(KeyError):
        form.add("name", TextField(label="New Name"))


def test_group_form_update_value():
    fields = {
        "name": TextField(label="Name", value="Alice"),
    }
    form = GroupForm(fields)

    new_field = TextField(label="Name", value="Bob")
    form.update_value("name", new_field)

    assert form.get_value("name") == "Bob"


def test_group_form_pop_field():
    fields = {
        "name": TextField(label="Name"),
        "age":  TextField(label="Age"),
    }
    form = GroupForm(fields)

    removed_field = form.pop("age")

    assert removed_field is not None
    assert "age" not in form.fields
