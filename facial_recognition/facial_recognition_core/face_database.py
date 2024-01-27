import uuid

import flet as ft
from pathlib import Path
from typing import Callable

import cv2
import imutils

from facial_recognition.util.constants import DATA_DIR
from facial_recognition.model.face_data import FaceData
from facial_recognition.util.constants import MAX_FACES
from facial_recognition.util.image import frame_to_image

type OnCaptureComplete = Callable[[], None]
type OnImageCaptured = Callable[[int, ImageContent], None]
type ImageContent = str


class FaceDatabase:
    _face_path: Path
    _face_data: FaceData
    _video_capture: cv2.VideoCapture

    _is_capturing = True
    on_capture_complete: OnCaptureComplete
    on_image_captured: OnImageCaptured

    def __init__(self, face_data: FaceData, on_capture_complete: OnCaptureComplete,
                 on_image_captured: OnImageCaptured) -> None:
        self._face_data = face_data
        self._face_path = DATA_DIR / str(face_data.data_path)

        self.on_capture_complete = on_capture_complete
        self.on_image_captured = on_image_captured

    def _create_directory(self) -> None:
        if not self._face_path.exists():
            self._face_path.mkdir()

    def _on_stop_capture(self) -> None:
        self._video_capture.release()
        # cv2.destroyAllWindows()
        self.on_capture_complete()

    def _add_face_indicators(self, face_count, faces, frame, resized_frame):
        for x, y, w, h in faces:
            if not self._is_capturing:
                break
            cv2.rectangle(resized_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face = frame[y:y + h, x:x + w]
            face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)

            self._store_face_image(face)
            self.on_image_captured(face_count, frame_to_image(resized_frame))
            # cv2.imshow('frame', resized_frame)
            # key = cv2.waitKey(delay=1)
            # if key == 27:  # ESC key
            # break

    def _store_face_image(self, face):
        image_path = str(self._face_path / f'face-{uuid.uuid4()}.jpg')
        cv2.imwrite(image_path, face)

    def capture_face(self) -> None:
        self._create_directory()
        self._video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        for face_count in range(MAX_FACES):
            if not self._is_capturing:
                self._on_stop_capture()
                break

            ret, frame = self._video_capture.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized_frame = imutils.resize(frame, width=640)

            faces = face_classifier.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

            self._add_face_indicators(face_count, faces, frame, resized_frame)
        else:
            self._on_stop_capture()

    def stop_capture(self) -> None:
        self._is_capturing = False


if __name__ == "__main__":
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()


    def main(page: ft.Page) -> None:
        def update_image_captured(face_count: int, image: ImageContent) -> None:
            text.value = f"Captured {face_count} faces"
            image_webcam.src_base64 = image
            page.update()

        face_data = FaceData(name="test")
        face_database = FaceDatabase(
            face_data=face_data,
            on_capture_complete=lambda: print("Captured face"),
            on_image_captured=update_image_captured
        )
        text = ft.Text("")
        image_webcam = ft.Image()
        page.add(
            ft.Column(
                controls=[
                    ft.TextButton("Stop", on_click=lambda e: face_database.stop_capture()),
                    text,
                    image_webcam
                ]
            )
        )
        face_database.capture_face()


    ft.app(target=main)
