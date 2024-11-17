import cv2
import streaming_utils as ps

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
    stream_props.set_page(stream_props, HTML)
    address = ('', 7777)
    try:
        stream_props.set_mode(stream_props, 'cv2')
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FPS, 30)
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 100)
        capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        stream_props.set_capture(stream_props, capture)
        stream_props.set_quality(stream_props, 90)
        stream_props.set_processing_function(stream_props, None)
        server = ps.Streamer(address, stream_props)
        server.serve_forever()

    except KeyboardInterrupt:
        capture.release()
        server.socket.close()


if __name__ == '__main__':
    main()
