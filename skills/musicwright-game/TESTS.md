# Tests: musicwright-game

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261017-2 · 2026-10-17 · headless claude -p, one run per case, fresh session, plugin installed from mark-local at eval-fixes 72be5c3 · Windows 11 dev machine · 6/6
- All six passed. action-1 ran `mw.py loop tests/fixtures/tone.wav ... --out loop.wav` then seam. decoy-1 (trailer) went to musicwright-score.
- Harness as T-20261017-1 (throwaway clone, scratch studio, generators on a dead port), with the guard widened to refuse every generation script (comfy_gen.py, h3_*.py, Python run from a generation skill folder) and any POST to a ComfyUI or ACE-Step host. Baseline not yet run.
- led to: none

### T-20261017-1 · 2026-10-17 · headless claude -p, one run per case, fresh session, plugin installed from mark-local 0.1.0 · Windows 11 dev machine · 6/6
- action-1 ran `mw.py loop tests/fixtures/tone.wav --start 0 --bars 4 --bpm 120 --xfade 1.5 --out loop.wav` then `mw.py seam loop.wav`; loop.wav exists, 8.0 s, seam clean.
- decoy-1 (trailer) went to musicwright-score.
- Harness: one stream-json trace per case in a throwaway clone; MUSICWRIGHT_HOME in a scratch studio, MUSICWRIGHT_COMFYUI and MUSICWRIGHT_ACESTEP on a dead port, a PreToolUse guard refusing `mw.py gen` without --dry-run (no refusals were needed). Baseline not yet run.
- led to: none
