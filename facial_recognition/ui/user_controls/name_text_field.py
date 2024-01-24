from typing import Callable

import flet as ft
from pydantic import ValidationError

from facial_recognition.model.face_data import FaceData

type OnCaptureClick = Callable[[FaceData], None]


class NameTextField(ft.UserControl):
    text_field_ref = ft.Ref[ft.TextField]()

    on_capture_click: OnCaptureClick

    def __init__(self, on_capture_click: OnCaptureClick) -> None:
        super().__init__()
        self.on_capture_click = on_capture_click

    def on_click(self, event: ft.ControlEvent) -> None:
        name = self.text_field_ref.current.value
        try:
            face_data = FaceData(name=name)
            self.clear_text_field()
            self.on_capture_click(face_data)
        except ValidationError:
            self.text_field_ref.current.helper_text = "Name is required"

    def clear_text_field(self) -> None:
        self.text_field_ref.current.value = ""
        self.text_field_ref.current.helper_text = ""
        self.text_field_ref.current.update()

    def build(self) -> ft.Row:
        return ft.Row(
            [
                ft.TextField(
                    label="Name",
                    expand=True,
                    border=ft.InputBorder.OUTLINE,
                    filled=True,
                    ref=self.text_field_ref,
                ),
                ft.OutlinedButton(
                    text="Capture",
                    on_click=self.on_click
                ),
            ]
        )
