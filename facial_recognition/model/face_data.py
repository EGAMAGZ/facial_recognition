import uuid

from pydantic import BaseModel, Field
from datetime import datetime


class FaceData(BaseModel):
    name: str = Field(min_length=1)
    data_path: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
