# Example usage in a Page
from flet.core.page import Page

from front.insert_form_components import employer_group_form


def main(page: Page):
    # Example callback
    def on_employer_submit(data):
        print(f"Employer submitted: {data}")

    employer_form = employer_group_form()
    page.add(employer_form)


import flet as ft
ft.app(target=main)
