#!/usr/bin/env bash
# Finitura FINALE del Reel (versione narratore, 24/11/2026): post + plate + voce + swish sui tagli.
# Uso: bash reel_final.sh CARTELLA_PNG NOME [T0 DUR]   (CARTELLA_PNG relativa a videos/_bench/reel-tessuto, PNG f%04d.png dal fotogramma T0*24+1)
# Scrive videos/_bench/reel-tessuto/NOME.mp4 (master crf 15) e NOME-telefono.mp4 (crf 22). Il piano dei tagli e delle plate sta qui sotto: cambia la partitura = cambia qui.
set -e
D=$1; N=$2; T0=${3:-0}; DUR=${4:-16.04}
G=/d/ClaudeCodeTest/videos/_bench/reel-tessuto
SF=/d/ClaudeCodeTest/.claude/skills/youtube-edit/assets/sfx/licensed
[ -f $G/font.ttf ] || cp /d/ClaudeCodeTest/videos/_bench/gemello/font.ttf $G/font.ttf
cd $G
S=$(python -c "print(int(round($T0*24))+1)")
# --- audio: voce + swish; ogni swish parte (picco - t) prima del taglio cosi' il picco cade SUL taglio. Mai suoni sul parlato.
# soft-clean picco 0.73 s, medium-transition picco 0.86 s (misurati 24/11)
CUTS="2.80:soft 5.20:med 6.60:soft 8.95:soft 9.60:soft 11.40:med"
IN="-i vo/vo.wav"; FC="[1:a]aresample=44100,apad=whole_dur=$DUR[vo]"; MIX="[vo]"; k=2   # ingresso 0 = fotogrammi, 1 = voce, 2.. = swish
for c in $CUTS; do
  t=${c%%:*}; kind=${c##*:}
  if [ $kind = soft ]; then f=$SF/es-whoosh-soft-clean.mp3; pk=0.73; vol=0.20; else f=$SF/es-whoosh-medium-transition.mp3; pk=0.86; vol=0.26; fi
  ms=$(python -c "print(max(0,int(round(($t-$pk)*1000))))")
  IN="$IN -i $f"
  FC="$FC;[$k:a]atrim=0:1.6,afade=t=out:st=1.2:d=0.4,volume=$vol,aresample=44100,adelay=$ms|$ms[s$k]"
  MIX="$MIX[s$k]"; k=$((k+1))
done
FC="$FC;${MIX}amix=inputs=$((k-1)):normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=9[au]"
# --- video: post come finish.sh del gemello + plate (gesso su ruggine) con dissolvenza in/out
POST="format=gbrp,split[a][b];[b]curves=all='0/0 0.75/0 1/1',gblur=sigma=28[g];[a][g]blend=all_mode=screen:all_opacity=${BLOOM:-0.12},vignette=angle=${VIG:-PI/7},curves=all='${CURVE:-0/0 0.25/0.21 0.75/0.79 1/1}',noise=alls=6:allf=t+u,format=yuv420p"
plate() { # testo t0 t1 y
  echo ",drawtext=fontfile=font.ttf:text='$1':fontsize=170:fontcolor=0xEDE6D6:box=1:boxcolor=0xB5532B@0.93:boxborderw=30:x=(w-text_w)/2:y=$4:enable='between(t,$2,$3)':alpha='min(1,(t-$2)/0.12)*min(1,($3-t)/0.15)'"
}
PL="$(plate '×2' 10.40 11.35 h*0.74)$(plate '€0' 13.15 14.60 h*0.74)"
ffmpeg -v error -y -framerate 24 -start_number $S -i $D/f%04d.png $IN -filter_complex "[0:v]${POST}${PL}[v];${FC}" \
  -map "[v]" -map "[au]" -t $DUR -c:v libx264 -preset slow -crf 15 -c:a aac -b:a 192k $N.mp4
ffmpeg -v error -y -i $N.mp4 -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k $N-telefono.mp4
ls -la $N.mp4 $N-telefono.mp4
