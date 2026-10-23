# Changelog: musicwright-score

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261023-2 · 2026-10-23 · A temp track's sections from analyze
- because: decisions 2026-10-23-books-track11
- files: references/spotting.md (Temp tracks)
- The temp-track analysis names `mw.py analyze --sections`, which says where its sections change.

### C-20261023-1 · 2026-10-23 · Check cues under dialogue for presence bursts
- because: user request (books track 8: Oltheten, Mixing With Impact 5.4)
- files: references/spotting.md (Ducking under dialogue)
- A cue under speech is checked with `mw.py mixcheck`; BRIGHT or a high presence_db means it competes with the voice.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
