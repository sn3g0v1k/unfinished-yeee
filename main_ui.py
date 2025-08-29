import flet as ft

from editor_ui import main
from flet_file_system import file_system_widgets


def whole_ui(page: ft.Page):
    top_button_row, editor_column = main(page)

    toggle_column, drawer = file_system_widgets(page)
    content_box = ft.Container(
        expand=True,
        content=ft.Column(
            controls=[
                top_button_row,
                editor_column,
            ],
            spacing=10,
            expand=True,
        ),
        padding=16,
    )
    layout = ft.Row(
        controls=[
            toggle_column,
            drawer,
            content_box,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
    return layout
