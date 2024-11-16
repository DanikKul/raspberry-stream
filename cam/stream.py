import cv2
import json
import multiprocessing as mp
from detect import detect_cameras


def start_stream_local(no: int):
    cam = cv2.VideoCapture(no)

    while True:
        ret, frame = cam.read()

        cv2.imshow(f'Camera #{no}', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    processes = []
    a = json.loads(detect_cameras())
    for i in range(len(a)):
        processes.append(mp.Process(target=start_stream_local, args=[a[i]]))
        processes[i].start()

    for i in range(len(a)):
        processes[i].join()