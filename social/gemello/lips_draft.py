"""Bozza della partitura labiale italiana (23/11/2026): sillabe scritte a mano + inviluppo della voce a 10 ms.
Uso: python lips_draft.py VO_DIR SYL.json OUT.json
 VO_DIR/vo.wav = voce montata, VO_DIR/words.json = {pN: {off, words:[[parola,t0,t1],...]}} (Whisper, tempi relativi al paragrafo),
 SYL.json = {parola_minuscola_senza_punteggiatura: ["sil","la","be"]} (ortografia fonetica: gli=lj, sc=sh... si scrive come si dice).
Mappa (SOP gemello): a=D e=C i=B o=E u=F; m b p = A (chiusura piena); f v = G; l = H; t d n s r k g c z = B.
Ogni sillaba = [consonanti iniziali] + vocale + [consonanti finali]. Il nucleo e' un picco dell'inviluppo dentro la parola; i confini sono i minimi tra picchi.
La bozza NON basta: i tempi vanno controllati a mano contro l'inviluppo (stampa con --env) e le chiusure m/b/p guardate una per una.
"""
import sys, json, wave, struct, math

VOW = {"a": "D", "e": "C", "i": "B", "o": "E", "u": "F"}
CONS = {"m": "A", "b": "A", "p": "A", "f": "G", "v": "G", "l": "H"}

def read_env(path):
    w = wave.open(path); sr = w.getframerate(); n = w.getnframes()
    d = struct.unpack("<%dh" % n, w.readframes(n)); hop = sr // 100
    e = [math.sqrt(sum(x * x for x in d[i:i + hop]) / hop) for i in range(0, len(d) - hop, hop)]
    mx = max(e); return [x / mx for x in e]

def smooth(e):
    return [(e[max(0, i - 1)] + 2 * e[i] + e[min(len(e) - 1, i + 1)]) / 4 for i in range(len(e))]

def syl_visemes(s):
    """(closure_letters, vowel_viseme, tail) di una sillaba: sequenza di visemi con peso relativo."""
    seq = []
    for ch in s:
        v = VOW.get(ch) or CONS.get(ch) or "B"
        seq.append((ch, v))
    return seq

def split_nuclei(es, a, b, n):
    """n picchi (nuclei) dentro [a,b) in campioni da 10 ms: i n picchi piu' prominenti, ordinati nel tempo."""
    pk = [i for i in range(max(a, 1), min(b, len(es) - 1) - 1) if es[i] >= es[i - 1] and es[i] > es[i + 1]]
    if len(pk) < n:   # troppo pochi picchi: distribuisci uniforme
        return [int(a + (b - a) * (k + 0.5) / n) for k in range(n)]
    pk.sort(key=lambda i: -es[i]); pk = sorted(pk[:n]); return pk

def main():
    vo_dir, sylf, outf = sys.argv[1:4]
    env = read_env(vo_dir + "/vo.wav"); es = smooth(env)
    words = json.load(open(vo_dir + "/words.json")); syl = json.load(open(sylf))
    lips = [(0.0, "X")]; report = []
    for pk_, blk in words.items():
        off = blk["off"]
        for wd, t0, t1 in blk["words"]:
            key = "".join(c for c in wd.lower() if c.isalpha() or c in "àèéìòù")
            sl = syl.get(key)
            if not sl: print("MANCA", key); continue
            a = int((off + float(t0)) * 100) - 2; b = int((off + float(t1)) * 100) + 2
            nuc = split_nuclei(es, a, b, len(sl))
            # confini tra sillabe = minimo dell'inviluppo tra due nuclei
            bnd = [a] + [min(range(nuc[k], nuc[k + 1] + 1), key=lambda i: es[i]) for k in range(len(nuc) - 1)] + [b]
            for k, s in enumerate(sl):
                s0, s1 = bnd[k] / 100.0, bnd[k + 1] / 100.0; tv = nuc[k] / 100.0
                seq = syl_visemes(s); vi = next((j for j, (c, _) in enumerate(seq) if c in VOW), None)
                onset = seq[:vi] if vi is not None else seq; vow = seq[vi][1] if vi is not None else None; coda = seq[vi + 1:] if vi is not None else []
                t = s0
                # consonanti iniziali: fino al nucleo; la chiusura (m b p) dura 0.07 s e finisce 0.03 s prima del picco
                for c, v in onset:
                    if v == "A": lips.append((round(max(t, tv - 0.12), 2), "A")); t = max(t, tv - 0.12) + 0.07
                    else: lips.append((round(max(t, tv - 0.09), 2), v)); t = max(t, tv - 0.09) + 0.05
                if vow: lips.append((round(max(t, tv - 0.04), 2), vow))
                tc = tv + 0.06
                for c, v in coda:
                    lips.append((round(min(tc, s1 - 0.02), 2), v)); tc += 0.06
                report.append((s, round(s0, 2), round(tv, 2), round(s1, 2)))
    # pulizia: tempi monotoni, scarta duplicati consecutivi, X nei silenzi lunghi (> 0.25 s senza voce)
    lips.sort(key=lambda x: x[0]); clean = []
    for t, v in lips:
        if clean and abs(t - clean[-1][0]) < 0.001: clean[-1] = (t, v); continue
        if clean and clean[-1][1] == v and v != "A": continue
        clean.append((t, v))
    json.dump({"lips": clean, "report": report}, open(outf, "w"), ensure_ascii=False)
    for r in report: print("%-8s %.2f %.2f %.2f" % r)
    print(len(clean), "cue")

if __name__ == "__main__":
    main()
