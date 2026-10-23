# Changelog: musicwright-produce

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261023-3 · 2026-10-23 · Listening checks moved TUNING-GAP, REPEATS and BRIGHT
- because: L-005, decisions 2026-10-23-listening-checks
- files: references/mixing.md (mixcheck flags and how often they fire; analyze flags and how often they fire)
- TUNING-GAP fires over 30 cents (0 of 14 real layers), REPEATS left the table and the share is reported only, and BRIGHT's note says a take at -7.6 dB was slightly tiring, not harsh.

### C-20261023-2 · 2026-10-23 · Tuning and layering checks from mw.py analyze
- because: L-004, T-20261023-2, decisions 2026-10-23-books-track11
- files: SKILL.md (Step 1), references/mixing.md (Scripted checks; analyze flags and how often they fire), evals/evals.json (action-4, hold-out)
- Step 1 says `analyze` gives tuning and repetition and that a layer's `cents_from_first` against the lead tells whether they beat. mixing.md lists the four analyze flags with their rates on real AI and human recordings.

### C-20261023-1 · 2026-10-23 · mixcheck, fair comparisons and fixes the agent can run
- because: R-20261023-1, L-002, L-003, T-20261023-1
- files: SKILL.md (description; Step 1; Step 1b; Step 3; Rules), references/mixing.md (AI renders: what goes wrong and what to run; Scripted checks; mixcheck flags and how often they fire), evals/evals.json (trigger-3, trigger-4, action-2, action-3)
- Step 3 now runs monobass, section automation and background darkening instead of only suggesting EQ; fades go after master when it reports dynamic; `master --peak -6` makes a pre-master. The description names the mix check and matched comparisons.

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
