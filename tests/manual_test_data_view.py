from flet.core.colors import Colors

from front.controls.database_view import DatabaseView


def main(p):
    p.add(DatabaseView('tests/data/test_database.db', 'users', select_query='SELECT * FROM users',
                       row_colors=Colors.GREEN_ACCENT, interlaced_rows=True,
                       column_names=['id', 'name', 'age', 'email']
                       )
          )
    p.update()


if __name__ == '__main__':
    import flet as ft
    ft.app(target=main)
