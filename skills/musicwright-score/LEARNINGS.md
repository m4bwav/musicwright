# Learnings: musicwright-score

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

### L-score-tail-pad · 2026-11-08 · `render-movements-12-15s-longer-than-slot`
- Trigger: a game trailer cue; ACE-Step 1.5 XL movements rendered "a few seconds longer" than their slots (26 s for 22 s, 42 s for 38 s) ended with 7.5-9.8 s of quiet (`mw.py measure` tail_silence_s), so `join` crossfaded into silence and left a hole at the hit point; two re-rolls.
- Hypothesis: the model writes its own outro whatever the duration.
- Rule: duration = slot + 12-15 s; run `mw.py measure` for tail_silence_s before `join`, and look at the sheet of the joined cue. Retire when Step 2's wording says this or a recipe trims trailing quiet itself.
- Scope: skill · Status: active · helpful 1 · harmful 0 · last_confirmed 2026-11-08
