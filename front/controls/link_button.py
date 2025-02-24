import os
from typing import Optional
from flet import TextButton, Icons
from flet.core.buttons import ButtonStyle
from flet.core.canvas.color import Color
from flet.core.colors import Colors
from flet.core.icon import Icon
from flet.core.padding import Padding


def link_button(url: str, text_to_show: Optional[str], icon: Icons = Icons.LINK):
    return TextButton(text=text_to_show if text_to_show else '',
                      icon=icon,
                      tooltip=url,
                      url=url,
                      style=ButtonStyle(padding=Padding(top=5, bottom=5, left=10, right=10), ), )


import os
import subprocess
import sys


def path_button(url: str, text_to_show: Optional[str]):
    if os.path.isfile(url):
        url_type = 'File'
        icon = Icons.FILE_OPEN
        icon_color = Colors.YELLOW_ACCENT_700
    elif os.path.isdir(url):
        url_type = 'Directory'
        icon = Icons.FOLDER_OPEN
        icon_color = Colors.BROWN_300
    else:
        url_type = 'DNE'
        icon = Icons.BLOCK
        icon_color = Colors.RED_300

    def on_click(e):
        if not os.path.exists(url):
            return
        if sys.platform == "win32":
            os.startfile(url)  # Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", url])  # macOS
        else:
            subprocess.run(["xdg-open", url])  # Linux

    return TextButton(text=text_to_show if text_to_show else '',
                      icon=icon,
                      icon_color=icon_color,
                      tooltip=url,
                      disabled=icon == Icons.BLOCK,
                      style=ButtonStyle(padding=Padding(top=5, bottom=5, left=10, right=10)), on_click=on_click)

# Not everything justifies a test - sometimes, things can be assumed to be working.
