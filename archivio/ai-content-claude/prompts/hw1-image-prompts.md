# Homework 1 — Image Prompts

Tool usato: **Gemini**
Brand: Luxury Italian Fashion / Old Money

---

## Variante 1 — Camera sinistra, wide angle

```
Young elegant Italian man, 25 years old, 1.80m tall, driving a vintage 1980s Ferrari convertible through a scenic Tuscan countryside road lined with tall umbrella pine trees on both sides. He wears a crisp white dress shirt, red tie, dark bold sunglasses, classic Italian old money style. Relaxed confident expression, effortless charm, timeless masculine elegance.

Shot with an exterior camera rig mounted on the left side of the car, attached from the side window toward the hood, reverse angle framing focused on the driver, with a visible portion of the front windshield and front body of the Ferrari. Wide-angle lens 16mm–24mm, low camera position, slightly forward-facing perspective. Realistic driving motion blur on road and trees, dynamic speed feeling, cinematic realism.

Warm golden sunset light coming from behind the camera, illuminating the subject's face and upper torso with rich amber tones. Polarized reflections on the windshield, glossy car paint, realistic shadows.

Subject positioned center-left, between second and third vertical thirds from the left. Composition balanced, luxury editorial framing.

Atmosphere of classic Italian dolce vita, Tuscany lifestyle, effortless wealth, 1980s Italian Riviera energy, subtle Berlusconi-era vintage success aesthetic, simplicity and pleasure of beautiful life. Minimal clean luxury fashion campaign photography, high realism, premium Instagram brand image, refined color grading, soft film grain, timeless sophisticated mood.
```

---

## Variante 2 — Camera destra, wide angle

```
[Stessa descrizione soggetto e mood della Variante 1]

Shot with an exterior camera rig mounted on the RIGHT side of the car, attached from the side window toward the hood, reverse angle framing focused on the driver. Wide-angle lens 16mm–24mm, low camera position.

Subject positioned center-RIGHT, between second and third vertical thirds from the right.
```

**Differenza rispetto alla V1:** lato camera e posizione soggetto speculari.

---

## Variante 3 — Camera sinistra, 85mm portrait

```
Young elegant Italian man, 25 years old, 1.80m tall, driving a vintage 1980s Ferrari convertible through a scenic Tuscan countryside road lined with tall umbrella pine trees. He wears a crisp white dress shirt, red tie, dark bold sunglasses, classic Italian old money style. Confident yet reflective expression, subtle emotion, timeless masculine elegance.

Shot with an exterior camera rig mounted on the left side of the car. Close camera distance, intimate composition.

Captured with an 85mm telephoto portrait lens, shallow depth of field, compressed cinematic perspective, emphasizing facial features and emotional presence. Eyes subtly visible through the dark sunglasses lenses, detailed skin texture, refined reflections on glasses.

Warm golden sunset light coming from behind the camera, illuminating the subject's face with rich amber tones. Soft highlights on cheekbones, nose and jawline. Polarized windshield reflections, luxury realism.

Subject placed center-left with portrait priority. Background softly blurred Tuscan road and pine trees, motion blur suggesting real movement.

Atmosphere of classic Italian dolce vita, Tuscany freedom, emotional silence, effortless wealth, 1980s Italian success energy, nostalgic elegance. Minimal clean luxury fashion campaign photography, high realism, premium Instagram editorial image, subtle film grain, sophisticated color grading.
```

**Differenza rispetto alla V1:** lens 85mm invece di 16–24mm → più intimo, background più sfocato, focus sul volto.

---

## JSON Prompt — Versione 3D stylized

```json
{
  "camera": {
    "angle": "left side exterior reverse three-quarter view",
    "lens": "85mm cinematic portrait lens",
    "movement": "mounted car rig tracking shot",
    "height": "low slightly above door line",
    "distance": "close to subject",
    "focus": "driver face and eyes through sunglasses"
  },
  "lighting": {
    "type": "golden hour natural sunlight",
    "key_light": "warm sunset light from behind camera",
    "fill_light": "soft ambient sky bounce",
    "rim_light": "subtle glow on hair and shoulders",
    "shadow_style": "soft cinematic contrast"
  },
  "color_palette": ["#F5E6C8", "#C9A46A", "#8B0000", "#1E1E1E", "#F8F8F2", "#2E4A3D"],
  "subject": {
    "type": "young elegant Italian man",
    "age": "25",
    "style": "classic old money Italian fashion",
    "outfit": {
      "shirt": "crisp white dress shirt",
      "tie": "deep red tie",
      "eyewear": "dark semi-transparent luxury sunglasses"
    },
    "pose": "one hand on steering wheel, relaxed posture, leaning slightly toward road",
    "expression": "confident, calm, subtle nostalgic emotion",
    "features": "eyes faintly visible through lenses"
  },
  "vehicle": {
    "type": "1980s Ferrari convertible",
    "color": "classic red",
    "finish": "glossy polished paint",
    "details": "visible windshield frame, dashboard, hood edge"
  },
  "environment": {
    "location": "Tuscan countryside road",
    "road_type": "two-lane scenic road",
    "surroundings": "tall umbrella pine trees on both sides, warm summer landscape",
    "weather": "clear sky"
  },
  "composition": {
    "subject_position": "center-left",
    "framing": "tight portrait with partial car body visible",
    "depth": "blurred background with motion streaks",
    "balance": "luxury editorial symmetry"
  },
  "mood": {
    "keywords": ["dolce vita", "bella vita italiana", "1980s success", "timeless elegance", "effortless wealth", "summer freedom"]
  },
  "render_style": {
    "type": "stylized 3D luxury editorial illustration",
    "shading": "semi-realistic toon shading",
    "materials": "premium glossy surfaces and soft fabric textures",
    "detail_level": "high",
    "post_process": "subtle film grain, cinematic color grading"
  }
}
```

---

## JSON Prompt — Versione fotorealistica

```json
{
  "camera": {
    "angle": "left side exterior reverse three-quarter view",
    "lens": "85mm portrait lens",
    "movement": "mounted car rig tracking shot",
    "height": "low slightly above door line",
    "distance": "close to subject",
    "focus": "driver face and eyes through sunglasses",
    "depth_of_field": "shallow cinematic depth"
  },
  "lighting": {
    "type": "golden hour natural sunlight",
    "key_light": "warm sunset light from behind camera",
    "fill_light": "soft sky bounce",
    "rim_light": "subtle natural edge light",
    "shadow_style": "soft realistic contrast"
  },
  "color_palette": ["#F4E7CF", "#C89D63", "#8B0000", "#111111", "#F8F8F8"],
  "subject": {
    "type": "real young Italian man",
    "age": "25",
    "body": "lean athletic build",
    "hair": "dark brown neatly styled hair",
    "skin": "natural realistic skin texture",
    "outfit": {
      "shirt": "white dress shirt",
      "tie": "dark red silk tie",
      "eyewear": "luxury dark semi-transparent sunglasses"
    },
    "pose": "one hand on steering wheel, relaxed confident posture",
    "expression": "calm, successful, subtle emotion",
    "eyes": "slightly visible through sunglasses"
  },
  "vehicle": {
    "type": "1980s Ferrari convertible",
    "color": "classic deep red",
    "finish": "real glossy paint reflections"
  },
  "environment": {
    "location": "Tuscan countryside road",
    "details": "umbrella pine trees on both sides, summer road, Italy"
  },
  "composition": {
    "subject_position": "center-left",
    "framing": "tight portrait with visible windshield and hood",
    "background": "slightly blurred motion scenery"
  },
  "style": {
    "type": "photorealistic luxury fashion photography",
    "medium": "cinematic DSLR campaign photo",
    "texture": "real skin, real fabric, real glass reflections",
    "quality": "ultra realistic",
    "post_process": "subtle film grain, premium editorial grading"
  },
  "negative_prompt": ["cartoon", "3D render", "toon shading", "illustration", "plastic skin", "CGI face", "fake anatomy", "animated character"]
}
```

---

## Note e osservazioni

- La variante con 85mm crea un'immagine molto più intima e portrait-focused rispetto al wide angle
- Il JSON prompt fotorealistico con `negative_prompt` produce risultati più stabili
- Gemini tende ad aggiungere dettagli di sfondo anche quando non richiesti — specificare sempre "blurred background"
