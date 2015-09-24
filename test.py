# -*- coding: utf-8 -*-

import picamera, io
my_stream = io.BytesIO()
camera = picamera.PiCamera()
camera.start_preview()
camera.capture(my_stream, 'png')
print(my_stream)

while True:
  pass