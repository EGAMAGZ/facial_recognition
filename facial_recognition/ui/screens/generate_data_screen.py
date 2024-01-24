import flet as ft

from facial_recognition.database import Database
from facial_recognition.model.face_data import FaceData
from facial_recognition.ui.user_controls.name_text_field import NameTextField


class GenerateDataScreen(ft.UserControl):
    text_ref = ft.Ref[ft.Text]()

    face_data_list: list[FaceData] = []

    def __init__(self) -> None:
        super().__init__()
        self.load_face_data()

    def load_face_data(self) -> None:
        with Database() as db:
            db.all()
            self.face_data_list: list[FaceData] = db.all()[0]

    def on_capture_click(self, face_data: FaceData) -> None:
        with Database() as db:
            db.insert(face_data.model_dump())

        self.load_face_data()
        # self.text_ref.current.value = f"Loaded {len(self.face_data_list)} faces"
        self.update()

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    NameTextField(on_capture_click=self.on_capture_click),
                    ft.Text(value=f"Loaded {len(self.face_data_list)} faces", ref=self.text_ref),
                ]
            ),
            padding=ft.padding.only(top=20)
        )
