# Decisions

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
