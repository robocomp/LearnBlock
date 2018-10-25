#!/usr/bin/env python3
from __future__ import print_function, absolute_import

import io
import picamera
import subprocess
import time
import paho.mqtt.client
import os, inspect
from learnbot_components.camera import path
subprocess.Popen("mosquitto -c " + os.path.join(path, "mosquitto.conf"), shell=True)
time.sleep(2)

client = None

def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='camara', qos=2)

class SplitFrames(object):
    def __init__(self):
        self.stream = io.BytesIO()
        self.count = 0
        self.start = time.time()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            size = self.stream.tell()
            if size > 0:
                self.stream.seek(0)
                image = self.stream.read(size)
                self.stream.seek(0)
                client.publish('camara', image.__str__())
                self.count += 1
                if self.count == 60:
                    print(self.count/(time.time()-self.start), "fps")
                    self.start = time.time()
                    self.count = 0
        self.stream.write(buf)

try:
    output = SplitFrames()
    #with picamera.PiCamera(resolution='VGA', framerate=20) as camera:
    with picamera.PiCamera(resolution=(320,240), framerate=20) as camera:
        time.sleep(2)
        camera.start_recording(output, format='mjpeg', resize=(320,240))
        client = paho.mqtt.client.Client(client_id='server', clean_session=False)
        client.on_connect = on_connect
        client.connect(host='192.168.16.1', port=50000)
        client.loop_forever()
except KeyboardInterrupt:
    pass
