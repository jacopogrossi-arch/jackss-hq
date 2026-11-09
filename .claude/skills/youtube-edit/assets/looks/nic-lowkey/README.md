# nic-lowkey

Look creato il 09/11/2026 dal colore di **Nic Salvatori** (@nicsalvatori), il creator modello di Jacopo. Studio completo: `personale/youtube/inspo-nick-salvatori.md` §6.

**Non è una copia del suo prima/dopo.** È il look `nic-lowkey` di `presets/vacanze-grading/preset.json`, con i numeri cercati finché 60 frame di 20 clip di Jacopo (D-Log, D-Log2, D-Log M) avevano gli stessi tratti misurati sul finito di Nic (7 episodi, senza filigrana IG, testi e archivio).

## I file

| File | Su cosa si mette |
|---|---|
| `nic-lowkey-dlog2.cube` | girato **D-Log2** del Pocket 4P (anche gli export di Mimo in D-Log2). Contiene già la LUT DJI |
| `nic-lowkey-dlog.cube` | girato **D-Log** del Pocket 4P. Contiene già la LUT DJI |
| `nic-lowkey-dlogm.cube` | girato **D-Log M** dell'Osmo Nano. Contiene già la LUT DJI |
| `nic-lowkey-rec709.cube` | clip già in **Rec.709** (telefono normale, clip già convertite) |

Le versioni log vanno messe **al posto** della LUT DJI, non sopra (sopra si convertirebbe due volte).
Nei file `.cube` manca la **vignetta leggera** (0,2), perché dipende dalla posizione del pixel e una LUT non può contenerla: in CapCut aggiungila a mano, intorno al 15-20%. Nella skill la vignetta c'è già.

## Nella skill
```
python grade-apply.py --video clip.MP4 --scan DIR/report.json --out DIR --look nic-lowkey            # anteprima
python grade-apply.py --video clip.MP4 --scan DIR/report.json --out DIR --look nic-lowkey --render   # video
```

## Cosa fa
- Esposizione **−0,6 stop**; nero intorno all'1,2% (profondo, senza patina matte).
- **Spalla presto**: le luci si fermano intorno all'80%, mai bianco pieno. L'allungamento delle luci per clip è spento.
- Luci **crema-calde**, ombre neutre appena magenta; **pelle dorata** (tinta spostata verso il giallo, saturazione pelle ×1,2).
- **Verdi verso l'oliva** (−25° di tinta), colore generale contenuto, luci leggermente desaturate.

## Cosa non fa
Il buio vero di Nic viene dalla **luce delle scene**: camino, auto, ora blu, finestre, luce pratica e poca. Il grading lo accompagna ma non lo crea: per il suo look bisogna anche girare con poca luce e lasciare il buio nel quadro. Se una clip esce troppo scura, alza l'esposizione con `--stops 0.3`.
