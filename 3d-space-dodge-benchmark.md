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

| Rank | Model | Type | Time | Tokens | Size | Cost | Score | Bot |
|------|-------|------|------|--------|------|------|-------|-----|
| 1 | **DeepSeek V4 Pro** | API | ~2s | 8,335 | 18.5 KB | $0.075 | **95** | ✅ |
| 2 | **DeepSeek V4 Flash** | API | 30s | ~8K | 14.3 KB | $0.001 | **92** | ✅ |
| 3 | **Tencent Hy3 Preview** | API | ~5s | 7,459 | 16.1 KB | $0 | **91** | ✅ |
| 4 | **Xiaomi Mimo V2.5** | API | ~2s | 7,970 | 13.3 KB | $0.005 | **90** | ✅ |
| 5 | **Nemotron 3 Ultra (550B)** | API | ~2s | 7,350 | 11.7 KB | $0.003 | **89** | ✅ |
| 6 | **Mistral Small** | Free API | 21s | 6,689 | 11.6 KB | $0 | **88** | ✅ |
| 7 | **owl-alpha** | Free API | 6s | 8,913 | 13.1 KB | $0 | **85** | ✅ |
| 8 | **Gemma-4-31B** | Free API | ~2s | 4,032 | 7.9 KB | $0 | **82** | ✅ |
| 9 | **poolside/laguna-m.1** | Free API | ~2s | 7,796 | 6.7 KB | $0 | **80** | ✅ |
| 10 | **Llama 3.1 8B** | Local | 128s | 2,591 | 8.0 KB | $0 | **76** | ✅ |
| 11 | **Qwen 3.5 9B** | Local | 462s | 5,435 | 9.5 KB | $0 | **74** | ✅ |
| 12 | **Gemma-4-12b-coder-fable** | Local | 181s | 2,128 | 3.4 KB | $0 | **72** | ✅ |
| 13 | **Gemma-4-12b-agentic-fable5** | Local | 234s | 2,577 | 3.6 KB | $0 | **71** | ✅ |
| 14 | **GLM-4.6V-Flash** | Local | 354s | 6,063 | 8.8 KB | $0 | **71** | ✅ |
| 15 | **Gemma-4-12b-qat** | Local | 691s | 8,431 | 8.3 KB | $0 | **70** | ✅ |
| 16 | **Nemotron-3-Nano-4B** | Local | 209s | 5,211 | 4.8 KB | $0 | **68** | ✅ |
| 17 | **GPT-OSS-120B** | Free API | ~2s | 3,292 | 6.7 KB | $0 | **62** | ❌ |
| 18 | GPT-OSS-20B | Local | 38s* | 1,235 | 4.2 KB | $0 | 65* | ❌ |

*GPT-OSS-20B: Prompt 2 failed due to memory pressure (model evicted from 16GB Mac Mini before completing).

### What the Numbers Tell Us

**All but 2 models produced working games.** 16 of 18 models generated valid Three.js HTML from Prompt 1 alone. The two failures were both on Prompt 2 — GPT-OSS-120B simply ignored the instruction and returned the same game without modifications, and GPT-OSS-20B was evicted from memory mid-task.

**Speed gap is absurd.** Cloud models finish in 2-30 seconds. Local models take 2-11 minutes. The 550B Nemotron Ultra on OpenRouter finished in 2 seconds — faster than the 4B Nemotron Nano running locally (209s). That's a 100x speedup for using API vs local.

**Size ≠ quality, but it correlates.** DeepSeek V4 Pro produced the largest output (18.5 KB, 447 lines) and scored the highest. The smallest output (Gemma-4-12b-coder-fable at 3.4 KB) still shipped a working game but had fewer features. The big models write more complete code.

**Free tier models are shockingly good.** Mistral Small, owl-alpha, and Gemma-4-31B all scored above 80 on the free tier. For a simple 3D game under 500 lines, you don't need a paid API.

**Local models are viable but slow.** Llama 3.1 8B is the clear winner among local options — 128s total, 8.0 KB output, bot mode working. It's 2-5x faster than other local models of similar size. If you're running on a Mac Mini M4, this is your best bet.

**Chain-of-thought models waste budget.** Qwen 3.5 9B spent 40% of its token budget (2,165 of 5,435 tokens) on reasoning before generating code. That doesn't make the output better — it just makes it slower and more expensive.

### Cost Breakdown

Paid models are cheap for single builds — the most expensive (DeepSeek V4 Pro) cost $0.075 for a complete game. Free tier and local models cost nothing but come with speed or rate-limit tradeoffs.

| Model | Tokens Used | Cost | Cost per 1K tokens |
|-------|-------------|------|-------------------|
| DeepSeek V4 Pro | 8,335 | $0.075 | $0.009 |
| DeepSeek V4 Flash | ~8,000 | $0.001 | $0.0001 |
| Xiaomi Mimo V2.5 | 7,970 | $0.005 | $0.0006 |
| Nemotron 3 Ultra (550B) | 7,350 | $0.003 | $0.0004 |
| Mistral Small (free tier) | 6,689 | $0 | — |
| owl-alpha (free tier) | 8,913 | $0 | — |
| Local models | 1,235–8,431 | $0 | — |

At these prices, **API cost is never the bottleneck** — build time and iteration speed are the real constraints. Local models take 2-11 minutes per build; cloud models finish in seconds. If your time is worth anything, the paid APIs save you hours per project.

### Era Grading

This was a **1970s-era game** (C grade on our [roadmap scale](/roadmap/)). Every model that completed both prompts earned a C — meaning they can handle fundamentals: 3D scene setup, physics, basic AI, and canvas rendering. The question now is whether these models can scale to 1980s complexity (Pac-Man, Mega Man) and beyond.

### Try the Games Yourself

Every model's output is playable. Each variant page shows the exact build metrics:

| Variant | Model | Time | Cost | Bot Mode | Notes |
|---------|-------|------|------|----------|-------|
| [DeepSeek V4 Pro](/games/3d-space-dodge/deepseek-v4-pro/) | DeepSeek V4 Pro | ~2s | $0.075 | ✅ | #1 overall. Largest output (18.5 KB). |
| [3D Space Dodge](/games/3d-space-dodge/) | DeepSeek V4 Flash | 30s | $0.001 | ✅ | Baseline. Full game on 1st prompt. |
| [Hy3 Preview](/games/3d-space-dodge/hy3-preview/) | Tencent Hy3 Preview | ~5s | $0 | ✅ | 16.1 KB output. Strong free-tier performer. |
| [Mimo V2.5](/games/3d-space-dodge/mimo-v2.5/) | Xiaomi Mimo V2.5 | ~2s | $0.005 | ✅ | 13.3 KB. Competitive with top-tier APIs. |
| [Nemotron 3 Ultra](/games/3d-space-dodge/nemotron-3-ultra/) | Nemotron 3 Ultra (550B) | ~2s | $0.003 | ✅ | 550B param model. Fast inference. |
| [Mistral Small](/games/3d-space-dodge/mistral-small/) | Mistral Small | 21s | $0 | ✅ | Best free API. Clean output. |
| [owl-alpha](/games/3d-space-dodge/owl-alpha/) | owl-alpha | 6s | $0 | ✅ | Free tier. Fastest overall build. |
| [Gemma-4-31B](/games/3d-space-dodge/gemma-31b/) | Gemma-4-31B | ~2s | $0 | ✅ | Free tier. 31B model, fast inference. |
| [poolside/laguna-m.1](/games/3d-space-dodge/poolside-laguna/) | poolside/laguna-m.1 | ~2s | $0 | ✅ | Free tier. Compact but functional. |
| [Llama 3.1 8B](/games/3d-space-dodge/llama-8b/) | Llama 3.1 8B (local) | 128s | $0 | ✅ | Best local option. Fastest local (128s). |
| [Qwen 3.5 9B](/games/3d-space-dodge/qwen-9b/) | Qwen 3.5 9B (local) | 462s | $0 | ✅ | 40% of tokens spent on CoT reasoning. |
| [Gemma-coder-fable](/games/3d-space-dodge/gemma-coder/) | Gemma-4-12b-coder-fable (local) | 181s | $0 | ? | Partial bot — detects ?bot=true URL but has no flee/wander steering logic. |
| [GLM-4.6V-Flash](/games/3d-space-dodge/glm-4.6v/) | GLM-4.6V-Flash (local) | 354s | $0 | ✅ | Mid-range local performance. |
| [Gemma-4-12b-qat](/games/3d-space-dodge/gemma-qat/) | Gemma-4-12b-qat (local) | 691s | $0 | ✅ | Slowest build (11.5 min). Working output. |
| [Nemotron-3-Nano-4B](/games/3d-space-dodge/nemotron-4b/) | Nemotron-3-Nano-4B (local) | 209s | $0 | ? | Bot code present but player didn't move — may not activate correctly. |
| [Gemma-agentic-fable5](/games/3d-space-dodge/gemma-agentic-fable/) | Gemma-4-12b-agentic-fable5 (local) | 234s | $0 | ❌ | Syntax error in output. Game doesn't render. |
| [GPT-OSS-120B](/games/3d-space-dodge/gpt-oss-120b/) | GPT-OSS-120B | ~2s | $0 | ❌ | Prompt 2 ignored. No bot mode or features added. |
| [GPT-OSS-20B](/games/3d-space-dodge/gpt-oss-20b/) | GPT-OSS-20B (local) | 38s* | $0 | ❌ | Prompt 2 failed — model evicted from memory. |

*Partial builds — Prompt 2 did not complete.

**Caveat:** Scores were verified with headless browser testing (Playwright/Chromium) — 16 of 18 games rendered a canvas and executed Three.js without syntax errors. Remaining failures: GPT-OSS-20B (partial build), Gemma-agentic-fable5 (syntax error in model output). Some WebGL-dependent rendering could not be verified in the headless environment — games flagged as working may have minor visual differences in a real browser.

### Key Takeaway

For a simple 3D game, **every model that can follow instructions will ship working code.** The differentiation is in speed, output density, and instruction adherence under iteration. The next test is harder: can these models build an 80s-era game with AI, tilemaps, and state machines?

[Play 3D Space Dodge](/games/3d-space-dodge/) &middot; [View Leaderboard](/leaderboard/) &middot; [GitHub Repo](https://github.com/driphtyio/3d-space-dodge)
