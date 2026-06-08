# Worklog

Reverse chronological. Append one entry per meaningful project session.

## [2026-06-08] — Forked, relocated, and validated local MisoTTS setup

- Assessed feasibility of running Miso TTS 8B locally on an M2 Max MacBook (96GB RAM): would run, but CPU-only — no hard CUDA blockers in the dependency tree, but upstream explicitly disables MPS.
- Cloned to `~/Downloads/MisoTTS`, installed via `uv sync --python 3.10`. First run failed: gated HF repo (`meta-llama/Llama-3.2-1B` tokenizer) needed authentication and Meta license acceptance.
- Logged in via `huggingface-cli login`; verified gated-repo access; re-ran successfully — generated `short_sentence.wav` ("Hello from Miso, running locally on a MacBook.", 5.76s, ~7-8 min wall time on CPU).
- Forked `MisoLabsAI/MisoTTS` → `yannickspiess/MisoTTS`; moved the repo from `~/Downloads` to this stable location (`daily app/MisoTTS`); reconfigured remotes (`origin` = fork via SSH, `upstream` = original); rebuilt the venv at the new path; pushed the test scripts (`run_short.py`, `run_output.log`).
- Onboarded the repo into the vault's [[External Repo Workflow]] conventions — added this `CLAUDE.md` and `docs/` scaffold (`HANDOFF.md`, `DECISIONS.md`, `WORKLOG.md`).
