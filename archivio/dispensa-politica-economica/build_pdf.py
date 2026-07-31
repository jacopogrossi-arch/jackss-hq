import markdown
import re
from pathlib import Path

BASE = Path(__file__).parent
SCHEMI = BASE / "schemi"
OUT_NAME = "Dispensa Politica Economica"

FILES_IN_ORDER = [
    "00c-mappa-priorita.md",
    "00b-glossario-simboli.md",
    "00a-formulario.md",
    "01-politica-fiscale-bilancio-pubblico.md",
    "02-inflazione-curva-phillips.md",
    "03-concorrenza-imperfetta-monopolio.md",
    "04-economia-benessere-teoria-normativa.md",
    "05-mercato-del-lavoro.md",
    "06-economia-aperta-bilancia-pagamenti.md",
    "07-teorie-macro-moneta-bce.md",
    "08-esternalita-fallimenti-mercato.md",
    "09-crescita-sviluppo.md",
    "10-disuguaglianze-stato-sociale.md",
]

parts = []
parts.append("# Dispensa Politica Economica\n\n**Esame 08/09/2026**\n\n[TOC]\n\n<div class=\"pagebreak\"></div>\n\n")

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
}
for fname, anchor in ANCHOR_MAP.items():
    combined_md = combined_md.replace(f"]({fname})", f"]({anchor})")

html_body = markdown.markdown(
    combined_md,
    extensions=["tables", "toc", "fenced_code", "sane_lists", "md_in_html"],
    extension_configs={
        "toc": {"toc_depth": "1-2", "anchorlink": False, "permalink": False},
    },
)

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
  code {{ background: #f2f2f2; padding: 1px 4px; font-family: 'Consolas', monospace; font-size: 10pt; }}
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
print(f"OK: {OUT_NAME}.md e {OUT_NAME}.html generati")
