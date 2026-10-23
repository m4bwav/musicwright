# Tests: musicwright-produce

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261023-1 · 2026-10-23 · headless claude -p with --plugin-dir on branch books-8 (installed copy disabled), three runs per case, in a repository clone and again in a folder holding only the fixtures · Windows 11 dev machine · 30/30
- trigger-1 to trigger-4, decoy-1, decoy-2 (after the description change): 18/18 in a clone; decoy-2 went to musicwright-game every time.
- action-2 (mixcheck --lowest on a "solo"): 3/3 clone, 3/3 fixtures-only. action-3 (blind matched copies): 3/3 clone, 3/3 fixtures-only, the key beside the folder after the fix.
- Read before grading: one fixtures-only action-2 run called mw.py through a shell variable (`python $M mixcheck ... --lowest C4`), which the first regex missed; widened and retested on right and wrong commands. Run 1 of action-3 moved the blind key out of the listening folder by hand and said the tool should not put it there.
- Baselines (no plugin, one run): 2/2 in a clone (they ran the repository's own mw.py), 0/2 fixtures-only.
- led to: L-004 (musicwright), C-20261023-1

### T-20261017-1 · 2026-10-17 · headless claude -p, one run per case, fresh session, plugin installed from mark-local 0.1.0 · Windows 11 dev machine · 6/6
- action-1 ran `mw.py master tests/fixtures/tone.wav --preset apple --out out.wav` and re-measured: -16.0 LUFS.
- trigger-1 gave no file, so the run mastered the repo's flute sample (-15.7 to -14.1 LUFS) and spent 167 s and 20 tool calls; decoy-2 (combat loop) went to musicwright-game.
- Harness: one stream-json trace per case in a throwaway clone; MUSICWRIGHT_HOME in a scratch studio, MUSICWRIGHT_COMFYUI and MUSICWRIGHT_ACESTEP on a dead port, a PreToolUse guard refusing `mw.py gen` without --dry-run (no refusals were needed). Baseline not yet run.
- led to: none
