import flet as ft

from facial_recognition.database import Database, Tables
from facial_recognition.facial_recognition_core.train_model import TrainModel
from facial_recognition.model.face_data import FaceData
from facial_recognition.util.document import to_face_data_list


class TrainModelScreen(ft.UserControl):
    status_card_ref = ft.Ref[ft.Card]()
    status_text_ref = ft.Ref[ft.Text]()

    _face_data_list: list[FaceData] = []

    def __init__(self) -> None:
        super().__init__()

    def _load_face_data(self) -> None:
        with Database(Tables.FACE_DATA) as db:
            self._face_data_list = to_face_data_list(db.all())

    def on_train_model(self) -> None:
        self._load_face_data()

        if len(self._face_data_list) == 0:
            self._show_no_face_data_dialog()
        else:
            train_model = TrainModel(
                face_data_list=self._face_data_list,
                on_training_complete=self.on_training_complete,
                on_step_change=self.on_step_change,
            )
            self.status_text_ref.current.value = "Initializing training..."
            self.status_card_ref.current.visible = True
            self.status_card_ref.current.update()

            train_model.start_training()

    def on_training_complete(self) -> None:
        def close_dialog(_event: ft.ControlEvent) -> None:
            dialog.open = False
            self.status_card_ref.current.visible = False
            self.status_card_ref.current.update()
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Model Trained"),
            content=ft.Text("Model trained successfully"),
            actions=[
                ft.TextButton(
                    text="Ok",
                    on_click=close_dialog
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def on_step_change(self, step: str) -> None:
        self.status_text_ref.current.value = step
        self.status_card_ref.current.update()

    def _show_no_face_data_dialog(self) -> None:
        def close_dialog(_event: ft.ControlEvent) -> None:
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("No face data"),
            content=ft.Text("No face data to train model"),
            actions=[ft.TextButton("Ok", on_click=close_dialog)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def build(self) -> ft.Container:
        return ft.Container(
            padding=ft.padding.only(top=20),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.FilledButton(
                                text="Train model",
                                on_click=lambda _: self.on_train_model(),
                                expand=True,
                            ),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Card(
                                content=ft.Container(
                                    ref=self.status_card_ref,
                                    content=ft.Row(
                                        controls=[
                                            ft.ProgressRing(),
                                            ft.Text(
                                                ref=self.status_text_ref,
                                            )
                                        ]
                                    ),
                                    padding=ft.padding.all(10),
                                ),
                                expand=True,
                                ref=self.status_card_ref,
                                visible=False,
                            )
                        ],
                    ),
                ]
            )
        )
