# Homework 2 — Video Prompts (Kling)

Tool usato: **Kling**
Brand: Luxury Italian Fashion / Old Money

---

## Task 1 — Text-to-Video (TTV)

Struttura obbligatoria: **Subject + Action + Context + Style**

```
Real young elegant Italian man driving a deep red 1980s Ferrari convertible on a Tuscan countryside road lined with umbrella pine trees. He wears a white dress shirt, dark red tie, luxury dark sunglasses. Golden sunset light, warm summer atmosphere.

Start with a left side exterior tracking shot of the moving car. Camera follows smoothly beside the Ferrari, then slowly pushes in for a cinematic close-up of the driver's face. The driver turns his head toward the camera, eyes subtly visible through the sunglasses, calm confident expression.

Hold the close-up briefly, then the camera stops while the Ferrari continues forward. Final shot shows the rear of the car driving away down the road toward the horizon.

Ultra realistic cinematic video, luxury fashion campaign, Italian dolce vita, 1980s success energy, premium warm color grading, subtle film grain, real skin texture, real reflections, no cartoon, no CGI.
```

---

## Task 2 — Image-to-Video (I2V)

**Immagine di partenza:** frame generato in Homework 1 (Variante 3, 85mm, camera sinistra)

**Regola I2V:** descrivere SOLO il movimento — cosa si muove, cosa è statico, endpoint finale.

```
Use the uploaded image as the first frame. Keep the same subject, Ferrari, road, lighting and composition.

Smooth cinematic side tracking shot moving forward at the same speed as the Ferrari. Camera slowly pushes closer toward the driver's face for a premium close-up. The man subtly turns his head toward the camera while continuing to drive, calm confident expression.

Hold the close-up briefly. Then the camera gently decelerates and remains behind as the Ferrari continues driving forward ahead on the road, naturally increasing distance from camera. The car must never reverse or move backward. The Ferrari passes ahead and continues away into the distance.

Final shot shows rear three-quarter view of the Ferrari getting smaller as it drives forward toward the horizon.

Maintain realistic forward wheel rotation, correct road perspective, natural suspension movement, subtle wind on hair and shirt, real reflections on sunglasses and car paint, shallow depth of field, smooth stabilization.

Ultra realistic cinematic luxury fashion campaign, elegant Italian dolce vita mood, no backward motion, no reverse driving, no cartoon, no CGI, no flicker, no face distortion.
```

---

## Note tecniche e problemi riscontrati

- **Bug I2V:** il video generato mostra la Ferrari che va all'indietro in alcuni casi → cause probabili: il modello interpreta "camera decelerates" come "soggetto rallenta e torna indietro". Soluzione da testare: aggiungere "The Ferrari always moves FORWARD. Wheels rotate forward only. No reverse motion whatsoever."
- **Modello usato:** Kling (specificare versione nei prossimi test)
- **TTV vs I2V:** il TTV senza frame di partenza ha più libertà creativa ma meno controllo; l'I2V con immagine forte di partenza garantisce coerenza visiva

---

## Prossimi miglioramenti da testare

- [ ] Aggiungere "forward motion only" esplicito per risolvere il bug del reverse
- [ ] Testare Kling Pro vs standard per stabilità I2V
- [ ] Provare motion endpoint diversi: es. "camera rises above car for aerial shot"
- [ ] Testare con immagine di partenza HiggsField invece di Gemini (qualità superiore)
