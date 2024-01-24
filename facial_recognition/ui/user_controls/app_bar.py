import flet as ft


def main_app_bar(page: ft.Page) -> ft.AppBar:
    return ft.AppBar(
        title=ft.Text("Facial Recognition"),
        center_title=True,
    )
