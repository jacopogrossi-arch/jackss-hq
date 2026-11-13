#!/bin/bash
# finish.sh: dalla pagina page/ al video finito. Ogni passo si salta se il suo file esiste già (si può rilanciare dopo un'interruzione).
# Uso: bash finish.sh draft   -> render2/draft.mp4 (30 fps, voce + musica) + qa
#      bash finish.sh final   -> autogrill-serpentone-v2.mp4 (1080p 60 fps, BT.709) + copia leggera se > 28 MB
set -e
cd "D:/videoeditor/autogrill"
SK="D:/ClaudeCodeTest/.claude/skills/youtube-edit"
MUSIC="$SK/assets/music/licensed/es-disque-magique.mp3"
mkdir -p render2
mix() {  # $1 video muto -> $2 con voce, effetti e musica (guadagno fisso, vedi mix.py)
  [ -s "$2" ] && return 0
  PYTHONIOENCODING=utf-8 python mix.py "$1" "$2" "$MUSIC"
}
if [ "$1" = "draft" ]; then
  [ -s render2/draft-raw.mp4 ] || npx hyperframes render page --quality draft --resolution 1080p --fps 30 --workers 4 -o render2/draft-raw.mp4
  mix render2/draft-raw.mp4 render2/draft.mp4
  PYTHONIOENCODING=utf-8 python "$SK/scripts/qa-motion.py" --video render2/draft.mp4 --out render2/qa-draft || echo "QA: vedi render2/qa-draft/qa-motion.md"
elif [ "$1" = "final" ]; then
  [ -s render2/final-raw.mp4 ] || npx hyperframes render page --quality high --resolution 1080p --fps 60 --workers 4 -o render2/final-raw.mp4
  mix render2/final-raw.mp4 render2/final-mix.mp4
  [ -s autogrill-serpentone-v2.mp4 ] || ffmpeg -y -v error -i render2/final-mix.mp4 -c copy -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart autogrill-serpentone-v2.mp4
  PYTHONIOENCODING=utf-8 python "$SK/scripts/qa-motion.py" --video autogrill-serpentone-v2.mp4 --out render2/qa-final || echo "QA: vedi render2/qa-final/qa-motion.md"
  SZ=$(stat -c %s autogrill-serpentone-v2.mp4)
  if [ "$SZ" -gt 28000000 ] && [ ! -s autogrill-serpentone-v2-leggero.mp4 ]; then
    ffmpeg -y -v error -i autogrill-serpentone-v2.mp4 -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a copy -movflags +faststart autogrill-serpentone-v2-leggero.mp4
  fi
  ls -la autogrill-serpentone-v2*.mp4
fi
