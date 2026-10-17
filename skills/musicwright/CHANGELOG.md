# Changelog: musicwright

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261017-2 · 2026-10-17 · mw.py loop and OGG output made portable across ffmpeg builds
- because: L-001
- files: scripts/mw.py (cmd_loop, out_codec, join)
- The loop crossfade runs on raw float samples in Python; atrim options are named; .ogg falls back to ffmpeg's built-in Vorbis encoder when libvorbis is missing.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `fast`, interval 14d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
