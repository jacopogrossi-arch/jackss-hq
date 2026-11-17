#!/bin/bash
# finish.sh (autogrill method, §9 of references/explainer-3d-sop.md): from comp/ to the finished Short. Each step is skipped if its file already exists (safe to re-run).
# Usage: bash finish.sh draft  -> renders/draft.mp4 (30 fps, voice + sfx + music) + QA   (Jacopo watches this)
#        bash finish.sh final  -> short-primo-pantalone-v3.mp4 (1080x1920, 60 fps, BT.709) + QA + light copy if > 28 MB
set -e
cd "D:/ClaudeCodeTest/videos/_bench/short1"
SK="D:/ClaudeCodeTest/.claude/skills/youtube-edit"
V=v5; NAME="short-primo-pantalone-$V"
mkdir -p renders
[ -s renders/mix.wav ] || PYTHONIOENCODING=utf-8 python -W ignore mix.py
mux() { [ -s "$2" ] || ffmpeg -y -v error -i "$1" -i renders/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$2"; }
if [ "$1" = "draft" ]; then
  [ -s renders/draft-raw.mp4 ] || npx hyperframes@0.9.35 render comp --quality draft --fps 30 --workers 4 -o renders/draft-raw.mp4 --quiet
  mux renders/draft-raw.mp4 renders/draft.mp4
  PYTHONIOENCODING=utf-8 python "$SK/scripts/qa-motion.py" --video renders/draft.mp4 --out renders/qa-draft || echo "QA: see renders/qa-draft/qa-motion.md"
elif [ "$1" = "final" ]; then
  [ -s renders/final-raw.mp4 ] || npx hyperframes@0.9.35 render comp --quality high --fps 60 --workers 4 -o renders/final-raw.mp4 --quiet
  mux renders/final-raw.mp4 renders/final-mix.mp4
  [ -s "$NAME.mp4" ] || ffmpeg -y -v error -i renders/final-mix.mp4 -c copy -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart "$NAME.mp4"
  PYTHONIOENCODING=utf-8 python "$SK/scripts/qa-motion.py" --video "$NAME.mp4" --out renders/qa-final || echo "QA: see renders/qa-final/qa-motion.md"
  SZ=$(stat -c %s "$NAME.mp4")
  if [ "$SZ" -gt 28000000 ] && [ ! -s "$NAME-leggero.mp4" ]; then
    # 2-pass at a fixed bitrate: crf 22 gave 69 MB on a 60 fps Short; 2300k + 160k audio = ~27 MB for 86 s
    ffmpeg -y -v error -i "$NAME.mp4" -c:v libx264 -preset slow -b:v 2300k -pass 1 -passlogfile renders/p2 -an -f mp4 NUL
    ffmpeg -y -v error -i "$NAME.mp4" -c:v libx264 -preset slow -b:v 2300k -pass 2 -passlogfile renders/p2 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 160k -movflags +faststart "$NAME-leggero.mp4"
  fi
  ls -la "$NAME"*.mp4
fi
