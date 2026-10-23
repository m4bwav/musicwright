# Learnings: musicwright-produce

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-004 · 2026-10-23 · Pitch spread is not drift, and an offset from A440 is not a fault
- Trigger: per-window tuning on real files. A blues flute take scattered about 20 cents either way from window to window with pyin agreeing, and a dub bed spread 42 cents, with no trend in either. One rendered jazz flute sat steadily 28 to 43 cents sharp. Four of 11 human recordings sit 18 to 33 cents off A440 (string players tuned sharp, a 1920 dance band).
- Hypothesis: window spread measures bends, vibrato and pitch effects; a steady offset is how the part was tuned. Neither matters until another part plays with it.
- Rule: read `mw.py analyze` tuning as three numbers. Spread alone is never a problem; OFF-A440 and TUNING-GAP are warnings for layering; DRIFT (the last third against the first, 90 s or more) is the only sign of a pitch that moves.
- Evidence: calibration 2026-10-23 (mixing.md, "analyze flags and how often they fire"); decisions 2026-10-23-books-track11 N2-N5
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-003 · 2026-10-23 · AI renders often fail in mono: check before a phone or a mono speaker
- Trigger: on 78 real renders (ACE-Step 1.5, MiniMax Music 3, film scores), 13 had more side than mid energy, so mono loses over 3 dB; one ACE-Step XL take loses 10 LU when folded (`aphasemeter` below zero 98% of the time). 14 had wide lows. A batch a listener liked in stereo holds three of the worst.
- Hypothesis: the generators' decoders write wide, partly out-of-phase stereo; no prompt word controls it, and stereo listening hides it.
- Rule: run `mw.py mixcheck` on any take bound for phones, laptops or a game that may play in mono; fix wide lows with `mw.py monobass`, and re-roll a MONO-LOSS take that must work in mono.
- Evidence: calibration 2026-10-23 (mixing.md, "mixcheck flags and how often they fire")
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-002 · 2026-10-23 · A low-mid mud ratio means nothing without a bass part
- Trigger: MUDDY (250-500 Hz over the average of the bass and mid bands) fired on both kept flute solos. With no bass part, the 60-250 Hz band sits 23-33 dB down and drags the average.
- Hypothesis: the ratio assumes all three bands are played.
- Rule: flag mud only when the bass band is within 15 dB of the whole; 5 of 78 real renders then fire.
- Evidence: calibration 2026-10-23; a test fixture with a low-mid tone and no bass; mutation check
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

<!-- Example (delete once you have a real entry):
### L-001 · 2026-10-17 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261017-1, T-20261017-1, confirmed 2026-10-17
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-17
-->

### L-001 · 2026-10-18 · Check for a pulse before adding percussion; duck an added part under the lead to make it answer
- Trigger: 2026-10-17, percussion lego over a free-time flute take invented its own grid in all six takes; the added second flute played along at the same level in the lead's rests as under its notes
- Hypothesis: a model conditioned on audio with no beat has nothing to lock to; lego follows the lead's dynamics rather than its phrasing
- Rule: run `mw.py pulse` on the lead first; with no steady pulse, offer a re-render at a fixed bpm or phrase-placed accents rather than a beat. For a call-and-response part, `mw.py duck PART --under LEAD --stem`, then `mw.py answer` to confirm it moved toward the rests
- Evidence: R-20261017-6 in musicwright-generate; the listener kept the ducked mix as best, 2026-10-18
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-18
