# Learnings: musicwright-compose

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

<!-- Example (delete once you have a real entry):
### L-002 · 2026-10-23 · Check a melody by returning rhythm and leaps, not by a single top note
- Trigger: the melody rules of thumb from Making Music, tried as checks on 18 public-domain tunes and six random walks: "one highest note" fired on 12 of the 18 tunes and did not separate the two sets; long step runs did not either.
- Hypothesis: folk and children's tunes return to their peak; what marks a tune is a rhythm that comes back and mostly stepwise motion.
- Rule: flag a line with over 25% leaps of a fourth or more, or under 65% of its notes inside a four-note rhythm that returns; report the peak and the step runs without a flag.
- Evidence: calibration 2026-10-23 (both flags: 0 of 18 tunes, 6 of 6 random walks); the repository's parser fixture tune.abc, four bars written to exercise the parser, reads 64% and gets the motif hint
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-001 · 2026-10-17 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261017-1, T-20261017-1, confirmed 2026-10-17
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17
-->

### L-001 · 2026-10-18 · Gate a transcription by level and range before reading it
- Trigger: 2026-10-18, both pyin and basic-pitch wrote 15-20 s of notes into a solo flute take's silent tail (hiss and hum), basic-pitch added D1 rumble notes, and pyin read part of a breathy phrase an octave up
- Hypothesis: pitch trackers report a pitch for any periodic noise; a wide search range lets breath noise lock onto harmonics
- Rule: set `--lowest`/`--highest` to the instrument's range and keep the level gate on (mw.py drops notes 35 dB under the loud passages); sheet the render of the transcription beside the recording before handing it over
- Evidence: R-20261018-1, confirmed 2026-10-18 (after the gate both transcriptions ended at 41 s with the take)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-18
