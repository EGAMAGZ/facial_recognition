import enum

from tinydb import JSONStorage, TinyDB
from tinydb.table import Table
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

from facial_recognition.serializer import UuidSerializer
from facial_recognition.util.constants import DATA_DIR, DATABASE_FILE


class Tables(enum.Enum):
    FACE_DATA = "face_data"


class Database:
    _db_instance: TinyDB
    table: Table

    def __init__(self, table: Tables) -> None:
        self._db_instance = self._build_database()
        self.table = self._db_instance.table(table.value)

    def _build_database(self) -> TinyDB:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir()

        serializer = SerializationMiddleware(JSONStorage)
        serializer.register_serializer(DateTimeSerializer(), "TinyDate")
        serializer.register_serializer(UuidSerializer(), "TinyUuid")

        return TinyDB(DATABASE_FILE, storage=serializer)

    def __enter__(self):
        return self.table

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_instance.close()
