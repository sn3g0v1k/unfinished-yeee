import flet as ft

from main_ui import whole_ui

def main(page: ft.Page):
    page.window.width = 1100
    page.window.height = 1300
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    layout = whole_ui(page)
    page.add(
        layout
    )


ft.app(target=main)