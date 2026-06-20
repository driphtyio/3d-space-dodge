---
title: "18 LLMs Build a 3D Game — Who Ships and Who Breaks?"
description: "We asked 18 different language models to build the same Three.js 3D dodge game from scratch — 2 prompts, no human edits. Results range from 2-second flawless builds to total instruction failure."
pubDate: 2026-06-19
tags: ["llm-benchmark", "threejs", "3d", "ai-game-dev", "comparison", "research"]
heroImage: "https://pub-0066f5275194430aa9f985cb23278abe.r2.dev/img-20260619-194133-1781923301.jpg"
---

Can a language model build a playable 3D game from a single prompt? We took 18 models — from cloud APIs to local 4B quantized models — and gave each the exact same task: build a Three.js survival dodge game with player sphere, enemy cubes, WASD movement, score tracking, and camera following. Then a second prompt: add bot mode, glow pulse, and arena boundary ring.

No human edits. No intermediate feedback. Two shots per model.

### The Test

**Prompt 1:**
> Build a 3D game using Three.js r128 loaded from CDN. The game is a top-down survival dodge where the player is a glowing blue sphere on a dark grid plane. Red cube enemies spawn from outside the visible area and home toward the player. WASD moves the player. Score increases every second. Game over when an enemy touches the player. Press R to restart. Camera should follow the player at a low angle. Use a 680x480 canvas. Dark theme with neon-style emissive materials.

**Prompt 2 (applied to the output of Prompt 1):**
> Add bot mode (?bot=true), glow pulse on player sphere, and dim arena boundary ring.

### The Full Results

All scores are composite: output quality, build speed, token efficiency, bug count, and feature completeness.

| Rank | Model | Type | Time | Size | Score | Bot Mode |
|------|-------|------|------|------|-------|----------|
| 1 | **DeepSeek V4 Pro** | API ($0.075) | ~2s | 18.5 KB | **95** | ✅ |
| 2 | **DeepSeek V4 Flash** | API ($0.001) | 30s | 14.3 KB | **92** | ✅ |
| 3 | **Tencent Hy3 Preview** | API | ~5s | 16.1 KB | **91** | ✅ |
| 4 | **Xiaomi Mimo V2.5** | API ($0.005) | ~2s | 13.3 KB | **90** | ✅ |
| 5 | **Nemotron 3 Ultra (550B)** | API ($0.003) | ~2s | 11.7 KB | **89** | ✅ |
| 6 | **Mistral Small** | Free API | 21s | 11.6 KB | **88** | ✅ |
| 7 | **owl-alpha** | Free API | 6s | 13.1 KB | **85** | ✅ |
| 8 | **Gemma-4-31B** | Free API | ~2s | 7.9 KB | **82** | ✅ |
| 9 | **poolside/laguna-m.1** | Free API | ~2s | 6.7 KB | **80** | ✅ |
| 10 | **Llama 3.1 8B** | Local (Mac Mini M4) | 128s | 8.0 KB | **76** | ✅ |
| 11 | **Qwen 3.5 9B** | Local | 462s | 9.5 KB | **74** | ✅ |
| 12 | **Gemma-4-12b-coder-fable** | Local | 181s | 3.4 KB | **72** | ✅ |
| 13 | **Gemma-4-12b-agentic-fable5** | Local | 234s | 3.6 KB | **71** | ✅ |
| 14 | **GLM-4.6V-Flash** | Local | 354s | 8.8 KB | **71** | ✅ |
| 15 | **Gemma-4-12b-qat** | Local | 691s | 8.3 KB | **70** | ✅ |
| 16 | **Nemotron-3-Nano-4B** | Local | 209s | 4.8 KB | **68** | ✅ |
| 17 | **GPT-OSS-120B** | Free API | ~2s | 6.7 KB | **62** | ❌ |
| 18 | GPT-OSS-20B | Local | 38s* | 4.2 KB | 65* | ❌ |

*GPT-OSS-20B: Prompt 2 failed due to memory pressure (model evicted from 16GB Mac Mini before completing).

### What the Numbers Tell Us

**All but 2 models produced working games.** 16 of 18 models generated valid Three.js HTML from Prompt 1 alone. The two failures were both on Prompt 2 — GPT-OSS-120B simply ignored the instruction and returned the same game without modifications, and GPT-OSS-20B was evicted from memory mid-task.

**Speed gap is absurd.** Cloud models finish in 2-30 seconds. Local models take 2-11 minutes. The 550B Nemotron Ultra on OpenRouter finished in 2 seconds — faster than the 4B Nemotron Nano running locally (209s). That's a 100x speedup for using API vs local.

**Size ≠ quality, but it correlates.** DeepSeek V4 Pro produced the largest output (18.5 KB, 447 lines) and scored the highest. The smallest output (Gemma-4-12b-coder-fable at 3.4 KB) still shipped a working game but had fewer features. The big models write more complete code.

**Free tier models are shockingly good.** Mistral Small, owl-alpha, and Gemma-4-31B all scored above 80 on the free tier. For a simple 3D game under 500 lines, you don't need a paid API.

**Local models are viable but slow.** Llama 3.1 8B is the clear winner among local options — 128s total, 8.0 KB output, bot mode working. It's 2-5x faster than other local models of similar size. If you're running on a Mac Mini M4, this is your best bet.

**Chain-of-thought models waste budget.** Qwen 3.5 9B spent 40% of its token budget (2,165 of 5,435 tokens) on reasoning before generating code. That doesn't make the output better — it just makes it slower and more expensive.

### Cost Breakdown

| Model | Total Build Cost | Time Penalty |
|-------|-----------------|--------------|
| DeepSeek V4 Pro | $0.075 | None |
| DeepSeek V4 Flash | $0.001 | None |
| Mistral Small | $0 (free) | None |
| Local models | $0 (free) | 2-11 min |
| OpenRouter free tier | $0 (free) | Rate-limited |

For a single game build, any API cost under $0.10 is negligible. The real cost is time — local models take 100x longer than cloud. If you're iterating during development, cloud wins. If you're running unattended overnight, local is fine.

### Era Grading

This was a **1970s-era game** (C grade on our [roadmap scale](/roadmap/)). Every model that completed both prompts earned a C — meaning they can handle fundamentals: 3D scene setup, physics, basic AI, and canvas rendering. The question now is whether these models can scale to 1980s complexity (Pac-Man, Mega Man) and beyond.

### Try the Games Yourself

Every model's output is playable on our [games page](/games/). Each variant page shows the exact metrics from the benchmark:

- [DeepSeek V4 Pro](/games/3d-space-dodge/deepseek-v4-pro/) — #1 overall
- [DeepSeek V4 Flash](/games/3d-space-dodge/) — baseline
- [Mistral Small](/games/3d-space-dodge/mistral-small/)
- [Llama 3.1 8B](/games/3d-space-dodge/llama-8b/) — best local
- [All variants](/games/)

The full benchmark data lives on the [leaderboard](/leaderboard/). Source code for the 3D Space Dodge is on [GitHub](https://github.com/driphtyio/3d-space-dodge) including all variant builds and the exact prompts used.

### Key Takeaway

For a simple 3D game, **every model that can follow instructions will ship working code.** The differentiation is in speed, output density, and instruction adherence under iteration. The next test is harder: can these models build an 80s-era game with AI, tilemaps, and state machines?

[Play 3D Space Dodge](/games/3d-space-dodge/) &middot; [View Leaderboard](/leaderboard/) &middot; [GitHub Repo](https://github.com/driphtyio/3d-space-dodge)
