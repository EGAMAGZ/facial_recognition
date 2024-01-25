import flet as ft
from humanize import naturalday

from facial_recognition.database import Database, Tables
from facial_recognition.model.face_data import FaceData
from facial_recognition.ui.user_controls.face_data_item import FaceDataItem
from facial_recognition.ui.user_controls.name_text_field import NameTextField
from facial_recognition.util.file import delete_face_directory


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
            self.face_data_list = list(
                map(
                    lambda row: FaceData(doc_id=row.doc_id, **row), db.all()
                )
            )

    def on_capture_click(self, face_data: FaceData) -> None:
        with Database(Tables.FACE_DATA) as db:
            # TODO: Check if their is a better implementation
            doc_id = db.insert(face_data.model_dump())
            face_data.doc_id = doc_id
            self.face_data_list.append(
                face_data
            )

        self.update_face_dada_list()

    def on_delete_click(self, face_data: FaceData) -> None:
        with Database(Tables.FACE_DATA) as db:
            self.face_data_list.remove(face_data)
            # delete_face_directory(face_data.data_path)
            db.remove(doc_ids=[face_data.doc_id])

        self.update_face_dada_list()

    def update_face_dada_list(self):
        self.text_ref.current.value = f"Number of loaded faces: {len(self.face_data_list)}"
        self.list_view_ref.current.controls = [
            FaceDataItem(
                face_data=face_data,
                on_delete_click=self.on_delete_click
            ) for face_data in self.face_data_list
        ]
        self.update()

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    NameTextField(on_capture_click=self.on_capture_click),
                    ft.Text(
                        ref=self.text_ref,
                        value=f"Number of loaded faces: {len(self.face_data_list)}",
                        theme_style=ft.TextThemeStyle.HEADLINE_LARGE
                    ),
                    ft.ListView(
                        ref=self.list_view_ref,
                        expand=True,
                        controls=[
                            FaceDataItem(
                                face_data=face_data,
                                on_delete_click=self.on_delete_click
                            ) for face_data in self.face_data_list
                        ],
                    )
                ]
            ),
            padding=ft.padding.only(top=20)
        )
