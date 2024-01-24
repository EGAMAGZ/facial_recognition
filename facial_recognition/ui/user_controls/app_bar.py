import flet as ft


def custom_app_bar() -> ft.AppBar:
    return ft.AppBar(
        title=ft.Text("Facial Recognition"),
        leading=ft.Icon(ft.icons.FACE),
    )
