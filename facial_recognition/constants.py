from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DATA_DIR = BASE_DIR / "data"

DATABASE_FILE = DATA_DIR / "face_data.json"
