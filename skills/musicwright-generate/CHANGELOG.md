# Changelog: musicwright-generate

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261018-1 · 2026-10-18 · Adding a part: DCW off, the server version, the lego recipe, pulse and answer
- because: R-20261017-6, L-001, user request (the listener's verdicts on the stage-2 mixes)
- files: SKILL.md (Step 5: add a part to a kept take), references/acestep-rest.md (Start and check; Working from existing audio), RESEARCH.md (R-20261017-6, Current understanding, Open questions), LEARNINGS.md (L-001); hub references/recipes.json (acestep-rest-lego)
- A new step routes a part added to a kept take through pulse, lego on the base checkpoint, duck --stem and mix; the REST reference names the server version that fixes DCW, how to start it per model and the measured VRAM.

### C-20261017-2 · 2026-10-17 · Source tasks (lego, complete, extract, cover, repaint) documented as run by mw.py
- because: R-20261017-4, R-20261017-5, user request
- files: references/acestep-rest.md (Working from existing audio), references/models.md (ACE-Step row), RESEARCH.md (Current understanding, Open questions)
- The REST reference now names the part list, the base checkpoints and their sizes, the upload and the planner-off rule; the tasks table replaced the "not yet run here" one.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `fast`, interval 14d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
