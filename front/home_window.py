import flet as ft

from utils.path_utils import PathManager, PathFlag

text = open(
    PathManager.resolve_path('README.md', PathFlag.R)
    , 'r').read()


def home_window():
    return ft.Container(
        content=ft.Column([
            ft.Markdown(text)
        ], spacing=10),
        expand=True,
        padding=20,
        border=ft.border.all(1, ft.Colors.BLACK12),
        border_radius=10
    )
