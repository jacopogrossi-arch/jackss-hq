#!/bin/bash
# run-windows.sh: il 4K finale del Video #4 a finestre (< 120 s l'una, vedi make-windows.py), poi unione e coda di run-4k.sh (mix, tag, controlli).
# Ogni finestra salta se il suo file esiste gia' con i fotogrammi giusti: rilanciare lo script riprende da dove era arrivato.
cd /d/ClaudeCodeTest/videos/04-identita/cut
SK=../../../.claude/skills/youtube-edit
export PYTHONUTF8=1 FFMPEG_PROCESS_TIMEOUT_MS=14400000 TEMP=D:/hf-tmp TMP=D:/hf-tmp HYPERFRAMES_HISTORY_ROOT=D:/hf-history
export PRODUCER_STREAMING_ENCODE_MAX_DURATION_SECONDS=3600 HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=1500 HF_SEGMENT_BROWSER_RECYCLE=1
export PRODUCER_BROWSER_GPU_MODE=hardware NODE_OPTIONS=--max-old-space-size=8192
log(){ echo "$(date '+%d/%m %H:%M:%S') $*" | tee -a final-4k/run.log; }
frames(){ ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 "$1" 2>/dev/null | tr -d '\r,'; }
python make-windows.py > final-4k/windows.log 2>&1 || { log "FINESTRE: make-windows fallito"; exit 3; }
N=$(python -c "import json;print(len(json.load(open('final-4k/windows.json'))))")
for i in $(seq 0 $((N-1))); do
  w=$(printf 'w%02d' $i); want=$(python -c "import json;print(json.load(open('final-4k/windows.json'))[$i]['frames50'])")
  out=final-4k/$w.mp4
  if [ -s $out ] && [ "$(frames $out)" = "$want" ]; then continue; fi
  for try in 1 2; do
    log "FINESTRA $w ($want fotogrammi) tentativo $try: inizio"
    rm -f $out
    python $SK/scripts/render-queue.py --wait-minutes 60 -- npx hyperframes@0.9.35 render final-4k/$w/public --fps 50 --resolution 4k --video-bitrate 60M --gpu --workers 1 --frames-cache-dir D:/hf-cache -o $out > final-4k/$w.log 2>&1
    got=$(frames $out)
    if [ "$got" = "$want" ]; then log "FINESTRA $w ok ($got fotogrammi)"; break; fi
    log "FINESTRA $w NON ok: fotogrammi '$got' attesi $want; $(tail -c 250 final-4k/$w.log | tr '\n' ' ')"
    [ $try = 2 ] && exit 5
  done
done
if [ ! -s final-4k/video4-4k-raw.mp4 ]; then
  : > final-4k/concat.txt; for i in $(seq 0 $((N-1))); do printf "file 'w%02d.mp4'\n" $i >> final-4k/concat.txt; done
  ffmpeg -y -v error -f concat -safe 0 -i final-4k/concat.txt -map 0:v -c copy -movflags +faststart final-4k/video4-4k-raw.tmp.mp4 || { log "UNIONE fallita"; exit 5; }
  got=$(frames final-4k/video4-4k-raw.tmp.mp4)
  [ "$got" = "63062" ] || { log "UNIONE: fotogrammi $got, attesi 63062"; exit 5; }
  mv final-4k/video4-4k-raw.tmp.mp4 final-4k/video4-4k-raw.mp4; log "UNIONE ok: $got fotogrammi"
fi
bash run-4k.sh
