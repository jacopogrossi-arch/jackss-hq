# 3D taste notes (moved from youtube-edit/references/taste.md on 16/11/2026)

Jacopo's verdicts on the 3D worlds and Shorts, in the order they were given. Read before building any 3D Short or explainer.

## 3D worlds: Jacopo's verdict (14/11/2026, on the first 3D fashion video)
- **Keep:** motion blur on the whips, depth of field on close shots, the camera moves. The UX proposals (arcs, follow-through, frequency of use, word-to-effect delay) are all OK; arcs nearly linear.
- **Never:** venetian-blind light (reads as a render error; only a real window with a real cross is allowed), the ink/"disegno" pass as a published look (not good enough), an empty room, a trouser standing like two tubes.
- **Do:** a dense, cartoon-but-real room in the autogrill way (many props in every shot, real daylight through a window, pendants with halos), a trouser with pockets, loops, fly and creases hung on a hanger, a camera tour between stations, cuts every 2-3 s, and a layer of sound effects (whip, label tick, chapter riser, material sounds) because silence kills retention.

## 3D Short "primo pantalone": Jacopo's notes on proof 1 (14/11/2026)
"Continuano così che quasi ci siamo." The direction is right; the bar is REALISM: the more correct details, the better the result.
- **Garments look like real garments.** Tailored trousers have NO contrast top-stitching on the side seams, inseam or hem (blind hem). Thread is tone-on-tone. Pockets read OPEN (a dark mouth with the front edge standing proud and a bar-tack at each end), never as a stitched-shut line. A hung trouser is flat front-to-back: no puffy hips or waist. Toile marks are the real ones (grain line, hip line, knee line), not random strokes.
- **Every action must be legible.** A tool never "moves at random": shears cut ALONG a drawn outline, with the cut appearing behind the blades. Pin a label on what the voice names (grain line, notch).
- **No empty beats.** A shot of a blank sheet or an empty table is a retention hole. Start the action as the cut lands.
- **Transitions.** A film burn / light leak with a whoosh on the hook-to-story cut (`World3D.leak(t, d)`, sounds `es-whoosh-medium-transition` + `es-film-advance-wind`).
- **Captions** need a soft dark pill so they read on white paper. Labels in 9:16 need about 56 px.
- **End card = the real logo** (`logoplate`, the paths of `inverso/logo/inverso-logo.svg`), not typed text.
- **The background counts too.** Spools stand upright, plant leaves hang on stalks, folded cloth has weave and a rolled fold. Anything that reads as a primitive box gets fixed.

## 3D Shorts: the detailed atelier method + the autogrill method (14/11/2026)
For Shorts, use the detailed "primo pantalone" world (realism) together with the autogrill workflow (`explainer-3d-sop.md`). Both are the default from now on.
- **Text on screen for the WHOLE video** ("sui reel fa tanto la differenza"). Word captions (`captions`) alternate with big statements (`big()`: title, numbers, the moral, the CTA). A big statement replaces the captions it overlaps. Each caption and big holds until the next text arrives, so there is no gap even in the pauses. Check with a script that the gap list is empty and no spoken word is uncovered.
- **The voice needs emotion.** Generate the cloned voice ONE PARAGRAPH AT A TIME with expressive punctuation (… ! ?), then join the paragraphs with 0.35–0.55 s gaps. A single long take came out flat.
- **Sound** follows the autogrill rules: an opening whoosh + hit, a riser peaking on the punch word, story events, automatic pops/swishes/whooshes at least 0.35 s apart, music 13 dB under the voice measured in LUFS, fixed gain to −16 LUFS.
- **Render** with `finish.sh`: a 30 fps draft with QA that Jacopo listens to (a contact sheet does not show the sound), then the 60 fps final with BT.709 tags, a version number in the name and a light copy. Before the draft, check for flicker across 3 consecutive frames.
- **Big statements stay modest in 9:16:** about 76–82 px (a number-punch like «117 cm» up to ~96). ONE line, TWO at most: three lines "non mi piace". A longer sentence becomes two statements in a row, or the tail goes back to the captions. At 100–175 px Jacopo found them "veramente troppo grosso"; the look must stay close to the captions.
- **Labels must not sit on the caption band** (y ≈ 1180 in 9:16) or cross the frame edge. Check them on the contact sheet.

## Short "primo pantalone" v3 vs Autogrill v2.2: why the Autogrill is better (14/11/2026)
Jacopo, on v3: "ce lo facciamo andare bene, però il risultato non mi fa impazzire… quello dell'autogrill rimane molto, molto meglio: i tempismi, la canzone di sottofondo, tutto". Measured differences, to fix on Short #2:
- **Change of view.** The Autogrill has 17 real changes of view in 93 s (exterior, aerial plan, road, macro on the shelves). The Short has 2: the same warm atelier at a medium distance, joined by blurred whips. Next time vary the SCALE: wide/aerial ↔ macro, and use a different place or angle for each paragraph.
- **A visual device that explains.** The Autogrill draws the dotted red path on the plan and runs a live counter («prodotti che ti passano davanti: 485»). The Short only shows objects. Each Short needs at least one diagram-like moment, for example the correct outline drawn over the wrong one, or 117 cm against the right measure.
- **Palette and contrast.** The Autogrill is bright and saturated (red, green, white). The Short is all beige and warm, so on a phone it reads flat. Keep a strong contrast colour in every shot.
- **Timing.** The Autogrill adds a pause after the words that close a paragraph (`BREAKS`, 0.4–1.1 s), and the view changes inside that pause. The Short joins the voice paragraphs with fixed gaps and does not cut on them.
- **Music.** It gets chosen against the edit (energy and bpm that match the cuts), not just as "a new track".

## Review frame by frame before the 4K (Short v4, 13/11/2026)
Jacopo: "prima di mandare il 4K… ti fai tutti i frame, 10 per secondo… capisci se c'è qualcosa che non va". He also means any physical or logical mistake, not only flicker.
- **Always do a 10 fps review of the draft before the final.** Extract the frames with `ffmpeg -vf "fps=10,scale=240:-2,drawtext=…pts…,tile=8x4"` into contact sheets of 3.2 s each and look at ALL of them. Then fix, snapshot the times you changed, and only after that render the 4K.
- **The physics must hold.** A tape measure wraps AROUND the garment and turns with it, so it never goes into the fabric. A marker (chalk, dot, pin) must sit ON an object, never float in the air. A dotted outline hugs the garment it explains and does not cross other things (dress forms, the floor).
- **The camera never goes through objects.** Before a fly to the aerial map, the pendant lamps fade out (`pendant(hide=[[t0,t1]])`); going through one gave the "flicker".
- **Every element of the aerial map is on screen before the dive.** Labels go near their badge without covering each other, the caption band or the frame edge.
- **Tools follow the path smoothly.** The shears turn at a corner by averaging the direction over ±8 points, never in a single 90° step.
- **Stale renders.** If a render was stopped, kill the hyperframes processes and DELETE `draft-raw.mp4` before re-rendering, then check the timestamp: `finish.sh` skips the render when the file already exists.

## Short v4 → v5: Jacopo's frame-by-frame notes (13/11/2026)
- **A live counter moves on with each PHASE, not with a word that comes later.** The cost pill read "niente" all through the pattern and "un foglio di carta" all through the toile, so at 52 s it contradicted the big statement. The rule: drawing = niente, pattern = paper (from "carta"), toile = cloth (from "tela").
- **No double text.** When a 3D label and the caption say the same thing at the same moment ("Gamba dritta" / "gamba dritta"), the label comes in 0.8 s later, once the caption has moved on, or it is dropped.
- **The hook must show the claim in the first frame.** "Sembrava una gonna" over a toile seen from the front doesn't read: open at 3/4, on the side where the volume is.

## Short #2, built alone overnight (13/11/2026): what the reviews caught
- **A new world for every Short, the same language.** Short #1 = the atelier by day; Short #2 = the Inverso studio at night (bosco walls, terrazzo, a black steel window on Rome, warm pendants). The map, the macros, the pinned labels and the phase pill stay the same; the objects change.
- **The 9:16 frame is tall: build words vertically.** A horizontal row of letter cubes did not fit; a vertical totem does, and it can turn on its axis.
- **Garments on a rail face the camera, or they read as planks.** Fan them about 45° (`fastrail` `fan`).
- **A hero garment hangs from the rail, not from the ceiling.** No long cord (`hang` ≈ 0).
- **Primitives that read as something else are worse than nothing.** An extruded sneaker looked like a stapler; a lofted one (footprint sole + superellipse sections + laces + collar) reads as a shoe.
- **Text on 3D surfaces: check it by eye in a snapshot.** Each mirroring is a guess until the frame says otherwise: a label seen from the reverse needed a 180° turn, not a mirror. The same goes for a logo on a cylinder cap.
- **Map badges and paths live only in the map.** Give every aerial map its own set (show at the arrival, out at the dive); never leave them on the floor during close shots.
- **Light patches through the window burn out a top-down diagram.** Put the diagram outside them, on a dark rug, and end with a push-in on the result ("Inverso" in the middle).
- **Rows of objects in 9:16: shoot them at 3/4**, so the row recedes and the boxes stay large.
- **Nothing important under the phase pill or the caption band**, including the ends of a diagram.

## Jacopo's review of Short #2 (14/11/2026)
- **The hero objects get the modelling hours.** The garment, and above all its inside, is what makes the reel. An object that reads as "a piece of fabric with a seam" fails, even in a good scene. It must read at first glance as the real thing: a whole pair of trousers, with waistband, belt loops, welt pockets, centre-back seam, two legs, the crease and the hems. It also needs real textile surface: soft folds, edges dropping onto the table, fabric sheen, and seam and stitch relief at about 2 px/mm. Spend the extra hours there, not on the room.
- **Open on the logo, not on a word.** The brand mark must be the first thing seen, so people remember it. In Short #2 this is a black lacquered sign with the cream Inverso logo in a steel swing frame: it starts upside down and flips upright on «Inverso».
- **Pops only when something appears on screen**: one soft pop per card as it lands, never a multi-pop burst.
- **Risers:** use `cc-riser-lungo` (Autogrill, Short #1). `al-charge-riser` is rejected ("bruttissimo").
- **Card text** shrinks to fit its card. Check that every card is fully inside the frame on the shot where it appears.

## Blender trouser test (16/11/2026)
- Jacopo, on the 3-way comparison (engine `trouserHi` / Blender glb in the engine / Blender Cycles): **the Blender glb in the engine "sembra molto più un pantalone"** because of the real drape and folds, despite the plastic look and defects. Bet on the Blender garment: simulated folds beat a cleaner procedural surface. Fix the plastic look (roughness, no specular shine, baked twill texture), keep the folds.
- Front slanted pockets modelled as a dark tube + a cord on top: **"bruttissime, sembrano un filo spesso sopra"**. A pocket opening is a flat folded edge of the same cloth with a thin shadow gap behind it.

## Short #3 v2 (sala campioni), review di Jacopo 17/11/2026
- **Voce: usare `eleven_v4`, MAI `eleven_v3`.** Con "Jacopo Prova" (0CeJTHP08UsLHht7KIni) v4 ha timbro e vivacita' dello Short #2 (misurato: F0 ~148 Hz, distanza MFCC 15); v3 e' piu' grave e lontana (100 Hz, distanza 46) e a Jacopo "non somiglia e non e' espressiva". Prima di rigenerare un paragrafo confronta un campione con la voce dello Short #2 (script: confronto F0 + MFCC con librosa).
- **Niente "pop", mai** (regola gia' in sound.md): per carte/etichette che appaiono solo swish morbidi (`es-swish-classic-filter`, `es-whoosh-soft-resonant`, `es-whoosh-generic-air`). Jacopo ha sentito i pop (`es-pops6`) a 0:10, 0:23, 0:35, 0:53 e li ha bocciati.
- **Non riusare l'apertura di un altro Short** (il logo che gira era gia' nello Short #2): aprire con un'altra immagine forte (qui il pantalone appeso con "€ ?"); il logo va alla fine.
- **Una plate col prezzo entra quando il prezzo viene DETTO e resta visibile almeno 1,2 s** (non prima, non via subito): se serve, allungare la pausa della voce prima del cambio di scena.
- **CTA chiara: dire COSA si riceve** ("scrivi PANTALONE e ti dico il prezzo finale"), non "il prossimo tiro".
- **Un oggetto 'appeso' ha la stampella** (gancio, barretta, due pinze).
- **Jacopo in miniatura: SI', ma non il cartoon.** Busto di cartone con la sua foto vera (tipo sticker con bordo bianco) che sta sui tavoli e saltella sulle parole che dice. Nuovo tipo di oggetto del motore: `w.standee(oid, pos, "img/me.png", w=...)` (PNG con alpha). Il ritaglio si fa con GrabCut da un fotogramma del girato (rect + maschera), foto solo in locale (repo pubblico).
