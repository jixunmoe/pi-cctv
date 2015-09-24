# -*- coding: utf-8 -*-

import time, os, io, picamera, threading
from flask import Flask, request, session, url_for, redirect, render_template, g, Response, send_file

# configuration
DATABASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'minitwit.db')
DEBUG = False
SECRET_KEY = 'This is a very secrey key.'

# PiCam, don't initialize the camera unless required.
class PiCam:
  def __init__(self):
    self.cam = None
    self.time = 0
    self.lock = threading.Lock()
    self.s = io.BytesIO()
    pass
  
  def init_cam(self):
    self.cam = picamera.PiCamera()
    self.cam.start_preview()
    self.cam.vflip = True
    self.cam.hflip = True
    time.sleep(2)
    pass
  
  def dup_stream(self):
    _s = io.BytesIO()
    self.lock.acquire()
    ### THREAD LOCK BEGIN
    self.s.seek(0)
    _s.write(self.s.read())
    ### THREAD LOCK END
    self.lock.release()
    _s.seek(0)
    return _s
  
  def capture(self):
    if (self.cam is None):
      self.init_cam()
    
    _t = time.time()
    # 30fps: 0.0333...
    if (_t - self.time > 0.02):
      self.time = _t
      
      self.lock.acquire()
      ### THREAD LOCK BEGIN
      self.s.seek(0)
      self.cam.capture(self.s, 'png')
      ### THREAD LOCK END
      self.lock.release()
    
    return self.dup_stream()

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('PICAM_SETTINGS', silent=True)

@app.route('/')
def the_camera():
  return render_template('index.html')

@app.route('/login')
def login():
  return 'TODO: Login';

my_cam = PiCam()
@app.route('/capture')
def capture():
  return send_file(my_cam.capture(), mimetype='image/png')

if __name__ == "__main__":
  app.run(host='0.0.0.0')
  while True:
    pass


