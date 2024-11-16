import cv2
import json


def detect_cameras():
    valid_cams = []
    for i in range(8):
        cap = cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', i)
        else:
            print('Detected camera: ', i)
            valid_cams.append(i)
    return json.dumps(valid_cams)


if __name__ == "__main__":
    print(detect_cameras())
