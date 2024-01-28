import flet as ft

from facial_recognition.ui.user_controls.facial_recognizer import FacialRecognizer
from facial_recognition.util.constants import DATA_DIR, MODEL_FILE_NAME


class FacialRecognitionScreen(ft.UserControl):

    def on_start_recognition(self) -> None:
        model_path = DATA_DIR / MODEL_FILE_NAME
        if model_path.exists():
            self._show_facial_recognizer_dialog()
        else:
            self._show_no_model_dialog()

    def _show_facial_recognizer_dialog(self):
        def close_dialog(_event: ft.ControlEvent) -> None:
            facial_recognizer.stop_recognition()
            facial_recognizer_dialog.open = False
            self.page.update()

        facial_recognizer = FacialRecognizer()
        facial_recognizer_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Recognizing..."),
            content=facial_recognizer,
            actions=[
                ft.TextButton(text="Stop", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = facial_recognizer_dialog
        facial_recognizer_dialog.open = True
        self.page.update()

    def _show_no_model_dialog(self):
        def close_dialog(_event: ft.ControlEvent) -> None:
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("No model found"),
            content=ft.Text("Please train the model first"),
            actions=[
                ft.TextButton(text="Ok", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.FilledButton(
                                text="Start recognition",
                                on_click=lambda _: self.on_start_recognition(),
                                expand=True
                            ),
                        ]
                    )
                ]
            ),
            padding=ft.padding.only(top=20)
        )
