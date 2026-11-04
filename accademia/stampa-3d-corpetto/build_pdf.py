"""Crea il PDF di consegna (Verifica Laboratorio Stampa 3D). Uso:  python build_pdf.py"""
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


s = []

# --- Copertina ---
s += [Spacer(1, 2 * cm), Paragraph("VERIFICA<br/>Laboratorio Stampa 3D", BIG), Spacer(1, 0.8 * cm),
      Paragraph(f"<b>{TITOLO}</b>", CEN), Spacer(1, 0.8 * cm),
      Paragraph(f"Nome: <b>{NOME}</b><br/>Cognome: <b>{COGNOME}</b><br/>Titolo del progetto: <b>{TITOLO}</b>", CEN),
      Spacer(1, 0.8 * cm), Paragraph("Consegna: mercoledì 4 novembre 2026", CEN),
      Spacer(1, 1 * cm), img("figurino-corretto.webp", width=8 * cm, max_h=11 * cm), PageBreak()]

# --- Parte 1 ---
s += [Paragraph("Parte 1 - Immagini del modulo", H1),
      Paragraph("Per il mio figurino ho pensato una canotta sagomata stampata tutta in 3D. Invece di stampare un pezzo unico, "
                "ho scelto di ripetere un solo modulo esagonale in TPU 95A. Ha una base sottile e flessibile e sopra una "
                "nervatura a Y in rilievo. Le immagini mostrano il modulo in scala 1:1, "
                "con le quote in mm, e le misure le ho controllate su Fusion 360.", P),
      Spacer(1, 6), img("04-posizione-modulo-figurino.png", width=W * 0.95, max_h=15.5 * cm),
      Paragraph("Dove metterei il modulo sul figurino: al centro del busto e sul petto. I fianchi sono a branchie "
                "e sotto le braccia lascio le parti lisce.", CAP), PageBreak(),
      Paragraph("Vista d'insieme del modulo", H2), img("03-vista-insieme.png", width=W * 0.7, max_h=9 * cm),
      Paragraph("Vista d'insieme del modulo (altezza ingrandita x2 per leggibilità).", CAP),
      Paragraph("Pianta quotata", H2), img("01-pianta-quotata.png", width=W * 0.7, max_h=9.5 * cm),
      Paragraph("Pianta in scala 1:1, quote in mm.", CAP), PageBreak(),
      Paragraph("Dettaglio degli spessori", H2), img("02-dettaglio-spessori.png", width=W * 0.85),
      Paragraph("Base da 0,8 mm e nervatura che porta lo spessore totale a 2,4 mm.", CAP),
      Paragraph("Dimensioni del modulo", H2),
      tabella([["Dimensione", "Valore"],
               ["Larghezza (vertice - vertice)", "60,00 mm"],
               ["Altezza (lato - lato)", "51,96 mm (circa 52 mm)"],
               ["Spessore base", "0,8 mm"],
               ["Spessore totale (base + nervatura)", "2,4 mm"],
               ["Larghezza nervatura (bracci della Y)", "4,0 mm"],
               ["Fori di fissaggio", "6 fori, diametro 3 mm, ai vertici"]],
              [9 * cm, 7 * cm]), PageBreak(),
      Paragraph("Verifica delle quote in Fusion 360", H2),
      img("screenshot-fusion/01-vista-insieme.webp", width=W * 0.9, max_h=7 * cm),
      Paragraph("Il modulo importato in Fusion 360 (unità in mm).", CAP),
      img("screenshot-fusion/02-lato-lato-51-962.webp", width=W * 0.9, max_h=7 * cm),
      Paragraph("Misura lato - lato: 51,962 mm.", CAP),
      img("screenshot-fusion/03-spessore-base-0-8.webp", width=W * 0.9, max_h=7 * cm),
      Paragraph("Spessore della base: 0,80 mm.", CAP), PageBreak(),
      img("screenshot-fusion/04-larghezza-nervatura-4.webp", width=W * 0.9, max_h=8 * cm),
      Paragraph("Larghezza della nervatura: 4,00 mm.", CAP),
      img("screenshot-fusion/05-altezza-totale-2-4.webp", width=W * 0.9, max_h=8 * cm),
      Paragraph("Spessore totale base + nervatura: 2,40 mm.", CAP), PageBreak()]

# --- Parte 2 ---
s += [Paragraph("Parte 2 - Scheda tecnica del singolo modulo", H1),
      tabella([["Dato", "Valore"],
               ["Software di slicing", "OrcaSlicer"],
               ["Stampante / ugello", "Bambu Lab H2D, ugello 0,4 mm"],
               ["Materiale", "TPU 95A"],
               ["Altezza dello strato", "0,20 mm (profilo Standard)"],
               ["Parametri di stampa", "2 perimetri, 5 strati superiori, 3 inferiori, riempimento 15%"],
               ["Supporti", "non necessari"],
               ["Tempo di stampa per 1 modulo", "12 min 10 s"],
               ["Filamento per 1 modulo", "2,74 g (0,94 m)"]],
              [6 * cm, 10 * cm]),
      Spacer(1, 8),
      Paragraph("<b>Perché ho scelto il TPU.</b> Il TPU 95A è un filamento flessibile ed elastico. Una canotta si piega e si "
                "torce di continuo mentre la si indossa, e un materiale rigido come il PLA si spezzerebbe. Con la base di soli 0,8 mm "
                "il TPU lascia ai moduli la libertà di seguire le curve del busto e di muoversi col corpo, e la nervatura resta comunque "
                "in rilievo. In più è leggero e regge bene le piegature ripetute.", P),
      Spacer(1, 4), img("screenshot-orca/01-slicing-1-modulo.webp", width=W, max_h=6.8 * cm),
      Paragraph("Slicing di un modulo in OrcaSlicer: tempo di stampa del modello 12 min 10 s, filamento 2,74 g.", CAP),
      img("screenshot-orca/02-impostazioni-resistenza.webp", width=W, max_h=6.8 * cm),
      Paragraph("Impostazioni di stampa (profilo 0,20 mm Standard per H2D, TPU 95A) e piatto con i moduli.", CAP), PageBreak()]

# --- Parte 3 ---
s += [Paragraph("Parte 3 - Dati dell'intero capo", H1),
      Paragraph("<b>Quanti moduli servono.</b> Ho stimato la zona a moduli sul figurino: il davanti del busto è circa "
                "30 x 40 cm, quindi 1.200 cm². Un modulo esagonale copre circa 23,4 cm² (area di un esagono con lato 30 mm). "
                "Faccio 1.200 / 23,4 e ottengo circa 52 moduli. Ne aggiungo un 10% di scorta, perché qualche pezzo può "
                "venire male e va rifatto: 52 x 1,10 = <b>57 moduli da stampare</b>, tutti uguali.", P),
      Spacer(1, 6),
      tabella([["Dato", "Calcolo", "Totale"],
               ["Numero di moduli", "1.200 cm² / 23,4 cm²", "52 (57 con scorta del 10%)"],
               ["Tempo di stampa", "57 x 12 min", "11 h 24 min"],
               ["Preparazione dei piatti", "3 piatti x 6 min", "18 min"],
               ["Tempo di stampa totale", "11 h 24 min + 18 min", "circa 11 h 45 min"],
               ["Filamento totale", "57 x 2,70 g", "circa 154 g (0,15 kg)"]],
              [5 * cm, 6 * cm, 5.5 * cm]),
      Spacer(1, 6),
      Paragraph("Sul piatto dell'H2D ne entrano circa 20 per volta, lasciando un po' di spazio tra un pezzo e l'altro. "
                "Quindi mi servono 3 piatti (20 + 20 + 17). Una bobina da 1 kg basta e avanza.", P),
      Paragraph("Stima complessiva dei tempi", H2),
      Paragraph("Per stare tranquillo aggiungo un 20% di margine, per riprove, pulizia del piatto e piccoli errori: "
                "11 h 45 min x 1,2 = circa 14 ore di stampa con una sola stampante. Poi c'è l'assemblaggio: i 57 moduli si uniscono "
                "con il filo passato nei fori. Calcolo circa 3 minuti a modulo, quindi circa 3 ore in più.", P),
      Spacer(1, 4),
      tabella([["Stampanti disponibili", "Tempo di stampa", "In giorni di laboratorio (8 h)"],
               ["1 stampante (H2D)", "circa 14 h", "circa 2 giorni"],
               ["2 stampanti", "circa 7 h", "circa 1 giorno"],
               ["3 stampanti", "circa 5 h", "mezza giornata"]],
              [5 * cm, 4.5 * cm, 7 * cm]),
      Spacer(1, 4),
      img("screenshot-orca/03-slicing-3-moduli.webp", width=W, max_h=6.5 * cm),
      Paragraph("Prova con 3 moduli sullo stesso piatto: 8,11 g di filamento, 36 min di stampa e 42 min in tutto "
                "con la preparazione. Questi 3 moduli li porto al professore insieme al PDF.", CAP)]

doc = SimpleDocTemplate(str(DIR / OUT_NAME), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm,
                        title=f"{TITOLO} - {NOME} {COGNOME}", author=f"{NOME} {COGNOME}")
doc.build(s, onLaterPages=piede)
print("ok", OUT_NAME)
