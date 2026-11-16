# HANDOFF — Blender trouser v10 (started 16/11/2026, long autonomous job)

Jacopo approved the Short #3 script, but says the trouser "is not there yet". He gave up to 10 hours to make it much better, mainly with Blender. Goal: the critic judge scores >= 8/10 against the Gemini target `.critic/target.png` (prompt in `.critic/target_prompt.txt`).

## Why v10 (not more v9 tuning)
v9 = loft -> 5.5 mm voxel remesh -> cloth. The voxels round every sharp feature: the crease and pleats are barely visible, there is a bulge at the fly and the turn-ups are lumpy (critic 3/10).

## v10 plan (script `videos/_bench/fashion3d/blender/build_trouser10.py`, copy in `scripts/blender_trouser10.py`)
1. Build a quad mesh directly with the classic trouser topology (two leg tubes that merge at the crotch into one hip tube). It has columns placed exactly on the front/back creases, the pleat folds and the fly edge, so these can carry subdivision edge creases.
2. A hidden mannequin collider (legs + hips) gives the trouser a body, like the target's stand. Cloth sim pinned at the waist.
3. Sharp edges come from Subdivision (viewport 1 for the glb, render 2 for Cycles) with edge creases. Ridges are reinforced after the sim.
4. Details reused from v9: waistband, loops, adjusters, J-fly, pockets, welts. Cuffs are rebuilt as smoothed rings.
5. Judge with a Cycles still (`render_target.py`) AND the engine (`lab_target.py`), with a Sonnet judge on side-by-side images.

## Status log (update at every step)
- 16/11 v10 started: HANDOFF written.
- 16/11 v10b: topologia a quad OK (niente scalino al cavallo: l'ellisse del bacino rientra solo al centro davanti/dietro), manichino con vuoto tra le gambe, sim ~80 s con bacino bloccato (pin z 0.70-0.84) e bending 25. Pinces con profilo a gradino, cintura liscia (band smooth=8), tasche e risvolti piu' sottili. Colore #4b5134 (il render era 2,5x troppo chiaro: in Cycles usare EXPOSURE -1.2). Runner: `videos/_bench/fashion3d/blender/run10.py` (build+render+foglio). Render Cycles "hero" 768x1344 in 6 s. Prossimo: voto del giudice (round3), poi lab_target.py col glb nuovo.
- 16/11 round 3 giudice (Sonnet): 4/10 (composizione 1.5, luce 0.5, materiali 1.5, dettagli 0.5). Fatto dopo: colore #4d4a22, roughness 0.82 + sheen 0.4, bump twill 0.3, key piu' laterale (420) e fill 6, Cycles EXPOSURE -1.2 (round5.jpg: colore ora vicino). DA FARE: bordo superiore della cintura seghettato (passanti/pinces), tasche che galleggiano, pinces ancora poco leggibili, patta piatta, gamba piu' conica, prospettiva 3/4 dall'alto, poi nuovo voto e lab_target.py col glb.

## Ricerca tutorial (16/11, richiesta di Jacopo: "informati a 360 gradi")
Le ricerche web danno poco di operativo; i punti utili:
- Cloth (Blender Artists, "tailor's approach"): pezzi di cartamodello piani a scala 1:1 ~10k facce, cuciti con sewing e lasciati avvolgere il corpo; preset Denim per i pantaloni; collisione oggetto 5 mm, self-collision 2 mm; speed multiplier 0.5; dopo la sim unire i vertici di cucitura e lisciare a mano. Alternative: add-on Modeling Cloth (stile Marvelous Designer), Marvelous Designer per pinces/pieghe poi retopo + subdivision in Blender, scultura delle pieghe (pose brush).
- Tessuto (guide V-Ray/Arnold, valgono per Cycles): sheen sottile, tinta appena piu' chiara della base, largo e morbido per lana/feltro; pilotare lo sheen con rumore o mappa della trama; con luce frontale piatta lo sheen sparisce -> serve area light grande laterale. Twill = trama piu' comune (jeans, drill).
- Scena/luce: lampada calda ~3800 K (blackbody) debole; l'eroe deve restare il piu' illuminato (niente sole caldo che ruba l'attenzione); volumetrica/god rays solo se serve (render molto piu' lunghi); DOF con "focus on object"; fotogramma cinematografico mai nitido ovunque.
- Test A/B 16/11: stesso glb v10 nel motore three.js (lab_target10.py) vs Blender Cycles: il motore da' atmosfera di scena (lampada con alone, scaffali, parquet) ma il capo e' troppo scuro/marrone; Blender da' la geometria/pieghe ma lo sfondo e' vuoto. Idea: combinare (capo Blender + scena motore).
