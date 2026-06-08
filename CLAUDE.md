# MisoTTS — Agent Instructions

## Project

- Fork of `MisoLabsAI/MisoTTS` — Miso TTS 8B, an 8.2B-parameter conversational text-to-speech model (English only, RVQ Transformer / Sesame-CSM-inspired architecture).
- Local project root: `/Users/yannickspiess/Documents/daily app/MisoTTS`
- Remotes: `origin` = your fork (`yannickspiess/MisoTTS`, SSH, push-ready), `upstream` = the original (`MisoLabsAI/MisoTTS`).
- Used as the local engine for the vault's [[Text-to-Speech Generation Workflow]]; routed here via [[External Repo Workflow]].

## Session Start

Always read these first, in order:

1. `docs/HANDOFF.md`
2. `docs/DECISIONS.md`
3. `docs/WORKLOG.md`

These continuity files are governed by the `repo-handoff` skill — use it to keep them current rather than editing ad hoc.

## Build & Test

```bash
cd "/Users/yannickspiess/Documents/daily app/MisoTTS"
source .venv/bin/activate          # uv-managed venv, Python 3.10
uv sync --python 3.10              # rebuild/sync deps if pyproject changes
python run_misotts.py              # full demo conversation -> full_conversation.wav
python run_short.py                # single short-sentence smoke test -> short_sentence.wav
```

- Model + codec weights (~36GB) are cached in `~/.cache/huggingface` — a global HF cache shared across all local tools, not repo-local. Don't expect to find them inside this repo.
- HF auth is required for the gated `meta-llama/Llama-3.2-1B` tokenizer. Already logged in via `huggingface-cli login` (token persists at `~/.cache/huggingface/token`); should survive indefinitely unless revoked.
- **Inference is CPU-only on Apple Silicon.** Upstream explicitly skips MPS ("float64 limitations" — see `docs/DECISIONS.md`). Budget several minutes per sentence; set expectations before kicking off anything long.

## Operating Rules

- **Always work directly on `main`.** Do not create feature branches or git worktrees. This overrides any Superpowers or default agent preference for branching.
- **When using any Superpowers skill**, skip the "show in a web browser" offer. Assume the answer is always "no".
- **Commit and push to `origin` (your fork) after every meaningful chunk of work.** `git add … && git commit … && git push origin main` in one sequence — never leave commits unpushed. Origin is the sole backup for a solo developer.
- To pull upstream improvements: `git fetch upstream && git merge upstream/main`.

## Documentation & Handoff

At the end of every session that touches this repo:

- Update `docs/HANDOFF.md` with current objective, state, validation, risks, and next steps.
- Append a dated entry to `docs/WORKLOG.md`.
- Add or update `docs/DECISIONS.md` for non-obvious technical/product choices.
- Use the `repo-handoff` skill to keep these accurate.
- Do not leave important continuity only in chat.
