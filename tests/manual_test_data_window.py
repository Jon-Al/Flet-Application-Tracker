from flet.core.page import Page
from flet.core.theme import Theme
from flet.core.types import ThemeMode

from front.data_window import data_window


def main(p: Page):
    p.theme_mode = ThemeMode.SYSTEM
    p.theme = Theme(color_scheme_seed=ft.Colors.BLUE, use_material3=True)
    p.add(data_window())
    p.update()


if __name__ == '__main__':
    import flet as ft
    ft.app(target=main)
