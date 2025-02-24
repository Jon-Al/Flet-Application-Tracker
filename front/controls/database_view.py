from copy import copy
from typing import Optional, Tuple, Union, Any, Dict, List

from flet import Container, Column, Control, DataTable, DataColumn, DataRow, DataCell
from flet.core.row import Row
from flet.core.text import Text
from flet.core.text_style import TextThemeStyle
from flet.core.types import TextAlign, MainAxisAlignment, ControlStateValue, ColorValue, \
    OptionalControlEventCallable, ScrollMode
from flet.core.border import all as all_borders, BorderSide

from front.controls.link_button import link_button, path_button
from utils.database_handler import DatabaseHandler


class DatabaseView(Container):
    def __init__(self, db_path: str,
                 table_or_view_name: str,
                 select_query: str,
                 column_names: List[str],
                 select_params: Optional[Tuple] = None,
                 edit_row_cell: Optional[DataCell] = None,
                 row_colors: ControlStateValue[ColorValue] = None,
                 interlaced_rows: Optional[bool] = None) -> None:
        """
        :param db_path:
        :param table_or_view_name:
        :param select_query: WITHOUT sorting.
        :param edit_row_cell:
        """
        super().__init__()
        self.expand = False
        self.db = DatabaseHandler(db_path)
        self.db.execute_mode(True)
        self.select_params = select_params or ()
        self.data = self.db.execute_query(select_query, self.select_params, fetch_mode=-1)
        self.table_name = table_or_view_name
        self.select_query = select_query
        self.column_headers = column_names
        cols = [self._make_column(h) for h in self.column_headers]
        self.edit_row_cell = edit_row_cell
        if interlaced_rows:
            rows = [self._make_row(r, color=row_colors, even_or_odd=(i % 2 == 0)) for i, r in enumerate(self.data)]
        else:
            rows = [self._make_row(r, color=row_colors) for r in self.data]
        if self.edit_row_cell:
            rows.append(edit_row_cell)
        self.table = DataTable(columns=cols,
                               rows=rows,
                               expand=False,
                               border=all_borders(1),
                               horizontal_lines=BorderSide(1),
                               vertical_lines=BorderSide(1),
                               horizontal_margin=5,
                               data_row_min_height=10,
                               )
        self.content = Row([Column(controls=[Text(self.table_name.capitalize(),
                                                  style=TextThemeStyle.HEADLINE_SMALL, text_align=TextAlign.CENTER),
                                             self.table
                                             ], scroll=ScrollMode.AUTO,
                                   alignment=MainAxisAlignment.CENTER)], scroll=ScrollMode.AUTO
                           )

    def _make_row(self, row_data: Dict[str, Any],
                  color: ControlStateValue[ColorValue] = None,
                  selected: Optional[bool] = None,
                  on_long_press: OptionalControlEventCallable = None,
                  on_select_changed: OptionalControlEventCallable = None,
                  edit_row_cell: Optional[DataCell] = None,
                  even_or_odd: Optional[bool] = None,
                  data: Any = None,
                  ) -> DataRow | None:
        if not row_data:
            return None
        cells = []
        for ch in self.column_headers:
            if ch.startswith('URL'):
                lb = link_button(row_data[ch], 'open')
                cells.append(self._make_cell(control=lb))
            elif ch.startswith('Path'):
                lb = path_button(row_data[ch], 'open')
                cells.append(self._make_cell(control=lb))
            else:
                cells.append(self._make_cell(row_data[ch]))
        if edit_row_cell:
            cells.append(copy(edit_row_cell))
        if even_or_odd is True:
            color = color.with_opacity(0.5, color)
        row = DataRow(cells=cells,
                      color=color,
                      selected=selected,
                      on_long_press=on_long_press,
                      on_select_changed=on_select_changed,
                      data=row_data,
                      )
        return row

    @staticmethod
    def _make_cell(string_content: str = "",
                   control: Optional[Control] = None,
                   content: Optional[Any] = None,
                   show_edit_icon: Optional[bool] = None,
                   on_tap: OptionalControlEventCallable = None,
                   on_double_tap: OptionalControlEventCallable = None,
                   on_long_press: OptionalControlEventCallable = None,
                   on_tap_cancel: OptionalControlEventCallable = None,
                   ref=None,
                   visible: Optional[bool] = None,
                   disabled: Optional[bool] = None,
                   is_id: Optional[bool] = None,
                   data: Any = None,
                   ) -> DataCell:
        """
        :param string_content: Will be used if control and content are None.
        :param content: Will be used if control is None.
        :param control: Used if not None.
        :return:
        """
        if control:
            ctrl = control
        elif isinstance(string_content, str):
            ctrl = Text(value=string_content, color='black', no_wrap=len(string_content) < 50, selectable=True)
        elif isinstance(string_content, int):
            ctrl = Text(value=str(string_content), color='black', text_align=TextAlign.CENTER, selectable=True)
        elif content:
            ctrl = Text(value=str(string_content), color='black', no_wrap=False, selectable=True)
        else:
            ctrl = Text(value='--', color='black', no_wrap=False, text_align=TextAlign.CENTER, selectable=True)
        return DataCell(
            ctrl,  # First non-None will be used.
            show_edit_icon=show_edit_icon,
            on_tap=on_tap,
            on_double_tap=on_double_tap,
            on_long_press=on_long_press,
            on_tap_cancel=on_tap_cancel,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data
        )

    # region BUILDER METHODS
    @staticmethod
    def _make_column(title: Union[str, Control],
                     numeric: Optional[bool] = None, tooltip: Optional[str] = None,
                     heading_row_alignment: Optional[MainAxisAlignment] = "start",
                     ref=None,
                     visible: Optional[bool] = None, disabled: Optional[bool] = None,
                     data: Any = None, ) -> DataColumn:
        table_column = DataColumn(
            label=Text(title, theme_style=TextThemeStyle.TITLE_SMALL, ) if isinstance(title, str) else title,
            numeric=numeric,
            heading_row_alignment=heading_row_alignment,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            ref=ref
        )
        table_column.expand = False
        return table_column
