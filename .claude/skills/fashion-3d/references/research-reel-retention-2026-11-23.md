# Research: what makes a Reel / Short work in 2026, and ElevenLabs at full power (23/11/2026)

Why: Jacopo wants the twin method (`twin-shot-blender-sop.md`, Blender only, no AI shots) to produce a full Reel. Before building, collect what is actually known about retention, pacing, camera, sound and the voice pipeline.

**How to read this file.** Every claim carries a trust tag:
- **[OFFICIAL]** read on the platform's own page (URL given, read 23/11/2026).
- **[BLOG]** practitioner / vendor blog. They often contradict each other and quote numbers with no traceable method. Use as a heuristic, never as a threshold.
- **[OURS]** already proven in this repo (taste-3d.md, short-3d-sop.md, twin SOP, HANDOFFs).
- **[GAP]** nothing reliable found.

## 1. What the platforms really say

**Instagram** (Mosseri, "Instagram Ranking Explained", 31/05/2023, so old) https://about.instagram.com/blog/announcements/instagram-ranking-explained
- [OFFICIAL] For Reels the key predictions are: will the user **reshare** it, **watch it all the way through**, like it, and go to the audio page. Reshare is the most important. (The word "send" is not in the text; sends = reshares is an inference, and other blogs say "sends per reach".)
- [OFFICIAL] Penalised: low resolution or watermarked, **muted** Reels, Reels with borders, **mostly-text** Reels, Reels already posted on Instagram.
- [OFFICIAL] Instagram polls users "is this post worth your time?".
- [GAP] No official number for first seconds, ideal length, loops, captions. creators.instagram.com / help.instagram.com gave no usable text in the fetch.
- [BLOG] "Watch time, likes per reach, sends per reach" as the 3 signals (Mosseri Jan 2025, second-hand), first 3 s decide, watch past 3 s, under 90 s. Hootsuite 07/2026 reprints a 3-minute cap for recommendations. https://blog.hootsuite.com/instagram-algorithm/ · https://www.dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers

**YouTube Shorts** https://support.google.com/youtube/answer/10059070
- [OFFICIAL] Since 31/03/2025 a Short view counts every time it starts or replays, "with no minimum watch time requirement"; the old metric is renamed **Engaged views** (viewers who chose to keep watching). Max length 3 minutes. YouTube Studio has a "Get feedback" tool that analyses "hook, pacing".
- [GAP] Official text on viewed-vs-swiped-away, loops, ranking weights: not found.
- [BLOG] 30-45 s sweet spot, or 15-30 s; "30 s at 85% retention beats 60 s at 50%"; a visual change or payoff tease every 7-10 s; loops help (unverified). https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention · https://aibrify.com/blog/youtube-shorts-retention-curve-playbook

**TikTok**: [GAP] official pages are behind login or empty. Everything below is [BLOG].

**Honest summary of the numbers.** Every retention benchmark found (60-70% under 15 s, 50% at 15-30 s, "72% average", "65% completion on 30 s entertainment") comes from vendor blogs that do not agree and cannot be traced. Do not design to a number. The only consistent direction: **keep the percentage of people who stay as high as possible, and give them a reason to share.**

## 2. Hook and first seconds
- [BLOG, consistent] The first 1-3 s decide whether the swipe happens. "A 10% gain in 1-second retention is worth more than a 100% gain in production quality" (aibrify, unverified).
- [OURS] **The hook must show the claim in the first frame** (taste-3d.md): the object or the problem visible and readable at once, opened at 3/4. An opening never equal to a previous video. Never open on a blank sheet or empty table: "an empty beat is a retention hole".
- [OURS] Start the action AS the cut lands; the voice begins on frame 1-6, no breath before.
- [BLOG] Pattern that fits our character: a **claim that is slightly wrong or surprising said to one person** («Il pantalone costa meno di 30 euro») then the proof. Curiosity gap beats a greeting.
- Rule for us: the first line of the voice is the hook AND the title card; if it does not make sense muted + read, rewrite it.

## 3. Pace, silence, rhythm
- [BLOG] Cut or change the picture every 1.5-3 s (claims of +23% completion are unsourced). "Dead time" (nothing new on screen or in the audio) is what kills retention.
- [OURS] Cuts every 2-3 s, camera tour between stations, dense set: many props in every shot (taste-3d.md). Max 2 gestures per 5 s of a single character shot (twin SOP). Silence kills retention: always a layer of sound.
- Our reconciliation: in ONE continuous Blender shot, the "cut" is a **change inside the frame**: camera push or reframe, a gesture, a prop entering, a plate, a light change. Aim for one visible change every ~2 s.
- **Pauses.** A pause is a tool, not dead time, when the picture is doing something: [OURS] a riser needs a real pause >= 0.6 s before a reveal, a price plate stays >= 1.2 s after it is said (sound.md, taste-3d.md). Use a 0.3-0.5 s silence (picture frozen, camera still pushing) ONLY just before the punchline.
- Length: [BLOG+OURS] 20-35 s for a one-idea Reel; 45-65 s only with several scenes (our Shorts #3/#11 are 60 s, not the sweet spot here). The twin shot is 5 s: a Reel of ~25-30 s = 4-5 beats of this kind.
- **Loop**: [BLOG, unverified] end on a line that reads as the start of the first; cheap to do, free to test.

## 4. Camera for a 3D character in 9:16
- [BLOG, practitioner] In vertical, the move is a **push-in** (into the frame), not a lateral dolly; a push invites the viewer in and adds presence to a mascot; a pull-out reads as isolation. No independent measurement that it raises retention.
- [OURS] Twin shot already uses an eased arc rig + Camera Shakify handheld (location scale 0.1) and a push-in "more visible than the AI's". Keep: quintic ease, never linear. f/3.5 so foreground props read.
- Practical set for a Reel (one move per beat, each tied to a word, never decorative):
  1. Hook: slightly wide, low 3/4, whole figure + the prop in the blurred foreground.
  2. Claim: slow push to mid (head and hands), the most readable gesture of the beat.
  3. Proof: cut/whip to a prop close-up (macro, DOF), 1-1.5 s, then back.
  4. Punchline: 0.3 s freeze of the camera, then a last small push on the face and a grin (the "meno di trenta" beat of the twin shot).
  5. Loop frame: same framing as the hook.
- [OURS] Keep the face readable: the mouth scale follows the camera (`--mwide`), the camera must be "centred and frontal" for key beats (feedback short 16: off-centre cameras were rejected).
- No dolly zoom, no whip pans inside a single lip-sync beat (the mouth gets smeared).

## 5. Music, silence and effects
- [OFFICIAL] Muted Reels are penalised on Instagram: there must be real audio, but see below.
- [OURS] SFX only on a real cause: a swish on a camera move, a soft tick on a plate, a metallic riser only before a built reveal, never a "pop" on every logo. Epidemic Sound via MCP, files local only (sound.md). Voice first, effects ~-18 dB under it, music bed -26 / -30 LUFS under the voice if used; nothing under elegant titles.
- Music under a talking-character Reel: [BLOG] low-key bed or none; trending audio helps discovery only on Instagram (audio page is an official prediction), but an original voice line is our brand, so: voiceover + SFX + (optional) a quiet bed; decide per Reel.
- Captions: [OFFICIAL] only the penalty for mostly-text Reels. [BLOG] captions help sound-off viewing (no measured data). Our plates carry the key phrases (one per beat); no full karaoke captions.
- ElevenLabs can make SFX (eleven_text_to_sound_v3, 0.1-30 s) and music (music_v2_5, 3 s-5 min, cleared for commercial use incl. social); Epidemic remains the default source (licensed, curated).

## 6. ElevenLabs at full power (official docs, read 23/11/2026)
Sources: https://elevenlabs.io/docs/overview/models · https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices · https://elevenlabs.io/docs/api-reference/text-to-speech/convert · https://elevenlabs.io/docs/overview/capabilities/voice-changer · https://elevenlabs.io/docs/api-reference/speech-to-speech/convert · https://elevenlabs.io/docs/creative-platform/voices/voice-cloning · https://elevenlabs.io/docs/overview/capabilities/text-to-dialogue

**Models (TTS).** [OFFICIAL] `eleven_v4` = most emotionally rich, 90+ languages, 100,000 chars per request, high-fidelity cloning and PVC support. `eleven_v4_turbo` = real-time (~100 ms), expressive. `eleven_v3` and `eleven_v3_conversational` = "previous generation" (v3: 5,000 chars). `eleven_multilingual_v2` = 29 languages, "most stable on long-form". `eleven_flash_v2_5` = ultra-fast, cheapest, 32 languages. Italian is supported by all of those except `eleven_flash_v2`. [OURS] **Use `eleven_v4`, never `eleven_v3`** for "Jacopo Prova" (measured: v4 F0 ~148 Hz, MFCC distance 15 to the Short #2 voice; v3 100 Hz, distance 46).

**Voice.** "Jacopo Prova" = IVC (instant clone), id `0CeJTHP08UsLHht7KIni`; the PVC "Jacopo" `b0cIVJILRNq2Nnc6D7im` is not preferred. [OFFICIAL] IVC needs ~1-2 min of clean audio (more than 2-3 min brings little and can make the clone unstable); the clone copies pace, pauses, breaths and "uhm" of the source recording. Both clone types can be used with v4. The official page gives NO recommended stability/similarity values for clones: [GAP] we test (see below).

**Voice settings** (`voice_settings`). [OFFICIAL, defaults] `stability` 0.5 ("lower = broader emotional range; higher can be monotonous"), `similarity_boost` 0.75, `style` 0 (exaggeration; costs latency when not 0), `speed` 1.0 (0.7-1.2 per best practices), `use_speaker_boost` true. New: `clone_strength` 0-1 for v4 with PVC (docs: 0 in most cases, 0.5 fallback) — it applies to PVC, so not to our IVC. The Creative / Natural / Robust presets are from v3 blogs ([BLOG]): not in the official pages read, so the product UI may differ; in API use the numeric stability.
- Starting plan for a talking Reel ([BLOG + test]): stability 0.35-0.5, similarity 0.75, style 0.15-0.3 (test only; raise carefully), speed 1.0-1.08, speaker boost on. Test 3 values on the SAME sentence and keep the best by ear: this is a taste decision, not a rule.
- `seed` (0-4294967295): best-effort determinism; use the same seed to compare settings fairly, vary it to get a different take. `previous_text` / `next_text`: give the neighbouring paragraphs so the prosody is continuous when a Reel is generated in several calls. `apply_text_normalization`: auto (numbers like "30" spoken correctly in Italian? check by ear: spell out «trenta» when in doubt). `language_code` "it" (ignored by multilingual_v2).
- Output: wav or pcm 44.1 kHz needs the Pro plan; mp3 44100_128 default.

**Audio tags and writing the line.** [OFFICIAL] Tags are lowercase in square brackets: `[whispering]`, `[laughs]`, `[sighs]`, `[sarcastic]`, `[low, gravelly voice]`; a tag may not work if the voice has no such delivery in training. **v4 and v3 do NOT support SSML `<break>`**: pauses come from punctuation (`...` adds pause and weight, `-`/`--` short breaks), capital letters add emphasis ("It was a VERY long day [sigh] ... nobody listens"). Too many tags or break tags make the output unstable ([BLOG+OFFICIAL on breaks]).
- Our recipe: 1 tag per emotional beat at most; write the line as spoken Italian with short clauses; put the stress word in CAPS only once per sentence; build the "meno di trenta" punchline with a comma + ellipsis before it; for a real silence generate separate paragraphs and join them with ffmpeg silence (as short-16: 0.45 s pauses), which gives exact control.
- One paragraph per generation (as in all our Shorts), 1 take, regenerate only the line that fails; compare against the Short #2 voice (F0 + MFCC with librosa) before spending more.
- Cost reference [OURS]: ~510 credits for 36.7 s (5 paragraphs, 1 take each).

**Speech-to-speech (voice changer)** [OFFICIAL]. Model `eleven_multilingual_sts_v2` (29 languages incl. Italian); `eleven_english_sts_v2` English only. It "preserves whispers, laughs, cries, accents and emotional cues of the original": Jacopo records the line with the acting he wants (pace, stress, pauses, smile) on the phone, the tool swaps the timbre for "Jacopo Prova". Max 5 min per segment; billed 1,000 characters per minute of audio; `remove_background_noise` available; `voice_settings` per request (JSON string), `seed`. [GAP] official acting tips for recording: use the clone-recording rules (quiet room, ~20 cm from the mic, 20 cm off-axis, peaks -6 to -3 dB). This is THE way to get human timing and a real laugh/grin in a line (the weak point of v4 TTS is timing; the weak point of STS is that Jacopo must act). Strategy: TTS first (free of acting), STS for the 1-2 lines that must feel human (the hook and the punchline), judged blind A/B.
- Caveat: STS output is tied to Jacopo's real timing, so the Rhubarb-style lip score must be written from the OUTPUT.

**Text to Dialogue** [OFFICIAL]: v4 recommended; many speakers, 2,000 chars per request, non-deterministic, tags in development — useful if a Reel has two voices (character and off-screen narrator), not needed for a monologue.

**Do not forget (permissions / money):** ElevenLabs is reached through the `creative_*` MCP tools of the connected ElevenLabs server (`creative_generate_speech` with `voice_id`); ask before spending credits and state the number first (memory: reference-voce-elevenlabs).

## 7. Practical rules (the short list)
1. Frame 1 shows the claim; the first spoken word comes within 0.2 s; muted + captions must still be readable.
2. One idea, 20-35 s, 4-5 beats; one visible change every ~2 s; no empty frame.
3. One camera move per beat, tied to a word; push-in as the default; stop the camera before the punchline.
4. Voice: `eleven_v4`, Jacopo Prova, one paragraph per call, seed fixed per comparison, 1 tag per emotional beat; silences built in ffmpeg between paragraphs; STS for the lines that must feel acted.
5. Pause only where the picture still moves; a 0.3-0.5 s hold before the punchline; riser only after a real pause.
6. Sound: voice on top, swishes with camera moves, nothing "pop"; quiet bed or none.
7. Share trigger: end on a line worth forwarding (a price, a rule, a challenge), not on a call-to-like; the official strongest Reels signal is the reshare.
8. Resolution full HD or more, no watermark, no borders; render 1080x1920, no text-only frames.
9. Judge on the phone: send a re-encoded copy (crf 22) and a 24 fps face-cam clip with the waveform for lip sync.
10. Do not trust any retention "benchmark" without a primary source: measure on our own analytics (Engaged views / Instagram insights) and write the result back here.

## 8. Open questions (to verify on our own posts)
- Does the loop ending raise watch time on our account? (A/B on two Reels of the same length.)
- Voice settings: which of stability 0.35 / 0.5 / 0.65 with style 0.2 reads closest to the Short #2 voice with the most life (blind A/B)?
- STS vs TTS on the hook line: which gets more comments?
- TikTok primary source: not reachable without login; ask Jacopo if he wants to paste the Creator Center page.
