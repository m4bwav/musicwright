# Learnings: musicwright-produce

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

### L-001 · 2026-10-18 · Check for a pulse before adding percussion; duck an added part under the lead to make it answer
- Trigger: 2026-10-17, percussion lego over a free-time flute take invented its own grid in all six takes; the added second flute played along at the same level in the lead's rests as under its notes
- Hypothesis: a model conditioned on audio with no beat has nothing to lock to; lego follows the lead's dynamics rather than its phrasing
- Rule: run `mw.py pulse` on the lead first; with no steady pulse, offer a re-render at a fixed bpm or phrase-placed accents rather than a beat. For a call-and-response part, `mw.py duck PART --under LEAD --stem`, then `mw.py answer` to confirm it moved toward the rests
- Evidence: R-20261017-6 in musicwright-generate; the listener kept the ducked mix as best, 2026-10-18
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-18
