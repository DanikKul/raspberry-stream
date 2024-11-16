import json
import time
import threading
import cv2
import numpy as np
import cam_utils.detect as detect


class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []

    def append(self, frame):
        if len(self.buffer) > self.size:
            self.buffer.pop(0)
        self.buffer.append(frame)

    def pop(self):
        if len(self.buffer) > 1:
            return self.buffer.pop()
        else:
            return self.buffer[0]

    def __getitem__(self, idx):
        return self.buffer.index(self.buffer[0])

    def __len__(self):
        return len(self.buffer)

class Distribution:

    def __init__(self):
        pass

    def init(self):
        detected = json.loads(detect.detect_cameras())
        self.cameras = []
        self.frames = []
        serve_cams = []
        for cam in detected:
            self.cameras.append(cv2.VideoCapture(cam))
            self.cameras[-1].set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m', 'j', 'p', 'g'))
            serve_cams.append(threading.Thread(target=self.serve_camera, args=[cam]))
            serve_cams[-1].start()
            self.frames.append(Buffer(1000))

    def serve_camera(self, idx):
        while True:
            t1 = time.time()
            ret, frame = self.cameras[idx].read()
            self.frames[idx].append(frame)
            t2 = time.time()
            print(f'CAM: {idx} TIME: {t2 - t1}')

    def get_frame(self, cam_idx: int, resize: tuple | None = None, detect: bool = False) -> np.ndarray:
        frame = self.frames[cam_idx].buffer[-1]
        print(frame)
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
