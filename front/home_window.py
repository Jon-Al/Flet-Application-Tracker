import flet as ft

from utils.path_utils import PathManager, PathFlag


def home_window():
    text = open(
        PathManager.resolve_path('README.md', PathFlag.R)
        , 'r').read()
    r = ft.Row([ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.AMBER),
                ft.Text("Warning\nSome features are not available for web deployment. Yet.",
                        theme_style=ft.TextThemeStyle.BODY_LARGE, text_align=ft.TextAlign.CENTER),
                ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.AMBER),
                ], alignment=ft.MainAxisAlignment.CENTER)

    c = ft.Container(r, bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.AMBER), alignment=ft.Alignment(0, 0))

    return ft.Container(
        content=ft.Column([
            c,
            ft.Text("WELCOME!", theme_style=ft.TextThemeStyle.HEADLINE_LARGE),
            ft.Markdown(text)
        ], spacing=10,
            scroll=ft.ScrollMode.AUTO),
        expand=True,
        padding=20,
        border=ft.border.all(1, ft.Colors.BLACK12),
        border_radius=10
    )
