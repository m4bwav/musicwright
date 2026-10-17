# Handoff

State on 2026-10-17, end of the first session.

## Done

- Public repository m4bwav/musicwright: seven skills with references, evergreen companions and eval suites; mw.py with 15 commands; 49 unit tests on synthetic audio and a fake ComfyUI and ACE-Step server; check_skills.py and budget.py green; CI green on Linux, macOS and Windows (Python 3.9 and 3.14); release workflow; dependabot; secret scanning and push protection.
- Research pass in ai-docs/research (models and licences, agent tools, fundamentals).
- Real runs: three ACE-Step XL flute takes sheeted and measured; master, loop with OGG tags and seam on real audio.
- Agent evals: T-20261017-1 40/42 over all seven skills, T-20261017-2 24/24 on hub, generate, game and compose after the routing fix.

## Owed

1. Evals: baselines without the plugin, three runs per case, and a re-run of the generate action case with its new prompt (it no longer names the plugin).
2. Not yet run on real hardware: the MiniMax Music 3 and REST recipes through `mw.py gen`, REST cover, repaint and extract, YuE2 and Stable Audio 3 (download, measure VRAM and time; add recipes only after a listener keeps a take).
3. `mw.py gen --collect` for `--no-wait` jobs: needs the queued recipe saved (a ledger row with status queued) so collected takes are measured and logged.
4. A loudness-curve fit for film cues and an optional learned quality score: open questions in the hub's RESEARCH.md.
5. Wiki: check it is live and matches the code after any mw.py change.
6. Release v0.1.0 when the owner says yes (tag `v0.1.0`; release.yml checks the tag against plugin.json).

## Next steps

Start from INDEX.md, or paste [next-session-prompt.md](next-session-prompt.md). Run `python tests/check_skills.py`, `python tests/test_mw.py`, `python scripts/budget.py` before every commit; work through pull requests on main and merge your own once CI is green.
