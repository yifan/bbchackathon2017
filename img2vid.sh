#!/bin/bash

touch list.txt
for IMGFILE in $@; do
  VIDFILE=${IMGFILE%\.*}.mp4
  VIDFILE=mp4_aljazeera${VIDFILE##data_aljazeera}
  DIRNAME=$(dirname $VIDFILE)
  mkdir -p $DIRNAME
  ffmpeg -loop 1 -t 1 -i $IMGFILE -s hd720 -c:v mpeg4 -pix_fmt yuv420p -vf scale=1280:720 $VIDFILE
  echo file $VIDFILE >> list.txt
done

ffmpeg -f concat -safe 0 -i list.txt -c copy video.mp4
rm list.txt
