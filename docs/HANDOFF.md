# Handoff

Last updated: 2026-06-08

## Current Objective

Stand up a working local MisoTTS setup as your own fork — a stable base for experimentation (voice cloning, parameter tuning, possibly upstream contributions).

## Current State

**What is done:**
- Forked `MisoLabsAI/MisoTTS` → `yannickspiess/MisoTTS`. Originally cloned to `~/Downloads/MisoTTS` for a feasibility test, then moved to this stable location once the fork was created.
- Remotes configured: `origin` = your fork (SSH, push-ready), `upstream` = the original repo.
- `uv`-managed venv (Python 3.10) installed and verified at this path (`uv sync --python 3.10`).
- Logged in to Hugging Face (`huggingface-cli login`, token `m2maxYS`, persisted at `~/.cache/huggingface/token`) — required because the text tokenizer (`meta-llama/Llama-3.2-1B`) is a gated repo that needs Meta's license accepted.
- Full model + codec cache downloaded (~36GB into `~/.cache/huggingface`, a global cache shared across HF tools — not repo-local).
- Verified end-to-end generation: `run_short.py` produced `short_sentence.wav` (5.76s, 24kHz mono) from "Hello from Miso, running locally on a MacBook." Confirms the full pipeline (model load → tokenize → autoregressive generation → Mimi decode → watermark → save) works on this machine.
- Confirmed **CPU-only inference on Apple Silicon**: upstream's `run_misotts.py` explicitly skips MPS ("Skipping MPS due to float64 limitations" — Apple GPUs lack hardware float64). See `docs/DECISIONS.md`. A single short sentence took roughly 7-8 minutes wall time including model load.
- Validated end-to-end **delivery pipeline** (generate → convert → iMessage to self): generated WAVs now save to `output/<YYYY-MM-DD>_<slug>.{wav,m4a}` (gitignored), converted to AAC/M4A via `afconvert -f m4af -d aac` (~20x smaller, no audible quality loss for speech), and delivered via `osascript` driving Messages.app directly — **not** the `mcp__Read_and_Send_iMessages__send_imessage` MCP tool, whose `message` param is text-only and can't carry attachments. Discovered and worked around a macOS 15+ Messages.app sandbox bug: sending directly from `output/` reports success but silently fails ("Not Delivered", no real error) because Messages can't read files outside its entitled directories. Fix: stage the file into `~/Library/Messages/.send-staging/` first, send from there, then clean up. Full pipeline documented in [[Text-to-Speech Generation Workflow]].

**What is not done / open:**
- Voice cloning not yet tried — requires passing a reference audio clip + its transcript via the `context` argument (see README "Prompted generation" section).
- MPS acceleration not attempted. Getting it to *run* would be a one-line `PYTORCH_ENABLE_MPS_FALLBACK=1` env var; getting it to run *faster* would need profiling whether the float64 fallback sits inside the autoregressive per-frame loop (if so, GPU↔CPU transfer overhead could cancel any gain).

## Validation

- `run_short.py` exited 0, produced a valid 24kHz mono WAV with no errors after HF auth was fixed.
- `whoami()` confirms HF auth and gated-repo access (`meta-llama/Llama-3.2-1B` tokenizer loads cleanly).
- Repo verified functional from its new path post-move (deps, model cache, and auth all reachable).

## Risks

- Generation is slow (CPU-only) — fine for short experimental clips, not viable for longer-form audio as-is.
- Pinned deps (`torch==2.4.0`, `torchtune==0.4.0`, `torchao==0.9.0`, `moshi==0.2.2`) may conflict with any attempt to upgrade `torch` for better MPS coverage later.

## Next Steps

- Try voice cloning with a short reference clip + transcript.
- If pursuing MPS: set the fallback env var, profile the generation loop, decide whether patching float64 ops is worth the effort.
