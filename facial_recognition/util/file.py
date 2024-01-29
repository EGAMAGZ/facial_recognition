import shutil
import uuid

from facial_recognition.util.constants import DATA_DIR, MODEL_FILE_NAME


def delete_face_directory(directory: uuid.UUID) -> None:
    face_path = DATA_DIR / str(directory)
    if not face_path.exists():
        return
    shutil.rmtree(face_path)


def delete_model_file() -> None:
    model_path = DATA_DIR / MODEL_FILE_NAME
    if model_path.exists():
        model_path.unlink()
