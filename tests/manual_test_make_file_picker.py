import flet

from front.controls.make_file_picker import create_file_picker_controls


def manual_test_make_file_picker(page: flet.Page):
    row = flet.Row([v for v in create_file_picker_controls("demo").values()])
    cont = flet.Container(row, bgcolor=flet.Colors.with_opacity(0.2, flet.Colors.BLUE))
    page.add(cont)


flet.app(target=manual_test_make_file_picker)
