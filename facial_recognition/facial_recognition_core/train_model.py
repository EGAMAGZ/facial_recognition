from typing import Callable

import flet as ft
import cv2
import numpy as np

from facial_recognition.util.constants import DATA_DIR
from facial_recognition.database import Tables, Database
from facial_recognition.model.face_data import FaceData
from facial_recognition.util.constants import MODEL_FILE_NAME
from facial_recognition.util.document import to_face_data_list

type OnTrainingModelComplete = Callable[[], None]
type OnStepChange = Callable[[str], None]


class TrainModel:
    _face_data_list: list[FaceData]

    on_training_complete: OnTrainingModelComplete
    on_step_change: OnStepChange

    def __init__(self, face_data_list: list[FaceData], on_training_complete: OnTrainingModelComplete,
                 on_step_change: OnStepChange) -> None:
        self._face_data_list = face_data_list
        self.on_training_complete = on_training_complete

        self.on_step_change = on_step_change

    def start_training(self) -> None:
        faces_data = []
        labels: list[int] = []

        for index, face_data in enumerate(self._face_data_list):
            self.on_step_change(f"Reading face data: {index}/{len(self._face_data_list)}")
            face_path = DATA_DIR / str(face_data.data_path)

            for image_path in face_path.iterdir():
                labels.append(index)
                faces_data.append(cv2.imread(str(image_path), 0))

        self._face_recognize(faces_data, labels)
        self._on_training_complete()

    def _face_recognize(self, faces_data, labels):
        model_path = str(DATA_DIR / MODEL_FILE_NAME)

        face_recognizer = cv2.face.LBPHFaceRecognizer.create()
        self.on_step_change("Training model...")
        face_recognizer.train(faces_data, np.array(labels))
        self.on_step_change("Saving model...")
        face_recognizer.write(model_path)

    def _on_training_complete(self) -> None:
        self.on_step_change("Training complete")
        self.on_training_complete()


if __name__ == "__main__":
    def main(page: ft.Page) -> None:
        text_ref = ft.Ref[ft.Text]()

        def on_training_complete() -> None:
            dialog.open = True
            page.update()

        def on_step_change(step: str) -> None:
            text_ref.current.value = step
            page.update()

        def close_dialog(_event: ft.ControlEvent) -> None:
            dialog.open = False
            page.update()

        train_model: TrainModel
        with Database(Tables.FACE_DATA) as db:
            face_data_list = to_face_data_list(db.all())
            train_model = TrainModel(
                face_data_list=face_data_list,
                on_training_complete=on_training_complete,
                on_step_change=on_step_change
            )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Model Trained"),
            content=ft.Text("Model trained successfully"),
            actions=[
                ft.TextButton(
                    text="Ok",
                    on_click=close_dialog
                ),
            ],
        )
        page.dialog = dialog

        page.add(
            ft.TextButton(
                text="Train model",
                on_click=lambda _: train_model.start_training()
            ),
            ft.Text(
                value="No model trained yet",
                ref=text_ref,
            )
        )


    ft.app(target=main)
