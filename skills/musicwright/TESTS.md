# Tests: musicwright

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261017-1 · 2026-10-17 · headless claude -p, one run per case, fresh session, plugin installed from mark-local 0.1.0 · Windows 11 dev machine · 4/6
- trigger-1 · trigger · undertrigger · musicwright-generate was invoked instead of the hub; it read the hub's SKILL.md itself, scaffolded the project and ran `mw.py gen ... --dry-run` (backends on a dead port)
- trigger-2 · trigger · undertrigger · musicwright-game was invoked instead; it planned a menu loop and dry-ran gen; the hub was never called
- Passed without the hub firing: action-1 ran `mw.py measure tests/fixtures/tone.wav` with no Skill call, because the prompt names "musicwright's script" (rewrite it so it does not name the tool); outcome-1 was answered by musicwright-curate (regex `sheet` matched; says the listener decides and that the agent has not heard the takes). The hub fired in none of the 42 runs of the plugin's suites.
- Harness: one stream-json trace per case in a throwaway clone; MUSICWRIGHT_HOME in a scratch studio, MUSICWRIGHT_COMFYUI and MUSICWRIGHT_ACESTEP on a dead port, a PreToolUse guard refusing `mw.py gen` without --dry-run (no refusals were needed). Baseline not yet run.
- led to: none
