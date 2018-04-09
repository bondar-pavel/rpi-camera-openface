from io import BytesIO
from time import sleep
from picamera import PiCamera

import base64
import websocket
import ssl
import json
try:
    import thread
except ImportError:
    import _thread as thread

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(2):
            sleep(1)
            ws.send(json.dumps(get_frame()))
        sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

def get_frame():
    stream = BytesIO()
    camera.capture(stream, 'jpeg', resize=(400, 300))
    data = 'data:image/jpeg;base64,' + base64.b64encode(stream.getvalue()).decode()
    stream.close()
    frame = {
        'type': 'FRAME',
        'dataURL': data,
        'identity': ''
    }
    # print(frame)
    return frame

def init_camera():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    return camera

camera = init_camera()

websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://192.168.0.110:9000/",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
ws.on_open = on_open
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

