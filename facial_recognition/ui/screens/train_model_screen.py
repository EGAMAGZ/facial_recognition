import flet as ft

from facial_recognition.database import Database, Tables
from facial_recognition.model.face_data import FaceData
from facial_recognition.util.document import to_face_data_list


class TrainModelScreen(ft.UserControl):
    face_data_list: list[FaceData] = []

    def __init__(self) -> None:
        super().__init__()

    def load_face_data(self) -> None:
        with Database(Tables.FACE_DATA) as db:
            self.face_data_list = to_face_data_list(db.all())

    def on_train_model(self) -> None:
        self.load_face_data()
        print(len(self.face_data_list))
        if len(self.face_data_list) == 0:
            self.show_no_face_data_dialog()
        else:
            print("train model")

    def show_no_face_data_dialog(self) -> None:
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
                    ft.TextButton("Train model", on_click=lambda _: self.on_train_model()),
                ]
            )
        )
