#!/bin/bash
# renders every prove/* page at 1080p, then stitches each Prima|Dopo pair side by side (960x540 each on a 1920x1080 canvas)
cd /d/ClaudeCodeTest/videos/_bench/video-3d-moda/prove
for d in */; do
  n=${d%/}
  npx --yes hyperframes@0.9.35 render "$n" -q looks -o "$n.mp4" --quiet > "$n.log" 2>&1
  echo "$n done $?"
done
for pair in 01-veneziana 03-motion-blur 04-profondita; do
  ffmpeg -v error -y -i $pair-prima.mp4 -i $pair-dopo.mp4 -filter_complex "[0:v]scale=960:540[a];[1:v]scale=960:540[b];[a][b]hstack=2,pad=1920:1080:0:270:color=0x14100c[v]" -map "[v]" -c:v libx264 -crf 18 -pix_fmt yuv420p $pair-PRIMA-DOPO.mp4
done
cp 02-passaggi-dopo.mp4 02-passaggi.mp4
echo ALL DONE
