#!/bin/bash
# run-4k.sh: catena del 4K finale del Video #4 (vedi ../STATO-NOTTE.md, "4K FINALE"). Ogni passo salta se il suo file esiste gia'. Log: final-4k/run.log
cd /d/ClaudeCodeTest/videos/04-identita/cut
SK=../../../.claude/skills/youtube-edit
export PYTHONUTF8=1 FFMPEG_PROCESS_TIMEOUT_MS=14400000 TEMP=D:/hf-tmp TMP=D:/hf-tmp HYPERFRAMES_HISTORY_ROOT=D:/hf-history
# ricetta del 4K a 60 fps del Video #3 (final-v5/run.sh): encode in streaming, un worker, cattura a segmenti con ripresa
export PRODUCER_STREAMING_ENCODE_MAX_DURATION_SECONDS=3600 HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=1500 HF_SEGMENT_BROWSER_RECYCLE=1
export PRODUCER_BROWSER_GPU_MODE=hardware NODE_OPTIONS=--max-old-space-size=8192
# tramite ffprobe (ffprobe-fast/ffprobe.cs): risponde subito al controllo keyframe che HyperFrames 0.9.35 uccide dopo 30 s col disco sotto carico
#export HYPERFRAMES_FFPROBE_PATH="D:/ClaudeCodeTest/videos/04-identita/cut/ffprobe-fast/ffprobe.exe" HF_KEYFRAMES_FILE="D:/ClaudeCodeTest/videos/04-identita/cut/final-4k/keyframes.txt" HF_KEYFRAMES_FOR="D:/ClaudeCodeTest/videos/04-identita/cut/build/public/input-video.mp4"
#export HYPERFRAMES_FFMPEG_PATH="D:/ClaudeCodeTest/videos/04-identita/cut/ffprobe-fast/ffmpeg.exe" HF_EXTRACT_SLOTS=3 HF_REAL_FFMPEG="C:/Users/Jacopo Grossi/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe"
export HF_FFMPEG_LOG="D:/ClaudeCodeTest/videos/04-identita/cut/final-4k/ffmpeg-calls.log" HF_FFPROBE_LOG="D:/ClaudeCodeTest/videos/04-identita/cut/final-4k/ffprobe-calls.log" HF_REAL_FFPROBE="C:/Users/Jacopo Grossi/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffprobe.exe"
log(){ echo "$(date '+%d/%m %H:%M:%S') $*" | tee -a final-4k/run.log; }
if [ ! -s proxy/layout-4k.mp4 ]; then
  log "PASSO 2 layout 4K: inizio (3 processi insieme)"
  python build-layout-4k.py --part 0/3 > layout4k/part0.log 2>&1 & python build-layout-4k.py --part 1/3 > layout4k/part1.log 2>&1 & python build-layout-4k.py --part 2/3 > layout4k/part2.log 2>&1 & wait
  log "parti: $(tail -qn1 layout4k/part0.log layout4k/part1.log layout4k/part2.log | tr '
' ' ')"
  python build-layout-4k.py > layout4k/full.log 2>&1 || { log "PASSO 2 FALLITO: $(tail -3 layout4k/full.log)"; exit 2; }
fi
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 proxy/layout-4k.mp4)
python -c "import sys; sys.exit(0 if abs(float('$D')-1261.24)<0.1 else 1)" || { log "PASSO 2 DURATA SBAGLIATA: $D s (attesi 1261.24): un pezzo in layout4k e' incompleto, cancellarlo e rilanciare"; mv proxy/layout-4k.mp4 proxy/layout-4k.SBAGLIATO.mp4; exit 2; }
log "PASSO 2 ok: $D s"
if [ ! -s final-4k/video4-4k-raw.mp4 ]; then
  if [ ! -f final-4k/.built ]; then
    rm -f build/public/input-video.mp4
    python $SK/scripts/plates-build.py . --plates plates --video proxy/layout-4k.mp4 --out build > final-4k/plates-build.log 2>&1 || { log "PASSO 4 FALLITO: $(tail -3 final-4k/plates-build.log)"; exit 4; }
    python add-sounds.py >> final-4k/plates-build.log 2>&1 || { log "add-sounds FALLITO"; exit 4; }
    touch final-4k/.built
  fi
  t0=$(date +%s); ffprobe -v error -select_streams v:0 -skip_frame nokey -show_entries frame=pts_time -of csv=p=0 build/public/input-video.mp4 > final-4k/keyframes.txt; t1=$(date +%s)
  log "PASSO 4 ok: $(grep -E 'plates in' final-4k/plates-build.log); keyframe $(wc -l < final-4k/keyframes.txt), probe $((t1-t0)) s"
  RES=""; [ -f final-4k/.started ] && RES="--resume"; touch final-4k/.started
  log "PASSO 5 render 4K 50 fps: inizio $RES"
  python $SK/scripts/render-queue.py --wait-minutes 60 -- npx hyperframes@0.9.35 render build/public --fps 50 --resolution 4k --video-bitrate 60M --gpu --workers 1 --frames-cache-dir D:/hf-cache $RES -o final-4k/video4-4k-raw.mp4 > final-4k/render.log 2>&1
  [ -s final-4k/video4-4k-raw.mp4 ] || { log "PASSO 5 FALLITO: $(tail -c 400 final-4k/render.log)"; exit 5; }
fi
log "PASSO 5 ok: $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate:format=duration -of csv=p=0 final-4k/video4-4k-raw.mp4 | tr '\n' ' ')"
python $SK/scripts/mix-audio.py --index build/public/index-sound.html --voice proxy/flat-1080p.mp4 --video final-4k/video4-4k-raw.mp4 --out final-4k/video4-4k-mix.mp4 --music $SK/assets/music/licensed/bed-video4.mp3 --music-db -10 --stems stems > final-4k/mix.log 2>&1 || { log "PASSO 6 mix FALLITO: $(tail -3 final-4k/mix.log)"; exit 6; }
ffmpeg -y -v error -i final-4k/video4-4k-mix.mp4 -c copy -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart final-4k/VIDEO4-FINALE-4K.mp4 || { log "tag FALLITO"; exit 6; }
python $SK/scripts/sound-report.py --stems stems --index build/public/index-sound.html --final final-4k/VIDEO4-FINALE-4K.mp4 --out final-4k/SOUND-REPORT.md > /dev/null 2>&1
python $SK/scripts/verify-render.py --render final-4k/VIDEO4-FINALE-4K.mp4 --index build/public/index-sound.html --res 3840x2160 --out final-4k/VERIFY.md > final-4k/verify.log 2>&1; log "verify-render exit $?"
log "PASSO 6 ok: FINITO final-4k/VIDEO4-FINALE-4K.mp4 $(ls -la final-4k/VIDEO4-FINALE-4K.mp4 | awk '{print $5}') byte"
