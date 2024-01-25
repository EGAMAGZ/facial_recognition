import shutil
import uuid

from facial_recognition.constants import DATA_DIR


def delete_face_directory(directory: uuid.UUID) -> None:
    face_path = DATA_DIR / directory
    if not face_path.exists():
        return
    shutil.rmtree(DATA_DIR / directory)
