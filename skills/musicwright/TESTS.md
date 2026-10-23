# Tests: musicwright

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261023-1 · 2026-10-23 · headless claude -p with --plugin-dir on branch books-8 (installed copy disabled), three runs per case, in a repository clone and again in a folder holding only the fixtures · Windows 11 dev machine · 6/6
- action-2 (two takes to hear): 3/3 clone, 3/3 fixtures-only; every run handed over `mw.py preview` copies, and every run loaded musicwright-produce rather than the hub (the evidence is the call, so it passes).
- Read before grading: all three fixtures-only runs called the script through a shell variable; the regex was widened and retested.
- Baselines: 1/1 in a clone, 0/1 fixtures-only.
- led to: none

### T-20261017-2 · 2026-10-17 · headless claude -p, one run per case, fresh session, plugin installed from mark-local at eval-fixes 72be5c3 · Windows 11 dev machine · 6/6
- All six passed. trigger-1 (flute solo) and trigger-2 (card game menu music) now invoke the hub (both failed in T-20261017-1); each set up the project and dry-ran gen.
- action-1 (rank a.wav and b.wav) invoked the hub, ran `mw.py sheet` and read the picture; it said the fixtures are synthetic tones it had not heard.
- outcome-1 passed with no Skill call (regex `sheet` matched; says the listener decides and the agent has not heard the takes).
- trigger-1: the guard refused one Write of brief.md because its text named `mw.py gen` without --dry-run (a false positive on a note); the run rewrote the file and went on.
- Harness as T-20261017-1 (throwaway clone, scratch studio, generators on a dead port), with the guard widened to refuse every generation script (comfy_gen.py, h3_*.py, Python run from a generation skill folder) and any POST to a ComfyUI or ACE-Step host. Baseline not yet run.
- led to: none

### T-20261017-1 · 2026-10-17 · headless claude -p, one run per case, fresh session, plugin installed from mark-local 0.1.0 · Windows 11 dev machine · 4/6
- trigger-1 · trigger · undertrigger · musicwright-generate was invoked instead of the hub; it read the hub's SKILL.md itself, scaffolded the project and ran `mw.py gen ... --dry-run` (backends on a dead port)
- trigger-2 · trigger · undertrigger · musicwright-game was invoked instead; it planned a menu loop and dry-ran gen; the hub was never called
- Passed without the hub firing: action-1 ran `mw.py measure tests/fixtures/tone.wav` with no Skill call, because the prompt names "musicwright's script" (rewrite it so it does not name the tool); outcome-1 was answered by musicwright-curate (regex `sheet` matched; says the listener decides and that the agent has not heard the takes). The hub fired in none of the 42 runs of the plugin's suites.
- Harness: one stream-json trace per case in a throwaway clone; MUSICWRIGHT_HOME in a scratch studio, MUSICWRIGHT_COMFYUI and MUSICWRIGHT_ACESTEP on a dead port, a PreToolUse guard refusing `mw.py gen` without --dry-run (no refusals were needed). Baseline not yet run.
- led to: none
