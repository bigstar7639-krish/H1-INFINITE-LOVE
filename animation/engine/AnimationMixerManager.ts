// Phase 05 - Mixer Manager Spec
// Real Three.js code in Phase 12 (Full-screen world). This file defines interface.

export interface MixerConfig {
  fadeInSeconds: number;
  fadeOutSeconds: number;
  loop: boolean;
}

export const DEFAULT_MIXER_CONFIG: MixerConfig = {
  fadeInSeconds: 0.3,
  fadeOutSeconds: 0.3,
  loop: true,
};

// Lip-sync + Eye are separate in Phase 07 / Phase 04 rig.
// This manager ONLY handles body animation blending, not face.
