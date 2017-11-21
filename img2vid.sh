#!/bin/bash

touch list.txt
cat images.txt | while read IMGFILE; do
  VIDFILE=${IMGFILE%\.*}.mp4
  WAVFILE=$(dirname $IMGFILE).wav
  VIDFILE=mp4_aljazeera${VIDFILE##data_aljazeera}
  DIRNAME=$(dirname $VIDFILE)
  mkdir -p $DIRNAME
  ffmpeg -loop 1 -t 1 -i $IMGFILE -s hd720 -c:v mpeg4 -pix_fmt yuv420p -vf scale=1280:720 $VIDFILE
  if [[ -s $VIDFILE ]]; then
    echo file \'$VIDFILE\' >> list.txt
  else
    echo ffmpeg -loop 1 -t 1 -i $IMGFILE -s hd720 -c:v mpeg4 -pix_fmt yuv420p -vf scale=1280:720 $VIDFILE >> failed.txt
  fi
done

ffmpeg -f concat -i list.txt -c copy video.mp4
rm list.txt
