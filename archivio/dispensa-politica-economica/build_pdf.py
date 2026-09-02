import markdown
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
SCHEMI = BASE / "schemi"
OUT_NAME = "Dispensa Politica Economica"

# l'ordine segue la mappa di priorità, non la numerazione dei file: gli schemi
# 11-14 sono stati aggiunti dopo, ma alcuni valgono più di quelli già presenti
FILES_IN_ORDER = [
    "00c-mappa-priorita.md",
    "00b-glossario-simboli.md",
    "00a-formulario.md",
    # core
    "01-politica-fiscale-bilancio-pubblico.md",
    "02-inflazione-curva-phillips.md",
    "03-concorrenza-imperfetta-monopolio.md",
    "04-economia-benessere-teoria-normativa.md",
    "11-teoria-normativa-obiettivi-strumenti.md",
    # secondari
    "05-mercato-del-lavoro.md",
    "06-economia-aperta-bilancia-pagamenti.md",
    "07-teorie-macro-moneta-bce.md",
    "08-esternalita-fallimenti-mercato.md",
    "13-valutazione-progetti-acb.md",
    "12-fallimenti-stato-political-economy.md",
    # copertura di sicurezza
    "09-crescita-sviluppo.md",
    "10-disuguaglianze-stato-sociale.md",
    "14-sistema-monetario-internazionale.md",
    # autoverifica, in coda
    "00d-domande-preselezione.md",
]

def controlla_formule(files):
    """Segnala LaTeX rimasto e trattini bassi fuori da blocchi/apici, che markdown
    interpreta come corsivo mangiandosi pezzi di formula. Avvisa, non blocca."""
    comando_latex = re.compile(r"\\[a-zA-Z]+")
    avvisi = []
    for fname in files:
        dentro_blocco = False
        for n, riga in enumerate((SCHEMI / fname).read_text(encoding="utf-8").split("\n"), 1):
            if riga.lstrip().startswith("```"):
                dentro_blocco = not dentro_blocco
                continue
            if dentro_blocco:
                continue
            fuori_apici = re.sub(r"`[^`]*`", "", riga)
            if "$" in fuori_apici:
                avvisi.append(f"{fname}:{n}  simbolo $ fuori da un blocco (LaTeX non viene reso nel PDF)")
            if comando_latex.search(fuori_apici):
                avvisi.append(f"{fname}:{n}  comando LaTeX (\\frac, \\dot...) non reso nel PDF")
            if "_{" in fuori_apici or "^{" in fuori_apici:
                avvisi.append(f"{fname}:{n}  graffe LaTeX in pedice/apice: usare _(...) o ^(...)")
    return avvisi


# pedici e apici: nei sorgenti si scrivono Q_M e (1+i)^t, che restano leggibili e
# facili da modificare; qui diventano pedici e apici tipografici veri, come sul manuale
PEDICE_PAR = re.compile(r"(?<=[A-Za-zΔθπεωγλσ0-9)])_\(([^()]{1,12})\)")
PEDICE = re.compile(r"(?<=[A-Za-zΔθπεωγλσ0-9)])_([A-Za-z]{1,2}(?:,[A-Za-z]{1,2})?[0-9]?|[0-9]{1,2}|trans)\b")
APICE_PAR = re.compile(r"(?<=[A-Za-zΔθπεωγλσ0-9)])\^\(([^()]{1,12})\)")
APICE = re.compile(r"(?<=[A-Za-zΔθπεωγλσ0-9)])\^([A-Za-z]{1,4}|[0-9]{1,2})\b")


def _posizioni(riga):
    """larghezza resa di ogni carattere: un pedice/apice occupa 0,75, il _ o ^ sparisce"""
    x = 0.0; pos = []; i = 0
    while i < len(riga):
        m = PEDICE.match(riga, i) or APICE.match(riga, i) or PEDICE_PAR.match(riga, i) or APICE_PAR.match(riga, i)
        if m and i > 0 and riga[i-1] != " ":
            for ch in m.group(1).strip("()"):
                pos.append((x, ch)); x += 0.75
            i = m.end()
        else:
            pos.append((x, riga[i])); x += 1.0; i += 1
    return pos


def _gruppi(riga, char=None):
    """blocchi di testo contigui (separati da 3+ spazi), come (x_inizio, x_fine)"""
    out = []; cur = None; vuoti = 0
    for x, ch in _posizioni(riga):
        if ch.strip() and (char is None or ch == char):
            cur = [x, x + 1] if cur is None else [cur[0], x + 1]
            vuoti = 0
        elif cur is not None:
            vuoti += 1
            if vuoti >= 3: out.append(tuple(cur)); cur = None
    if cur is not None: out.append(tuple(cur))
    return out


LARGHEZZA_MAX = 74   # nel riquadro ci stanno ~76 caratteri: 74 lascia un margine


def _larghezza(riga):
    tot = 0.0; i = 0
    while i < len(riga):
        m = PEDICE.match(riga, i) or APICE.match(riga, i) or PEDICE_PAR.match(riga, i) or APICE_PAR.match(riga, i)
        if m and i > 0 and riga[i-1] != " ":
            tot += 0.75 * len(m.group(1).strip("()")); i = m.end()
        else:
            tot += 1.0; i += 1
    return tot


def controlla_larghezza(files):
    """Una riga piu' larga della pagina viene TAGLIATA nel PDF: a schermo compare una
    barra di scorrimento, in stampa il testo oltre il bordo sparisce e basta."""
    avvisi = []
    for fname in files:
        dentro = False
        for n, riga in enumerate((SCHEMI / fname).read_text(encoding="utf-8").split("\n"), 1):
            if riga.lstrip().startswith("```"):
                dentro = not dentro; continue
            if dentro:
                w = _larghezza(riga.rstrip())
                if w > LARGHEZZA_MAX:
                    avvisi.append(f"{fname}:{n}  riga larga {w:.0f} caratteri (max {LARGHEZZA_MAX}): nel PDF verrebbe tagliata")
    return avvisi


def controlla_allineamento(files):
    """Numeratori e denominatori devono restare centrati sulla barra di frazione:
    il pedice reso e' piu' stretto del testo sorgente, quindi le frazioni scritte
    a occhio si disallineano. Qui si misura la larghezza resa e si segnala."""
    avvisi = []
    for fname in files:
        righe = (SCHEMI / fname).read_text(encoding="utf-8").split("\n")
        dentro = False; blocco = []; inizio = 0
        for n, l in enumerate(righe, 1):
            if l.lstrip().startswith("```"):
                if dentro:
                    for k, riga in enumerate(blocco):
                        for b in _gruppi(riga, "─"):
                            centro_barra = (b[0] + b[1]) / 2
                            for dk in (-1, 1):
                                if not (0 <= k + dk < len(blocco)) or _gruppi(blocco[k + dk], "─"):
                                    continue
                                sopra = [g for g in _gruppi(blocco[k + dk]) if g[0] < b[1] and g[1] > b[0]]
                                if not sopra: continue
                                g = max(sopra, key=lambda g: min(g[1], b[1]) - max(g[0], b[0]))
                                scarto = (g[0] + g[1]) / 2 - centro_barra
                                if abs(scarto) > 0.75:
                                    dove = "numeratore" if dk == -1 else "denominatore"
                                    avvisi.append(f"{fname}:{inizio+k}  {dove} fuori centro di {scarto:+.1f} caratteri")
                    blocco = []
                dentro = not dentro; inizio = n; continue
            if dentro: blocco.append(l)
    return avvisi


def applica_pedici_apici(html):
    """Trasforma X_y in X<sub>y</sub> e X^y in X<sup>y</sup>.

    Agisce SOLO sul testo fuori dai tag: dentro i tag ci sono le ancore dell'indice
    (id="esercizio-tipo-svolto_3"), che verrebbero rotte insieme ai link che le puntano.
    """
    def converti(testo):
        testo = PEDICE_PAR.sub(r"<sub>\1</sub>", testo)
        testo = APICE_PAR.sub(r"<sup>\1</sup>", testo)
        testo = PEDICE.sub(r"<sub>\1</sub>", testo)
        testo = APICE.sub(r"<sup>\1</sup>", testo)
        return testo

    pezzi = re.split(r"(<[^>]+>)", html)
    return "".join(p if i % 2 else converti(p) for i, p in enumerate(pezzi))


def controlla_html(html):
    """Il trattino basso puo' essere interpretato da markdown come corsivo, mangiando
    il testo in mezzo alla formula. Qui si verifica il risultato reso: un <em> o uno
    <strong> che contiene _ o $ e' sempre sintomo di formula corrotta."""
    avvisi = []
    # solo <em>: il grassetto con trattini bassi (**MC_S**) e' corretto, mentre un
    # corsivo che contiene _ o $ e' sempre un corsivo che markdown ha inventato
    for contenuto in re.findall(r"<em>([^<]*)</em>", html):
        if "_" in contenuto or "$" in contenuto:
            avvisi.append(f"corsivo inventato da markdown (testo mangiato): {contenuto[:70]!r}")
    return avvisi


def stampa_avvisi(avvisi):
    if avvisi:
        print("\n!! FORMULE DA CONTROLLARE — nel PDF verrebbero illeggibili:")
        for a in avvisi:
            print("   " + a)
        print("   Soluzione: mettere la formula in un blocco recintato ``` oppure fra `apici inversi`.\n")
    else:
        print("Controllo formule: nessun problema rilevato.")


avvisi_sorgente = (controlla_formule(FILES_IN_ORDER)
                   + controlla_allineamento(FILES_IN_ORDER)
                   + controlla_larghezza(FILES_IN_ORDER))

parts = []
HEADER = """# Dispensa Politica Economica

**Esame 08/09/2026**

**Struttura della prova** (modalità d'esame 2026-2027)

| Fase | Cosa | Tempo | Soglia |
|---|---|---|---|
| Preselezione | 11 domande a risposta multipla | 10 minuti | almeno 6 corrette, altrimenti non si accede allo scritto |
| Scritto | 2 domande aperte + 1 esercizio | 1 ora | — |
| Orale | facoltativo, oppure a richiesta del docente | — | — |

Testo di riferimento: Paesani, P., *Manuale di politica economica*, II edizione, Giappichelli, 2020.

Appelli a.a. 2026-27: 20 gennaio · 10 febbraio · 16 giugno · 14 luglio · 8 settembre.

**Una sigla da conoscere prima di iniziare.** Alcuni titoli di sezione portano la dicitura *(dal manuale, non dalle slide)*: quella parte viene dal **manuale di riferimento** (Paesani) e **non** trova riscontro nei PDF della professoressa. È materiale del programma, ma senza conferma che sia stato trattato a lezione: **da studiare per ultimo**, ed è la prima cosa da sacrificare se il tempo stringe. Tutto il resto viene dalle slide del corso. Lo schema 14 (sistema monetario internazionale) è interamente in questa condizione.

[TOC]

<div class="pagebreak"></div>

"""
parts.append(HEADER)

for i, fname in enumerate(FILES_IN_ORDER):
    text = (SCHEMI / fname).read_text(encoding="utf-8")
    # gli schemi referenziano le immagini come ../grafici/..., il documento unito vive
    # nella cartella superiore, quindi il prefisso "../" va tolto
    text = text.replace("](../grafici/", "](grafici/")
    if i > 0:
        parts.append('\n\n<div class="pagebreak"></div>\n\n')
    parts.append(text)

combined_md = "\n".join(parts)
(BASE / f"{OUT_NAME}.md").write_text(combined_md, encoding="utf-8")

# nel documento unico i link tra file .md diventano ancore alla stessa pagina;
# nei file sorgente restano link a file separati (utili su GitHub/VSCode)
ANCHOR_MAP = {
    "00a-formulario.md": "#formulario-riassuntivo",
    "00b-glossario-simboli.md": "#glossario-dei-simboli",
    "00c-mappa-priorita.md": "#mappa-di-priorita-argomento-esercizio-tipo-pagina",
    "01-politica-fiscale-bilancio-pubblico.md": "#politica-fiscale-bilancio-pubblico-e-debito-pubblico",
    "02-inflazione-curva-phillips.md": "#inflazione-e-curva-di-phillips",
    "03-concorrenza-imperfetta-monopolio.md": "#concorrenza-imperfetta-monopolio-e-politiche-per-la-concorrenza",
    "04-economia-benessere-teoria-normativa.md": "#economia-del-benessere-e-teoria-normativa-della-politica-economica",
    "05-mercato-del-lavoro.md": "#mercato-del-lavoro-disoccupazione-e-intervento-pubblico",
    "06-economia-aperta-bilancia-pagamenti.md": "#economia-aperta-bilancia-dei-pagamenti-e-modello-is-lm-bp",
    "07-teorie-macro-moneta-bce.md": "#is-lm-teorie-macro-comparate-moneta-e-politica-monetariabce",
    "08-esternalita-fallimenti-mercato.md": "#esternalita-e-fallimenti-di-mercato",
    "09-crescita-sviluppo.md": "#crescita-e-sviluppo-economico",
    "10-disuguaglianze-stato-sociale.md": "#disuguaglianze-economiche-di-genere-e-stato-sociale",
    "11-teoria-normativa-obiettivi-strumenti.md": "#teoria-normativa-obiettivi-strumenti-e-modelli-di-politica-economica",
    "12-fallimenti-stato-political-economy.md": "#i-fallimenti-dello-stato-e-la-political-economy",
    "13-valutazione-progetti-acb.md": "#la-valutazione-dei-progetti-pubblici-e-lanalisi-costi-benefici",
    "14-sistema-monetario-internazionale.md": "#il-sistema-monetario-internazionale",
    "00d-domande-preselezione.md": "#banca-domande-per-la-preselezione",
}
for fname, anchor in ANCHOR_MAP.items():
    combined_md = combined_md.replace(f"]({fname})", f"]({anchor})")

html_body_grezzo = markdown.markdown(
    combined_md,
    extensions=["tables", "toc", "fenced_code", "sane_lists", "md_in_html"],
    extension_configs={
        "toc": {"toc_depth": "1-2", "anchorlink": False, "permalink": False},
    },
)

html_body = applica_pedici_apici(html_body_grezzo)

html_template = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Dispensa Politica Economica</title>
<style>
  @page {{ size: A4; margin: 18mm 16mm; }}
  body {{ font-family: 'Georgia', 'Times New Roman', serif; font-size: 11pt; line-height: 1.45; color: #1a1a1a; max-width: 100%; }}
  h1 {{ font-size: 20pt; border-bottom: 2px solid #1a5276; padding-bottom: 6px; margin-top: 0; color: #1a5276; }}
  h2 {{ font-size: 14.5pt; color: #922b21; margin-top: 22px; border-left: 4px solid #922b21; padding-left: 8px; }}
  h3 {{ font-size: 12.5pt; color: #333; margin-top: 16px; }}
  p, li {{ text-align: justify; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }}
  th, td {{ border: 1px solid #999; padding: 5px 8px; text-align: left; vertical-align: top; }}
  th {{ background: #eef2f7; }}
  img {{ max-width: 92%; display: block; margin: 14px auto; page-break-inside: avoid; }}
  code {{ background: #f2f2f2; padding: 1px 4px; font-family: 'Consolas', 'DejaVu Sans Mono', monospace; font-size: 10pt; }}
  /* riquadro delle formule: il contenuto di un blocco recintato non viene toccato da
     markdown, quindi nessun simbolo puo' essere mangiato o interpretato come corsivo */
  pre {{ background: #f7f9fb; border: 1px solid #dde; border-left: 4px solid #1a5276;
        padding: 10px 14px; margin: 12px 0; page-break-inside: avoid; }}
  /* pre-wrap invece di pre: una riga troppo lunga va a capo (allineamento rovinato ma
     visibile) invece di essere tagliata in silenzio dalla stampa, come faceva overflow-x */
  pre code {{ background: none; padding: 0; font-size: 10.5pt; line-height: 1.35;
             white-space: pre-wrap; overflow-wrap: break-word; color: #16324f; }}
  /* la tecnica classica: line-height 0 e posizionamento relativo, cosi' pedici e apici
     non allargano l'interlinea ne' sfasano le righe delle frazioni nei riquadri */
  sub, sup {{ font-size: 75%; line-height: 0; position: relative; vertical-align: baseline; }}
  sub {{ bottom: -0.25em; }}
  sup {{ top: -0.5em; }}
  blockquote {{ border-left: 3px solid #ccc; margin-left: 0; padding-left: 12px; color: #555; }}
  .pagebreak {{ page-break-before: always; }}
  a {{ color: #1a5276; text-decoration: none; }}
  .toc {{ background: #f7f9fb; border: 1px solid #dde; padding: 14px 22px; }}
  .toc ul {{ list-style: none; padding-left: 14px; }}
  .toc > ul {{ padding-left: 0; }}
  .toc a {{ color: #1a1a1a; }}
  .toc > ul > li > a {{ font-weight: bold; color: #1a5276; }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

(BASE / f"{OUT_NAME}.html").write_text(html_template, encoding="utf-8")

stampa_avvisi(avvisi_sorgente + controlla_html(html_body_grezzo))
print(f"OK: {OUT_NAME}.md e {OUT_NAME}.html generati")
