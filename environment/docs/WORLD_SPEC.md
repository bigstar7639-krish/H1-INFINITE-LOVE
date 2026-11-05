# World Spec - Phase 12 - FULL-SCREEN

## Worlds (3)
1. Bedroom - 8x8m - Bed, Desk, Wardrobe, Window, Lamp, Bookshelf - DEFAULT
2. Garden - 20x20m - Trees, Flowers, Bench, Pond, Path, Swing
3. Living Room - 10x8m - Sofa, TV, Table, Plant, Lamp, Rug

## Full-screen Rules
- World fills 100% screen, NOT mini-screen
- Aira is full-body in world, can walk / sit / stand
- User can swipe to look around, tap objects, tap Aira to talk
- Top bar: World switch + Settings (minimal, not blocking world)
- Bottom: Chat / Talk bar (collapsible)

## Systems
- Day/Night: Real time OR user set - Morning / Afternoon / Evening / Night - lighting changes
- Weather: Sunny / Rainy / Cloudy / Snowy / Stormy - particles + light + sound
- Lighting: Ambient + Sun/Moon + Lamp + TV - brightness + warm controls
- Interactive Objects: Tap -> Animation + Reply (see InteractiveObjects.ts)

## Customization
- Wall color, Floor, Furniture layout, Lamp, Weather, Time

## What is NOT done
- No 3D world .glb yet - build in Blender / Three.js
- No Three.js viewer yet - Phase 17 Website will have viewer, Android will use WebView in Phase 13

Next: Phase 13 Mobile Integrations
