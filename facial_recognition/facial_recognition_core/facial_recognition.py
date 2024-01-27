from pathlib import Path

import cv2


# from facial_recognition.util.constants import DATA_DIR


class FacialRecognition:
    _video_capture: cv2.VideoCapture

    def __init__(self):
        pass

    def start_recognition(self):
        image_paths = (Path(__file__).parent.parent / "data").iterdir()
        print(image_paths)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        face_recognizer = cv2.face.LBPHFaceRecognizer.create()
        face_recognizer.read((Path(__file__).parent.parent / "data"))

        self._video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        while True:
            ret, frame = self._video_capture.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aux_frame = gray.copy()

            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for x, y, w, h in faces:
                face = aux_frame[y:y + h, x:x + w]
                face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(face)

                cv2.putText(frame, f'{result}', (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

                # LBPHFace
                if result[1] < 70:
                    cv2.putText(frame, '{}'.format(image_paths[result[0]]), (x, y - 25), 2, 1.1, (0, 255, 0), 1,
                                cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2.imshow('frame', frame)
            key = cv2.waitKey(delay=1)
            if key == 27:  # ESC key
                break

        self._video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    facial_recognition = FacialRecognition()
    facial_recognition.start_recognition()
