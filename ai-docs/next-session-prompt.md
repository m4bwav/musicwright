# Next session prompt

Paste this into a fresh session in the musicwright repository.

---

Continue musicwright (this repository, public m4bwav/musicwright). Read AGENTS.md, then ai-docs/INDEX.md and ai-docs/HANDOFF.md, and check each skill's `evergreen.json` for due dates. Work the "Owed" list in HANDOFF.md in order, skipping the release unless the owner has said yes:

1. Evals: re-run the generate action case, then baselines without the plugin and three runs per case for the hub and generate (headless `claude -p` in a throwaway clone; on Windows start claude through the full path from `shutil.which`). Never let an eval submit real GPU jobs: guard generation scripts and ComfyUI posts, and never cancel other people's jobs on a shared ComfyUI. Record runs in each TESTS.md and evergreen.json.
2. Measure the untested routes on real hardware when the GPU is free (MiniMax Music 3 and REST recipes, YuE2, Stable Audio 3); write numbers into the relevant RESEARCH.md and add a recipe only after a listener keeps a take.
3. Add `mw.py gen --collect` with tests.

For each change: research before recall, log the reason in the skill's CHANGELOG.md, run `python tests/check_skills.py`, `python tests/test_mw.py`, `python scripts/budget.py`, and work through a pull request you merge yourself once CI is green. Before you finish, update HANDOFF.md and the log, and write the next session prompt here with this same instruction.
