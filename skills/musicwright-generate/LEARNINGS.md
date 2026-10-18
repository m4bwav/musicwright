# Learnings: musicwright-generate

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

<!-- Example (delete once you have a real entry):
### L-001 · 2026-10-17 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261017-1, T-20261017-1, confirmed 2026-10-17
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17
-->

### L-001 · 2026-10-18 · Base-checkpoint source tasks need DCW off; check a lego take is not noise before judging it
- Trigger: 2026-10-17, the first three lego takes on the 2B base came back as broadband noise; sheets showed no partials at all
- Hypothesis: the server forced DCW on for every model (ACE-Step issue #1259); base checkpoints were not trained for it
- Rule: send `dcw_enabled: false` for lego, complete and extract on base checkpoints (mw.py does), run a server at or after ca1e85f, and sheet every source-task take before anyone listens: noise has no harmonic lines
- Evidence: R-20261017-6, confirmed 2026-10-17 (three noise takes, then clean takes with the same seeds after the fix)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17
