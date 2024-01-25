from typing import Callable

import flet as ft
from humanize import naturalday

from facial_recognition.model.face_data import FaceData

type OnDeleteClick = Callable[[int], None]


class FaceDataItem(ft.UserControl):
    on_delete_click: OnDeleteClick

    doc_id: int
    face_data: FaceData

    def __init__(self, face_data: FaceData, doc_id: int, on_delete_click: OnDeleteClick) -> None:
        super().__init__()
        self.face_data = face_data
        self.doc_id = doc_id
        self.on_delete_click = on_delete_click

    def build(self) -> ft.Card:
        return ft.Card(
            ft.ListTile(
                title=ft.Text(self.face_data.name),
                subtitle=ft.Text(naturalday(self.face_data.created_at)),
                trailing=ft.IconButton(ft.icons.CLOSE, on_click=lambda _: self.on_delete_click(self.doc_id))
            )
        )
