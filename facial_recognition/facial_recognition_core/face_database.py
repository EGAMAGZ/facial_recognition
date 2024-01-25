import flet as ft
from pathlib import Path
from typing import Callable

import cv2
import imutils

from facial_recognition.constants import DATA_DIR
from facial_recognition.model.face_data import FaceData

type OnCaptureComplete = Callable[[], None]


class FaceDatabase:
    _face_path: Path
    _face_data: FaceData
    on_capture_complete: OnCaptureComplete

    def __init__(self, face_data: FaceData, on_capture_complete: OnCaptureComplete) -> None:
        self._face_data = face_data
        self._face_path = DATA_DIR / str(face_data.data_path)
        self.on_capture_complete = on_capture_complete

    def _create_directory(self) -> None:
        if not self._face_path.exists():
            self._face_path.mkdir()

    def capture_face(self) -> None:
        self._create_directory()
        video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        for face_count in range(300):
            ret, frame = video_capture.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized_frame = imutils.resize(frame, width=640)

            faces = face_classifier.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(resized_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                face = frame[y:y + h, x:x + w]
                face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
                image_path = str(self._face_path / f'face-{face_count}.jpg')
                cv2.imwrite(image_path, face)

                cv2.imshow('frame', resized_frame)
                key = cv2.waitKey(1)
                if key == 27:
                    video_capture.release()
                    cv2.destroyAllWindows()
                    self.on_capture_complete()
                    break
        else:
            video_capture.release()
            cv2.destroyAllWindows()
            self.on_capture_complete()


if __name__ == "__main__":
    face_data = FaceData(name="test")
    face_database = FaceDatabase(face_data, lambda: print("Captured face"))
    face_database.capture_face()
