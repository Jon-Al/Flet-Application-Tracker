import pytest
from utils.enums import PlaceholderType
from core.placeholder_parsing import text_to_fields, FieldData, PlaceholderParser


@pytest.mark.parametrize("input_text, expected_output", [
    ("{{simple_text}}", ([], "simple_text", '', PlaceholderType.REQUIRED_PLACEHOLDER)),
    ("{{group1@group2@tooltip}}", (["group1", "group2"], "tooltip", '', PlaceholderType.REQUIRED_PLACEHOLDER)),
    (
            "[[|group1@tooltip|default_value]]",
            (["group1"], "tooltip", "default_value", PlaceholderType.DEFAULT_PLACEHOLDER)),
    ("[[tooltip]]", ([], "tooltip", "tooltip", PlaceholderType.DEFAULT_PLACEHOLDER))
])
def test_text_to_fields_valid(input_text, expected_output):
    assert text_to_fields(input_text) == expected_output


@pytest.mark.parametrize("invalid_text", [
    "{{invalid@", "[[|no_default|]]", "[[]]", "{{@}}"
])
def test_text_to_fields_invalid(invalid_text):
    with pytest.raises(ValueError):
        text_to_fields(invalid_text)


def test_field_data():
    field_data = FieldData("Test", PlaceholderType.DEFAULT_PLACEHOLDER, ["group1"], "Tooltip", "Default")
    expected_dict = {
        "original_text": "Test",
        "type":          PlaceholderType.DEFAULT_PLACEHOLDER,
        "groups":        ["group1"],
        "tooltip":       "Tooltip",
        "default_value": "Default"
    }
    assert field_data.dict() == expected_dict


def test_placeholder_parser():
    text = "[[tooltip]]"
    parsed_field = PlaceholderParser.parse_fields(text)

    assert parsed_field.original_text == text
    assert parsed_field.type == PlaceholderType.DEFAULT_PLACEHOLDER
    assert parsed_field.groups == []
    assert parsed_field.label == "tooltip"
    assert parsed_field.default_value == "tooltip"
