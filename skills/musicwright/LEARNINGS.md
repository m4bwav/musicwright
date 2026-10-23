# Learnings: musicwright

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-005 · 2026-10-23 · Read a seam's level at the seam, and check onsets are hits before calling a beat
- Trigger: the 0.1.1 wiki verification found `seam` reading a loop cut on a kick as "check by ear" (3.5 dB) and `pulse` calling a swelling tone with no beat "steady" at 120 bpm, though the 0.1.1 tests passed; the test kick was too short to show either.
- Hypothesis: a median over half a second measures a swell's slope times a quarter second, not a jump; the level envelope of a steady tone ripples, so a rising tone yields evenly spaced onsets of a few tenths of a dB that autocorrelate like a beat.
- Rule: fit a robust line (Theil-Sen) to the 50 ms levels each side and compare the two lines at the seam; in `pulse`, take the median rise over an onset and call it no pulse under 1 dB. Build test fixtures from the case that failed in use, not a simplified one.
- Evidence: the kit's loop read 1.29 dB (clean); a 2:1 level step still reads -12 dB; onset rise 0.41 dB on the swelling tone against 2.4 to 27.6 dB on 52 real renders and 6.5 on the kick take; tests test_loop_cut_on_a_kick_over_a_swelling_bed_is_clean, test_a_real_level_step_is_still_caught, test_swelling_tone_has_no_pulse; five mutations caught
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-004 · 2026-10-23 · A blind key must not sit in the folder the listener opens
- Trigger: in an eval run, the agent asked for blind copies saw `preview --blind` write the key into the listening folder, moved it out by hand and said the tool should not put it there.
- Hypothesis: a key beside the copies is one click from the listener, which undoes the blind test.
- Rule: write the key beside the folder (`<folder>_blind_key.json`), never inside it; say where it is and not to open it before the ranking.
- Evidence: T-20261023-1 (produce action-3, run 1); test_preview_matches_loudness_blind_and_phone checks the folder holds only the copies
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-003 · 2026-10-23 · Fold the lows to mono with a crossover, not by subtracting a low-passed side
- Trigger: the first `mw.py monobass` subtracted the low-passed side signal from each channel. On a real render with wide lows it moved the low-end correlation from -0.46 to -0.75, wider than before.
- Hypothesis: the low-pass filter shifts phase, so the part subtracted no longer lines up with the side signal it should cancel.
- Rule: use a Linkwitz-Riley crossover (two Butterworth stages a side): the high-passed left and right plus the low-passed mid in both channels. Measure low-end width only over content within 30 dB of the loud passages, or a faint residue reads as wide bass.
- Evidence: four real renders went to 0.88-1.0 at 160 Hz and 0.96-1.0 at 200 Hz; the subtraction version fails test_monobass_centres_the_lows_and_leaves_the_rest (mutation check)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-002 · 2026-10-17 · Rank takes on intruding parts first; a silent tail is a trim, not a defect
- Trigger: three solo-flute takes. The sheet flagged a low drone in one (the listener rejected it: "bass a flute can't make"), and the agent ranked a clean take first and a take with a 19 s silent tail second. The listener preferred the second, and asked about faint percussion in it.
- Hypothesis: listeners judge the melody and anything that breaks the brief (extra instruments); a quiet ending is fixed by trimming, so it should not cost a take its place.
- Rule: when ranking from sheets, order by (1) parts the brief excluded, (2) melodic line and phrasing, (3) the ending; mention a silent tail as a trim, not a fault. Ask the listener about faint percussion or bass in a solo, since the sheet shows breaths and tonguing as small vertical marks.
- Evidence: listener verdicts 2026-10-17 (keep, reject), sheet in the README
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

### L-001 · 2026-10-17 · ffmpeg filter graphs are not portable across versions: keep sample arithmetic in Python
- Trigger: the first CI run (2026-10-17) failed on Ubuntu's ffmpeg 6.1 while ffmpeg 9 on Windows passed: positional `atrim=a:b` meant start:starti there (loops one crossfade too long); `amix` with `duration=shortest` ended early, and with `longest` the following `concat` refused the stream. Homebrew's ffmpeg had no libvorbis.
- Hypothesis: filter option order and amix/concat buffering changed between ffmpeg releases; builds differ in encoders.
- Rule: name every filter option; do sample-exact work (crossfades, seams) on raw float samples in Python and use ffmpeg only to decode and encode; check `-encoders` before choosing libvorbis.
- Evidence: PR #1 (four CI rounds), C-20261017-2
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17

<!-- Example (delete once you have a real entry):
### L-001 · 2026-10-17 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261017-1, T-20261017-1, confirmed 2026-10-17
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17
-->
