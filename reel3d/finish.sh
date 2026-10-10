#!/usr/bin/env bash
# Join rendered chunks, add the soundtrack, write deliverables and QA sheets.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out qa
(cd parts && ls part_*.mp4 | sort | sed "s/^/file '/; s/$/'/" > list.txt)
ffmpeg -loglevel error -y -f concat -safe 0 -i parts/list.txt -c copy parts/joined.mp4
ffmpeg -loglevel error -y -i parts/joined.mp4 -i audio/reel_audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/XR_Universe_Studio_3D_Reel_1080x1920_REVIEW.mp4
ffmpeg -loglevel error -y -i parts/joined.mp4 -c copy -movflags +faststart out/XR_Universe_Studio_3D_Reel_1080x1920_REVIEW_silent.mp4
ffmpeg -loglevel error -y -ss 5.5 -i out/XR_Universe_Studio_3D_Reel_1080x1920_REVIEW.mp4 -frames:v 1 out/cover.jpg
ffmpeg -loglevel error -y -i out/XR_Universe_Studio_3D_Reel_1080x1920_REVIEW.mp4 -vf "fps=1,scale=216:384,tile=8x3:padding=4:color=0x080C12" -frames:v 1 qa/contact_sheet_1s.jpg
ffmpeg -loglevel error -y -i out/XR_Universe_Studio_3D_Reel_1080x1920_REVIEW.mp4 -vf "select='between(n\,86\,93)+between(n\,236\,243)+between(n\,296\,303)+between(n\,446\,453)+between(n\,596\,603)',scale=180:320,tile=8x5:padding=3" -vsync vfr -frames:v 1 qa/scene_boundaries.jpg
echo "done"
