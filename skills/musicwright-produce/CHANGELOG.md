# Changelog: musicwright-produce

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261018-1 · 2026-10-18 · Pulse before percussion, ducking to make a part answer
- because: L-001, R-20261017-6 (musicwright-generate)
- files: LEARNINGS.md (L-001), references/mixing.md (Layering a new part over a kept take)
- The layering section now names `mw.py pulse` and `mw.py answer` as the checks.

### C-20261017-2 · 2026-10-17 · Layering a new part over a kept take
- because: user request; pulse analysis of a free-time flute take (2026-10-17)
- files: references/mixing.md (Layering a new part over a kept take)
- How to build stage mixes with `mw.py mix`, keep two same-register parts apart, and check for a pulse before adding percussion.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
