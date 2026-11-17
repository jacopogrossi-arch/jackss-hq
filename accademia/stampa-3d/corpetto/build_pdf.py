"""Crea il PDF di consegna (Verifica Laboratorio Stampa 3D). Uso:  python build_pdf.py

Versione aggiornata: modulo FORATO (la Y e' un taglio passante, vedi modulo_forato.py).
Tempi e grammi del modulo sono stime dal volume: sostituirli con i dati di OrcaSlicer (MIN_MOD, G_MOD).
"""
import tempfile
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image as RLImage
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# --- da modificare se serve ---
NOME = "Jacopo"
COGNOME = "Grossi"
TITOLO = "Abysal Organica"
OUT_NAME = "Grossi_Jacopo_Verifica_Stampa3D.pdf"

# stime di stampa del modulo forato (da confermare con lo slicing in OrcaSlicer)
MIN_MOD = 17    # minuti per 1 modulo: volume 3310 mm3 contro 2311 mm3 del modulo vecchio (12 min 10 s) = x1,43
G_MOD = 3.9     # grammi per 1 modulo (vecchio: 2,74 g)
N_MOD = 57      # 52 moduli + 10% di scorta
PIATTO_MIN = 6  # preparazione di un piatto
# ------------------------------

DIR = Path(__file__).parent
TMP = Path(tempfile.mkdtemp())
VERDE = colors.HexColor("#0F6E56")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=18, textColor=VERDE, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=13, textColor=VERDE, spaceBefore=10, spaceAfter=4)
P = ParagraphStyle("P", parent=ss["BodyText"], fontSize=10.5, leading=14.5)
CAP = ParagraphStyle("CAP", parent=P, fontSize=9, textColor=colors.HexColor("#444444"), alignment=TA_CENTER, spaceAfter=8)
BIG = ParagraphStyle("BIG", parent=ss["Title"], fontSize=26, leading=32, textColor=VERDE)
CEN = ParagraphStyle("CEN", parent=P, alignment=TA_CENTER, fontSize=13, leading=20)

W = A4[0] - 4 * cm

# figurino: usa quello nuovo (forato) se esiste, altrimenti il vecchio
FIG = next((f for f in ("figurino-forato.png", "figurino-forato.webp", "figurino-forato.jpg") if (DIR / f).exists()),
           "figurino-corretto.webp")
if FIG == "figurino-corretto.webp":
    print("ATTENZIONE: manca figurino-forato.*, uso il figurino vecchio (Y in rilievo)")


def img(path, width=W, max_h=None):
    p = DIR / path
    im = Image.open(p).convert("RGB")
    out = TMP / (p.stem + ".jpg")
    im.save(out, quality=92)
    w = width
    h = w * im.height / im.width
    if max_h and h > max_h:
        h = max_h
        w = h * im.width / im.height
    return RLImage(str(out), width=w, height=h)


def tabella(righe, larghezze, header=True):
    t = Table(righe, colWidths=larghezze, hAlign="LEFT")
    stile = [
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        stile += [("BACKGROUND", (0, 0), (-1, 0), VERDE), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                  ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]
    t.setStyle(TableStyle(stile))
    return t


def piede(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2 * cm, 1.2 * cm, f"{NOME} {COGNOME} - {TITOLO}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def ore(minuti):
    minuti = int(round(minuti))
    return f"{minuti // 60} h {minuti % 60:02d} min"


def ore15(minuti):
    """Ore arrotondate al quarto d'ora (per le stime 'circa')."""
    return ore(round(minuti / 15) * 15)


def num(x, dec=1):
    return f"{x:.{dec}f}".replace(".", ",")


tot_stampa = N_MOD * MIN_MOD
tot_prep = 3 * PIATTO_MIN
tot = tot_stampa + tot_prep
t2 = 29 * MIN_MOD + 2 * PIATTO_MIN
t3 = 19 * MIN_MOD + 2 * PIATTO_MIN
tot_g = N_MOD * G_MOD
tre_min = 3 * MIN_MOD + PIATTO_MIN

s = []

# --- Copertina ---
s += [Spacer(1, 2 * cm), Paragraph("VERIFICA<br/>Laboratorio Stampa 3D", BIG), Spacer(1, 0.8 * cm),
      Paragraph(f"<b>{TITOLO}</b>", CEN), Spacer(1, 0.8 * cm),
      Paragraph(f"Nome: <b>{NOME}</b><br/>Cognome: <b>{COGNOME}</b><br/>Titolo del progetto: <b>{TITOLO}</b>", CEN),
      Spacer(1, 0.8 * cm),
      Paragraph("Consegna: mercoledì 4 novembre 2026<br/>Versione aggiornata con il modulo forato", CEN),
      Spacer(1, 1 * cm), img(FIG, width=8 * cm, max_h=11 * cm), PageBreak()]

# --- Parte 1 ---
s += [Paragraph("Parte 1 - Immagini del modulo", H1),
      Paragraph("Per il mio figurino ho pensato una canotta sagomata stampata tutta in 3D. Invece di stampare un pezzo unico, "
                "ho scelto di ripetere un solo modulo esagonale in TPU 95A. Nella prima versione il modulo aveva una nervatura "
                "a Y in rilievo. Su proposta del professore l'ho cambiato: ora è una piastra piatta e la Y è un "
                "<b>taglio passante</b>. Attraverso la Y si vede la pelle, e il pattern sul busto è più leggero e più "
                "traspirante. Le immagini mostrano il modulo in scala 1:1, con le quote in mm.", P),
      Spacer(1, 6), img("05-forato-pianta-quotata.png", width=W * 0.8, max_h=12 * cm),
      Paragraph("Pianta quotata del modulo forato (scala 1:1, quote in mm).", CAP), PageBreak(),
      Paragraph("Come si vede sul busto", H2), img("06-forato-effetto-pattern.png", width=W * 0.75, max_h=12 * cm),
      Paragraph("Più moduli accostati su fondo color pelle: la Y lascia vedere la pelle attraverso la piastra.", CAP),
      Paragraph("Dove metterei i moduli sul figurino: al centro del busto e sul petto. I fianchi sono a branchie "
                "e sotto le braccia lascio le parti lisce.", P),
      Paragraph("Dimensioni del modulo", H2),
      tabella([["Dimensione", "Valore"],
               ["Larghezza (vertice - vertice)", "60,00 mm"],
               ["Altezza (lato - lato)", "51,96 mm (circa 52 mm)"],
               ["Spessore (piastra piatta, tutta uguale)", "1,6 mm"],
               ["Taglio a Y passante", "3 bracci a punta, larghi 7,0 mm al centro"],
               ["Bordo tra la punta del braccio e il lato", "2,5 mm"],
               ["Fori di fissaggio", "6 fori, diametro 3 mm, vicino ai vertici"],
               ["Parte aperta della piastra (taglio + fori)", "circa 11,5%"],
               ["Volume del modulo", "circa 3.310 mm³"]],
              [9 * cm, 7 * cm]), PageBreak()]

# --- Parte 2 ---
s += [Paragraph("Parte 2 - Scheda tecnica del singolo modulo", H1),
      tabella([["Dato", "Valore"],
               ["Software di slicing", "OrcaSlicer"],
               ["Stampante / ugello", "Bambu Lab H2D, ugello 0,4 mm"],
               ["Materiale", "TPU 95A"],
               ["Altezza dello strato", "0,20 mm (profilo Standard)"],
               ["Parametri di stampa", "2 perimetri, 5 strati superiori, 3 inferiori, riempimento 15%"],
               ["Supporti", "non necessari (piastra piatta)"],
               ["Tempo di stampa per 1 modulo", f"circa {MIN_MOD} min (stima)"],
               ["Filamento per 1 modulo", f"circa {num(G_MOD)} g (stima)"]],
              [6 * cm, 10 * cm]),
      Spacer(1, 8),
      Paragraph("<b>Perché ho scelto il TPU.</b> Il TPU 95A è un filamento flessibile ed elastico. Una canotta si piega e si "
                "torce di continuo mentre la si indossa, e un materiale rigido come il PLA si spezzerebbe. Con una piastra di "
                "soli 1,6 mm il TPU lascia ai moduli la libertà di seguire le curve del busto e di muoversi col corpo. "
                "In più è leggero e regge bene le piegature ripetute.", P),
      Spacer(1, 4),
      Paragraph("<b>Cosa cambia con la versione forata.</b> Il modulo è tutto alla stessa altezza, quindi si stampa senza supporti "
                "e con 8 strati uguali (5 superiori e 3 inferiori coprono già tutto lo spessore). Pesa un po' di più di quello "
                "con la nervatura, perché la piastra è più spessa, anche se la Y tagliata lo alleggerisce. Le stime di tempo e "
                "filamento sono calcolate dal volume del modulo: 3.310 mm³ contro 2.311 mm³ della versione in rilievo, che "
                "avevo slicato (12 min 10 s e 2,74 g).", P),
      PageBreak()]

# --- Parte 3 ---
s += [Paragraph("Parte 3 - Dati dell'intero capo", H1),
      Paragraph("<b>Quanti moduli servono.</b> Ho stimato la zona a moduli sul figurino: il davanti del busto è circa "
                "30 x 40 cm, quindi 1.200 cm². Un modulo esagonale copre circa 23,4 cm² (area di un esagono con lato 30 mm). "
                "Faccio 1.200 / 23,4 e ottengo circa 52 moduli. Ne aggiungo un 10% di scorta, perché qualche pezzo può "
                "venire male e va rifatto: 52 x 1,10 = <b>57 moduli da stampare</b>, tutti uguali.", P),
      Spacer(1, 6),
      tabella([["Dato", "Calcolo", "Totale"],
               ["Numero di moduli", "1.200 cm² / 23,4 cm²", "52 (57 con scorta del 10%)"],
               ["Tempo di stampa", f"57 x {MIN_MOD} min", ore(tot_stampa)],
               ["Preparazione dei piatti", f"3 piatti x {PIATTO_MIN} min", f"{tot_prep} min"],
               ["Tempo di stampa totale", f"{ore(tot_stampa)} + {tot_prep} min", f"circa {ore15(tot)}"],
               ["Filamento totale", f"57 x {num(G_MOD)} g", f"circa {round(tot_g)} g (0,22 kg)"]],
              [5 * cm, 6 * cm, 5.5 * cm]),
      Spacer(1, 6),
      Paragraph("Sul piatto dell'H2D ne entrano circa 20 per volta, lasciando un po' di spazio tra un pezzo e l'altro. "
                "Quindi mi servono 3 piatti (20 + 20 + 17). Una bobina da 1 kg basta e avanza.", P),
      Paragraph("Stima complessiva dei tempi", H2),
      Paragraph(f"Con una sola stampante servono circa {ore15(tot)} di stampa. Poi c'è l'assemblaggio: i 57 moduli si uniscono "
                "con il filo passato nei fori. Calcolo circa 3 minuti a modulo, quindi circa 3 ore in più. "
                "Il margine di errore è già dentro i 57 moduli, grazie al 10% di scorta.", P),
      Spacer(1, 4),
      tabella([["Stampanti disponibili", "Tempo di stampa", "In giorni di laboratorio (8 h)"],
               ["1 stampante (H2D)", f"circa {ore15(tot)}", "circa 2 giorni"],
               ["2 stampanti", f"circa {ore15(t2)}", "circa 1 giorno"],
               ["3 stampanti", f"circa {ore15(t3)}", "mezza giornata"]],
              [5 * cm, 4.5 * cm, 7 * cm]),
      Spacer(1, 6),
      Paragraph(f"Porto al professore 3 moduli stampati insieme al PDF: sullo stesso piatto sono circa {tre_min} min in tutto "
                f"({3 * MIN_MOD} min di stampa e {PIATTO_MIN} min di preparazione) e circa {num(3 * G_MOD)} g di filamento.", P)]

doc = SimpleDocTemplate(str(DIR / OUT_NAME), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm,
                        title=f"{TITOLO} - {NOME} {COGNOME}", author=f"{NOME} {COGNOME}")
doc.build(s, onLaterPages=piede)
print("ok", OUT_NAME)
