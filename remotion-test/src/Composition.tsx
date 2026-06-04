import {
  AbsoluteFill,
  Audio,
  Sequence,
  Video,
  useCurrentFrame,
  interpolate,
  staticFile,
} from "remotion";

const VOICEOVER = "hf_20260601_113702_a8138b7d-feda-4727-9312-2328908dac1c.mp3";

const CLIPS = [
  "hf_20260601_115925_fa91c77b-f272-49af-b84a-3086164cc12f.mp4",
  "hf_20260601_121703_a32dce72-e60e-4d29-a208-21f4fbee1612.mp4",
  "hf_20260602_144225_6e38e4ff-585e-49b8-86b4-4c503ae8264f.mp4",
  "hf_20260602_144555_28cf1b8b-ac9f-4414-b82a-3164ebd9b913.mp4",
  "hf_20260602_144638_2cbaf6c1-260c-4896-95f2-e83a45b9a2d4.mp4",
  "hf_20260602_150133_b0769e11-73c8-408d-a5dd-13a7dcafca3b.mp4",
];

// 6 clips × 125 frames = 750 frames = 25s at 30fps
const CLIP_DURATION = 125;

const OVERLAYS: { line: string; from: number; duration: number }[] = [
  { line: "WHAT IF AI COULD BUILD\nA FASHION BRAND?", from: 30,  duration: 75 },
  { line: "I'M BUILDING IT —\nPUBLICLY.",            from: 420, duration: 75 },
  { line: "FOLLOW IF YOU WANT\nTO SEE WHERE THIS GOES.", from: 510, duration: 90 },
  { line: "YOU'LL SEE WHAT\nACTUALLY WORKS.",        from: 615, duration: 60 },
  { line: "AND WHAT DOESN'T.",                        from: 675, duration: 60 },
];

function TextLine({ line, totalDuration }: { line: string; totalDuration: number }) {
  const frame = useCurrentFrame();

  const opacity = interpolate(
    frame,
    [0, 12, totalDuration - 12, totalDuration],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const y = interpolate(frame, [0, 18], [28, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{ display: "flex", alignItems: "flex-end", padding: "0 64px 140px" }}
    >
      <p
        style={{
          margin: 0,
          opacity,
          transform: `translateY(${y}px)`,
          color: "#fff",
          fontFamily: "Georgia, 'Times New Roman', serif",
          fontSize: 68,
          fontWeight: 400,
          lineHeight: 1.15,
          letterSpacing: "0.04em",
          textTransform: "uppercase",
          whiteSpace: "pre-line",
          textShadow: "0 2px 40px rgba(0,0,0,0.95)",
        }}
      >
        {line}
      </p>
    </AbsoluteFill>
  );
}

function ClipTransition({ totalDuration }: { totalDuration: number }) {
  const frame = useCurrentFrame();

  const fadeIn = interpolate(frame, [0, 10], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [totalDuration - 10, totalDuration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const opacity = Math.max(fadeIn, fadeOut);

  return (
    <AbsoluteFill
      style={{ background: `rgba(0,0,0,${opacity})`, pointerEvents: "none" }}
    />
  );
}

export function ManifestoReel() {
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {/* Voiceover */}
      <Audio src={staticFile(VOICEOVER)} />

      {/* Video clips in sequence */}
      {CLIPS.map((clip, i) => (
        <Sequence key={clip} from={i * CLIP_DURATION} durationInFrames={CLIP_DURATION}>
          <Video
            src={staticFile(clip)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "sepia(12%) brightness(0.88) contrast(1.06)",
            }}
          />
          <ClipTransition totalDuration={CLIP_DURATION} />
        </Sequence>
      ))}

      {/* Radial vignette */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at 50% 45%, transparent 28%, rgba(0,0,0,0.65) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* Bottom gradient — keeps text readable */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(to top, rgba(0,0,0,0.92) 0%, rgba(0,0,0,0.25) 28%, transparent 48%)",
          pointerEvents: "none",
        }}
      />

      {/* Text overlays */}
      {OVERLAYS.map((o, i) => (
        <Sequence key={i} from={o.from} durationInFrames={o.duration}>
          <TextLine line={o.line} totalDuration={o.duration} />
        </Sequence>
      ))}

      {/* Film grain */}
      <AbsoluteFill
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='256' height='256'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='256' height='256' filter='url(%23n)'/%3E%3C/svg%3E")`,
          opacity: 0.07,
          mixBlendMode: "overlay",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
}

// keep old export for backward compat
export const MyComposition = ManifestoReel;
