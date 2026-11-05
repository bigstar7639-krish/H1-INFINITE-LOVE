# Animation Spec - Phase 05

## 14 Animations
Idle, Walking, Running, Dancing, Sitting, Standing, Sleeping, Talking, Laughing, Crying, Eating, Drinking, Looking Around, Hand Gestures

## How it works
1. StateMachine checks if transition allowed
2. Checks if clip file exists
3. If not exists -> returns NOT_IMPLEMENTED, does NOT fake play
4. If exists -> Mixer fades 0.3 sec, plays clip, loops if needed

## Blender Guide
- Make each clip in Blender Action Editor
- Export each as separate .glb with only that action
- Name exactly as in animation-clips.json
- Keep same skeleton (55 bones) for all clips

## Eye + Lip-sync
- Eye: Phase 04 rig, controlled separately
- Lip-sync: Phase 07 voice, visemes A-E-I-O-U-M

Next: Phase 06 Emotion Engine
