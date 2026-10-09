import React from 'react';
import {Composition} from 'remotion';
import {DURATION, FPS, H, Reel, W} from './Reel';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Reel" component={Reel} durationInFrames={DURATION} fps={FPS} width={W} height={H} defaultProps={{showText: true, withAudio: true}} />
    <Composition id="ReelClean" component={Reel} durationInFrames={DURATION} fps={FPS} width={W} height={H} defaultProps={{showText: false, withAudio: false}} />
  </>
);
