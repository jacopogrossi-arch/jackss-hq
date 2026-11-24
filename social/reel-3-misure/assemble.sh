#!/usr/bin/env bash
# Montaggio del Reel «Le 3 misure»: fotogrammi + finitura (bloom, vignetta, grana) + sottotitoli parola per parola (captions.py)
# + light leak procedurali sui tagli (leaks.py, blend screen) + voce + effetti sonori Epidemic allineati sul picco di ogni taglio (file solo in locale: videos/_bench/reel-3-misure/sfx/).
# Uso: bash assemble.sh FRAMES_DIR OUT.mp4 [LARGHEZZA]   (540 anteprima, 1080 finale)
set -e
FR=$1; OUT=$2; WID=${3:-540}; HGT=$((WID * 16 / 9))
G=/d/ClaudeCodeTest/videos/_bench/reel-3-misure; VO=$G/vo/vo.wav; SX=$G/sfx
POST="format=gbrp,split[a][b];[b]curves=all='0/0 0.75/0 1/1',gblur=sigma=$((WID / 38))[g];[a][g]blend=all_mode=screen:all_opacity=0.08,vignette=angle=PI/7,curves=all='0/0 0.25/0.21 0.75/0.79 1/1',noise=alls=4:allf=t+u,format=yuv420p"
# effetti: file:istante del taglio:picco nel file (s):guadagno dB
SFX=("big:3.24:0.87:-4" "mid:6.75:0.74:3" "mid:12.38:0.74:3" "mid:18.12:0.74:3" "mid:23.15:0.74:3" "mid:29.33:0.74:3" "small:9.00:0.21:-12" "small:15.10:0.21:-12" "small:20.30:0.21:-12" "small:26.20:0.21:-12")
INP=(-framerate 24 -start_number 1 -i "$FR/f%04d.png" -framerate 24 -start_number 1 -i "$G/caps/c%04d.png" -framerate 24 -start_number 1 -i "$G/leaks/l%04d.png" -i "$VO")
AF="[3:a]loudnorm=I=-14:TP=-1.5:LRA=9[va]"; MIX="[va]"; N=4; K=0
for e in "${SFX[@]}"; do
  IFS=: read -r name tc pk gain <<< "$e"; ms=$(python -c "print(max(0,int(round(($tc-$pk+0.03)*1000))))")
  INP+=(-i "$SX/$name.wav"); AF+=";[$N:a]aformat=sample_rates=44100:channel_layouts=mono,volume=${gain}dB,adelay=${ms}:all=1[s$K]"; MIX+="[s$K]"; N=$((N+1)); K=$((K+1))
done
AF+=";${MIX}amix=inputs=$((K+1)):normalize=0:duration=first,alimiter=limit=0.95[au]"
FC="[0:v]${POST}[v0];[1:v]scale=$WID:$HGT,format=rgba[cp];[v0][cp]overlay=0:0:format=auto,format=gbrp[vb];[2:v]scale=$WID:$HGT,format=gbrp[lk];[vb][lk]blend=all_mode=screen:all_opacity=1,format=yuv420p[v];${AF}"
ffmpeg -v error -y "${INP[@]}" -filter_complex "$FC" -map "[v]" -map "[au]" -t 32.75 -c:v libx264 -preset slow -crf 19 -c:a aac -b:a 192k "$OUT"
ls -la "$OUT"
