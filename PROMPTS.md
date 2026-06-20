# Prompt 1 — Build the Game

> Build a 3D game using Three.js r128 loaded from CDN. The game is a top-down survival dodge where the player is a glowing blue sphere on a dark grid plane. Red cube enemies spawn from outside the visible area and home toward the player. WASD moves the player. Score increases every second. Game over when an enemy touches the player. Press R to restart. Camera should follow the player at a low angle. Use a 680x480 canvas. Dark theme with neon-style emissive materials.

# Prompt 2 — Add Features (applied to Prompt 1 output)

> Add bot mode (?bot=true), glow pulse on player sphere, and dim arena boundary ring.

# Single Comprehensive Prompt (experiment — worse results)

> Build a 3D game using Three.js r128 from CDN. Top-down survival dodge. Player is a glowing blue sphere. Red cube enemies home toward player. WASD moves. Score. Game over. Camera follows. 680x480. Dark theme. Include bot mode (?bot=true auto-dodges), glow pulse on player, arena boundary ring.

**Result:** Single prompt produced 4,159 chars vs 11,675 chars from 2-prompt. Missing bot mode and glow. The 2-prompt format is better.

# Tested Models

## PASS (11)
- DeepSeek V4 Pro, DeepSeek V4 Flash, Mistral Small, owl-alpha, Gemma-4-12b-qat, Nemotron 3 Ultra (550B), poolside/laguna-m.1, GPT-OSS-120B, Gemma-4-31B, Xiaomi Mimo V2.5, Tencent Hy3 Preview

## DEGRADED (1)
- Qwen 3.5 9B — 6 const reassignment errors at runtime, still renders and plays

## FAILED (6)
- GPT-OSS-20B — evicted from 16GB memory mid-task
- Llama 3.1 8B — canvas.getContext('2d') locks canvas before WebGLRenderer
- GLM-4.6V-Flash — 2 extra closing parens break JavaScript parser
- Gemma-4-12b-coder-fable — hit 8,192 token limit, output truncated mid-function
- Nemotron-3-Nano-4B — `now` used at top level without declaration
- Gemma-4-12b-agentic-fable5 — multiple syntax errors throughout output
