import flet as ft
from flet.core.text_style import TextThemeStyle
from flet.core.types import TextAlign

from front.controls.dark_theme_toggle import theme_toggle_button
from front.data_window import data_window
from front.home_window import home_window
from front.template_dashboard_window import template_dashboard_window


def on_page_resized(e):
    e.control.update()


def initiate_content(index: int = 0, parent=None):
    r = [home_window(), template_dashboard_window(), data_window()][index]
    if parent:
        parent.content = r
        parent.update()
    else:
        return r


def main_window(page: ft.Page):
    page.on_page_resized = on_page_resized
    page.window.maximized = True
    page.title = "Job Application Tracking Database"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    header = ft.Container(
        content=ft.Row(
            [
                ft.Text("Application Tracker", theme_style=TextThemeStyle.HEADLINE_SMALL),
                ft.Text("Proof of\nConcept", theme_style=TextThemeStyle.BODY_MEDIUM,
                        text_align=TextAlign.CENTER),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        margin=ft.margin.only(bottom=20)
    )
    # Create a placeholder for the main content
    content_area = ft.Pagelet(
        content=initiate_content(),
        expand=True
    )

    # Create the sidebar navigation
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        expand=True,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Home"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD_OUTLINED,
                selected_icon=ft.Icons.DASHBOARD,
                label="Dashboard"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.DATASET_OUTLINED,
                selected_icon=ft.Icons.DATASET_SHARP,
                label="Data Views"
            )
        ],
        on_change=lambda e: initiate_content(e.control.selected_index, content_area)
    )
    nav_area = ft.Column([nav_rail, theme_toggle_button(page)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=100,
                         expand=False)

    # Create a status bar
    status_bar = ft.Container(
        content=ft.Row(
            [
                ft.Text("Status: Ready", italic=True, theme_style=TextThemeStyle.BODY_SMALL),
                ft.Text("v: 0.0.01", italic=True, theme_style=TextThemeStyle.BODY_SMALL)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        margin=ft.margin.only(top=20)
    )

    page.add(
        header,
        ft.Row(
            [
                nav_area,
                ft.VerticalDivider(width=1),
                ft.Column([content_area, status_bar], expand=True),

            ],
            expand=True
        )
    )
    page.update()
