import re
from dataclasses import dataclass
from typing import List, Tuple

from utils.enums import PlaceholderType


def text_to_fields(text: str) -> Tuple[List[str], str, str, PlaceholderType]:
    """
    Parses a placeholder text and extracts its components.

    :param text: The placeholder string.
    :return: Tuple containing groups, tooltip, default value, and type.
    """
    if text is None or not isinstance(text, str):
        raise TypeError('text cannot be None')

    t = text.strip()

    if t.startswith('{{') and t.endswith('}}'):
        inner_text = t[2:-2].strip()
        if not inner_text or inner_text == "@":
            raise ValueError("Invalid required placeholder format")

        parts = inner_text.split('@')
        if len(parts) == 1:
            return [], parts[0], '', PlaceholderType.REQUIRED_PLACEHOLDER
        return parts[:-1], parts[-1], '', PlaceholderType.REQUIRED_PLACEHOLDER

    elif t.startswith('[[') and t.endswith(']]'):
        inner_text = t[2:-2].strip()

        if not inner_text:
            raise ValueError("Invalid default placeholder format")

        pattern = re.compile(r'^\|\s*([^|]*)\s*\|\s*([^\[\]]+)\s*$')

        if '|' in inner_text:
            match = pattern.match(inner_text)
            if not match:
                raise ValueError("Invalid default placeholder format")

            groups_part, default_value = match.groups()
            groups = groups_part.split('@') if groups_part else []
            tooltip = groups[-1] if groups else ''
            return groups[:-1] if groups else [], tooltip, default_value, PlaceholderType.DEFAULT_PLACEHOLDER

        return [], inner_text, inner_text, PlaceholderType.DEFAULT_PLACEHOLDER

    raise ValueError("Invalid placeholder format")


@dataclass
class FieldData:
    original_text: str
    type: PlaceholderType
    groups: List[str]
    label: str
    default_value: str = ''

    def dict(self):
        return {
            'original_text': self.original_text,
            'type':          self.type,
            'groups':        self.groups,
            'label':         self.label,
            'default_value': self.default_value
        }

    def __eq__(self, other):
        return self.original_text == other.original_text

    def __ne__(self, other):
        return self.original_text != other.original_text

    def __lt__(self, other):
        return self.original_text < other.original_text

    def __gt__(self, other):
        return self.original_text > other.original_text

    def __le__(self, other):
        return self.original_text <= other.original_text

    def __ge__(self, other):
        return self.original_text >= other.original_text

    def __bool__(self):
        return bool(self.original_text)

    def __hash__(self):
        return hash(self.original_text)


class PlaceholderParser:
    @staticmethod
    def parse_fields(placeholder_text) -> FieldData:
        groups, tooltip, default_value, placeholder_type = text_to_fields(placeholder_text)
        return FieldData(placeholder_text,
                         PlaceholderType.DEFAULT_PLACEHOLDER,
                         groups,
                         tooltip,
                         default_value
                         )
