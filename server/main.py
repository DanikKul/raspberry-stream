from flask import Flask, request
from flask import render_template
from flask import Response
import cam_utils as cu

dist = cu.Distribution()
dist.init()
cam_number = dist.count_cameras()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', camera_number=cam_number)


@app.route('/stream', methods=['GET'])
def get_stream():
    cam = request.args.get('cam', 0, type=int)
    detection = request.args.get('detection', False, type=bool)
    return render_template('stream.html', cam=cam, detection=detection)


@app.route('/video', methods=['GET'])
def video():
    cam = request.args.get('cam', 0, type=int)
    detection = request.args.get('detection', False, type=bool)
    return Response(dist.get_packet_frame(cam, (720, 480), detection), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)
