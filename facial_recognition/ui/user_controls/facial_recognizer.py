import flet as ft

from facial_recognition.facial_recognition_core.facial_recognition import FacialRecognition, ImageContent


class FacialRecognizer(ft.UserControl):
    _facial_recognition: FacialRecognition

    image_ref = ft.Ref[ft.Image]()
    container_ref = ft.Ref[ft.Container]()

    def __init__(self) -> None:
        super().__init__()

        self._facial_recognition = FacialRecognition(
            on_image_captured=self._on_image_captured,
        )

    def did_mount(self) -> None:
        self._facial_recognition.start_recognition()
        self.update()

    def _on_image_captured(self, image: ImageContent) -> None:
        self.image_ref.current.src_base64 = image
        self.image_ref.current.visible = True
        self.container_ref.current.visible = False

        self.update()

    def stop_recognition(self) -> None:
        self._facial_recognition.stop_recognition()

    def build(self) -> ft.Stack:
        return ft.Stack(
            controls=[
                ft.Image(
                    visible=False,
                    ref=self.image_ref,
                ),
                ft.Container(
                    content=ft.Text(
                        value="Initializing...",
                    ),
                    bgcolor=ft.colors.BLACK,
                    ref=self.container_ref
                )
            ]
        )
