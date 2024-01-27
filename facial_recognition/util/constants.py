from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

DATA_DIR = BASE_DIR / "data"

DATABASE_FILE = DATA_DIR / "face_data.json"

APP_TITLE = "Facial Recognition"

MAX_FACES = 300

MODEL_FILE_NAME = "modelLBPHFace.xml"

DEFAULT_THRESHOLD = 70
