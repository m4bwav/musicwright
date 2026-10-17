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
5. Wiki: 17 pages are written and verified against main 62231a9 (every command run on Linux and Windows), but GitHub creates the wiki repository only after the owner saves a first page at https://github.com/m4bwav/musicwright/wiki/_new. Then run the publish script kept in the owner's private notes (wiki-build/publish.sh: preflight, build, check, push, live check). Re-verify output sections after the bug fixes below.
7. Bugs found while verifying the wiki (fix with tests, one PR):
   - master, edit, join, loop and duck fail with a raw ffmpeg error when the --out folder does not exist (sheet, new and gen create it).
   - duck cuts the music to the length of --under and returns the mix, not a music stem; add a --stem or keep-length option and say which it returns.
   - master's "dynamic" warning blames peaks even when loudnorm went dynamic because the measured LRA was 0 (steady tones and drones).
   - gen sends 90 bpm and C major when --bpm/--key are omitted, against the brief's "leave to the model"; minimax-music3 ignores --bpm/--key and acestep-rest ignores --cfg/--steps/--sampler/--scheduler/--shift/--planner/--set without saying so.
   - new accepts an unknown --preset; master --lufs/--tp without --preset reports "streaming"; gen creates --out before validating, leaving empty folders on dry or failed runs.
   - verdict accepts a missing file and, for a take gen never logged, records the name with its extension so ledger never matches it.
   - seam's level jump uses the first and last 50 ms, so a loop starting on a drum hit reads "check by ear" with a smooth seam.
   - Docs: cli.md and the game skill say a seam ratio of "about 1 or less" is clean while the code says up to 2; argument errors exit 2 with usage on stderr, not JSON; contract.md omits music.json's `created`.
6. Release v0.1.0 when the owner says yes (tag `v0.1.0`; release.yml checks the tag against plugin.json).

## Next steps

Start from INDEX.md, or paste [next-session-prompt.md](next-session-prompt.md). Run `python tests/check_skills.py`, `python tests/test_mw.py`, `python scripts/budget.py` before every commit; work through pull requests on main and merge your own once CI is green.
