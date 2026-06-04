import "./index.css";
import { Composition } from "remotion";
import { ManifestoReel } from "./Composition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ManifestoReel"
        component={ManifestoReel}
        durationInFrames={750}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
