#!/bin/bash
# Short #11: build -> render bozza 1080p 30 fps -> mix -> mux -> fogli di revisione a 10 fps. Uso: bash run.sh [nome]
set -e
N=${1:-draft}
cd "D:/ClaudeCodeTest/social/short-11-pantalone-3d/v1"
python -I build.py > /dev/null
python mix.py | tail -1
W="D:/ClaudeCodeTest/videos/_bench/short11"
rm -rf "$W/comp" "$W/renders/$N-raw.mp4"; cp -r comp "$W/comp"
cd "$W"
TMP="D:\hf-tmp" TEMP="D:\hf-tmp" TMPDIR="D:\hf-tmp" npx hyperframes@0.9.35 render comp --quality draft --fps 30 --workers 3 -o renders/$N-raw.mp4 --quiet > renders/render.log 2>&1
ffmpeg -y -v error -i renders/$N-raw.mp4 -i renders/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart renders/$N.mp4
ffmpeg -v error -ss 35 -i renders/$N.mp4 -f null -
rm -rf review; python D:/ClaudeCodeTest/.claude/skills/fashion-3d/scripts/review8.py sheets renders/$N.mp4 review | tail -1
echo FATTO
