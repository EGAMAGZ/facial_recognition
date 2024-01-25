import base64

import cv2


def frame_to_image(frame) -> str:
    _, image_array = cv2.imencode('.png', frame)
    image_base64 = base64.b64encode(image_array)
    return image_base64.decode('utf-8')
