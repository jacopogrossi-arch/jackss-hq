#!/bin/bash
set -e
cd "D:/ClaudeCodeTest/videos/_bench/short3e"
NAME=short3-sala-campioni-v7
rm -f renders/final-raw.mp4 "$NAME.mp4"
TMP="D:\hf-tmp" TEMP="D:\hf-tmp" TMPDIR="D:\hf-tmp" npx hyperframes@0.9.35 render comp --quality high --fps 60 --workers 4 -o renders/final-raw.mp4 --quiet
ffmpeg -y -v error -i renders/final-raw.mp4 -i renders/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart renders/final-mix.mp4
ffmpeg -y -v error -i renders/final-mix.mp4 -c copy -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart "$NAME.mp4"
ffmpeg -v error -ss 63 -i "$NAME.mp4" -f null -
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration,size -of default=nw=1 "$NAME.mp4"
mkdir -p "/c/Users/Jacopo Grossi/iCloudDrive/Video 3D moda"
cp "$NAME.mp4" "/c/Users/Jacopo Grossi/iCloudDrive/Video 3D moda/$NAME.mp4"
echo DONE
