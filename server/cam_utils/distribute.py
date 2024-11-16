import json

import cam_utils.detect as detect
import cv2
import numpy as np


class Distribution:

    def __init__(self):
        pass

    def init(self):
        detected = json.loads(detect.detect_cameras())
        self.cameras = []
        for cam in detected:
            self.cameras.append(cv2.VideoCapture(cam))
            self.cameras[-1].set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m', 'j', 'p', 'g'))

    def get_frame(self, cam_idx: int, resize: tuple | None = None, detect: bool = False) -> np.ndarray:
        ret, frame = self.cameras[cam_idx].read()
        if resize is not None:
            frame = cv2.resize(frame, resize, interpolation=cv2.INTER_LINEAR)
        return frame

    def get_packet_frame(self, cam_idx: int, resize: tuple | None = None, detect: bool = False) -> bytes:
        while True:
            frame = cv2.imencode('.jpg', self.get_frame(cam_idx, resize=resize, detect=detect))[1].tobytes()
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'

    def setup_camera(self, idx) -> None:
        self.cameras.append(cv2.VideoCapture(idx))

    def release_camera(self, idx) -> None:
        self.cameras[idx].release()

    def count_cameras(self) -> int:
        return len(self.cameras)
