#!/usr/bin/env bash
# Finitura dello shot gemello + confronto con la clip AI.
# Uso: bash finish.sh NOME   (legge videos/_bench/gemello/NOME/f%04d.png, scrive NOME.mp4, NOME-vs-ai.mp4 e i fogli a 8 fps)
set -e
N=${1:-v1}
G=/d/ClaudeCodeTest/videos/_bench/gemello
AI=/d/ClaudeCodeTest/videos/_bench/ibrido/video/lipsync-v1.mp4
AUD=/d/ClaudeCodeTest/social/ibrido-jacopino/battuta.mp3
FONT=font.ttf   # copia locale: i percorsi Windows con "C:" rompono il filtro drawtext
cd $G
# 1) post: bloom morbido sulle luci (soglia + sfocatura in modalita' screen), vignettatura, grana in movimento; audio vero (battuta da 4,3 s, poi silenzio)
ffmpeg -v error -y -framerate 24 -i $N/f%04d.png -i $AUD -filter_complex \
 "[0:v]format=gbrp,split[a][b];[b]curves=all='0/0 0.75/0 1/1',gblur=sigma=28[g];[a][g]blend=all_mode=screen:all_opacity=0.22,vignette=angle=PI/5,noise=alls=6:allf=t+u,format=yuv420p[v];[1:a]apad[au]" \
 -map "[v]" -map "[au]" -t 5.042 -c:v libx264 -preset slow -crf 15 -c:a aac -b:a 192k $N.mp4
# 2) affiancato: a sinistra la clip AI (Seedance + lipsync), a destra Blender; audio dello shot gemello
ffmpeg -v error -y -i $AI -i $N.mp4 -filter_complex \
 "[0:v]scale=540:960,setsar=1,drawtext=fontfile=$FONT:text='AI (Seedance)':x=20:y=20:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.5[l];[1:v]scale=540:960,setsar=1,drawtext=fontfile=$FONT:text='Blender (${N})':x=20:y=20:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.5[r];[l][r]hstack[v]" \
 -map "[v]" -map 1:a -t 5.042 -c:v libx264 -crf 18 -c:a aac $N-vs-ai.mp4
# 3) fogli a 8 fps, 24 fotogrammi per foglio (6x4), ogni cella = coppia AI | Blender
mkdir -p review
ffmpeg -v error -y -i $N-vs-ai.mp4 -vf "fps=8,scale=360:-2,tile=6x4:padding=4:color=black" review/$N-8fps-%02d.jpg
ls -la $N.mp4 $N-vs-ai.mp4 review/$N-8fps-*.jpg
