import os
from sqlite3 import DatabaseError
from typing import List, Optional, Dict, Set

import flet as ft
from flet.core.colors import Colors
from flet.core.container import Container
from flet.core.responsive_row import ResponsiveRow
from flet.core.row import Row
from flet.core.text import Text
from flet.core.text_style import TextThemeStyle
from flet.core.textfield import TextField
from flet.core.types import ScrollMode

from core.doc_manager import DocManager
from core.global_handlers import UNIVERSAL_DATABASE_HANDLER as UDH, LOGGER
from core.placeholder_parsing import FieldData, PlaceholderParser
from front.controls.create_button_methods import create_add_button, create_clear_button, create_restore_button
from front.controls.group_form import GroupForm
from front.controls.make_file_picker import create_file_picker_controls
from front.insert_form_components import create_employer_group_form
from utils.enums import PlaceholderType
from utils.path_utils import resume_or_cover_letter


class FilePickersRow(ft.Container):
    def __init__(self):
        self._resume_title_text: ft.Text
        self._resume_copy_path: ft.TextButton
        self._resume_open_picker_button: ft.ElevatedButton
        self._resume_path_field: ft.TextField
        self._resume_pick_file: ft.FilePicker
        self._cover_letter_title_text: ft.Text
        self._cover_letter_copy_path: ft.TextButton
        self._cover_letter_open_picker_button: ft.ElevatedButton
        self._cover_letter_path_field: ft.TextField
        self._cover_letter_pick_file: ft.FilePicker
        self._resume_title_text, self._resume_copy_path, self._resume_open_picker_button, self._resume_path_field, self._resume_pick_file = create_file_picker_controls(
            "Resume")
        self._cover_letter_title_text, self._cover_letter_copy_path, self._cover_letter_open_picker_button, self._cover_letter_path_field, self._cover_letter_pick_file = create_file_picker_controls(
            "Cover Letter")

        resume_column = ft.Column([
            self.resume_title_text,
            self.resume_path_field,
            ft.Row([self.resume_open_picker_button, self.resume_copy_path]),
            self.resume_pick_file
        ], expand=True)
        cover_letter_column = ft.Column([
            self.cover_letter_title_text,
            self.cover_letter_path_field,
            ft.Row([self.cover_letter_open_picker_button, self.cover_letter_copy_path]),
            self.cover_letter_pick_file
        ], expand=True)
        self._main_row = ft.Row([resume_column, cover_letter_column])
        super().__init__(expand=True, content=self._main_row)

    def add_column(self, title: str, control1: Optional[ft.Control], control2: Optional[ft.Control]):
        title = ft.Text(title, style=ft.TextThemeStyle.BODY_MEDIUM)
        if not control1:
            control1 = ft.Placeholder()
        if not control2:
            control2 = ft.Placeholder()
        self._main_row.controls.append(ft.Column([title, control1, control2], expand=True))

    @property
    def main_row(self) -> ft.Row:
        return self._main_row

    @property
    def resume_title_text(self):
        return self._resume_title_text

    @property
    def resume_copy_path(self):
        return self._resume_copy_path

    @property
    def resume_open_picker_button(self):
        return self._resume_open_picker_button

    @property
    def resume_path_field(self):
        return self._resume_path_field

    @property
    def resume_pick_file(self):
        return self._resume_pick_file

    @property
    def cover_letter_title_text(self):
        return self._cover_letter_title_text

    @property
    def cover_letter_copy_path(self):
        return self._cover_letter_copy_path

    @property
    def cover_letter_open_picker_button(self):
        return self._cover_letter_open_picker_button

    @property
    def cover_letter_path_field(self):
        return self._cover_letter_path_field

    @property
    def cover_letter_pick_file(self):
        return self._cover_letter_pick_file


def make_file_pickers():
    """
    keys: ``file_picker``, ``pick_file_button``, ``title_text``, ``path_result_text``, ``"copy_path_button":``
    :return: two instances of the above dictionary containing the two file related controls.
    """
    return FilePickersRow()


def update_docs_job_picker(docs_job_picker):
    result = UDH.execute_query(
        """
SELECT  j.jobID as id, j.job_title as title, e.employer_name as employer
FROM Jobs j
         INNER JOIN Employers e ON j.employerID = e.employerID
WHERE j.status != 'Rejected'
ORDER BY j.last_updated DESC;
        """, fetch_mode=-1
    )
    options = []
    for job in result:
        row = ft.Row([ft.Text(value=i) for i in job.values()])
        op = ft.dropdown.Option(key=job['id'], content=row)
        options.append(op)
    docs_job_picker.options = options


def get_title_and_employer(job_id: int) -> tuple[str, str]:
    db = UDH.execute_query("""
    SELECT j.job_title as 'job', e.employer_name as 'employer' 
    FROM Jobs j
    INNER JOIN Employers e
    ON j.employerID = e.employerID
    WHERE j.jobID = ?""", (job_id,), -1)
    job_title = db[0]['job']
    employer_name = db[0]['employer']
    return job_title, employer_name


def update_page(e):
    if hasattr(e, 'page'):
        e.page.update()
    elif hasattr(e, 'control'):
        e.control.update()
    e.page.update()


def make_input_field(field: FieldData):
    # TODO : change to strategy for making various interactions.
    def on_click(e):
        input_field.value = field.default_value

    restore_field_button = create_restore_button(tooltip="reset field", on_click=on_click)
    restore_field_button.padding = 0
    restore_field_button.expand = False
    input_field = TextField(
        label=field.label,
        icon=restore_field_button,
        # bgcolor=Colors.with_opacity(0.2, Colors.TERTIARY_CONTAINER),
        # focused_bgcolor=Colors.with_opacity(0.3, Colors.ON_TERTIARY_CONTAINER),
        value=field.default_value,
        multiline=True,
        min_lines=1,
        max_lines=4,
        expand=True,
        content_padding=5,
        data=field
    )
    return input_field


def create_ph_field_group(placeholders_set: Optional[Set[str]]) -> GroupForm:
    group_form: GroupForm = GroupForm()
    for ph in placeholders_set:
        field: FieldData = PlaceholderParser.parse_fields(ph)
        text_field: TextField = make_input_field(field)
        text_field.default_value = field
        group_form.add(field.original_text, text_field)
    return group_form


def create_placeholders_area(placeholders_set: Optional[Set[str]],
                             area_title: Optional[str] = None,
                             required_subarea_title: Optional[str] = None,
                             default_subarea_title: Optional[str] = None) -> List[Container | GroupForm | None]:
    """
    Takes care of sorting to default and non-default; creates fields, returns fields.
    :param placeholders_set: Unprocessed placeholders.
    :param area_title: Area's title (will appear first).
    :param required_subarea_title: Required subarea title (will appear above the required placeholders).
    :param default_subarea_title: Default subarea title (will appear above the required placeholders)
    :return: Container, GroupForm
    """
    if not placeholders_set:
        return [None, None]
    default_ungroup = {}
    default_groups = {}
    required_ungroup = {}
    required_groups = {}
    placeholder_parser = PlaceholderParser
    group_form: GroupForm = GroupForm()
    for ph in placeholders_set:
        field: FieldData = placeholder_parser.parse_fields(ph)
        text_field: TextField = make_input_field(field)
        group_form.add(field.original_text, text_field)
        if not field.groups:
            if field.type == PlaceholderType.DEFAULT_PLACEHOLDER:
                default_groups[field.label] = text_field
            if field.type == PlaceholderType.REQUIRED_PLACEHOLDER:
                required_groups[field.label] = text_field
        else:
            k = '~~'.join(field.groups) + '~~' + field.label
            if field.type == PlaceholderType.DEFAULT_PLACEHOLDER:
                default_ungroup[k] = text_field
            if field.type == PlaceholderType.REQUIRED_PLACEHOLDER:
                required_ungroup[k] = text_field

    default_ungroups_row = ResponsiveRow(
        [default_ungroup[k] for k in sorted(default_ungroup.keys())],
        spacing=5,
        run_spacing=20,
        expand=True
    )
    default_groups_row = ResponsiveRow(
        [default_groups[k] for k in sorted(default_groups.keys())],
        spacing=5,
        run_spacing=20,
        expand=True
    )
    required_ungroups_row = ResponsiveRow(
        [required_ungroup[k] for k in sorted(required_ungroup.keys())],
        spacing=5,
        run_spacing=20,
        expand=True
    )
    required_groups_row = ResponsiveRow(
        [required_groups[k] for k in sorted(required_groups.keys())],
        spacing=5,
        run_spacing=20,
        expand=True
    )

    medium_title = Text(area_title, theme_style=TextThemeStyle.TITLE_MEDIUM) if area_title else None
    small_title_1 = Text(required_subarea_title,
                         theme_style=TextThemeStyle.TITLE_SMALL) if required_subarea_title else None
    small_title_2 = Text(default_subarea_title,
                         theme_style=TextThemeStyle.TITLE_SMALL) if default_subarea_title else None
    area = Row(controls=[medium_title,
                         small_title_1,
                         required_ungroups_row,
                         required_groups_row,
                         small_title_2,
                         default_ungroups_row,
                         default_groups_row],
               expand=True, wrap=True, )
    output = Container(content=area, bgcolor=Colors.with_opacity(0.3, Colors.PRIMARY_CONTAINER))
    return [output, group_form]


def template_dashboard_window():
    column = ft.Column(expand=True, scroll=ScrollMode.AUTO)
    container = ft.Container(content=column, expand=True)
    field_groups_collector: Dict[str, GroupForm] = {}

    def apply_replacements(doc_path, replacements, job_title, employer_name, job_id, doc_type, on_complete):
        nonlocal result_label
        nonlocal container
        full_path = resume_or_cover_letter(doc_path)
        file_name = os.path.basename(doc_path)
        doc_manager = DocManager(full_path)
        if not doc_manager.callable:
            return
        doc_manager.apply_replacements(replacements)
        result_label.value = f'{result_label.value}\nApplied Replacements to {file_name}'
        new_file_name = f"{file_name.replace('.docx', '')} - {job_title} - {employer_name}.docx"
        pdf_output_path = f"{file_name.replace('.docx', '')} - {job_title}.pdf"
        # Check if there's a Document for this document.
        doc_id = UDH.execute_query(
            "SELECT documentID FROM Documents WHERE jobID = ? AND documentType = ?",
            (job_id, doc_type),
            fetch_mode=-1
        )
        if doc_id:  # all good, only ID matters.
            doc_id = doc_id[0][0]  # Extract the first column of the first row
        else:  # Insert if not.
            doc_id = UDH.execute_query(
                "INSERT INTO Documents (jobID, documentType) VALUES (?, ?)",
                (job_id, doc_type),
                True
            )
        # create new data for storage.
        new_file_path = doc_manager.save_docx(new_file_name)
        new_file_directory = os.path.dirname(new_file_path)
        # update label:
        result_label.value = f'{result_label.value}\nSaved the new file to {new_file_path}.'
        check_storage = UDH.execute_query(
            "SELECT StorageID FROM Document_Storage WHERE documentID = ?",
            (doc_id,)
        )

        # check storage, insert or update as needed
        if not check_storage:
            UDH.execute_query(
                "INSERT INTO Document_Storage (documentID, fileType, path, file_name) VALUES (?, ?, ?, ?)",
                (doc_id, 'docx', new_file_directory, file_name)
            )

        else:
            UDH.execute_query(
                """
                UPDATE Document_Storage 
                SET fileType = ?, path = ?, file_name = ?, date_created = datetime('now') 
                WHERE documentID = ?
                """, (doc_type, new_file_directory, new_file_name, doc_id))

        result_label.value = f'{result_label.value}\nDatabases updated.'
        doc_manager.save_pdf(pdf_output_path)
        json_success = doc_manager.save_placeholders_to_json()
        if json_success:
            result_label.value = f'{result_label.value}\n{json_success}.'
        else:
            result_label.value = f'{result_label.value}\nFailed to save json.'
        on_complete(new_file_name)
        for placeholder, value in replacements.items():
            # Insert variable name if it doesn't already exist
            UDH.execute_query(
                "INSERT OR IGNORE INTO Variables (variable_name) VALUES (?)",
                (placeholder.strip('{}[]'),)  # Ensure it's a single-item tuple
            )

            # Retrieve the variable ID
            variable_id_result = UDH.execute_query(
                "SELECT variableID FROM Variables WHERE variable_name = ?",
                (placeholder.strip('{}[]'),),  # Ensure it's a single-item tuple
                fetch_mode=-1
            )

            # Extract the variableID if it exists
            variable_id = variable_id_result[0][0] if variable_id_result else None

            if variable_id is None:
                # Log or handle the error if variable_id could not be retrieved
                result_label.value += f"\nError: Variable ID not found for placeholder '{placeholder}'"
                continue

            # Insert the relationship between document and variable
            UDH.execute_query(
                "INSERT OR IGNORE INTO Document_Variables (documentID, variableID, placeholder_name) VALUES (?, ?, ?)",
                (doc_id, variable_id, placeholder.strip('{}[]'))
            )

    def load_employers():
        nonlocal employers
        employers_from_db = UDH.execute_query(
            "SELECT employerID as id, employer_name as name FROM Employers ORDER BY employerID DESC", fetch_mode=-1)
        new_employers = []

        for employer in employers_from_db:
            e = tuple([employer['id'], employer['name'], ])
            if e not in underlying_employers_set:
                new_employers.append(e)
        for e in new_employers:
            underlying_employers_set.add(e)
        employers = employers_from_db

    def add_employer(e):
        nonlocal result_label
        text = f"""{e.control}, 

"""
        result_label.text = e.control
        result_label.text = e.control
        result_label.text = e.control
        result_label.text = e.control
        if not employer_name_field or employer_name_field.value == '' or employer_name_field.value is None:
            add_employer_result_label.value = "Please insert the employer name."
            update_page(e)
            return
        try:
            new_employer_id = UDH.execute_query(
                "INSERT INTO Employers (employer_name, location, notes) VALUES (?, ?, ?)",
                (employer_name_field.value.strip(), employer_location_field.value.strip(),
                 employer_notes_field.value.strip()), True)
            update_page(e)
        except DatabaseError as err:
            add_employer_result_label.value = f"Failed to add employer.\n Error: {err}"
            update_page(e)
            return
        nonlocal employer_dropdown
        clear_employer_fields()
        update_employer_dropdown()
        add_employer_result_label.value = f"Employer added successfully. ID: {new_employer_id}"
        employer_dropdown.value = new_employer_id
        update_page(e)

    def add_job(e):
        selected_employer_id = employer_dropdown.value
        if not selected_employer_id:
            add_job_result_label.value = "Please select an employer."
            update_page(e)
            return
        new_id = UDH.execute_query(
            "INSERT INTO Jobs (job_title, employerID, location, URL, status, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (job_title_field.value.strip(),
             selected_employer_id.strip(),
             job_location_field.value.strip(),
             job_url_field.value.strip(),
             job_status_field.value.strip(),
             job_notes_field.value.strip()),
            True)
        title, employer = get_title_and_employer(new_id)
        add_job_result_label.value = (f"Job added successfully!\nJob ID: {new_id}\n"
                                      f"Title: {title}\n"
                                      f"Employer: {employer}\n")
        nonlocal docs_job_picker
        update_docs_job_picker(docs_job_picker)
        docs_job_picker.value = new_id
        update_page(e)

    def fetch_placeholders(e):
        def add_placeholder_area(title: str, placeholders_, width=None):
            """
            Adds placeholder areas grouped by default and required placeholders.
            :param title: The title of the placeholder area.
            :param placeholders_: The list of placeholders.
            :param width: The width of the placeholder area.
            """

            field_group = create_ph_field_group(placeholders_)
            default_row = ft.ResponsiveRow(
                spacing=5,
                run_spacing=20,
            )
            required_row = ft.ResponsiveRow(
                spacing=5,
                run_spacing=20,
            )

            placeholders_list.controls.append(Text(title, theme_style=TextThemeStyle.TITLE_MEDIUM))
            for ph in placeholders_:
                field = PlaceholderParser.parse_fields(ph)
                text_field = ft.TextField(
                    label=field.label,
                    value=field.default_value,
                    multiline=True,  # Allow multiline input
                    min_lines=2,
                    max_lines=2,
                    col=2,
                    data=field)

                if field.type == PlaceholderType.DEFAULT_PLACEHOLDER:
                    default_row.controls.append(text_field)
                elif field.type == PlaceholderType.REQUIRED_PLACEHOLDER:
                    required_row.controls.append(text_field)

            # Add grouped rows to the placeholder list
            if default_row.controls:
                placeholders_list.controls.append(ft.Text("Default Placeholders:", size=14, weight=ft.FontWeight.BOLD))
                placeholders_list.controls.append(default_row)
            if required_row.controls:
                placeholders_list.controls.append(ft.Text("Required Placeholders:", size=14, weight=ft.FontWeight.BOLD))
                placeholders_list.controls.append(required_row)

        nonlocal placeholders

        if template1_name_field.value:
            doc_manager1 = DocManager(template1_name_field.value)
            placeholders1 = doc_manager1.get_placeholders()
        else:
            placeholders1 = {}
        if template2_name_field.value:
            doc_manager2 = DocManager(template2_name_field.value)
            placeholders2 = doc_manager2.get_placeholders()
        else:
            placeholders2 = {}
        if placeholders1 and placeholders2:
            common_placeholders = set(placeholders1.keys()) & set(placeholders2.keys())
            unique_placeholders1 = set(placeholders1.keys()) - common_placeholders
            unique_placeholders2 = set(placeholders2.keys()) - common_placeholders
            placeholders_list.controls.clear()
            add_placeholder_area('Common Placeholders', common_placeholders)
            add_placeholder_area('Resume Placeholders', unique_placeholders1)
            add_placeholder_area('Cover Letter Placeholders', unique_placeholders2)
        elif placeholders1:
            placeholders_list.controls.clear()
            add_placeholder_area('Placeholders', set(placeholders1.keys()))
        elif placeholders2:
            placeholders_list.controls.clear()
            add_placeholder_area('Placeholders', set(placeholders2.keys()))
        result_label.value = ""
        update_page(e)


    def apply_replacements_and_generate(e):
        def get_replacements():
            candidates = placeholders_list.controls
            while len(candidates) > 0:
                control_candidate = candidates.pop(0)
                if isinstance(control_candidate, ft.TextField):
                    replacements[
                        control_candidate.label] = control_candidate.value  # FIXME - change to the correct placeholder name; label is now changed
                elif hasattr(control_candidate, 'controls') and len(control_candidate.controls) > 0:
                    candidates.extend(control_candidate.controls)

        def on_complete(doc_name):
            generate_button.disabled = False
            result_label.value = f"{result_label.value}\nConversion complete. Output: {str(doc_name)}.\n"
            nonlocal sound
            sound.play()
            update_page(e)

        replacements = {}
        get_replacements()

        job_id = docs_job_picker.value

        if not job_id:
            result_label.value = "Please select a job to associate the documents with."
            update_page(e)
            return

        job_title, employer_name = UDH.execute_query("""SELECT j.job_title as title, e.employer_name as employer
        FROM Jobs j
                 INNER JOIN Employers e ON j.employerID = e.employerID
         WHERE  j.jobID = ?""", (job_id,), fetch_mode=-1)[0]

        for i in '{}[]':
            job_title = job_title.replace(i, '')
            employer_name = employer_name.replace(i, '')

        if not job_title:
            try:
                UDH.execute_query("""
                SELECT             
                """)
            except Exception as e:
                LOGGER.log(e)
                job_title = 'dummy_job_title'
        if not employer_name:
            employer_name = 'dummy_employer_name'
        result_label.value = "Generating documents..."
        result_label.update()
        try:
            generate_button.disabled = True
            if template1_name_field.value:
                apply_replacements(template1_name_field.value,
                                   replacements.copy(),
                                   job_title,
                                   employer_name,
                                   job_id,
                                   'resume',
                                   on_complete)
            if template2_name_field.value:
                apply_replacements(template2_name_field.value,
                                   replacements.copy(),
                                   job_title, employer_name,
                                   job_id,
                                   'cover_letter',
                                   on_complete)
        except Exception as ee:
            result_label.value = f"Failed to generate documents.\nError: {ee}"
            update_page(e)
        finally:
            generate_button.disabled = False
            update_page(e)

    def clear_employer_fields(e=None):
        employer_name_field.value = ""
        employer_location_field.value = "Toronto, ON"
        employer_notes_field.value = ""
        update_page(e)

    def autofill_placeholders_from_dropdown(e):
        job_id = docs_job_picker.value
        if not job_id:
            result_label.value = "Please select a job first."
            update_page(e)
            return
        job_title, employer_name = get_title_and_employer(int(job_id))
        # Auto-fill placeholders only if the field is empty
        for control in placeholders_list.controls:
            if isinstance(control, ft.TextField):
                if not control.value.strip():  # Only fill empty fields
                    if "position" in control.label.lower() or "job" in control.label.lower():
                        control.value = job_title
                        control.update()
                    elif "employer" in control.label.lower():
                        control.value = employer_name
                        control.update()
            elif hasattr(control, 'controls') and len(control.controls) > 0:
                for sub_control in control.controls:
                    if isinstance(sub_control, ft.TextField) and not sub_control.value.strip():
                        if "position" in sub_control.label.lower() or "job" in sub_control.label.lower():
                            sub_control.value = job_title
                        elif "employer" in sub_control.label.lower():
                            sub_control.value = employer_name

        result_label.value = "Placeholders auto-filled for empty fields."
        update_page(e)

    def clear_job_fields(e):
        job_title_field.value = ""
        job_location_field.value = "Toronto, ON"
        job_url_field.value = ""
        job_status_field.value = "Applied"
        job_notes_field.value = ""
        update_page(e)

    def update_employer_dropdown():
        load_employers()
        employer_dropdown.options = [
            ft.dropdown.Option(key=str(employer['id']), text=employer['name']) for employer in employers
        ]

    placeholders = {}
    underlying_employers_set = set()
    employers = []
    add_job_result_label = ft.Text(expand=True)
    add_employer_result_label = ft.Text(expand=True)

    # Employer Input Fields

    employer_group_form = create_employer_group_form()

    employer_name_field = employer_group_form['employer_name']
    employer_location_field = employer_group_form['location']
    employer_notes_field = employer_group_form['notes']
    employer_industry_field = employer_group_form['industry']

    # Job Input Fields
    # Row 1
    job_title_field = ft.TextField(label="Job Title", expand_loose=True, col=3, )
    job_location_field = ft.TextField(label="Location", expand_loose=True, col=3)
    job_location_field.value = 'Toronto, ON'
    job_status_field = ft.TextField(label="Status", col=1)
    job_notes_field = ft.TextField(label="Notes", multiline=True,
                                   max_lines=6, expand=True
                                   )
    job_status_field.value = 'Applied'
    # row 2
    job_url_field = ft.TextField(label="Job URL", expand_loose=True)
    # Dropdown for Employer Selection
    employer_dropdown = ft.Dropdown(label="Select Employer", options=[], expand_loose=True)

    # Document Placeholder Fields
    file_pickers = FilePickersRow()
    template1_name_field = file_pickers.resume_path_field
    template2_name_field = file_pickers.cover_letter_path_field
    placeholders_list = ft.Row(wrap=True)

    # BUTTONS
    # Buttons and Result Label
    add_employer_button = create_add_button(tooltip="Add Employer", on_click=add_employer)
    add_job_button = create_add_button(tooltip="Add Job", on_click=add_job)
    clear_employer_button = create_clear_button(tooltip='Clear Employer', on_click=clear_employer_fields)
    clear_job_button = create_clear_button(tooltip='Clear Employer', on_click=clear_job_fields)
    auto_fill_button = ft.ElevatedButton(
        text="Auto-Fill Placeholders",
        on_click=autofill_placeholders_from_dropdown,
    )

    fetch_placeholders_button = ft.ElevatedButton("Get Placeholders", on_click=fetch_placeholders)
    generate_button = ft.ElevatedButton("Generate Documents", on_click=apply_replacements_and_generate)
    result_label = ft.Text()

    job_section = ft.Column(controls=[
        ft.Text("Add Job", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([  # ROW 1
            job_title_field,
            job_location_field,
            job_status_field,
        ], spacing=5, expand=True),
        ft.Row([  # ROW 2
            employer_dropdown,
            job_url_field,
        ], spacing=5, expand=True, alignment=ft.MainAxisAlignment.START),
        ft.Row([  # ROW 2
            job_notes_field
        ], spacing=5, expand=True, alignment=ft.MainAxisAlignment.START),
        ft.Row([  # Results Row
            add_job_button,
            clear_job_button,
            add_job_result_label
        ], spacing=5, expand=True, alignment=ft.MainAxisAlignment.START),


    ], expand=True, spacing=5)

    employer_section = ft.Column(
        controls=[
            ft.Text("Add Employer", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([  # ROW 1
                employer_name_field,
                employer_location_field,
                employer_industry_field
            ], spacing=5, expand_loose=True),
            ft.Row([  # ROW 2
                employer_notes_field,
            ], spacing=5, expand_loose=True),

            ft.Row([  # Results Row
                add_employer_button,
                clear_employer_button,
                add_employer_result_label,
            ], spacing=5, expand_loose=True),
        ], spacing=5, expand=True)
    docs_job_picker = ft.Dropdown(label="Select Job",
                                  options=[],
                                  on_change=autofill_placeholders_from_dropdown,
                                  # options_fill_horizontally=True,
                                  # expand_loose=False,
                                  expand=True
                                  )
    file_pickers.add_column('Pick Job', docs_job_picker, generate_button)

    document_section = ft.Column(controls=[
        ft.Text("Document Placeholders and Replacement", style=ft.TextThemeStyle.TITLE_LARGE),
        ft.Row([  # ROW 1
            file_pickers],
            spacing=5, expand=True
        ),
        ft.Row([
            fetch_placeholders_button,
            auto_fill_button,
            generate_button,
        ],
            spacing=5, expand=True),
        ft.Container(placeholders_list, expand_loose=True,
                     bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.PRIMARY_CONTAINER), ),
    ], spacing=5, expand=True)

    column.controls.extend([
        employer_section, ft.Divider(),
        job_section, ft.Divider(),
        document_section, ft.Divider(),
        result_label]
    )

    sound = ft.Audio(src="tada.wav")
    column.controls.append(sound)
    update_docs_job_picker(docs_job_picker)
    update_employer_dropdown()
    return container
