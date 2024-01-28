from typing import Callable

import cv2

from facial_recognition.database import Database, Tables
from facial_recognition.util.constants import DATA_DIR, MODEL_FILE_NAME, DEFAULT_THRESHOLD
from facial_recognition.util.document import to_face_data
from facial_recognition.util.image import frame_to_image

type ImageContent = str
type OnImageCaptured = Callable[[ImageContent], None]
type OnRecognitionComplete = Callable[[], None]


class FacialRecognition:
    _video_capture: cv2.VideoCapture
    _is_recognizing: bool = True

    on_image_captured: OnImageCaptured

    def __init__(self, on_image_captured: OnImageCaptured):
        self.on_image_captured = on_image_captured

    def start_recognition(self):
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        model_path = str(DATA_DIR / MODEL_FILE_NAME)
        face_recognizer = cv2.face.LBPHFaceRecognizer.create()
        face_recognizer.read(model_path)

        self._video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        while True:
            if not self._is_recognizing:
                self._on_stop_recognition()
                break

            ret, frame = self._video_capture.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aux_frame = gray.copy()

            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            self._add_face_indicators(aux_frame, face_recognizer, faces, frame)

    def _add_face_indicators(self, aux_frame, face_recognizer, faces, frame):
        for x, y, w, h in faces:
            if not self._is_recognizing:
                break

            face = aux_frame[y:y + h, x:x + w]
            face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
            doc_id, threshold = face_recognizer.predict(face)

            self._tag_face(doc_id, frame, h, threshold, w, x, y)

    def _tag_face(self, doc_id, frame, h, threshold, w, x, y):
        cv2.putText(frame, f'{threshold}', (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
        if threshold < DEFAULT_THRESHOLD:
            with Database(Tables.FACE_DATA) as db:
                face_data = to_face_data(db.get(doc_id=doc_id))
                cv2.putText(frame, face_data.name, (x, y - 25), 2, 1.1, (0, 255, 0), 1,
                            cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Unknown', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        self.on_image_captured(frame_to_image(frame))

    def _on_stop_recognition(self) -> None:
        self._video_capture.release()

    def stop_recognition(self) -> None:
        self._is_recognizing = False
