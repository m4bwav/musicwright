# Changelog: musicwright-compose

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261018-1 · 2026-10-18 · Notation to audio and back (mw.py render, notate, transcribe)
- because: user request ("feed musicwright musical notation or tabs and have it produce the music, and the reverse"), R-20261018-1, L-001
- files: SKILL.md (description, Step 1, Step 3 table, Step 4: notation to audio and back, References), references/notation.md (new), references/symbolic.md (Formats and libraries, Models that write notes), evals/evals.json (trigger-3, trigger-4, action-2)
- The skill now plays ABC, tabs, MusicXML and MIDI through mw.py, converts between them, and transcribes recordings to MIDI, ABC, MusicXML and tab. The description names these; nothing else moved.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
