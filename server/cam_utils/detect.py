import cv2
import json


def detect_cameras():
    valid_cams = []
    for i in range(1):
        cap = cv2.VideoCapture(cv2.CAP_V4L2)
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', i)

        else:
            print('Detected camera: ', i)
            valid_cams.append(i)
            cap.release()
    return json.dumps(valid_cams)


if __name__ == "__main__":
    print(detect_cameras())
