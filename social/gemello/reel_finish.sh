#!/usr/bin/env bash
# Finitura del Reel (23/11/2026): post + versione telefono + clip di controllo del labiale.
# Uso: bash reel_finish.sh NOME T0 DUR [FACE_CROP]
#   NOME = cartella dei PNG in videos/_bench/reel-tessuto/NOME (f%04d.png, primo numero = T0*24+1), T0/DUR in secondi nella voce montata
#   FACE_CROP = w:h:x:y del viso nel fotogramma 1080x1920 (default 760:760:160:150)
# Scrive: NOME.mp4 (master crf 15), NOME-telefono.mp4 (crf 22, < 30 MB per Remote Control), NOME-labiale.mp4 (viso + onda + metà velocità)
set -e
N=$1; T0=$2; DUR=$3; CROP=${4:-760:760:160:150}
G=/d/ClaudeCodeTest/videos/_bench/reel-tessuto
VO=$G/vo/vo.wav
FONT=$G/font.ttf   # copia locale: il percorso con "C:" rompe drawtext
[ -f $FONT ] || cp /d/ClaudeCodeTest/videos/_bench/gemello/font.ttf $FONT
cd $G
S=$(python -c "print(int(round($T0*24))+1)")
POST="format=gbrp,split[a][b];[b]curves=all='0/0 0.75/0 1/1',gblur=sigma=28[g];[a][g]blend=all_mode=screen:all_opacity=${BLOOM:-0.12},vignette=angle=${VIG:-PI/7},curves=all='${CURVE:-0/0 0.25/0.21 0.75/0.79 1/1}',noise=alls=6:allf=t+u,format=yuv420p"
# 1) master: post come finish.sh del gemello + voce della finestra, loudnorm leggero
ffmpeg -v error -y -framerate 24 -start_number $S -i $N/f%04d.png -ss $T0 -t $DUR -i $VO -filter_complex "[0:v]${POST}[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=9[au]" \
  -map "[v]" -map "[au]" -t $DUR -c:v libx264 -preset slow -crf 15 -c:a aac -b:a 192k $N.mp4
# 2) telefono (< 30 MB)
ffmpeg -v error -y -i $N.mp4 -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k $N-telefono.mp4
# 3) labiale: viso ingrandito, onda audio sotto, una volta a velocita' reale e una a meta' (voce a meta' velocita' con atempo)
ffmpeg -v error -y -i $N.mp4 -filter_complex "[0:v]crop=$CROP,scale=720:720,setsar=1[f];[0:a]showwaves=s=720x140:mode=cline:colors=white:rate=24[w];[f][w]vstack[v1];[v1]split[a][b];[b]setpts=2*PTS[bs];[a][bs]concat=n=2:v=1:a=0[v];[0:a]asplit[x][y];[y]atempo=0.5[ys];[x][ys]concat=n=2:v=0:a=1[au]" \
  -map "[v]" -map "[au]" -c:v libx264 -crf 20 -c:a aac $N-labiale.mp4
ls -la $N.mp4 $N-telefono.mp4 $N-labiale.mp4
