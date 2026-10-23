---
kind: note
status: active
date: 2026-10-18
title: Prompt for the next musicwright session (owed work from HANDOFF)
tags: handoff,prompt
---

# Next session prompt

Paste this into a fresh session in the musicwright repository.

---

Continue musicwright (this repository, public m4bwav/musicwright). Read AGENTS.md, then ai-docs/INDEX.md and ai-docs/HANDOFF.md, and check each skill's `evergreen.json` for due dates. Work the "Owed" list in HANDOFF.md in order, skipping the release unless the owner has said yes:

1. Evals: baselines without the plugin and three runs per case for the hub, generate and compose (headless `claude -p` in a throwaway clone; reinstall the plugin first so the new descriptions load). Never let an eval submit real GPU jobs: guard generation scripts and ComfyUI posts, and never cancel other people's jobs on a shared ComfyUI. Record runs in each TESTS.md and evergreen.json.
2. Notation: run the cover-for-realism route on hardware (render an ABC tune, then `gen --task cover --src` at strengths 0.5, 0.7, 0.9) and write the result into compose's RESEARCH.md; verify the MuseScore command-line export; consider Guitar Pro import only if someone asks.
3. Measure the untested routes on real hardware when the GPU is free (MiniMax Music 3 and REST recipes, YuE2, Stable Audio 3); add a recipe only after a listener keeps a take.
4. Add `mw.py gen --collect` with tests.

For each change: research before recall, log the reason in the skill's CHANGELOG.md, run `python tests/check_skills.py`, `python tests/test_mw.py`, `python scripts/budget.py` (the tracked size is yellow: trim before growing), and work through a pull request you merge yourself once CI is green. Before you finish, update HANDOFF.md and the log, and write the next session prompt here with this same instruction.
