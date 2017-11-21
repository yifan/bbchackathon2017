#!/bin/bash

for IMGFILE in $@; do
  VIDFILE=${IMGFILE%\.*}.mp4
  VIDFILE=mp4_aljazeera${VIDFILE##data_aljazeera}
  DIRNAME=$(dirname $VIDFILE)
  mkdir -p $DIRNAME
  ffmpeg -loop 1 -i $IMGFILE -s hd720 -c:v mpeg4 -pix_fmt yuv420p $VIDFILE
done
