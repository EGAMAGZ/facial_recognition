from tinydb import TinyDB

from facial_recognition.constants import DATABASE_FILE, DATA_DIR


def init_database():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()
    return TinyDB(DATABASE_FILE)


db = init_database()
