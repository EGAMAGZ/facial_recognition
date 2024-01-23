from tinydb import TinyDB, JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

from facial_recognition.constants import DATABASE_FILE, DATA_DIR
from facial_recognition.serializer import UuidSerializer


def init_database():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()

    serializer = SerializationMiddleware(JSONStorage)
    serializer.register_serializer(DateTimeSerializer(), "TinyDate")
    serializer.register_serializer(UuidSerializer(), "TinyUuid")

    return TinyDB(DATABASE_FILE, storage=serializer)


db = init_database()
