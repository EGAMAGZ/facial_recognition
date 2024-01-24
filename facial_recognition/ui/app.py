import flet as ft

from facial_recognition.ui.user_controls.app_bar import main_app_bar


class FaceRecognitionApp(ft.UserControl):
    def build(self) -> ft.Control:
        return ft.SafeArea(
            ft.Tabs(
                tabs=[
                    ft.Tab(
                        text="Generate data",
                        icon=ft.icons.INSERT_CHART
                    ),
                    ft.Tab(
                        text="Train model",
                        icon=ft.icons.ATTACH_FILE
                    ),
                    ft.Tab(
                        text="Recognize faces",
                        icon=ft.icons.FIND_IN_PAGE
                    )
                ],
                expand=True,
            )
        )


def app(page: ft.Page) -> None:
    page.title = "Facial Recognition"
    page.add(FaceRecognitionApp())

    page.appbar = main_app_bar(page=page)
    page.theme = ft.Theme(color_scheme_seed=ft.colors.YELLOW)
    page.update()


def start_app() -> None:
    ft.app(target=app)
