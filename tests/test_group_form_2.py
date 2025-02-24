import flet as ft
from front.controls import GroupForm
from front.insert_form_components import job_form, employer_group_form


# Example usage in a Page
def test1(page: ft.Page):
    jobs = job_form()
    employer_form = employer_group_form()
    page.add(jobs)
    page.add(employer_form)
    page.update()


def test2(page: ft.Page):
    page.title = "GroupForm Test"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Define fields
    fields = {
        "name":   ft.TextField(label="Name"),
        "age":    ft.TextField(label="Age"),
        "status": ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("Applied"),
                ft.dropdown.Option("Interview"),
                ft.dropdown.Option("Offer"),
                ft.dropdown.Option("Rejected"),
            ]
        ),
    }

    # Result text
    result_text = ft.Text(value="Form output will appear here.")

    # Action buttons
    def on_submit(e):
        result_text.value = f"Submitted: {form.values}"
        page.update()

    def on_clear(e):
        form.clear_fields()
        result_text.value = "Form cleared."
        page.update()

    submit_button = ft.ElevatedButton(text="Submit", on_click=on_submit)
    clear_button = ft.ElevatedButton(text="Clear", on_click=on_clear)

    # Create form
    form = GroupForm(fields, action_buttons=[submit_button, clear_button], result_text=result_text)

    # Add form to page
    page.add(form)


# ft.app(target=test1)
ft.app(target=test2)
