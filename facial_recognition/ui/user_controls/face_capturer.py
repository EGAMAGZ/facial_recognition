import flet as ft

from facial_recognition.facial_recognition_core.face_database import (
    FaceDatabase,
    ImageContent,
    OnCaptureComplete,
)
from facial_recognition.model.face_data import FaceData
from facial_recognition.util.constants import MAX_FACES


class FaceCapturer(ft.UserControl):
    _face_database: FaceDatabase

    image_ref = ft.Ref[ft.Image]()
    text_ref = ft.Ref[ft.Text]()
    on_capture_complete: OnCaptureComplete

    def __init__(self, face_data: FaceData, on_capture_complete: OnCaptureComplete) -> None:
        super().__init__()
        self.on_capture_complete = on_capture_complete

        self._face_database = FaceDatabase(
            face_data=face_data,
            on_capture_complete=self._on_capture_complete,
            on_image_captured=self._on_image_captured
        )

    def did_mount(self) -> None:
        self._face_database.capture_face()

    def _on_capture_complete(self) -> None:
        self.on_capture_complete()

    def _on_image_captured(self, face_count: int, image: ImageContent) -> None:
        self.image_ref.current.src_base64 = image
        self.image_ref.current.visible = True

        self.text_ref.current.value = f"Captured {face_count + 1} / {MAX_FACES} faces"
        self.update()

    def stop_capture(self) -> None:
        self._face_database.stop_capture()

    def build(self) -> ft.Stack:
        return ft.Stack(
            controls=[
                ft.Image(
                    ref=self.image_ref,
                    visible=False,
                ),
                ft.Container(
                    content=ft.Text(
                        ref=self.text_ref,
                        value="Initializing...",
                    ),
                    bgcolor=ft.colors.BLACK,
                )
            ]
        )
