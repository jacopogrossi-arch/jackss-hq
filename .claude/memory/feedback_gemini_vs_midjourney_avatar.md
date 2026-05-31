---
name: feedback-gemini-vs-midjourney-avatar
description: "Gemini batte Midjourney per generare foto consistenti dell'avatar AI (HiggsField)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8c889836-8f1d-4f46-af6e-7b7e2d5f7697
---

Per generare variazioni consistenti dell'avatar AI creato con HiggsField, **Gemini funziona meglio di Midjourney**.

**Why:** Midjourney --cref non mantiene la consistenza per avatar AI-generated. Testato su v7 (--cref non supportato) e v6.1 (supportato ma risultati pessimi — il personaggio cambia completamente). Gemini con immagine di riferimento in input mantiene le caratteristiche del viso molto bene.

**How to apply:** Quando serve generare variazioni dell'avatar (Soul ID, Character Reference, foto promozionali), usare Gemini caricando l'immagine master come riferimento. Il watermark SynthID è invisibile e non crea problemi. Midjourney può essere usato per altri scopi (sfondi, texture, mood board) ma non per la consistenza del personaggio.

[[personal-brand-ai-moda]]
