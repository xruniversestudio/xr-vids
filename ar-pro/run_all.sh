#!/usr/bin/env bash
# Render both formats (3 parallel chunks each), then join and add the soundtrack.
set -u
cd "$(dirname "$0")"; mkdir -p parts out qa
for F in h v; do
  P=8700; [ "$F" = v ] && P=8710
  FMT=$F PORT=$((P+1)) node render.js video 0 360   > log_${F}0.txt 2>&1 &
  FMT=$F PORT=$((P+2)) node render.js video 360 720 > log_${F}1.txt 2>&1 &
  FMT=$F PORT=$((P+3)) node render.js video 720 1080 > log_${F}2.txt 2>&1 &
  wait
  (cd parts && ls ${F}_*.mp4 | sort | sed "s/^/file '/; s/$/'/" > list_$F.txt)
  ffmpeg -loglevel error -y -f concat -safe 0 -i parts/list_$F.txt -c copy parts/joined_$F.mp4
  NAME=$([ "$F" = v ] && echo "XR_Universe_AR_Types_Reel_1080x1920" || echo "XR_Universe_AR_Types_1920x1080")
  ffmpeg -loglevel error -y -i parts/joined_$F.mp4 -i audio/music_v1.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/$NAME.mp4
  ffmpeg -loglevel error -y -i out/$NAME.mp4 -c:v libx264 -crf 23 -preset slow -c:a copy -movflags +faststart out/${NAME}_preview.mp4
  echo "DONE $F"
done
echo ALLDONE
