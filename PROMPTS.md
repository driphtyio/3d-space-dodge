# Prompts Used

The entire 3D Space Dodge game was generated with two prompts to DeepSeek V4 Flash.

## Prompt 1 — Initial Game

> Build a 3D game using Three.js r128 loaded from CDN. The game is a top-down survival dodge where the player is a glowing blue sphere on a dark grid plane. Red cube enemies spawn from outside the visible area and home toward the player. WASD moves the player. Score increases every second. Game over when an enemy touches the player. Press R to restart. Camera should follow the player at a low angle. Use a 680x480 canvas. Dark theme with neon-style emissive materials.

**Result:** Complete working game on first attempt — 680 lines, all Three.js scene setup, lighting, enemy spawning, collision detection, and UI overlays.

## Prompt 2 — Bot Mode + Polish

> Add a bot mode that plays automatically. If the URL has ?bot=true, the bot should flee from the nearest enemy using flee-from-nearest-enemy steering with random wander direction and edge avoidance. Also add a glow pulse to the player sphere and a dim ring to show the arena boundary.

**Result:** Full autonomous AI steering and visual polish in one shot.
