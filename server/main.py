import cv2
import pyshine as ps

HTML = """
<html>
<head>
<title>Streaming</title>
</head>

<body>
<center><h1>Streaming</h1></center>
<center><img src="stream.mjpg" style="height: 70%" autoplay playsinline></center>
</body>
</html>
"""


def main():
    stream_props = ps.StreamProps
    stream_props.set_Page(stream_props, HTML)
    address = ('', 7777)
    try:
        stream_props.set_Mode(stream_props, 'cv2')
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 4)
        # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        capture.set(cv2.CAP_PROP_FPS, 30)
        stream_props.set_Capture(stream_props, capture)
        stream_props.set_Quality(stream_props, 90)
        server = ps.Streamer(address, stream_props)
        server.serve_forever()

    except KeyboardInterrupt:
        capture.release()
        server.socket.close()


if __name__ == '__main__':
    main()

