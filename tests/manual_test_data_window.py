def main(p: Page):
    p.theme_mode = ThemeMode.SYSTEM
    p.theme = Theme(color_scheme_seed=ft.Colors.BLUE, use_material3=True)
    p.add(data_view())
    p.update()


if __name__ == '__main__':
    import flet as ft
    ft.app(target=main)
