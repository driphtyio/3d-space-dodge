---
title: "3D Space Dodge — Building a Three.js Survival Game with AI"
description: "We take the classic dodge-em-up into 3D with Three.js, using DeepSeek V4 Flash to generate the entire game from scratch. Complete with perspective camera, enemy AI, and bot-mode steering."
pubDate: 2026-06-19
tags: ["threejs", "3d", "ai-game-dev", "tutorial", "game-dev"]
heroImage: "https://pub-0066f5275194430aa9f985cb23278abe.r2.dev/3d-space-dodge-1781914048.jpg"
---

How far can a single prompt take you when you switch from 2D Phaser to full 3D with Three.js? We asked DeepSeek V4 Flash to build a 3D survival dodge game from scratch — no human edits to the game logic, no post-processing, just the raw model output with one follow-up prompt to add bot mode.

### Play the Game

> Dodge the red cubes in 3D space. **WASD** to move, **R** to restart. The arena boundary glows dimly at the edges. Survive as long as you can.

<div class="game-embed">
  <iframe src="/games/3d-space-dodge/" title="3D Space Dodge — Three.js survival game" loading="lazy" allow="keyboard"></iframe>
</div>
<em>Built by <strong>DeepSeek V4 Flash</strong> — 2 prompts, ~30s generation, ~8K tokens</em>

The arena is a dark grid plane viewed from a low-angle perspective camera that follows your movement. Red cubes spawn from the outer ring, homing toward you with slight jitter so they're predictable but not trivial. Speed and spawn rate scale with your score.

### The Prompt Chain

The entire game was built with two prompts:

**Prompt 1 — Initial game:**
> Build a 3D game using Three.js r128 loaded from CDN. The game is a top-down survival dodge where the player is a glowing blue sphere on a dark grid plane. Red cube enemies spawn from outside the visible area and home toward the player. WASD moves the player. Score increases every second. Game over when an enemy touches the player. Press R to restart. Camera should follow the player at a low angle. Use a 680x480 canvas. Dark theme with neon-style emissive materials.

The model produced a complete, working game on the first attempt — 680 lines, all Three.js scene setup, lighting, enemy spawning, collision detection, and UI overlays. The only structural issue was that the arena boundary ring wasn't visible enough at the default camera angle.

**Prompt 2 — Bot mode + polish:**
> Add a bot mode that plays automatically. If the URL has ?bot=true, the bot should flee from the nearest enemy using flee-from-nearest-enemy steering with random wander direction and edge avoidance. Also add a glow pulse to the player sphere and a dim ring to show the arena boundary.

This added the full autonomous AI steering and visual polish in one shot.

### How It Works

The game is a single HTML file with three core systems:

1. **3D Scene** — Three.js r128 with a `PerspectiveCamera` at 50° FOV positioned above and behind the player. Lighting uses ambient + directional lights with shadow mapping for depth perception. The ground is a `1200x1200` dark plane with a 30-segment grid helper for spatial reference.

2. **Enemy AI** — Red cubes spawn at a random angle along a 450-unit radius outside the visible arena. Each frame, every enemy calculates the vector toward the player and moves along it with a small random jitter (`±15` units in x and z). The jitter prevents enemies from forming a perfect converging line, creating emergent swarming behavior. Enemy speed starts at 55 and increases by 0.8 per score point (capped at +60). Spawn interval drops from 2200ms to a minimum of 600ms. At high scores, extra enemies spawn automatically when the interval drops below 800ms.

3. **Player Movement** — WASD drives velocity on the x-z plane with diagonal normalization (`0.7071`). The player is clamped to a circular boundary of radius 330 units. Collision is distance-based: `sqrt(dx² + dz²) < playerRadius + enemySize/2`. On death, the player turns red, all enemies stop, and a game-over overlay appears. Telemetry fires via GoatCounter.

4. **Bot Mode** — The `?bot=true` URL parameter activates autonomous steering. The bot computes the nearest enemy, then blends a flee vector (away from that enemy, weighted by proximity) with a random wander direction that changes every 500-1500ms. Edge-avoidance pushes the bot back when it drifts within 60 units of the boundary. Speed is capped at 220 units/s (slightly faster than the human speed of 200, since the bot needs a reaction-time edge).

### Token & Cost Breakdown

| Metric | Value |
|--------|-------|
| Prompts | 2 |
| Model | DeepSeek V4 Flash |
| Temperature | 0.7 |
| Max Tokens | 4,096 |
| Input Tokens | ~400 |
| Output Tokens | ~7,600 |
| Total Cost | ~$0.001 |
| Build Time | ~30s |
| File Size | 14.3 KB |

For a simple 3D game under 500 lines, the cost is negligible — less than a tenth of a cent. A more complex 3D scene with physics, networking, or custom shaders would cost more due to longer prompts and more iterations.

### Remix Ideas

- **Power-ups** — Add green orbs that give temporary speed boost or shield
- **Enemy types** — Mix in slow large cubes and fast small spheres with different behaviors
- **Weapon system** — Click to fire projectiles that destroy enemies
- **Score multipliers** — Collectible gems that multiply score gain for a few seconds
- **Particles** — Add particle trails to the player and explosion effects on enemy destruction
- **Mobile support** — Add touch joystick controls for mobile play
- **Endless runner variant** — Instead of a static arena, make the camera move forward and enemies spawn ahead

The full source is on [GitHub](https://github.com/driphtyio/3d-space-dodge) ([prompts](https://github.com/driphtyio/3d-space-dodge/blob/master/PROMPTS.md)). Try the [bot mode](/games/3d-space-dodge/?bot=true) to see the AI-steered player in action.
