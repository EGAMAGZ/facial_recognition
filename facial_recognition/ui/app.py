import flet as ft

from facial_recognition.ui.screens.facial_recognition_screen import (
    FacialRecognitionScreen,
)
from facial_recognition.ui.screens.generate_data_screen import (
    GenerateDataScreen,
)
from facial_recognition.ui.screens.train_model_screen import TrainModelScreen
from facial_recognition.ui.user_controls.app_bar import custom_app_bar
from facial_recognition.util.constants import APP_TITLE


class FaceRecognitionApp(ft.UserControl):
    def build(self) -> ft.Control:
        return ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Generate data",
                    icon=ft.icons.INSERT_CHART,
                    content=ft.Text("Generate data"),
                ),
                ft.Tab(
                    text="Train model",
                    icon=ft.icons.ATTACH_FILE,
                    content=ft.Text("Train model"),
                ),
                ft.Tab(
                    text="Recognize faces",
                    icon=ft.icons.FIND_IN_PAGE,
                    content=ft.Text("Recognize faces"),
                )
            ],
            expand=True,
        )


def app(page: ft.Page) -> None:
    page.title = APP_TITLE
    page.add(
        ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Generate data",
                    icon=ft.icons.INSERT_CHART,
                    content=GenerateDataScreen()
                ),
                ft.Tab(
                    text="Train model",
                    icon=ft.icons.ATTACH_FILE,
                    content=TrainModelScreen(),
                ),
                ft.Tab(
                    text="Recognize faces",
                    icon=ft.icons.FIND_IN_PAGE,
                    content=FacialRecognitionScreen()
                )
            ],
            expand=True,
        ),
    )

    page.appbar = custom_app_bar()
    page.theme = ft.Theme(color_scheme_seed=ft.colors.YELLOW)
    page.update()


def start_app() -> None:
    ft.app(target=app)
