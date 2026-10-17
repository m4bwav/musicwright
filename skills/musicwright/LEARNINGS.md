# Learnings: musicwright

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

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
