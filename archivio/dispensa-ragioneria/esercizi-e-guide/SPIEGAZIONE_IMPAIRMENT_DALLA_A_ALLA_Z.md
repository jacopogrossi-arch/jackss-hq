# Impairment test — Spiegazione dalla A alla Z

Spiegazione passo-passo dell'esercizio sull'impairment dell'impianto (Esercizio 1 del PDF "Esercizi 1", soluzioni in `SOLUZIONI_ESERCIZI_1_PDF.md`). La procedura è sempre la stessa: imparati i 4 passi e all'esame lo risolvi con qualsiasi numero.

---

## Il problema in una frase

L'azienda ha un impianto scritto in bilancio a un certo valore, ma sospetta che ormai **valga meno**. La legge dice: se un bene ha perso valore in modo durevole, non puoi lasciarlo in bilancio al valore vecchio, devi **svalutarlo**. La verifica si chiama **impairment test**.

---

## Passo 1 — Trova il valore contabile netto (quanto "dice" il bilancio)

```
Costo storico             5.000   (quanto l'ho pagato)
− Fondo ammortamento     −2.000   (quanto ho già ammortizzato negli anni)
= Valore contabile netto  3.000   ← questo è il valore da "mettere alla prova"
```

Nota anche: vita residua 5 anni, quote costanti → se non succedesse niente, l'ammortamento annuo sarebbe:

```
3.000 / 5 = 600 all'anno
```

Tieni da parte questo **600**, serve al passo 2.

---

## Passo 2 — Calcola i due "valori alternativi"

Per capire quanto vale davvero l'impianto, si confrontano due strade possibili: **venderlo** oppure **continuare a usarlo**.

### Strada A — Venderlo

Il perito dice che venduto frutta **1.700** (prezzo netto di vendita). Questo lo dà il testo, non si calcola nulla.

### Strada B — Continuare a usarlo (valore d'uso)

Qui c'è la tabella da compilare, ed è il cuore dell'esercizio. Il ragionamento: "quanto margine genererà questo impianto nei 5 anni che gli restano?"

Come si compila:

1. Il **margine lordo industriale** è già dato (500, 400, 300, 400, 300)
2. Nella riga **Ammortamento Impianto** scrivi **−600** in ogni anno (il 600 del passo 1)
3. Il **margine industriale netto** è la differenza: 500 − 600 = −100, 400 − 600 = −200, e così via
4. La **capacità di ammortamento** è la **somma dei margini lordi dei 5 anni**:

```
500 + 400 + 300 + 400 + 300 = 1.900
```

| Piano industriale | 2023 | 2024 | 2025 | 2026 | 2027 |
|---|---|---|---|---|---|
| = Margine lordo industriale | 500 | 400 | 300 | 400 | 300 |
| Ammortamento Impianto | −600 | −600 | −600 | −600 | −600 |
| = Margine industriale netto | −100 | −200 | −300 | −200 | −300 |
| **Capacità di ammortamento** | **1.900** | | | | |

Questo **1.900 è il valore d'uso**: l'impianto, usandolo fino in fondo, "restituirà" al massimo 1.900 di margine.

> 💡 Il senso della riga "margine industriale netto": viene **negativa ogni anno** → l'impianto non riesce a "ripagare" i suoi 600 di ammortamento annuo. È il campanello d'allarme che c'è una perdita di valore.

---

## Passo 3 — Trova il valore recuperabile e confrontalo

Regola fissa (da imparare a memoria, è sempre uguale):

> **Valore recuperabile = il MAGGIORE tra prezzo netto di vendita e valore d'uso**

Perché il maggiore? Perché un imprenditore razionale sceglie la strada più conveniente: se vendere rende di più, vende; se usare rende di più, usa.

```
Valore recuperabile = max(1.700 ; 1.900) = 1.900
```

Confronto finale:

```
Valore recuperabile 1.900  <  Valore contabile 3.000  →  SVALUTAZIONE
```

L'impianto va iscritto in bilancio a **1.900** (svalutazione di 1.100). → **Risposta domanda 1: opzione 2) 1.900**

(Se invece il recuperabile fosse stato ≥ 3.000, non si toccava niente e il bene restava a 3.000.)

---

## Passo 4 — Ricalcola l'ammortamento sul valore nuovo

Dopo la svalutazione, il "nuovo punto di partenza" è 1.900, sempre da spalmare sui 5 anni residui:

```
1.900 / 5 = 380 all'anno
```

→ **Risposta domanda 2: opzione 1) 380**

> ⚠️ Errore classico: rispondere 600. No — dopo la svalutazione l'ammortamento si ricalcola sul **valore svalutato**, non su quello vecchio.

---

## Domanda 3 — La variante

"E se il perito avesse detto prezzo di vendita **2.600** invece di 1.700?" Si rifà solo il passo 3 con il numero nuovo:

```
Valore recuperabile = max(2.600 ; 1.900) = 2.600
2.600 < 3.000  →  si svaluta comunque, ma a 2.600
```

→ **Risposta domanda 3: opzione 2) 2.600** — il valore da ammortizzare diventa 2.600 (e la quota sarebbe 2.600 / 5 = 520, se la chiedessero).

---

## Riassunto da portare all'esame

1. **Valore contabile netto** = costo storico − fondo ammortamento
2. **Valore d'uso** = somma dei margini lordi degli anni residui (la "capacità di ammortamento")
3. **Valore recuperabile** = il **maggiore** tra prezzo netto di vendita e valore d'uso
4. Se recuperabile < contabile → **svaluti** al recuperabile, e il **nuovo ammortamento** = recuperabile / anni residui
