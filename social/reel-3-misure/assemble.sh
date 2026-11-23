#!/usr/bin/env bash
# Montaggio del Reel «Le 3 misure»: fotogrammi + finitura (bloom, vignetta, grana) + plate PNG con dissolvenza + voce.
# Uso: bash assemble.sh FRAMES_DIR OUT.mp4 [LARGHEZZA]   (LARGHEZZA = larghezza dei fotogrammi: 540 anteprima, 1080 finale)
set -e
FR=$1; OUT=$2; WID=${3:-540}; HGT=$((WID * 16 / 9))
G=/d/ClaudeCodeTest/videos/_bench/reel-3-misure; P=$G/plates; VO=$G/vo/vo.wav
POST="format=gbrp,split[a][b];[b]curves=all='0/0 0.75/0 1/1',gblur=sigma=$((WID / 38))[g];[a][g]blend=all_mode=screen:all_opacity=0.10,vignette=angle=PI/7,curves=all='0/0 0.25/0.21 0.75/0.79 1/1',noise=alls=4:allf=t+u,format=yuv420p"
# nome:inizio:fine:fade-in:fade-out
PLATES=("p1_gancio:0.2:2.95:1:1" "p2_vita:6.9:8.4:1:1" "p3_x2:10.4:12.0:1:1" "p4_cavallo:12.6:14.5:1:1" "p5_interno:18.2:20.1:1:1" "p6_numeri1:23.4:25.3:1:0" "p6_numeri2:25.3:27.1:0:0" "p6_numeri3:27.1:28.9:0:1" "p7_domanda:29.5:32.7:1:1")
INP=(-framerate 24 -start_number 1 -i "$FR/f%04d.png" -i "$VO"); FC="[0:v]${POST}[v0];"; N=2; LAST=v0; K=0
for pl in "${PLATES[@]}"; do
  IFS=: read -r name a b fi fo <<< "$pl"
  INP+=(-loop 1 -framerate 24 -t 33 -i "$P/$name.png")
  CH="[$N:v]format=rgba,scale=$WID:$HGT"
  [ "$fi" = 1 ] && CH+=",fade=t=in:st=$a:d=0.14:alpha=1"
  [ "$fo" = 1 ] && CH+=",fade=t=out:st=$(python -c "print(round($b-0.14,2))"):d=0.14:alpha=1"
  FC+="${CH}[pl$K];[$LAST][pl$K]overlay=0:0:format=auto:enable='between(t,$a,$b)'[v$((K+1))];"
  LAST=v$((K+1)); N=$((N+1)); K=$((K+1))
done
FC+="[1:a]loudnorm=I=-14:TP=-1.5:LRA=9[au]"
ffmpeg -v error -y "${INP[@]}" -filter_complex "$FC" -map "[$LAST]" -map "[au]" -t 32.75 -c:v libx264 -preset slow -crf 19 -c:a aac -b:a 160k "$OUT"
ls -la "$OUT"
