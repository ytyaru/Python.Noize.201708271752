#https://github.com/pgk/python-portaudio-examples/blob/master/sine.py
from __future__ import division

import pyaudio
import time
import math
from array import array

NUM_SECONDS = 5
SAMPLE_RATE = 44100
FRAMES_PER_BUFFER = 64

_2PI = 3.14159265 * 2.0

TABLE_SIZE = 1024 



class SineWave(object):

  def __init__(self):
    self.sine = array('f')

    for i in range(TABLE_SIZE):
      item = math.sin( (i / TABLE_SIZE) * _2PI )
      self.sine.append( item )
    self.phase = 0
    self.data = array('f')
    for i in range(TABLE_SIZE):
      self.data.append(self.sine[i])

  def callback(self, in_data, frame_count, time_info, status):
    for i in range(frame_count):
      self.data[i] = self.sine[self.phase]
      self.phase += 8
      if self.phase >= TABLE_SIZE:
        self.phase = 0

    return (self.data.tostring(), pyaudio.paContinue)


sine = SineWave()
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                output=True,
                frames_per_buffer = FRAMES_PER_BUFFER,
                stream_callback=sine.callback)

stream.start_stream()

try:
  while stream.is_active():
    time.sleep(0.5)

except KeyboardInterrupt:
  stream.stop_stream()
  stream.close()
  p.terminate()
print('')
