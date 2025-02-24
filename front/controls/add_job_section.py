import flet as ft
from flet.core.container import Container

from core.shared_database_handler import UNIVERSAL_DATABASE_HANDLER as UDH


class JobSection(Container):
    def __init__(self):
        super().__init__()
        self.employers_list = []  # employers
        self._employers_set = set()  # underlying_employers_set
        # Job Input Fields
        # Row 1
        job_title_field = ft.TextField(label="Job Title", expand_loose=True, col=3, )
        job_location_field = ft.TextField(label="Location", expand_loose=True, col=3)
        job_location_field.value = 'Toronto, ON'
        job_status_field = ft.TextField(label="Status", col=3)
        job_notes_field = ft.TextField(label="Notes", multiline=True,
                                       max_lines=6, expand=True
                                       )
        job_status_field.value = 'Applied'
        # row 2
        job_url_field = ft.TextField(label="Job URL", expand_loose=True)
        # Dropdown for Employer Selection
        employer_dropdown = ft.Dropdown(label="Select Employer", options=[], expand_loose=True)


    def load_employers(self):
        employers_from_db = UDH.execute_query(
            "SELECT employerID, employer_name FROM Employers ORDER BY employerID DESC", fetch_mode=True)
        new_employers = []
        for employer in employers_from_db:
            if employer[0] not in self._employers_set:
                new_employers.append(employer)
                self._employers_set.add(employer[0])
        self.employers_list = employers_from_db
        employer_dropdown.options = [
            ft.dropdown.Option(key=str(employer[0]), text=employer[1]) for employer in employers
        ]
        employer_dropdown.update()
        page.update()


def main(page):
    def close_anchor(e):
        text = e.control.data
        anchor.close_view(text)

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        anchor.open_view()

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(f"Color {i}"), on_click=close_anchor, data=i)
            for i in range(10)
        ],
    )

    page.add(anchor)


ft.app(main)
#
# class JobSection(Container):
#     def __init__(self):
#         super().__init__()
#         self.employers_list = set()
#         # Job Input Fields
#         # Row 1
#         job_title_field = ft.TextField(label="Job Title", expand_loose=True, col=3, )
#         job_location_field = ft.TextField(label="Location", expand_loose=True, col=3)
#         job_location_field.value = 'Toronto, ON'
#         job_status_field = ft.TextField(label="Status", col=3)
#         job_notes_field = ft.TextField(label="Notes", multiline=True,
#                                        max_lines=6, expand=True
#                                        )
#         job_status_field.value = 'Applied'
#         # row 2
#         job_url_field = ft.TextField(label="Job URL", expand_loose=True)
#         # Dropdown for Employer Selection
#         employer_dropdown = ft.Dropdown(label="Select Employer", options=[], expand_loose=True)
#
#     def update(self):
#         super().update()
#
#     def update_employers(self):
#         employers_from_db = UDH.execute_query(
#             "SELECT employerID, employer_name FROM Employers ORDER BY employerID DESC",
#             fetch_mode=-1)  # since the higher the ID, the more recent the employer.
#
#         new_employers = [employer for employer in employers_from_db if employer[0] not in underlying_employers_set]
#         for employer in new_employers:
#             self.employers_list.add(employer[0])
#         self.employers_list = employers_from_db
#
#         self.load_employers()
#
#         employer_dropdown.update()
#         page.update()
#
#     def load_employers(self):
#         employer_dropdown.options = [
#             ft.dropdown.Option(key=str(employer[0]), text=employer[1]) for employer in self.employers_list
#         ]
#
#
# jobID_field = TextField()
# job_title_field = TextField()
# employerID_field = TextField()
# location_field = TextField()
# URL_field = TextField()
# status_field = TextField()
# annual_pay_field = TextField()
# ft_pt_field = TextField()
# job_type_field = TextField()
# work_model_field = TextField()
# date_added_field = TextField()
# date_applied_field = TextField()
# job_text_field = TextField()
# notes_field = TextField()
# archived_field = TextField()
# last_updated_field = TextField()
#
#
# def job_section():
#     # Layout Setup for job section
#     job_section = ft.Column(controls=[
#         ft.Text("Add Job", size=16, weight=ft.FontWeight.BOLD),
#         ft.Row([  # ROW 1
#             job_title_field,
#             job_location_field,
#             job_status_field,
#         ], spacing=5, expand=True),
#         ft.Row([  # ROW 2
#             employer_dropdown,
#             job_url_field,
#         ], spacing=5, expand=True, alignment=ft.MainAxisAlignment.START),
#         ft.Row([  # ROW 3
#             job_notes_field
#         ], spacing=5, expand=True, alignment=ft.MainAxisAlignment.START),
#         ft.Row([  # Results Row
#             add_job_button,
#             clear_job_button,
#             add_job_result_label
#         ], spacing=5, expand=True, alignment=ft.MainAxisAlignment.START),
#     ], expand=True, spacing=5)
#     return job_section
