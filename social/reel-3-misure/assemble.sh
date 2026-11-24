#!/usr/bin/env bash
# Montaggio del Reel «Le 3 misure»: fotogrammi + finitura (bloom, vignetta, grana) + sottotitoli parola per parola (captions.py) + flash sui tagli + voce.
# Uso: bash assemble.sh FRAMES_DIR OUT.mp4 [LARGHEZZA]   (540 anteprima, 1080 finale)
set -e
FR=$1; OUT=$2; WID=${3:-540}; HGT=$((WID * 16 / 9))
G=/d/ClaudeCodeTest/videos/_bench/reel-3-misure; VO=$G/vo/vo.wav
POST="format=gbrp,split[a][b];[b]curves=all='0/0 0.75/0 1/1',gblur=sigma=$((WID / 38))[g];[a][g]blend=all_mode=screen:all_opacity=0.08,vignette=angle=PI/7,curves=all='0/0 0.25/0.21 0.75/0.79 1/1',noise=alls=4:allf=t+u,format=yuv420p"
# flash caldo sui tagli: tempo:intensita' (decade in 3 passi ~0.2 s). Il taglio a 3.24 e' quello forte.
FL=""; for c in "3.24:0.95" "6.75:0.40" "12.38:0.40" "18.12:0.40" "23.15:0.40" "29.33:0.40"; do
  t=${c%%:*}; a=${c##*:}
  for step in "0.00:0.05:1.0" "0.05:0.11:0.55" "0.11:0.20:0.25"; do
    IFS=: read -r s0 s1 k <<< "$step"
    FL+=",drawbox=x=0:y=0:w=iw:h=ih:color=0xFFE9C8@$(python -c "print(round($a*$k,3))"):t=fill:enable='between(t,$(python -c "print(round($t+$s0,3))"),$(python -c "print(round($t+$s1,3))"))'"
  done
done
ffmpeg -v error -y -framerate 24 -start_number 1 -i "$FR/f%04d.png" -framerate 24 -start_number 1 -i "$G/caps/c%04d.png" -i "$VO" \
  -filter_complex "[0:v]${POST}[v0];[1:v]scale=$WID:$HGT,format=rgba[cp];[v0][cp]overlay=0:0:format=auto${FL}[v];[2:a]loudnorm=I=-14:TP=-1.5:LRA=9[au]" \
  -map "[v]" -map "[au]" -t 32.75 -c:v libx264 -preset slow -crf 19 -c:a aac -b:a 160k "$OUT"
ls -la "$OUT"
