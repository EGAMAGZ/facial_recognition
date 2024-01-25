import shutil
import uuid

from facial_recognition.constants import DATA_DIR


def delete_face_directory(path: uuid.UUID) -> None:
    face_path = DATA_DIR / path
    if not face_path.exists():
        return
    shutil.rmtree(DATA_DIR / path)
