# Worklog

Reverse chronological. Append one entry per meaningful project session.

## [2026-06-08] — Standardized generate-to-delivery pipeline (output/, AAC conversion, iMessage staging)

- Built and validated the vault's [[Text-to-Speech Generation Workflow]] end to end: generate → save WAV → convert to AAC/M4A → deliver via iMessage to self.
- Restructured generated-audio storage: created `output/` (gitignored) with naming convention `<YYYY-MM-DD>_<slug>.{wav,m4a}`; moved the existing `short_sentence.wav` there as `2026-06-08_short-sentence.wav`. Added `*.m4a` and `output/` to `.gitignore`.
- Diagnosed a macOS 15+ Messages.app sandbox bug: `osascript`-driven attachment sends from arbitrary paths report success but silently fail on-device ("Not Delivered", no real error). Root-caused via web research (matches [anthropics/claude-plugins-official#1113](https://github.com/anthropics/claude-plugins-official/issues/1113)) — Messages can only read files from entitled directories like `~/Library/Messages/`.
- Fix validated live: convert WAV → M4A via `afconvert -f m4af -d aac`, stage the M4A into `~/Library/Messages/.send-staging/`, send from there via `osascript` (not the iMessage MCP tool, which is text-only), then delete the staged copy. Confirmed actual playable audio arrived on phone.
- Documented the full pipeline and the sandbox workaround in `docs/DECISIONS.md` and the vault workflow; updated `docs/HANDOFF.md` accordingly.

## [2026-06-08] — Forked, relocated, and validated local MisoTTS setup

- Assessed feasibility of running Miso TTS 8B locally on an M2 Max MacBook (96GB RAM): would run, but CPU-only — no hard CUDA blockers in the dependency tree, but upstream explicitly disables MPS.
- Cloned to `~/Downloads/MisoTTS`, installed via `uv sync --python 3.10`. First run failed: gated HF repo (`meta-llama/Llama-3.2-1B` tokenizer) needed authentication and Meta license acceptance.
- Logged in via `huggingface-cli login`; verified gated-repo access; re-ran successfully — generated `short_sentence.wav` ("Hello from Miso, running locally on a MacBook.", 5.76s, ~7-8 min wall time on CPU).
- Forked `MisoLabsAI/MisoTTS` → `yannickspiess/MisoTTS`; moved the repo from `~/Downloads` to this stable location (`daily app/MisoTTS`); reconfigured remotes (`origin` = fork via SSH, `upstream` = original); rebuilt the venv at the new path; pushed the test scripts (`run_short.py`, `run_output.log`).
- Onboarded the repo into the vault's [[External Repo Workflow]] conventions — added this `CLAUDE.md` and `docs/` scaffold (`HANDOFF.md`, `DECISIONS.md`, `WORKLOG.md`).
