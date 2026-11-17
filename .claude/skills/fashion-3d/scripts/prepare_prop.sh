#!/bin/bash
# Prepara un GLB arrivato da Tripo per il motore: (1) decomprime EXT_meshopt se serve, (2) alleggerisce (decimazione + texture), (3) fa 4 viste di controllo.
# Uso: bash prepare_prop.sh input.glb cartella_output [triangoli=100000] [texture_px=2048]
# Richiede: Blender 5.1, Node/npx (gltf-transform si scarica da solo).
set -e
IN="$1"; OUT="$2"; TRIS="${3:-100000}"; TEX="${4:-2048}"
BL="C:/Program Files/Blender Foundation/Blender 5.1/blender.exe"; SK="D:/ClaudeCodeTest/.claude/skills/fashion-3d/scripts"
mkdir -p "$OUT"; NAME=$(basename "$IN" .glb)
cp "$IN" "$OUT/$NAME-orig.glb"
if grep -a -q "EXT_meshopt_compression" "$IN"; then
  echo "decomprimo meshopt..."; (cd "$OUT" && npx -y @gltf-transform/cli@4.1.1 copy "$NAME-orig.glb" "$NAME-dec.glb"); SRC="$NAME-dec.glb"
else SRC="$NAME-orig.glb"; fi
echo "alleggerisco a $TRIS triangoli..."
"$BL" -b -P "$SK/blender_optimize_glb.py" -- "$OUT/$SRC" "$OUT/$NAME-opt.glb" "$TRIS" "$TEX" 2>&1 | grep -E "triangoli|salvato|Error" || true
mkdir -p "$OUT/viste"
"$BL" -b -P "$SK/blender_views4.py" -- "$(cd "$OUT" && pwd -W 2>/dev/null || pwd)/$NAME-opt.glb" "$(cd "$OUT" && pwd -W 2>/dev/null || pwd)/viste" 2>&1 | grep -E "bbox" || true
ffmpeg -v error -y -i "$OUT/viste/v_a.png" -i "$OUT/viste/v_b.png" -i "$OUT/viste/v_c.png" -i "$OUT/viste/v_d.png" -filter_complex "hstack=4,scale=1600:-1" "$OUT/viste/foglio.png"
echo "FATTO: $OUT/$NAME-opt.glb  (viste: $OUT/viste/foglio.png)"
