# Decisions

## 2026-06-08 - Convert generated WAVs to AAC/M4A and stage through ~/Library/Messages/ before iMessage delivery

- Context:
  - Needed a working channel to deliver generated audio to Yannick's phone for playback (chat attachments in this environment can't be played back). iMessage to his own number (`+49 171 3120124`) was the chosen channel.
  - First attempt used the `mcp__Read_and_Send_iMessages__send_imessage` MCP tool with the `.wav` file path as the message — it just sent the literal path as text (the tool's schema is text-only, no attachment support).
  - Second attempt drove Messages.app directly via `osascript` (`send (POSIX file "...") to targetBuddy`) from the `.wav`'s original location in `daily app/MisoTTS/`. `osascript` reported success, the attachment bubble appeared correctly in Messages.app, but delivery failed ("Not Delivered", red icon) — while plain-text messages to the same recipient delivered and were read instantly.
  - Root cause (confirmed via web research, matches [anthropics/claude-plugins-official#1113](https://github.com/anthropics/claude-plugins-official/issues/1113)): Messages.app is sandboxed on macOS 15+ and can only read files from a small set of entitled directories (`~/Library/Messages/`, `~/Media/`, etc.). It accepts the `send` AppleEvent and returns success, but silently fails to actually read the file from an arbitrary path like `daily app/MisoTTS/output/` — no error is surfaced to `osascript`, hence the misleading "success" result paired with on-device "Not Delivered".
- Decision:
  - Standardize the delivery pipeline as: generate → save WAV to `output/<date>_<slug>.wav` → convert to AAC/M4A via macOS-native `afconvert -f m4af -d aac` (≈20x smaller, no audible quality loss for speech, and iMessage's native audio format) → copy into `~/Library/Messages/.send-staging/` → send via `osascript` from the staged path → clean up the staged copy.
  - Always drive Messages.app directly via `mcp__Control_your_Mac__osascript` for attachment delivery — never the iMessage MCP tool, which can only send plain text.
- Consequences:
  - Smaller files (≈28KB vs ≈550KB for a 6-second clip) upload and deliver faster over iMessage.
  - The staging directory is purely transient — must be cleaned up after each send to avoid accumulating copies in `~/Library/Messages/`.
  - This pipeline is now documented in the vault's [[Text-to-Speech Generation Workflow]] as the canonical delivery method; any future MCP tooling for iMessage attachments should be checked against this sandbox constraint before being adopted as a replacement.

## 2026-06-08 - Accept CPU-only inference; do not pursue MPS acceleration for now

- Context:
  - Investigated whether Miso TTS 8B (an 8.2B-param autoregressive TTS model) could use Apple Silicon's GPU (MPS backend in PyTorch) for faster local inference on the M2 Max.
  - Found that upstream's `run_misotts.py` explicitly skips MPS with the comment "Skipping MPS due to float64 limitations." Apple GPUs have no hardware float64 datapath (Metal doesn't support double precision), and some op in the inference path needs it — the exact line wasn't pinpointed; RoPE in `torchtune` already casts to float32, so the likely culprits are deeper in the Mimi audio codec (`moshi`), `torchaudio` resampling, or a sampling/distribution op.
- Decision:
  - Run on CPU for now. Don't invest time patching MPS support without first profiling whether it would actually help.
  - If revisited later: the cheap first step is `PYTORCH_ENABLE_MPS_FALLBACK=1` (silently falls back to CPU for unsupported ops). But because generation is autoregressive — frame-by-frame, token-by-token across 32 codebooks — a float64 op *inside* that loop would mean per-step GPU↔CPU data transfer, which could cancel out or exceed any MPS speedup. That has to be measured, not assumed.
- Consequences:
  - Expect roughly minutes per sentence on CPU, not real-time. Workable for short experimental clips; not viable for longer-form generation in its current form.
  - Revisit if: upstream bumps `torch` past `2.4.0` (MPS op coverage has improved meaningfully in 2.5+), or if someone roots-causes the specific float64 op and it turns out to be outside the hot generation loop.

## 2026-06-08 - Fork instead of working from a plain clone

- Context:
  - Initially cloned `MisoLabsAI/MisoTTS` directly to test feasibility. That setup tracked upstream `main` with no path to push changes.
  - Decided to use this repo as an ongoing local base for experimentation (and possibly contributions), not just a one-off test.
- Decision:
  - Forked to `yannickspiess/MisoTTS`, moved the local clone from the original throwaway location (`~/Downloads/MisoTTS`) to `/Users/yannickspiess/Documents/daily app/MisoTTS`, and set `origin` = fork (push-ready via SSH), `upstream` = original.
- Consequences:
  - Can commit and push freely to `origin` without affecting the upstream project.
  - To stay current with upstream improvements: `git fetch upstream && git merge upstream/main`.
