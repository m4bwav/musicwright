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

### L-002 · 2026-10-23 · Density section tags did not beat mood words on one blind pair; cfg 9 makes takes brighter
- Trigger: one caption and seed on ACE-Step 1.5 XL SFT, 180 s, five sections. The take with tags naming who plays (piano only, strings enter, horns and timpani join, full orchestra, piano alone) was not judged better than the take with mood words (calm, hopeful, rising, triumphant, peaceful); the listener found the mood take solid and missed a full-orchestra chorus in both, especially the density one. Separately, cfg 9 against 4.5 on the same seed raised the 2-5 kHz band from -11.8 to -7.6 dB and from -17.7 to -15.2.
- Hypothesis: the XL text encoder reads section tags as mood and timbre more than as an instrument count; a tutti needs the caption's instrument list, not a section tag.
- Rule: keep density tags as a try, not a promise; when a section must get fuller, name the added instruments in the caption too and check the sections by ear. Keep cfg at 4.5 unless the caption is ignored.
- Evidence: listening checks 2026-10-23 (decisions 2026-10-23-listening-checks, track 8 K10)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-001 · 2026-10-18 · Base-checkpoint source tasks need DCW off; check a lego take is not noise before judging it
- Trigger: 2026-10-17, the first three lego takes on the 2B base came back as broadband noise; sheets showed no partials at all
- Hypothesis: the server forced DCW on for every model (ACE-Step issue #1259); base checkpoints were not trained for it
- Rule: send `dcw_enabled: false` for lego, complete and extract on base checkpoints (mw.py does), run a server at or after ca1e85f, and sheet every source-task take before anyone listens: noise has no harmonic lines
- Evidence: R-20261017-6, confirmed 2026-10-17 (three noise takes, then clean takes with the same seeds after the fix)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17
