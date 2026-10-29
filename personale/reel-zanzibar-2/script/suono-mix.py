"""Sound design del reel 2 (piano approvato da Jacopo 29/10): ambienti veri sotto la canzone che seguono la giornata,
lo splash sul tuffo, bolle sott'acqua, una raffica d'aria + il light leak dorato sul passaggio giorno -> sera (29,13 s).
Versione A = ambienti + leak. Versione B = A + canzone ovattata mentre siamo sott'acqua (19,93-23,5), che si riapre
di colpo sullo stacco della barca. L'audio originale delle clip non si usa: in barca e' tutto vento sul microfono e motore.
Suoni Epidemic Sound in suono/es/ (solo locale). Immagine = zanzibar-reel2_4k_4x3.mp4 (pellicola-oro), non si rigrada.
uso: python -I suono/mix.py   -> suono/zanzibar-reel2_suono-A|B_INSTAGRAM_4x3.mp4 + _telefono.mp4"""
import os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..")
ES = os.path.join(HERE, "es")
SRC = os.path.join(R, "zanzibar-reel2_4k_4x3.mp4")
SWOOSH = os.path.join(R, "..", "..", "..", ".claude", "skills", "youtube-edit", "assets", "sfx", "licensed", "es-swoosh-wide.mp3")
LEAK = os.path.join(R, "..", "..", "..", ".claude", "skills", "youtube-edit", "assets", "packs", "light-leaks", "Light Leaks (5).mp4")
DUR = 36.3
XF = 0.5          # dissolvenza fra un ambiente e l'altro
# (file, da dove leggere nel file, inizio, fine, LUFS). Jacopo 29/10 sulla prima prova: "l'onda" solo sulla prima clip,
# a -32 (musica a -14: ~18 dB sotto); dopo, solo sulle clip di mare, un ALTRO suono di mare "che quasi non si deve sentire".
# Niente palme, niente grilli della sera.
AMB = [("barca", 6, 0, 2.433, -32),          # barca a vela al tramonto: l'onda che gli e' piaciuta
       ("laguna", 12, 5.7, 13.0, -40),       # arco sul mare -> spiaggia -> barca: acqua calma, appena percepibile
       ("motoscafo", 8, 13.0, 16.467, -32),  # il ragazzo che guida la barca: fuoribordo + acqua che corre (Jacopo 29/10)
       ("laguna", 30, 16.467, 19.933, -40),  # laguna
       ("laguna", 60, 23.5, DUR, -40)]       # banco di sabbia -> sera -> silhouette
# "un filo di piu'" (29/10): il mare basso da -43 a -40
# (file, picco nel file, istante del picco nel reel, dB rispetto al suo livello normalizzato)
# Provati sullo stacco laguna -> sott'acqua uno swoosh e tre transizioni visive (zoom con sfocatura, whip orizzontale,
# "tuffo" verticale con lampo): Jacopo 29/10 "forse e' meglio senza transition". Resta lo stacco netto con lo splash.
FX = [("tuffo", 0.65, 19.933, 0),     # entra in acqua: lo stacco sul tuffo e' gia' sott'acqua
      ("sottacqua", 1.30, 21.2, -2),  # bolle e movimento sott'acqua, sotto le due clip subacquee
      ("raffica", 1.20, 29.133, -4)]  # soffio d'aria sul passaggio giorno -> sera (al posto del whoosh)
FX_LUFS = -24     # lo splash ~10 dB sotto la musica
UNDER = (19.933, 23.5)
# transizione visiva laguna -> sott'acqua (Jacopo 29/10, sotto lo swoosh). Lo zoom con sfocatura "non mi piace":
# whip pan "molto dinamico ma elegante". La laguna scivola a sinistra accelerando (6 fotogrammi), la clip subacquea
# entra da destra frenando (7 fotogrammi), velocita' massima sullo stacco. Ogni clip e' affiancata a se stessa, cosi' il
# bordo che scorre resta coperto dalla sfocatura orizzontale (la copia e' specchiata: niente giuntura visibile), piu' forte dove la camera va piu' veloce.
# 498 = primo fotogramma della clip nuova (misurato).
WCUT, WA, WB, WTRAV = 498, 6, 7, 0.45


def _blur(levels):
    return ",".join("avgblur=sizeX=%d:sizeY=1:enable='eq(n,%d)',avgblur=sizeX=%d:sizeY=1:enable='eq(n,%d)'" % (sz, n, sz, n)
                    for n, sz in levels)


def _vblur(levels):
    return ",".join("avgblur=sizeX=1:sizeY=%d:enable='eq(n,%d)',avgblur=sizeX=1:sizeY=%d:enable='eq(n,%d)'" % (sz, n, sz, n)
                    for n, sz in levels)


# Il whip orizzontale "non so se mi convince": serve una transizione che matchi il suono dell'immersione.
# -> TUFFO: la camera si butta giu' (whip verticale). La laguna sale fuori dall'inquadratura accelerando, la clip subacquea
# arriva dal basso frenando; sullo stacco, insieme allo splash, un lampo di luce leggero come la schiuma dell'acqua.
WHIP = ("[0:v]split=3[s1][s2][s3];[s1]trim=end_frame={c0},setpts=PTS-STARTPTS[wa];"
        "[s2]trim=start_frame={c0}:end_frame={c1},setpts=PTS-STARTPTS,split[a1][a2];[a2]vflip[a3];[a1][a3]vstack,"
        "crop=2880:2160:x=0:y='{t}*2160*pow((n+1)/{na},2.5)',{ba},"
        "eq=brightness=0.06:enable='eq(n,{na}-1)'[wb];"
        "[s3]trim=start_frame={c1},setpts=PTS-STARTPTS[s4];[s4]split[s5][wc0];"
        "[s5]trim=end_frame={nb},setpts=PTS-STARTPTS,split[b1][b2];[b1]vflip[b3];[b3][b2]vstack,"
        "crop=2880:2160:x=0:y='2160-{t}*2160*pow(1-n/{nb},2.5)',{bb},"
        "eq=brightness=0.10:enable='eq(n,0)',eq=brightness=0.05:enable='eq(n,1)'[wc];"
        "[wc0]trim=start_frame={nb},setpts=PTS-STARTPTS[wd];[wa][wb][wc][wd]concat=n=4:v=1:a=0,"
        ).format(c0=WCUT - WA, c1=WCUT, na=WA, nb=WB, t=WTRAV,
                 ba=_vblur([(1, 12), (2, 30), (3, 80), (4, 180), (5, 300)]), bb=_vblur([(0, 300), (1, 180), (2, 80), (3, 30), (4, 12)]))
CUT_SERA, LEAK_FROM, LEAK_TO, LEAK_PEAK, LEAK_OPACITY = 29.133, 1.25, 2.0, 1.6, 0.35   # come il reel 1


def run(cmd, **kw):
    print(">", " ".join(os.path.basename(c) if os.path.exists(c) else c for c in cmd)[:180], flush=True)
    return subprocess.run(cmd, check=True, **kw)


def lufs(f, ss, t, hp=True):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", str(ss), "-t", str(t), "-i", f, "-af",
                        ("highpass=f=150," if hp else "") + "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


inputs, chains, labels = [], [], []
for i, (name, off, a, b, target) in enumerate(AMB):
    f = os.path.join(ES, name + ".wav")
    a0, b0 = max(0, a - XF / 2), min(DUR, b + XF / 2)
    g = target - lufs(f, off, b0 - a0)
    inputs += ["-i", f]
    fo = "afade=t=out:st=%.3f:d=%.2f," % (b0 - a0 - (1.5 if b0 >= DUR else XF), 1.5 if b0 >= DUR else XF)
    chains.append("[%d:a]atrim=start=%s:duration=%.3f,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                  "highpass=f=150,lowpass=f=9000,volume=%.1fdB,afade=t=in:d=%.2f,%sadelay=%d:all=1[m%d]"
                  % (len(inputs) // 2, off, b0 - a0, g, XF if a0 > 0 else 0.3, fo, a0 * 1000, i))
    labels.append("[m%d]" % i)
for j, (name, peak, at, db) in enumerate(FX):
    f = SWOOSH if name == "swoosh" else os.path.join(ES, name + ".wav")
    g = FX_LUFS - lufs(f, 0, 10) + db
    inputs += ["-i", f]
    chains.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=120,volume=%.1fdB,adelay=%d:all=1[f%d]"
                  % (len(inputs) // 2, g, (at - peak) * 1000, j))
    labels.append("[f%d]" % j)
amb = ";".join(chains) + ";" + "".join(labels) + "amix=inputs=%d:normalize=0:duration=longest,atrim=end=%.3f[amb]" % (len(labels), DUR)

# canzone: A pulita; B ovattata sott'acqua (si chiude in 0,08 s quando si entra in acqua, si riapre in 0,04 s sulla barca)
a0, a1 = UNDER
g = "clip((t-%.3f)/0.08,0,1)*clip((%.3f-t)/0.04,0,1)" % (a0, a1)
music = {"A": "[0:a]aresample=48000,anull[mus]",
         "B": "[0:a]aresample=48000,asplit[d][w];[d]volume='1-%s':eval=frame[d2];"
              "[w]lowpass=f=420,lowpass=f=420,volume=2dB,volume='%s':eval=frame[w2];"
              "[d2][w2]amix=inputs=2:normalize=0[mus]" % (g, g)}

work = os.path.join(HERE, "work")
os.makedirs(work, exist_ok=True)
# immagine: light leak dorato sullo stacco giorno -> sera, una volta sola, poi due passate per Instagram
leakv = os.path.join(work, "video-leak.mp4")
ig_v = os.path.join(work, "video-INSTAGRAM.mp4")
if not os.path.exists(ig_v):
    lstart, ldur = CUT_SERA - (LEAK_PEAK - LEAK_FROM), LEAK_TO - LEAK_FROM
    run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-i", LEAK, "-filter_complex",
         "[0:v]format=gbrp[base];[1:v]trim=start=%s:end=%s,setpts=PTS-STARTPTS,fps=25,scale=-2:2160,crop=2880:2160,format=gbrp,"
         "fade=t=in:d=0.5,fade=t=out:st=%.3f:d=0.5,tpad=start_duration=%.3f:stop_duration=%.3f:color=black[lk];"
         "[base][lk]blend=all_mode=screen:all_opacity=%s:shortest=1,format=yuv420p[v]"
         % (LEAK_FROM, LEAK_TO, ldur - 0.5, lstart, DUR, LEAK_OPACITY),
         "-map", "[v]", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", leakv])
    common = ["-c:v", "libx264", "-profile:v", "high", "-b:v", "25M", "-maxrate", "30M", "-bufsize", "50M", "-g", "50", "-r", "25",
              "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
              "-passlogfile", os.path.join(work, "ig2pass"), "-an"]
    run(["ffmpeg", "-v", "error", "-y", "-i", leakv] + common + ["-pass", "1", "-f", "null", "NUL"])
    run(["ffmpeg", "-v", "error", "-y", "-i", leakv] + common + ["-pass", "2", "-movflags", "+faststart", ig_v])

for v in ("B",):   # scelta di Jacopo 29/10: la B (canzone ovattata sott'acqua)
    wav = os.path.join(work, "mix-%s.wav" % v)
    run(["ffmpeg", "-v", "error", "-y", "-i", SRC] + inputs + ["-filter_complex",
         amb + ";" + music[v] + ";[mus][amb]amix=inputs=2:normalize=0,alimiter=limit=0.84:level=0[a]",
         "-map", "[a]", "-t", str(DUR), wav])
    ig = os.path.join(HERE, "zanzibar-reel2_suono-%s_FINALE_INSTAGRAM_4x3.mp4" % v)
    run(["ffmpeg", "-v", "error", "-y", "-i", ig_v, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", ig])
    run(["ffmpeg", "-v", "error", "-y", "-i", ig, "-vf", "scale=-2:960", "-c:v", "libx264", "-crf", "21", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", ig.replace("_INSTAGRAM_4x3", "_telefono")])
    print("ok", ig, "LUFS master %.1f" % lufs(wav, 0, DUR, hp=False))
