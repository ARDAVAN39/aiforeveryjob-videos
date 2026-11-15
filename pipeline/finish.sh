#!/bin/bash
# Usage: EP=<slug> bash finish.sh "<Output file name>.mp4"  -> joins scenes, adds narration, writes ../videos/<name>
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUTDIR="${WORK_DIR:-$HOME/work}/$EP"; cd "$OUTDIR"
ls scene_*.mp4 | sort | sed "s/.*/file '&'/" > v.txt
ls scene_*.wav | sort | sed "s/.*/file '&'/" > a.txt
ffmpeg -y -loglevel error -f concat -i v.txt -c copy video.mp4
ffmpeg -y -loglevel error -f concat -i a.txt -c copy audio.wav
DEST="$REPO/videos/$1"; mkdir -p "$(dirname "$DEST")"
ffmpeg -y -loglevel error -i video.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$DEST"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$DEST"
