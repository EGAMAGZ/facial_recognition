from facial_recognition.facial_recognition_core.facial_recognition import FacialRecognition
from facial_recognition.ui.app import start_app

if __name__ == "__main__":
    facial_recognition = FacialRecognition()
    facial_recognition.start_recognition()
    # start_app()
