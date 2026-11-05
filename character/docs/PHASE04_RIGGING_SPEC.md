# Phase 04 - 3D Model + Rigging Spec - Aira H1

## Status: SPEC + BUILD GUIDE ONLY
No .blend / .glb file in this phase yet - model must be built in Blender by user following this guide.
This is honest: we give exact measurements + rig, not a fake model.

## 1. Blender Setup (Phone / PC)
- Blender 4.0+ recommended. On phone: use PC / friend PC / Blender in cloud if possible.
- Units: Metric, Scale 1.0, Height 1.62m
- Orientation: -Z Forward, Y Up for VRM / GLB export

## 2. Model Build Order
1. Body base mesh - adult proportions, slim, natural
2. Head + Face - soft oval, follow Phase 03 spec
3. Hair - H1 Twin-Flow: base cap + front bangs (left longer) + 2 low twin-tails
4. Eyes - Violet-Blue gradient iris, separate eye mesh for LookAt
5. Mouth - lip-sync ready, separate inner mouth
6. Outfit - H1 Day Outfit: hoodie (separate mesh), skirt (separate mesh), sneakers
7. Accessories - H1 star clip, choker

## 3. Skeleton - 55 Bones
Root > Hips > Spine > Chest > Neck > Head
- Arms: Shoulder > UpperArm > Forearm > Hand (L/R) + 5 finger bones per hand (simplified: Thumb, Index, Middle, Ring, Pinky - 2 bones each in Phase 04, full in Phase 05)
- Legs: Thigh > Shin > Foot > Toe (L/R)
- Hair: 6 bones - Front 2, Tail Left 2, Tail Right 2
- Eyes: Eye L, Eye R
- Extras: Skirt 4 bones, Hoodie 2 bones

## 4. Facial Rig - 32 Blendshapes (from Phase 03)
All blendshapes must be sculpted on same base mesh, same vertex count.
Test: Move slider 0 -> 1, no mesh tearing.

## 5. Weight Painting Rules
- Each vertex max 4 bone influences
- Head 100% Head bone, Neck blends Neck/Head
- Hair tails 100% hair bones, not head
- Skirt blends Hips/Thigh/Skirt bones

## 6. Hair + Cloth Physics (Preview)
- Hair: Spring bones / VRM SpringBone - Stiffness 0.8, Gravity 0.2
- Skirt: Cloth sim in Blender, or VRM SpringBone for export
- Hoodie: No sim in Phase 04, rigid + slight sway in Phase 05

## 7. Export
- Blender -> VRM: Use VRM Add-on, set VRM 1.0, License: Original, Author: bigstar7639-krish
- Blender -> GLB: File > Export > glTF 2.0, Include: Skinning + Blendshapes + Animations
- Files go to: character/model/base/aira_h1_base.vrm + .glb
- File size target: < 25 MB

## 8. Verification Checklist (Test)
- [ ] Model opens, no missing textures
- [ ] 55 bones present
- [ ] 32 blendshapes present
- [ ] Eyes blink + look around
- [ ] Hair moves, no clipping through body
- [ ] Export GLB < 25 MB

Next: Phase 05 Animation Engine uses this rig.
