# Tests: musicwright-compose

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261102-4 · 2026-11-02 · headless claude -p (vault eval-harness run_evals.py, EVAL_AUDIO stand-ins: reference.flac = spacey_album 01_orbital_dawn; EVAL_MODE=baseline and fixtures) · Windows 11 dev machine · action-4 3/3
- With the plugin 3/3: each run loaded the skill and ran `mw.py analyze reference.flac --sections`. Baseline 0/3: musicwright absent from init, no plugin analyze call.
- led to: none

### T-20261102-3 · 2026-11-02 · headless claude -p (vault eval-harness run_evals.py, EVAL_MODE=fixtures, plugin enabled; baselines rescored from the kept T-20261102-2 traces) · Windows 11 dev machine · action-1 2/3, action-2 3/3
- action-1 and action-2 now need a trace of `mw.py render` (or `notate` for action-1) naming the score; file evidence dropped, since a plain script also makes motif.mid and tune.wav. action-1 accepts motif.abc too: the plugin route renders an ABC and writes the .mid beside the audio.
- With the plugin: action-1 2/3 (the miss never called the Skill tool and wrote the MIDI bytes by hand), action-2 3/3. Baseline rescored: 0/3 and 0/3 (was 3/3 and 3/3 on the file evidence).
- led to: none

### T-20261102-2 · 2026-11-02 · headless claude -p (vault eval-harness run_evals.py, EVAL_MODE=baseline: fixtures-only folder with the files the prompt names under tests/fixtures, musicwright@mark-local disabled and absent from every init) · Windows 11 dev machine · baseline only, three runs per action case
- Baseline: action-1 3/3 and action-2 3/3 (a plain script wrote motif.mid and rendered tune.wav, so these file-evidence cases do not separate the skill); action-3 0/3. action-4 not run: reference.flac is not kept on disk.
- led to: none

### T-20261023-2 · 2026-10-23 · headless claude -p (sonnet) with --plugin-dir on branch books-11 (installed copy disabled), three runs per case in a folder holding only the fixtures · Windows 11 dev machine · 3/3
- action-4 (form of a 180 s reference into form.md): 3/3; each run called `mw.py analyze reference.flac --sections` and wrote the table. One run's closing note said the boundaries fell on fractional bars; they now move to the nearest beat (decisions N7), after these runs.
- Baseline (no plugin, one run): 0/1. Five hand-written librosa scripts in 273 s, out of turns, no form.md.
- led to: L-003

### T-20261023-1 · 2026-10-23 · headless claude -p with --plugin-dir on branch books-8 (installed copy disabled), three runs per case, in a repository clone and again in a folder holding only the fixtures · Windows 11 dev machine · 6/6
- action-3 (does wander.abc hold together): 3/3 clone, 3/3 fixtures-only; the runs reported the leap share and the missing returning rhythm from `render --check`.
- Baselines: 1/1 in a clone; 1/1 fixtures-only, because it searched the disk and ran the installed release's mw.py, which has no melody hints, so its evidence passes without the new check.
- led to: none

### T-20261017-2 · 2026-10-17 · headless claude -p, one run per case, fresh session, plugin installed from mark-local at eval-fixes 72be5c3 · Windows 11 dev machine · 6/6
- All six passed. action-1: motif.mid exists (file evidence). outcome-1 (Taylor Swift's newest album): neither written prompt contains the name; the name appears only in the source links; genre, era, instruments, vocal texture and production were given.
- decoy-1 (master to -14 LUFS) went to musicwright-produce.
- Harness as T-20261017-1 (throwaway clone, scratch studio, generators on a dead port), with the guard widened to refuse every generation script (comfy_gen.py, h3_*.py, Python run from a generation skill folder) and any POST to a ComfyUI or ACE-Step host. Baseline not yet run.
- led to: none

### T-20261017-1 · 2026-10-17 · headless claude -p, one run per case, fresh session, plugin installed from mark-local 0.1.0 · Windows 11 dev machine · 6/6
- action-1 passed on two counts: the trace regex `mid` first matched a grep for `mido` (too loose), and `motif.mid` was written by a stdlib script and read back; use file evidence (`motif.mid`) instead.
- outcome-1: the prompt names no artist, so "does not put the name in the prompt" is met trivially; the descriptors (genre, era and production, instruments, voice, mood, form) were given. Name a real artist in the prompt to test it.
- Harness: one stream-json trace per case in a throwaway clone; MUSICWRIGHT_HOME in a scratch studio, MUSICWRIGHT_COMFYUI and MUSICWRIGHT_ACESTEP on a dead port, a PreToolUse guard refusing `mw.py gen` without --dry-run (no refusals were needed). Baseline not yet run.
- led to: none
