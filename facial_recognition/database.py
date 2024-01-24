from tinydb import TinyDB, JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

from facial_recognition.constants import DATABASE_FILE, DATA_DIR
from facial_recognition.serializer import UuidSerializer


class Database:
    db: TinyDB

    def __init__(self) -> None:
        self.db = self._build_database()

    def _build_database(self) -> TinyDB:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir()

        serializer = SerializationMiddleware(JSONStorage)
        serializer.register_serializer(DateTimeSerializer(), "TinyDate")
        serializer.register_serializer(UuidSerializer(), "TinyUuid")

        return TinyDB(DATABASE_FILE, storage=serializer)

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
