import uuid
from datetime import datetime

from facial_recognition.database import db
from facial_recognition.model.face_data import FaceData

if __name__ == "__main__":
    face = FaceData(name="John", data_path=uuid.uuid4(), created_at=datetime.now())
    print(face.model_dump())
    print(db.insert(face.model_dump()))
