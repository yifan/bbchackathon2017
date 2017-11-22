#!/bin/bash

touch list.txt
num=$(cat story.txt | wc -l)
for ((i=1;i<=$num;i++)); do
  DIRNAME=data_aljazeera/$i
  WAVFILE=$DIRNAME.wav
  DURATION=$(soxi -D $WAVFILE)
  NUMIMGS=$(ls $DIRNAME/*.jpg | wc -l)
  IMGDUR=$(echo "scale=2;c=$DURATION / $NUMIMGS;if (c > 1.5) { print c; } else { print 1.5; }" | bc -l)
  CORRECT_DURATION=$(echo "scale=2; $IMGDUR * $NUMIMGS" | bc -l)
  echo $DIRNAME $IMGDUR $CORRECT_DURATION
  for IMGFILE in $DIRNAME/*.jpg; do
    echo "    " $IMGFILE
    VIDFILE=$DIRNAME/$(basename $IMGFILE .jpg).mp4
    VIDFILE=mp4_aljazeera${VIDFILE##data_aljazeera}
    mkdir -p $(dirname $VIDFILE)
    ffmpeg -y -loop 1 -t $IMGDUR -i $IMGFILE -s hd720 -c:v mpeg4 -pix_fmt yuv420p -vf scale=1280:720 $VIDFILE &> /dev/null
    if [[ -s $VIDFILE ]]; then
      echo file \'$VIDFILE\' >> list.txt
    else
      echo ffmpeg -loop 1 -t 1 -i $IMGFILE -s hd720 -c:v mpeg4 -pix_fmt yuv420p -vf scale=1280:720 $VIDFILE >> failed.txt
    fi
  done
done

ffmpeg -y -f concat -i list.txt -c copy video.mp4 &> /dev/null
rm list.txt
