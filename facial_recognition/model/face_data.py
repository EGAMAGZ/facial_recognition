from pydantic import BaseModel
from datetime import datetime


class FaceData(BaseModel):
    name: str
    data_path: str
    created_at: datetime
