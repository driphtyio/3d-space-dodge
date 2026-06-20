# 3D Space Dodge 🚀

[![Play Online](https://img.shields.io/badge/Play-Online-00d4ff)](https://aigamingdev.com/games/3d-space-dodge/)
[![Blog Post](https://img.shields.io/badge/Blog-Benchmark-ff6b35)](https://aigamingdev.com/blog/3d-space-dodge-benchmark/)
[![Leaderboard](https://img.shields.io/badge/Leaderboard-LLM%20Scores-00ff87)](https://aigamingdev.com/leaderboard/)
[![Evolved Bot](https://img.shields.io/badge/Research-Evolved%20Bot-a855f7)](https://aigamingdev.com/blog/evolved-bot/)

A Three.js 3D survival dodge game — **built by 18 different LLMs from scratch, ranked head-to-head.**

```
┌──────────────────────────────────────────────┐
│                                              │
│    ██        ██                               │
│        ██        ██        ██                │
│    ██  🔵  ██        ██                     │
│            ██    ████████                    │
│  ██████████         ██    ████████████       │
│            ██                                │
│                                              │
└──────────────────────────────────────────────┘
     Dodge the red cubes. Survive. Compete.
```

## 🏆 LLM Benchmark — 18 Models Tested

Every model was given the same two prompts: build a 3D dodge game, then add bot mode + glow + boundary. No human edits.

| Status | Count | Models |
|--------|-------|--------|
| ✅ **PASS** | 11 | DeepSeek V4 Pro (95), Hy3 Preview (91), Mimo V2.5 (90), Nemotron 3 Ultra (89), Mistral Small (88), owl-alpha (85), Gemma-4-31B (82), poolside/laguna (80), Gemma-qat (70), GPT-OSS-120B (60) |
| ⚠️ **DEGRADED** | 1 | Qwen 3.5 9B (68 — renders with runtime errors) |
| ❌ **FAILED** | 6 | GPT-OSS-20B, Llama 3.1 8B, GLM-4.6V-Flash, Gemma-coder-fable, Nemotron-Nano-4B, Gemma-agentic-fable5 |

**Key finding:** All 10 API models passed. Only 2/8 local models produced working output.

[Full Benchmark Blog Post →](https://aigamingdev.com/blog/3d-space-dodge-benchmark/)

## 🧬 Evolved Bot

A 6-weight evolutionary strategy produced a bot that survives 69% longer than random movement — in just 2 generations. The enemies home toward current position, so a simple flee-when-close strategy trivially beats them.

[Read the Experiment →](https://aigamingdev.com/blog/evolved-bot/)

## 🎮 Play All Variants

Each model's output is playable online. See how differently they approach the same game:

| Model | Score | Play |
|-------|-------|------|
| DeepSeek V4 Pro | 95 🥇 | [Play](https://aigamingdev.com/games/3d-space-dodge/deepseek-v4-pro/) |
| Tencent Hy3 Preview | 91 🥉 | [Play](https://aigamingdev.com/games/3d-space-dodge/hy3-preview/) |
| Xiaomi Mimo V2.5 | 90 | [Play](https://aigamingdev.com/games/3d-space-dodge/mimo-v2.5/) |
| Nemotron 3 Ultra | 89 | [Play](https://aigamingdev.com/games/3d-space-dodge/nemotron-3-ultra/) |
| Mistral Small | 88 | [Play](https://aigamingdev.com/games/3d-space-dodge/mistral-small/) |
| owl-alpha | 85 | [Play](https://aigamingdev.com/games/3d-space-dodge/owl-alpha/) |
| Gemma-4-31B | 82 | [Play](https://aigamingdev.com/games/3d-space-dodge/gemma-31b/) |
| poolside/laguna-m.1 | 80 | [Play](https://aigamingdev.com/games/3d-space-dodge/poolside-laguna/) |
| Gemma-4-12b-qat | 70 | [Play](https://aigamingdev.com/games/3d-space-dodge/gemma-qat/) |
| GPT-OSS-120B | 60 | [Play](https://aigamingdev.com/games/3d-space-dodge/gpt-oss-120b/) |
| Qwen 3.5 9B | 68 ⚠️ | [Play](https://aigamingdev.com/games/3d-space-dodge/qwen-9b/) |

[Full Leaderboard →](https://aigamingdev.com/leaderboard/)

## 🎮 Play

- **WASD** — Move across the grid
- **R** — Restart on game over
- **?bot=true** — Autonomous bot mode

## 🧪 Testing Methodology

All variants tested with Playwright + SwiftShader WebGL in headless Chromium. Verified: canvas renders, WebGL context, zero JS errors, animation loop runs. Testing skill documented in the [game-benchmark-testing](https://github.com/driphtyio/3d-space-dodge) skill.

## 📊 Data

- [`benchmark-runs.json`](./benchmark-runs.json) — 27 benchmark runs (2D + 3D)
- [`evolution-results.json`](./evolution-results.json) — evolved bot genome and history
- [`PROMPTS.md`](./PROMPTS.md) — exact prompts used

## License

MIT
