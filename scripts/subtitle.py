import sys
import codecs
from pycaption import Caption, CaptionSet, CaptionNode
from pycaption import SRTWriter

stories = codecs.open('story.txt', 'r', 'utf-8').readlines()

def microsec(t):
  return t*1000000

offset = 0.0
captions = []
for line in sys.stdin:
  if line.startswith(' '):
    continue
  tokens = line.split()
  if len(tokens) != 3:
    continue
  dirname = tokens[0]
  index = int(dirname.split('/')[-1])-1
  duration = float(tokens[2])
  print duration
  text=stories[index]
  cap = Caption(microsec(offset), microsec(offset+duration), [CaptionNode.create_text(text)])
  offset += duration
  captions.append(cap)

caps = CaptionSet({'en': captions})

srt = codecs.open('output.srt', 'w', 'utf-8')
srt.write(SRTWriter().write(caps))
srt.close()
