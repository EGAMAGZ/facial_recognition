import cv2
import numpy as np

from facial_recognition.constants import DATA_DIR
from facial_recognition.database import Tables, Database
from facial_recognition.model.face_data import FaceData
from facial_recognition.util.constants import MODEL_FILE_NAME
from facial_recognition.util.document import to_face_data_list


class TrainModel:
    face_data_list: list[FaceData]

    def __init__(self, face_data_list: list[FaceData]) -> None:
        self.face_data_list = face_data_list

    def start_training(self) -> None:
        faces_data = []
        labels: list[int] = []

        for index, face_data in enumerate(self.face_data_list):
            face_path = DATA_DIR / str(face_data.data_path)

            for image_path in face_path.iterdir():
                labels.append(index)
                faces_data.append(cv2.imread(str(image_path), 0))
        # else:
        self._face_recognize(faces_data, labels)

    def _face_recognize(self, faces_data, labels):
        model_path = str(DATA_DIR / MODEL_FILE_NAME)

        face_recognizer = cv2.face.LBPHFaceRecognizer.create()
        face_recognizer.train(faces_data, np.array(labels))
        face_recognizer.write(model_path)

    def stop_training(self) -> None:
        print("stop training")


if __name__ == "__main__":
    with Database(Tables.FACE_DATA) as db:
        face_data_list = to_face_data_list(db.all())
        train_model = TrainModel(face_data_list=face_data_list)
        train_model.start_training()
