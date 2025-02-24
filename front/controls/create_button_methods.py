from flet.core.colors import Colors
from flet.core.icon_button import IconButton
from flet.core.icons import Icons


def create_delete_button(tooltip='', on_click=None):
    return IconButton(
        icon=Icons.DELETE_OUTLINED,
        icon_color="pink600",
        icon_size=20,
        tooltip=tooltip,
        on_click=on_click,
        expand=0
    )


def create_restore_button(tooltip='', on_click=None):
    return IconButton(
        icon=Icons.RESTORE,
        icon_color=Colors.CYAN_500,
        icon_size=20,
        tooltip=tooltip,
        on_click=on_click,
        expand=0
    )


def create_clear_button(tooltip='', on_click=None):
    return IconButton(
        icon=Icons.RESTORE,
        icon_color="teal60",
        icon_size=20,
        tooltip=tooltip,
        on_click=on_click,
        expand=0
    )


def create_add_button(tooltip='', on_click=None):
    return IconButton(
        icon=Icons.ADD_SHARP,
        icon_color="green60",
        icon_size=20,
        tooltip=tooltip,
        on_click=on_click,
        expand=0
    )
