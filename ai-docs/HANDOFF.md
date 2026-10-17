# Handoff

State on 2026-10-17, end of the first session.

## Done

- Seven skills with references, evergreen companions and eval suites; mw.py with 15 commands; 49 unit tests (tests/test_mw.py) on synthetic audio and a fake ComfyUI and ACE-Step server; check_skills.py and budget.py green; CI and release workflows.
- Research pass in ai-docs/research (models and licences, agent tools, fundamentals).
- Real runs: three ACE-Step XL flute takes sheeted and measured; master, loop with OGG tags, seam on real audio.

## Owed

1. Agent evals: one headless run per case recorded in each TESTS.md (see the log for how polywright ran them); then three runs per case and baselines without the skill.
2. Not yet run on real hardware: the MiniMax Music 3 and REST recipes through `mw.py gen`, REST cover, repaint and extract, YuE2 and Stable Audio 3 (download, measure VRAM and time, add recipes only after a listener keeps a take).
3. `mw.py gen --collect` for `--no-wait` jobs: needs the queued recipe saved (a ledger row with status queued) so collected takes are measured and logged.
4. A loudness-curve fit for film cues (rank takes against a per-section target) and an optional learned quality score: open questions in the hub's RESEARCH.md.
5. Release v0.1.0 when the owner says yes (tag `v0.1.0`; release.yml checks the tag against plugin.json).

## Next steps

Start from INDEX.md. Run `python tests/check_skills.py`, `python tests/test_mw.py`, `python scripts/budget.py` before every commit; work through pull requests on main.
