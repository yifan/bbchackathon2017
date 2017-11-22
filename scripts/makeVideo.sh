#1- make video no audio 
ffmpegCmd="/opt/ffmpeg/bin/ffmpeg"
$ffmpegCmd -i data_aljazeera.mp4 -strict -2 -vf subtitles=output.srt data_aljazeera.srt.mp4

#2- make video with simple audio track
rm -fr combined.wav
list=$(for i in {1..35}; do echo data_aljazeera/$i.wav; done)
sox -m $list combined.wav
$ffmpegCmd -i data_aljazeera.srt.mp4 -i combined.wav -strict -2 -vf subtitles=output.srt data_aljazeera.srt.audio.mp4


#2- make video with adjusted audio track
grep "\-\-" output.srt | sed 's:,:\.:g' | sed 's: --> :\::' |  \
awk -F: '{t1=($1*3600)+($2*60)+$3;t2=($4*3600)+($5*60)+$6;d=t2-t1;print d}' | \
nl | while read id duration2; do
  target=$(echo $duration2 | tr '\r' ' ' | sed 's: $::')
  current=$(soxi -D data_aljazeera/$i.wav)
  sildur=$(bc <<< "$target-$current")
  rm -fr tmp$$*
  sox music.wav tmp$$.wav trim 0 $sildur
  sox tmp$$.wav data_aljazeera/$id.music.wav fade 0:6 $sildur 0:7
  sox -n -r 24000 -c 1 data_aljazeera/$id.music.wav trim 0.0 $sildur
done 

rm -fr combined.sil.wav
list=$(for i in {1..35}; do echo data_aljazeera/$i.wav data_aljazeera/$i.sil.wav; done)

sox $list combined.sil.wav

$ffmpegCmd -i data_aljazeera.srt.mp4 -i combined.sil.wav -strict -2 -vf subtitles=output.srt data_aljazeera.srt.audio.sil.mp4
      

#3- make video with adjusted audio track
grep "\-\-" output.srt | sed 's:,:\.:g' | sed 's: --> :\::' |  \
awk -F: '{t1=($1*3600)+($2*60)+$3;t2=($4*3600)+($5*60)+$6;d=t2-t1;print d}' | \
nl | while read id duration2; do
  target=$(echo $duration2 | tr '\r' ' ' | sed 's: $::')
  current=$(soxi -D data_aljazeera/$i.wav)
  sildur=$(bc <<< "$target-$current")
  rm -fr tmp$$*
  sox music.wav tmp$$.wav trim 0 $sildur
  sox tmp$$.wav data_aljazeera/$id.music.wav fade 0:2 $sildur 0:2
  echo sox tmp$$.wav data_aljazeera/$id.music.wav fade 0:2 $sildur 0:2
done 

rm -fr combined.music.wav
list=$(for i in {1..35}; do echo data_aljazeera/$i.wav data_aljazeera/$i.music.wav; done)

sox $list combined.music.wav
$ffmpegCmd -i data_aljazeera.srt.mp4 -i combined.music.wav -strict -2 -vf subtitles=output.srt data_aljazeera.srt.audio.music.mp4
      
