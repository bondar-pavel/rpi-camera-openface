from io import BytesIO
from time import sleep
from picamera import PiCamera

import argparse
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
        # turn on training mode
        ws.send(json.dumps(get_training(1)))
        # say it is me on the screen
        ws.send(json.dumps(get_person('me')))
        # send a few pictures
        for i in range(3):
            sleep(1)
            ws.send(json.dumps(get_frame()))

        # say it is not me on the screen
        ws.send(json.dumps(get_person('not_me')))
        # turn off training mode
        ws.send(json.dumps(get_training(0)))
        # send a few more pictures
        for i in range(3):
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

def get_training(on):
    return {
       'type': 'TRAINING',
       'val' : on}

def get_person(name):
    return {
        'type': 'ADD_PERSON',
        'val' : name}

def init_camera():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    return camera

def parse_args():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Stream rpi camera to openface')
    parser.add_argument('--openface_host', default='192.168.0.110',
                        help='An optional integer positional argument')
    return parser.parse_args()

args = parse_args()
camera = init_camera()

#websocket.enableTrace(True)
openface = 'wss://' + args.openface_host + ':9000/'
print('Connecting to ' + openface)
ws = websocket.WebSocketApp(openface,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
ws.on_open = on_open
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

