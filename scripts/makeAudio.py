import os
import sys
import codecs
import struct
import wave
from pycaption import SRTReader

framerate = 24000

content = codecs.open('output.srt', 'r', 'utf-8').read()
srt = SRTReader().read(content, lang='en')
caps = srt.get_captions('en')
out = wave.open('output.wav', 'w')
out.setnchannels(1)
out.setsampwidth(2)
out.setframerate(framerate)
outnframes = 0
for i,cap in enumerate(caps):
  start = cap.start / 1000000.0
  end = cap.end / 1000000.0
  nframesToFill = int((end - start) * framerate)
  wav = wave.open(os.path.join('data_aljazeera', '%d.wav' % (i+1)), 'r')
  nframes = wav.getnframes()
  out.writeframes(wav.readframes(nframes))
  wav.close()
  # need to fill nframesToFill - nframes zero frames
  for j in xrange(nframesToFill-nframes):
    out.writeframes(struct.pack('h', 0))
  outnframes += nframesToFill



