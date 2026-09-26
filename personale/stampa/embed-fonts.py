#!/usr/bin/env python3
"""Scarica i font da Google Fonts e li incorpora nel sorgente: scrive build.html.

Tiene solo i sottoinsiemi latin/latin-ext (gli altri sono peso inutile) e
sostituisce ogni url() remota con un data URI base64, così il PDF risultante
non dipende dalla rete né dai font di sistema.

ATTENZIONE allo user-agent: Google Fonts serve woff2 con i commenti di
sottoinsieme (/* latin */) solo se la richiesta sembra venire da un browser
recente. Con un UA generico risponde con dei TTF senza commenti e il parsing
qui sotto non trova niente. Per questo l'UA di Chrome è cablato nel file.

Uso: python3 embed-fonts.py
"""

import base64
import io
import re
import subprocess
import sys

SORGENTE = "mandal-art-a4.src.html"
USCITA = "build.html"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")

CSS_URL = ("https://fonts.googleapis.com/css2"
           "?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,600"
           "&family=IBM+Plex+Mono:wght@400;500"
           "&family=IBM+Plex+Sans:wght@400;500;600&display=swap")


def scarica(url, minimo=500):
    r = subprocess.run(["curl", "-sS", "--max-time", "30", "-A", UA, url],
                       capture_output=True)
    if r.returncode != 0 or len(r.stdout) < minimo:
        sys.exit("download fallito: " + url)
    return r.stdout


def main():
    css = scarica(CSS_URL, minimo=2000).decode("utf-8")
    blocchi = re.findall(r"/\*\s*([a-z0-9\-\[\] ]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S)

    incorporati, cache = [], {}
    for subset, blocco in blocchi:
        if subset.strip() not in ("latin", "latin-ext"):
            continue
        url = re.search(r"url\((https://fonts\.gstatic\.com[^)]+)\)", blocco).group(1)
        if url not in cache:
            cache[url] = base64.b64encode(scarica(url)).decode()
        incorporati.append(blocco.replace(url, "data:font/woff2;base64," + cache[url]))

    if not incorporati:
        sys.exit("nessun @font-face latin trovato: Google Fonts ha risposto\n"
                 "in un formato inatteso (controlla lo user-agent).")

    sorgente = io.open(SORGENTE, encoding="utf-8").read()
    io.open(USCITA, "w", encoding="utf-8").write(
        sorgente.replace("/*FONTS*/", "\n".join(incorporati)))
    print("%s scritto — %d blocchi, %d file font" % (USCITA, len(incorporati), len(cache)))


if __name__ == "__main__":
    main()
