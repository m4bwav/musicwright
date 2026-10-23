# Changelog: musicwright-game

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261023-3 · 2026-10-23 · Seam ratio wording matches the code
- because: decisions 2026-10-23-listening-checks (bug list)
- files: SKILL.md (Step 3: cut the loop), references/loops.md (steps)
- The pages said a ratio of about 1 or less is clean; `mw.py seam` calls 2 or less clean.

### C-20261023-2 · 2026-10-23 · Cues from the level plan; mystery, warning, chase and villain-motif cues
- because: user request (books track 9: Rogers, Level Up! Levels 4, 10, 13, 17); decisions 2026-10-23-books-track9 M2-M6
- files: SKILL.md (description, Step 1, References), references/adaptive.md (Cues and lengths, new section Cues from the level plan), MAINTENANCE.md, evals/evals.json (trigger-3, outcome-2)
- Step 1 builds the cue list from a beat chart or LEVEL-PLAN.md when one exists and reads its music row for repeats; adaptive.md adds four cue types and rules on rotation, energy, the title piece, silence, stinger direction and a visual twin. MAINTENANCE.md now points at the hub's copy.

### C-20261023-1 · 2026-10-23 · Layers by subtraction; beds that never repeat
- because: user request (books track 8: DeSantis, Making Music ch. 37, 63, 72)
- files: references/adaptive.md (Techniques)
- Intensity layers come from one full take so they agree in key, tempo and length; ambient beds stack loops whose lengths share no factor.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
