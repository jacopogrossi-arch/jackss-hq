# Cartamodello Jeans Uomo — Guida tecnica (Metodo Müller)

Questo file spiega le formule e la logica dietro al cartamodello jeans generato dall'AI.
Serve a Jacopo per capire cosa Claude sta costruendo e per spiegarlo alla community.

---

## Perché il Metodo Müller?

Il Metodo Müller (Müller & Sohn) è il sistema di modellistica tedesco adottato in molte scuole di moda italiane.
Per i pantaloni maschili è particolarmente preciso perché:
- Usa formule matematiche derivate dalle proporzioni del corpo maschile
- Distingue chiaramente tra misure del corpo e abbondanze del vestito
- Produce un blocco base tecnico che poi si adatta alla silhouette desiderata

---

## I 4 pezzi del cartamodello jeans base

```
┌──────────────┐   ┌──────────────┐   ┌────────────────────┐   ┌──────────────┐
│   DAVANTI    │   │    DIETRO    │   │     CINTURA        │   │   TASCA      │
│              │   │              │   │  _________________ │   │  POSTERIORE  │
│  (× 2 pezzi) │   │  (× 2 pezzi) │   │ |                 |│   │  (× 2 pezzi) │
│              │   │              │   │ |_________________|│   │              │
│  Foglio A1   │   │  Foglio A1   │   │    Foglio A3       │   │  Foglio A3   │
└──────────────┘   └──────────────┘   └────────────────────┘   └──────────────┘
```

---

## Le variabili base

Partendo dalle misure corporee, si calcolano:

| Variabile | Formula | Taglia 48 (esempio) |
|-----------|---------|---------------------|
| W4 | Giro vita ÷ 4 | 82 ÷ 4 = 20.5 cm |
| H4 | Giro fianchi ÷ 4 | 98 ÷ 4 = 24.5 cm |
| T2 | Giro coscia ÷ 2 | 58 ÷ 2 = 29 cm |

La divisione per 4 serve perché ogni pezzo del cartamodello rappresenta **un quarto** del girovita/fianchi (metà corpo, metà anteriore/posteriore).

---

## Come funzionano le abbondanze (ease)

Le misure corporee ti dicono com'è il corpo. Le abbondanze ti dicono quanto spazio lasci nel vestito per:
1. **Movimento:** sedersi, camminare, salire le scale
2. **Stile:** la silhouette voluta (slim, baggy, ecc.)
3. **Tessuto:** il denim non stretcha, quindi serve più spazio di un jersey

### Tabella abbondanze per silhouette

| Silhouette | Ease anca | Ease coscia | Sensazione |
|-----------|-----------|-------------|------------|
| Ultra slim | +1 cm | +1 cm | Stretch denim obbligatorio |
| Slim | +2 cm | +2 cm | Denim rigido possibile |
| Regular | +3 cm | +4 cm | Comfort buono |
| Relaxed | +5 cm | +6 cm | Molto comodo, look anni '90 |
| Baggy | +8 cm | +10 cm | Oversized, Y2K vibes |

---

## Pezzo 1 — Davanti (Front Panel)

### Cosa è e come si costruisce

Il davanti del jeans è il pezzo più complesso perché ha:
- La cucitura laterale (lato destro del pezzo)
- La cucitura centrale (lato sinistro, dove va la cerniera/fly)
- La curva del cavallo (il "fondo della sella" dove ci sediamo)

### Le misure principali

```
       larghezza vita
       ←────────────→
  A ─────────────────── B    ← linea vita (aggiustata con slider)
  │                     │
  C ─────────────────── D    ← linea fianchi (a "altezza vita-fianchi" dalla vita)
  │                     │
  E                     F    ← linea coscia (a "cavallo frontale" dalla vita)
  ╰─ curva cavallo      │         (questa è la linea dove le due gambe si dividono)
                        │
        G ──────────── H      ← linea ginocchio (a metà lunghezza)
        │              │
        I ──────────── J      ← linea caviglia (fondo del pezzo)
```

### Formule

```
Larghezza vita davanti    = W4 + 1cm (margine) + ease_anca/2
Larghezza fianchi davanti = H4 + 1cm (margine) + ease_anca/2
Larghezza coscia davanti  = T2 + ease_coscia/2
Profondità cavallo dav.   = cavallo_frontale - altezza_vita_fianchi + 1cm
```

**Perché ease/2 e non ease intera?** Perché il davanti è metà del pantalone. L'altra metà dell'ease la metti nel pezzo dietro. Daw + Die = ease completa.

---

## Pezzo 2 — Dietro (Back Panel)

### Differenze rispetto al davanti

Il dietro è diverso dal davanti per 3 motivi:

1. **Più largo al sedere:** il corpo umano ha i glutei che sporgono → serve più spazio nel pezzo dietro. La vita dietro è più larga del davanti (+2.5cm di media).

2. **Vita inclinata:** la linea vita dietro non è orizzontale — è inclinata di ~2.5cm (il lato esterno è più alto). Questo serve per adattarsi alla forma della schiena.

3. **Cavallo più profondo:** il cavallo posteriore è sempre più lungo di quello frontale (siediti: il tessuto deve coprire il sedere). Differenza tipica: 6-10 cm.

### Formule

```
Larghezza vita dietro    = W4 + 2.5cm + ease_anca/2
Larghezza fianchi dietro = H4 + 1.5cm + ease_anca/2
Larghezza coscia dietro  = T2 + 3cm + ease_coscia/2
Profondità cavallo die.  = cavallo_posteriore
Inclinazione vita        = 2.5cm (lato esterno più alto)
```

---

## Pezzo 3 — Cintura (Waistband)

Il pezzo più semplice: un rettangolo.

```
Lunghezza = (giro_vita + ease_anca/2) × 2 + 4cm (per abbottonatura)
Altezza   = 8cm (nel cartamodello) → finisce a 4cm (piega a metà e cuce)
```

La cintura è 1 solo pezzo, tagliato con il dritto filo in orizzontale (la direzione del filo del tessuto va lungo la lunghezza della cintura, non l'altezza).

---

## Pezzo 4 — Tasca posteriore

Altro pezzo semplice: un rettangolo con gli angoli inferiori arrotondati.

```
Larghezza = 14cm (standard uomo)
Altezza   = 15cm
Raggio arrotondamento angoli inferiori = 2cm
N. pezzi = 2 (una per ogni gluteo)
```

---

## Gli elementi obbligatori del cartamodello

Ogni pezzo stampabile deve avere:

1. **Outline del pezzo** — il contorno da ritagliare
2. **Filo del tessuto (grain line)** — una freccia che indica in che direzione va il filo del tessuto. Fondamentale: se tagli nella direzione sbagliata il tessuto cade male.
3. **Tacche di montaggio (notches)** — piccoli taglietti sul bordo che ti dicono "allinea questo punto con il punto corrispondente sull'altro pezzo"
4. **Etichetta** — nome del pezzo, quante volte tagliarlo, se i margini sono inclusi
5. **Barra scala** — un rettangolo di 10cm con indicazione "10 cm". Serve per verificare che la stampa sia in scala 1:1.

---

## Come verificare la stampa

1. Apri l'SVG in un browser e premi "Stampa"
2. **Importante:** nelle impostazioni di stampa, metti "Scala: 100%" e deseleziona "Adatta alla pagina"
3. Una volta stampato, misura la barra scala con un righello fisico → deve misurare esattamente 10cm
4. Se non è 10cm, regola la scala di stampa di conseguenza

---

## Pezzi opzionali (V2)

- **Tasca orologio** — la tasca piccola nel jeans, 10cm × 8cm, 2 strati
- **Rinforzi tasconi anteriori** — per jeans workwear, 1cm più piccoli delle tasche principali
- **Passanti cintura** — 6 pezzi rettangolari 4cm × 7cm

---

## Riferimenti tecnici

- **Metodo Müller:** *Rundschau Modellbearbeitung — Herrenbekleidung* (libro tecnico tedesco)
- **Metodo Donnanno:** *Tecniche di modellistica 2* (versione italiana più accessibile)
- **Seamly2D:** software open source di modellistica, utile per verificare i cartamodelli generati
