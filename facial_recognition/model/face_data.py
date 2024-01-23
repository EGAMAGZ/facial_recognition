import uuid

from pydantic import BaseModel
from datetime import datetime


class FaceData(BaseModel):
    name: str
    data_path: uuid.UUID
    created_at: datetime
