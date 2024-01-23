import flet as ft


class FaceRecognitionApp(ft.UserControl):
    def build(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text(
                    "Facial Recognition", theme_style=ft.TextThemeStyle.DISPLAY_LARGE
                ),
            ]
        )


def app(page: ft.Page) -> None:
    page.title = "Facial Recognition"
    page.add(FaceRecognitionApp())


def start_app() -> None:
    ft.app(target=app)
