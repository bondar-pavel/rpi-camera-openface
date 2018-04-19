# rpi-camera-openface

WIP: Simple python script to send images from pi camera to the remote openface installation

Now it is able to read image from picamera, resize it to 300x400px and send to secure websocket
that unmodified OpenFace Web demo opened (port 9000).

Openface WebSocket message format is take from:
https://github.com/cmusatyalab/openface/blob/master/demos/web/websocket-server.py

Original client:
https://github.com/cmusatyalab/openface/blob/master/demos/web/js/openface-demo.js

# Requirements
- python-picamera
- websocket-client
