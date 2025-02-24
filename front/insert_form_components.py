from datetime import datetime
from typing import Optional, Callable, Set, List

from flet import (
    Text, TextField, Dropdown, Checkbox
)
from flet.core.colors import Colors
from flet.core.container import Container
from flet.core.dropdown import Option
from flet.core.responsive_row import ResponsiveRow
from flet.core.row import Row
from flet.core.text_style import TextThemeStyle

from core.database_interaction_methods import insert_employers, insert_jobs
from core.placeholder_parsing import PlaceholderParser, FieldData
from front.controls.create_button_methods import create_add_button, create_clear_button, create_restore_button
from front.controls.group_form import GroupForm
from utils.database_handler import DatabaseHandler
from utils.enums import PlaceholderType


def column_sizes(size_ratio: int):
    """
    Returns predefined column sizes for different screen breakpoints based on size_ratio.

    :param size_ratio: The relative importance of a field (1-12).
    :return: A dictionary mapping breakpoints to column sizes.
    """
    size_mapping = {
        1:  {"xs": 12, "sm": 6, "md": 4, "lg": 2, "xl": 1, "xxl": 1},
        2:  {"xs": 12, "sm": 6, "md": 4, "lg": 4, "xl": 3, "xxl": 2},
        3:  {"xs": 12, "sm": 6, "md": 6, "lg": 4, "xl": 3, "xxl": 2},
        4:  {"xs": 12, "sm": 6, "md": 6, "lg": 6, "xl": 4, "xxl": 3},
        5:  {"xs": 12, "sm": 6, "md": 6, "lg": 6, "xl": 5, "xxl": 4},
        6:  {"xs": 12, "sm": 6, "md": 6, "lg": 6, "xl": 6, "xxl": 5},
        7:  {"xs": 12, "sm": 6, "md": 8, "lg": 6, "xl": 6, "xxl": 6},
        8:  {"xs": 12, "sm": 6, "md": 8, "lg": 8, "xl": 6, "xxl": 6},
        9:  {"xs": 12, "sm": 12, "md": 9, "lg": 8, "xl": 7, "xxl": 6},
        10: {"xs": 12, "sm": 12, "md": 10, "lg": 9, "xl": 8, "xxl": 7},
        11: {"xs": 12, "sm": 12, "md": 11, "lg": 10, "xl": 9, "xxl": 8},
        12: {"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 10, "xxl": 9},
    }

    return size_mapping.get(size_ratio, size_mapping[6])  # Default to size 6 if out of range


def create_employer_group_form(call_after_insert: Optional[Callable] = None,
                               call_after_clear: Optional[Callable] = None) -> GroupForm:
    def insert(e):
        nonlocal gf
        data = gf.values
        if 'employer_name' not in data.keys():
            return False
        insert_employers(
            data['employer_name'] if 'employer_name' in data.keys else '',
            data['industry'] if 'industry' in data.keys else '',
            data['location'] if 'location' in data.keys else '',
            data['notes'] if 'notes' in data.keys else '')
        call_after_insert() if call_after_insert else None

    def clear(e):
        nonlocal gf
        gf.clear_fields()
        nonlocal result_text
        result_text.value = ''
        call_after_clear() if call_after_clear else None

    # Form fields
    employer_name_field = TextField(
        label="Employer Name*",
        hint_text="Enter employer name",
        col=column_sizes(4), expand=True,
    )
    industry_field = TextField(
        label="Industry",
        hint_text="Enter industry",
        col=column_sizes(4), expand=True,
    )
    location_field = TextField(
        label="Location",
        hint_text="City, Province/State",
        col=column_sizes(4),
        expand=True,
    )
    notes_field = TextField(
        label="Notes",
        tooltip="Additional notes about employer",
        multiline=True,
        min_lines=1,
        max_lines=6,
        expand=True,
        col=column_sizes(12)
    )
    result_text = Text(value='')
    add_button = create_add_button(insert)

    clear_button = create_clear_button(clear)

    gf = GroupForm({'employer_name': employer_name_field,
                    'industry':      industry_field,
                    'location':      location_field,
                    'notes':         notes_field
                    }
                   )
    return gf


def job_form(call_after_insert: Optional[Callable] = None,
             call_after_clear: Optional[Callable] = None):
    def update_employer_dropdown(dropdown: Dropdown, db: DatabaseHandler):
        """
        Updates the given employer dropdown with the latest employers from the database.

        :param dropdown: The Dropdown control to update.
        :param db: DatabaseHandler instance for querying the database.
        """
        employers = db.execute_query(
            "SELECT employerID, employer_name FROM Employers ORDER BY employerID DESC", fetch_mode=True
        )

        dropdown.options = [
            Option(key=str(employer[0]), text=employer[1]) for employer in employers
        ]

    def insert(e):
        nonlocal gf
        data = gf.values
        if 'job_title' not in data.keys() or 'employer_id' not in data.keys():
            return False
        insert_jobs(
            data.get('job_title', ''),  # Default: empty string if missing
            data.get('employer_id', ''),  # Default: empty string
            data.get('location', 'Toronto, ON'),  # Default: Toronto, ON
            data.get('url', ''),  # Default: empty string
            data.get('status', 'applied'),  # Default: applied
            data.get('annual_pay'),  # Default: None
            data.get('ft_pt', 'Full Time'),  # Default: Full Time
            data.get('job_type', 'Permanent'),  # Default: Permanent
            data.get('work_model', 'In Person'),  # Default: In Person
            datetime.now(),  # Always set to now
            data.get('date_applied'),  # Default: None
            data.get('job_text', ''),  # Default: empty string
            data.get('notes', ''),  # Default: empty string
            data.get('archived', False)  # Default: False
        )
        call_after_insert() if call_after_insert else None

    def clear(e):
        nonlocal gf
        gf.clear_fields()
        nonlocal result_text
        result_text.value = ''
        call_after_clear() if call_after_clear else None

    job_title_field = TextField(
        label="Job Title*",
        hint_text="Enter job title",
        col=column_sizes(4)
    )
    employer_id_field = Dropdown(
        label="Employer",
        hint_text="Pick employer",
        col=column_sizes(4)
    )
    update_employer_dropdown(employer_id_field, DatabaseHandler('data/applications.sqlite'))
    location_field = TextField(
        label="Location",
        hint_text="City, Province/State",
        col=column_sizes(4)
    )
    url_field = TextField(
        label="Job Posting URL",
        hint_text="Enter job URL",
        col=column_sizes(4)
    )
    status_field = Dropdown(
        label="Status",
        options=[Option('applied'),
                 Option('interview'),
                 Option('offer'),
                 Option('rejected'),
                 ],
        col=column_sizes(4)
    )
    annual_pay_field = TextField(
        label="Annual Pay",
        hint_text="Enter annual salary",
        col=column_sizes(4)
    )
    ft_pt_field = Dropdown(
        label="Full-Time/Part-Time",
        options=[Option('Full Time'), Option('Part Time')],
        col=column_sizes(4)
    )
    job_type_field = Dropdown(
        label="Job Type",
        options=[Option('Permanent'), Option('Contract'), Option('Freelance'),
                 Option('Temporary')],
        col=column_sizes(4)
    )
    work_model_field = Dropdown(
        label="Work Model",
        options=[Option('In Person'), Option('Remote'), Option('Hybrid')],
        col=column_sizes(4)
    )
    date_applied_field = TextField(
        label="Date Applied",
        hint_text="yyyy-mm-dd",
        multiline=False,
        col=column_sizes(4)
    )
    job_text_field = TextField(
        label="Job Description",
        hint_text="Enter job description",
        multiline=True,
        min_lines=3,
        max_lines=6,
        col=column_sizes(6)
    )
    notes_field = TextField(
        label="Notes",
        hint_text="Additional notes",
        multiline=True,
        min_lines=3,
        max_lines=6,
        col=column_sizes(6)
    )
    archived_field = Checkbox(
        label="Archived",
        col=column_sizes(1)
    )

    result_text = Text(value='')
    add_button = create_add_button('Add', on_click=insert)
    add_button.col = column_sizes(1)
    clear_button = create_clear_button('Clear', on_click=clear)
    clear_button.col = column_sizes(1)

    gf = GroupForm({'job_title':    job_title_field,
                    'employer_id':  employer_id_field,
                    'location':     location_field,
                    'url':          url_field,
                    'status':       status_field,
                    'annual_pay':   annual_pay_field,
                    'ft_pt':        ft_pt_field,
                    'job_type':     job_type_field,
                    'work_model':   work_model_field,
                    'date_applied': date_applied_field,
                    'job_text':     job_text_field,
                    'notes':        notes_field,
                    'archived':     archived_field
                    },
                   action_buttons=[add_button, clear_button],
                   result_text=result_text
                   )

    return gf


#
#
# def menu(page: Page):
#     page.add(employer_group_form())
#     page.add(job_form())
