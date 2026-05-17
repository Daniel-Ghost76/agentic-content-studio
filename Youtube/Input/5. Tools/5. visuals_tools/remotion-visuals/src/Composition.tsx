import type { CSSProperties } from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  OffthreadVideo,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const softText = "rgba(241, 255, 253, 0.92)";
const mutedText = "rgba(213, 244, 241, 0.68)";

const glassPanel: CSSProperties = {
  backdropFilter: "blur(26px) saturate(1.18)",
  background:
    "linear-gradient(135deg, rgba(233, 255, 252, 0.08), rgba(15, 40, 44, 0.18) 48%, rgba(5, 17, 19, 0.08))",
  border: "1px solid rgba(177, 255, 249, 0.24)",
  boxShadow:
    "0 34px 88px rgba(0, 0, 0, 0.22), 0 0 42px rgba(120, 221, 212, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.18)",
  color: softText,
  fontFamily:
    'Avenir Next, "SF Pro Display", "Helvetica Neue", sans-serif',
  overflow: "hidden",
  position: "absolute",
  WebkitBackdropFilter: "blur(26px) saturate(1.18)",
};

const dotLayer: CSSProperties = {
  backgroundImage:
    "radial-gradient(circle, rgba(201, 255, 250, 0.2) 1px, transparent 1.5px)",
  backgroundSize: "18px 18px",
  inset: 0,
  maskImage:
    "linear-gradient(135deg, rgba(0,0,0,0.85), rgba(0,0,0,0.08))",
  opacity: 0.3,
  position: "absolute",
};

const glowLayer: CSSProperties = {
  background:
    "radial-gradient(circle at 18% 20%, rgba(120, 221, 212, 0.15), transparent 34%), radial-gradient(circle at 80% 78%, rgba(77, 186, 178, 0.08), transparent 42%)",
  inset: 0,
  position: "absolute",
};

const innerGlass: CSSProperties = {
  backdropFilter: "blur(18px) saturate(1.22)",
  background:
    "linear-gradient(135deg, rgba(42, 126, 119, 0.5), rgba(9, 42, 45, 0.3))",
  border: "1px solid rgba(166, 244, 237, 0.48)",
  boxShadow:
    "0 24px 54px rgba(0, 0, 0, 0.3), 0 0 38px rgba(120, 221, 212, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.2)",
  WebkitBackdropFilter: "blur(18px) saturate(1.22)",
};

const contentLayer: CSSProperties = {
  inset: 0,
  position: "absolute",
  zIndex: 2,
};

const timedOpacity = (
  frame: number,
  start: number,
  end: number,
  peakOpacity = 0.88,
) =>
  interpolate(
    frame,
    [start, start + 10, end - 10, end],
    [0, peakOpacity, peakOpacity, 0],
    {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    },
  );

const softEnter = (frame: number, start: number, fps: number) =>
  spring({
    config: {
      damping: 18,
      mass: 0.72,
      stiffness: 95,
    },
    fps,
    frame: frame - start,
  });

const TimedOverlay: React.FC<{
  children: (progress: number, opacity: number) => React.ReactNode;
  end: number;
  peakOpacity?: number;
  start: number;
}> = ({ children, end, peakOpacity, start }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = timedOpacity(frame, start, end, peakOpacity);
  const progress = softEnter(frame, start, fps);

  if (frame < start - 12 || frame > end + 12) {
    return null;
  }

  return <>{children(progress, opacity)}</>;
};

const AiBusinessChip: React.FC = () => {
  const frame = useCurrentFrame();
  const progressWidth = interpolate(frame, [20, 49], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <TimedOverlay end={96} peakOpacity={0.97} start={8}>
      {(progress, opacity) => (
        <div
          style={{
            ...glassPanel,
            borderRadius: 48,
            height: 252,
            left: 300,
            opacity,
            top: 588,
            transform: `translate3d(${interpolate(progress, [0, 1], [-118, 0])}px, 0, 0) scale(${interpolate(progress, [0, 1], [0.94, 1])})`,
            width: 1180,
          }}
        >
          <div style={glowLayer} />
          <div style={dotLayer} />
          <div
            style={{
              ...contentLayer,
              alignItems: "center",
              display: "flex",
              gap: 42,
              padding: "38px 54px",
            }}
          >
            <div
              style={{
                ...innerGlass,
                alignItems: "center",
                borderRadius: 999,
                color: "rgba(221, 255, 252, 0.86)",
                display: "flex",
                fontSize: 36,
                fontWeight: 800,
                height: 126,
                justifyContent: "center",
                letterSpacing: 1,
                width: 126,
              }}
            >
              01
            </div>
            <div style={{ flex: 1 }}>
              <div
                style={{
                  fontSize: 82,
                  fontWeight: 800,
                  letterSpacing: 0.2,
                  lineHeight: 1,
                  textShadow: "0 0 18px rgba(238, 255, 252, 0.22)",
                }}
              >
                AI BUSINESS
              </div>
              <div
                style={{
                  color: mutedText,
                  fontSize: 32,
                  fontWeight: 700,
                  letterSpacing: 4,
                  marginTop: 14,
                }}
              >
                FROM SCRATCH
              </div>
              <div
                style={{
                  background: "rgba(183, 244, 238, 0.1)",
                  borderRadius: 999,
                  height: 7,
                  marginTop: 24,
                  overflow: "hidden",
                  width: 520,
                }}
              >
                <div
                  style={{
                    background:
                      "linear-gradient(90deg, rgba(88, 191, 181, 0.44), rgba(167, 255, 247, 0.72))",
                    borderRadius: 999,
                    height: "100%",
                    transform: `scaleX(${progressWidth})`,
                    transformOrigin: "left",
                    width: "100%",
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </TimedOverlay>
  );
};

const GoodBadUglyCards: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cards = [
    { accent: "#8bd8c8", label: "GOOD", start: 121, x: 56, rotate: -3 },
    { accent: "#d3ba72", label: "BAD", start: 134, x: 448, rotate: 1 },
    { accent: "#d9908d", label: "UGLY", start: 148, x: 840, rotate: 3 },
  ];

  return (
    <TimedOverlay end={220} peakOpacity={0.97} start={108}>
      {(progress, opacity) => (
        <div
          style={{
            ...glassPanel,
            borderRadius: 48,
            height: 306,
            left: 310,
            opacity,
            perspective: 1000,
            top: 558,
            transform: `translate3d(0, ${interpolate(progress, [0, 1], [34, 0])}px, 0) scale(${interpolate(progress, [0, 1], [0.975, 1])})`,
            width: 1240,
          }}
        >
          <div style={glowLayer} />
          <div style={dotLayer} />
          {cards.map((card) => {
            const cardIn = spring({
              config: {
                damping: 16,
                mass: 0.65,
                stiffness: 130,
              },
              fps,
              frame: frame - card.start,
            });
            const cardOpacity = interpolate(
              frame,
              [card.start - 4, card.start + 7],
              [0, 1],
              {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              },
            );

            return (
              <div
                key={card.label}
                style={{
                  ...innerGlass,
                  background: `linear-gradient(135deg, ${card.accent}36, rgba(9, 42, 45, 0.46))`,
                  border: `1px solid ${card.accent}88`,
                  borderRadius: 36,
                  boxShadow: `0 28px 64px rgba(0, 0, 0, 0.34), 0 0 42px ${card.accent}2e, inset 0 1px 0 rgba(255, 255, 255, 0.22)`,
                  height: 214,
                  left: card.x,
                  opacity: cardOpacity,
                  overflow: "hidden",
                  position: "absolute",
                  top: 46,
                  transform: `translate3d(${interpolate(cardIn, [0, 1], [-64, 0])}px, ${interpolate(cardIn, [0, 1], [32, 0])}px, 0) rotateY(${interpolate(cardIn, [0, 1], [-28, 0])}deg) rotateZ(${card.rotate}deg)`,
                  transformOrigin: "center bottom",
                  width: 344,
                }}
              >
                <div
                  style={{
                    ...glowLayer,
                    background: `radial-gradient(circle at 26% 24%, ${card.accent}4d, transparent 34%), radial-gradient(circle at 84% 78%, rgba(120, 221, 212, 0.1), transparent 40%)`,
                  }}
                />
                <div style={dotLayer} />
                <div
                  style={{
                    ...contentLayer,
                    alignItems: "center",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                  }}
                >
                  <div
                    style={{
                      background: card.accent,
                      borderRadius: 999,
                      boxShadow: `0 0 24px ${card.accent}66`,
                      height: 16,
                      marginBottom: 24,
                      width: 16,
                    }}
                  />
                  <div
                    style={{
                      color: softText,
                      fontSize: 70,
                      fontWeight: 850,
                      letterSpacing: 2,
                      textShadow: `0 0 20px ${card.accent}38`,
                    }}
                  >
                    {card.label}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </TimedOverlay>
  );
};

const WorkflowMap: React.FC = () => {
  const frame = useCurrentFrame();

  const arrowProgress = interpolate(frame, [304, 352], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const transcriptProgress = interpolate(frame, [386, 428], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <TimedOverlay end={486} start={286}>
      {(progress, opacity) => (
        <div
          style={{
            ...glassPanel,
            borderRadius: 44,
            height: 246,
            left: 82,
            opacity,
            top: 588,
            transform: `translate3d(0, ${interpolate(progress, [0, 1], [34, 0])}px, 0) scale(${interpolate(progress, [0, 1], [0.975, 1])})`,
            width: 1560,
          }}
        >
          <div style={glowLayer} />
          <div style={dotLayer} />
          <div
            style={{
              ...contentLayer,
              alignItems: "center",
              display: "flex",
              gap: 34,
              padding: "36px 46px",
            }}
          >
            <div
              style={{
                alignItems: "center",
                ...innerGlass,
                borderRadius: 32,
                display: "flex",
                gap: 24,
                height: 174,
                padding: "0 28px",
                width: 370,
              }}
            >
              <div
                style={{
                  ...innerGlass,
                  alignItems: "center",
                  borderRadius: 26,
                  display: "flex",
                  height: 96,
                  justifyContent: "center",
                  width: 96,
                }}
              >
                <div
                  style={{
                    borderBottom: "18px solid transparent",
                    borderLeft: "30px solid rgba(238, 255, 252, 0.86)",
                    borderTop: "18px solid transparent",
                    height: 0,
                    marginLeft: 5,
                    width: 0,
                  }}
                />
              </div>
              <div>
                <div
                  style={{
                    color: mutedText,
                    fontSize: 22,
                    fontWeight: 700,
                    letterSpacing: 2,
                  }}
                >
                  INPUT
                </div>
                <div
                  style={{
                    color: softText,
                    fontSize: 42,
                    fontWeight: 820,
                    lineHeight: 1.05,
                    marginTop: 6,
                  }}
                >
                  YouTube
                  <br />
                  channel
                </div>
              </div>
            </div>
            <div
              style={{
                alignItems: "center",
                display: "flex",
                flex: 1,
                gap: 22,
                justifyContent: "center",
              }}
            >
              <div
                style={{
                  background: "rgba(183, 244, 238, 0.1)",
                  borderRadius: 999,
                  height: 5,
                  overflow: "hidden",
                  width: 178,
                }}
              >
                <div
                  style={{
                    background:
                      "linear-gradient(90deg, rgba(88, 191, 181, 0.38), rgba(167, 255, 247, 0.72))",
                    height: "100%",
                    transform: `scaleX(${arrowProgress})`,
                    transformOrigin: "left",
                    width: "100%",
                  }}
                />
              </div>
              <div
                style={{
                  alignItems: "center",
                  ...innerGlass,
                  borderRadius: 999,
                  color: softText,
                  display: "flex",
                  fontSize: 24,
                  fontWeight: 800,
                  height: 96,
                  justifyContent: "center",
                  letterSpacing: 1,
                  width: 190,
                }}
              >
                AI FLOW
              </div>
              <div
                style={{
                  background: "rgba(183, 244, 238, 0.1)",
                  borderRadius: 999,
                  height: 5,
                  overflow: "hidden",
                  width: 178,
                }}
              >
                <div
                  style={{
                    background:
                      "linear-gradient(90deg, rgba(88, 191, 181, 0.38), rgba(167, 255, 247, 0.72))",
                    height: "100%",
                    transform: `scaleX(${arrowProgress})`,
                    transformOrigin: "left",
                    width: "100%",
                  }}
                />
              </div>
            </div>
            <div
              style={{
                ...innerGlass,
                borderRadius: 32,
                height: 174,
                padding: "26px 30px",
                width: 410,
              }}
            >
              <div
                style={{
                  color: mutedText,
                  fontSize: 22,
                  fontWeight: 700,
                  letterSpacing: 2,
                }}
              >
                OUTPUT
              </div>
              <div
                style={{
                  color: softText,
                  fontSize: 35,
                  fontWeight: 820,
                  marginTop: 6,
                  whiteSpace: "nowrap",
                }}
              >
                Transcript data
              </div>
              {[0, 1, 2].map((row) => (
                <div
                  key={row}
                  style={{
                    background: "rgba(221, 255, 252, 0.62)",
                    borderRadius: 999,
                    height: 6,
                    marginTop: 11,
                    opacity: interpolate(
                      transcriptProgress,
                      [row * 0.2, row * 0.2 + 0.2],
                      [0, 1],
                      {
                        extrapolateLeft: "clamp",
                        extrapolateRight: "clamp",
                      },
                    ),
                    width: [220, 264, 186][row],
                  }}
                />
              ))}
            </div>
          </div>
        </div>
      )}
    </TimedOverlay>
  );
};

const MotionGraphicOverlays: React.FC = () => {
  return (
    <>
      <AiBusinessChip />
      <GoodBadUglyCards />
      <WorkflowMap />
    </>
  );
};

export const MyComposition = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <OffthreadVideo
        src={staticFile("assets/1-video-day-1-browser-safe.mp4")}
        style={{
          height: "100%",
          objectFit: "cover",
          width: "100%",
        }}
      />
      <MotionGraphicOverlays />
    </AbsoluteFill>
  );
};
