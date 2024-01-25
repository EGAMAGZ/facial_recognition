import flet as ft
from humanize import naturalday

from facial_recognition.database import Database, Tables
from facial_recognition.model.face_data import FaceData
from facial_recognition.ui.user_controls.name_text_field import NameTextField


class GenerateDataScreen(ft.UserControl):
    text_ref = ft.Ref[ft.Text]()
    list_view_ref = ft.Ref[ft.ListView]()

    face_data_list: list[FaceData] = []

    def __init__(self) -> None:
        super().__init__()
        self.load_face_data()

    def load_face_data(self) -> None:
        with Database(Tables.FACE_DATA) as db:
            # TODO: Improve code quality
            self.face_data_list = list(map(lambda row: FaceData(**row), db.all()))

    def on_capture_click(self, face_data: FaceData) -> None:
        with Database(Tables.FACE_DATA) as db:
            db.insert(face_data.model_dump())

        self.load_face_data()
        self.update_face_dada_list()

    def update_face_dada_list(self):
        self.text_ref.current.value = f"Loaded {len(self.face_data_list)} faces"
        self.list_view_ref.current.controls = [
            ft.ListTile(title=ft.Text(face_data.name)) for face_data in self.face_data_list
        ]
        self.update()

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    NameTextField(on_capture_click=self.on_capture_click),
                    ft.Text(
                        value=f"Loaded {len(self.face_data_list)} faces",
                        ref=self.text_ref
                    ),
                    ft.ListView(
                        ref=self.list_view_ref,
                        controls=[
                            ft.Card(
                                ft.ListTile(
                                    title=ft.Text(face_data.name),
                                    subtitle=ft.Text(naturalday(face_data.created_at)),
                                )
                            ) for face_data in self.face_data_list
                        ],
                    )
                ]
            ),
            padding=ft.padding.only(top=20)
        )
