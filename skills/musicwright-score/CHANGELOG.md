# Changelog: musicwright-score

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-20261109-1 · 2026-11-09 · From Hill, Scoring the Screen
- because: R-20261109-1
- files: SKILL.md (Step 1, Step 2), references/spotting.md (Spotting notes, Tempo and hits, Temp tracks)

Spotting gets `says:`, `knows:`, a throughline sketched before rendering, one film palette from the cut's sound world, integrated or stinger hits, the knock-off trap and Bordwell's cutting-rhythm note. Documentation only: no mw.py check, since the source's thresholds are untested. Evals not re-run.

### C-20261105-9 · 2026-11-05 · Tempo search for several hits
- because: R-20261105-4
- files: references/spotting.md (Tempo and hits)

Tempo search for several hits, from round-two reading; see the RESEARCH entry for how strong each source is.

### C-20261107-1 · 2026-11-07 · Under-speech caption advice replaced
- because: R-20261107-1
- files: references/spotting.md (Ducking under dialogue)

Blind test failed, so the advice to caption cues with texture words is replaced by the result. Evals do not cover this sentence and were not re-run.

### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261106-3 · 2026-11-06 · Karlin and Wright: hit tolerance, entries and exits, treatment, gaps
- because: R-20261106-4
- files: SKILL.md (Steps 1, 2, 4), references/spotting.md (Spotting notes, Tempo and hits, Ducking, Temp tracks), RESEARCH.md (Current understanding)
- Replaces one frame with two on sharp events, the sound-or-cut entry rule with a shift of emphasis, and "under the whole cut" with a sequence plus chosen gaps. Evals owed.

### C-20261103-9 · 2026-11-03 · Sound tests point at the askwright page
- because: user request; T-20261103-1 (0/3: the hub-only rule was missed when this skill handled the request)
- files: SKILL.md
- One line sends listening tests to an askwright page when `mw.py doctor` reports the script.

### C-20261103-1 · 2026-11-03 · Rank takes against a loudness shape
- because: RESEARCH.md open question (loudness-curve fit); HANDOFF Owed item 4
- files: SKILL.md (Step 3, Loudness shape), RESEARCH.md (Open questions)
- Step 3 names `mw.py curve`, which ranks takes by how closely their short-term loudness follows a time:LUFS shape after removing the level offset.

### C-20261023-2 · 2026-10-23 · A temp track's sections from analyze
- because: decisions 2026-10-23-books-track11
- files: references/spotting.md (Temp tracks)
- The temp-track analysis names `mw.py analyze --sections`, which says where its sections change.

### C-20261023-1 · 2026-10-23 · Check cues under dialogue for presence bursts
- because: user request (books track 8: Oltheten, Mixing With Impact 5.4)
- files: references/spotting.md (Ducking under dialogue)
- A cue under speech is checked with `mw.py mixcheck`; BRIGHT or a high presence_db means it competes with the voice.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
