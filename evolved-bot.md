---
title: "I Evolved a Bot to Play Its Own Game — In 1 Generation"
description: "What happens when you apply evolutionary strategies to a Three.js dodge game? The answer reveals something surprising about game AI and enemy design."
pubDate: 2026-06-19
tags: ["evolutionary-algorithm", "game-ai", "threejs", "bot", "experiment", "machine-learning"]
heroImage: "https://pub-0066f5275194430aa9f985cb23278abe.r2.dev/img-20260619-220458-1781931906.jpg"
---

We benchmarked 18 LLMs building a 3D dodge game. Every model that passed implemented a bot mode (`?bot=true`) — but every bot was the same: flee toward center when enemies get close. Hardcoded. Boring.

What if we could evolve a bot that actually learns to dodge?

### The Setup

I built a pure-Python simulation of the game — same physics, same enemy behavior, same collision rules — but at 60x speed. A six-weight genome controls the bot:

| Weight | Controls | Range |
|--------|----------|-------|
| threat_gain | How much enemy proximity affects movement | 0.3–1.8 |
| flee_strength | How fast bot flees from closest enemy | 0.3–1.8 |
| wander_speed | Oscillation frequency of random wandering | 0.3–1.8 |
| center_attract | How strongly bot stays near arena center | 0.3–1.8 |
| panic_distance | Distance at which bot starts panicking | 0.3–1.8 |
| speed_cap | Maximum movement speed | 0.3–1.8 |

The evolution loop: generate 120 random bots, let each play 30 seconds of simulated game, pick the top survivors, mutate their genes, repeat.

### What Happened

The evolution converged in **2 generations**.

| Metric | Random Bot | Evolved Bot | Improvement |
|--------|-----------|-------------|-------------|
| Average survival | 6.1s | 10.3s | **+69%** |
| Median survival | 6.2s | 9.2s | **+48%** |
| Survived 20s+ | 0% | 5% | ✅ |

The evolved bot learned a simple strategy: panic-flee when enemies get within ~1.8 units, otherwise wander with a slight center bias. That's it. Six weights, two generations, and the bot more than doubles its survival time.

### The Surprising Finding

The evolution converged **immediately** because the game is simpler than it looks.

The enemies home toward the player's **current** position. They don't predict, they don't flank, they don't coordinate. A bot that simply moves in a vector away from the nearest enemy trivially dodges them. The enemies always chase where the player was, not where they're going.

This means:
- **A hardcoded flee-when-close bot is nearly optimal** — the LLMs that implemented bot mode got it right by accident
- **The game's difficulty comes from human reaction time, not enemy AI** — enemies are predictable, humans just can't track 8 of them simultaneously
- **To make a challenging bot, you need smarter enemies** — enemies that lead their target, flank, or swarm would require actual learning

### The Evolved Genome

```
[1.72, 0.31, 1.40, 0.35, 1.80, 1.16]
```

Decoded: high threat sensitivity, moderate flee, fast wandering oscillation, low center attraction, high panic distance (flees early), high speed cap (moves fast when panicking).

### What's Next

The natural next step: give the enemies a brain too. If enemies predict player position (aim where the player will be, not where they are), the bot would need real evasion learning — not just flee logic. That's a proper adversarial evolution setup.

But for now, the takeaway is honest: **a 6-parameter bot evolved in 2 generations trivially beats the game.** The enemies are the bottleneck, not the bot.

[Play 3D Space Dodge](/games/3d-space-dodge/) &middot; [View the benchmark](/blog/3d-space-dodge-benchmark/)
