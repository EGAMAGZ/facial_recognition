from typing import Callable

import flet as ft
from humanize import naturalday

from facial_recognition.model.face_data import FaceData

type OnDeleteClick = Callable[[FaceData], None]
type OnRecaptureClick = Callable[[FaceData], None]


class FaceDataItem(ft.UserControl):
    on_delete_click: OnDeleteClick
    on_recapture_click: OnRecaptureClick

    face_data: FaceData

    def __init__(self, face_data: FaceData, on_delete_click: OnDeleteClick,
                 on_recapture_click: OnRecaptureClick) -> None:
        super().__init__()
        self.face_data = face_data
        self.on_delete_click = on_delete_click
        self.on_recapture_click = on_recapture_click

    def build(self) -> ft.Card:
        return ft.Card(
            ft.ListTile(
                title=ft.Text(self.face_data.name),
                subtitle=ft.Text(naturalday(self.face_data.created_at)),
                trailing=ft.PopupMenuButton(
                    icon=ft.icons.MORE_VERT,
                    items=[
                        ft.PopupMenuItem(
                            icon=ft.icons.CLOSE,
                            text="Delete face",
                            on_click=lambda _: self.on_delete_click(self.face_data),
                        ),
                        ft.PopupMenuItem(
                            icon=ft.icons.REFRESH,
                            text="Recapture face",
                            on_click=lambda _: self.on_recapture_click(self.face_data),
                        )
                    ]
                )
            )
        )
