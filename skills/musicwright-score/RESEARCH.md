# Research: musicwright-score

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md. The first research pass is in the repository's [ai-docs/research](../../ai-docs/research/index.md).

Topic: Scoring to picture: spotting, hit maths, movements, ducking, temp tracks. Tier `moderate`. Last refresh 2026-10-17; next due per `evergreen.json`.

## Current understanding

- Spot first: cue list with starts, ends, hits and what music must not do (R-221).
- Hits land when bpm = 60 x beats / seconds; aim within 2 frames on sharp events, miss late (R-20261106-4, replacing one frame, R-222).
- One caption holds one colour: render movements and join on hit points; per-shot music re-attacks at cuts, so a sequence stays continuous, with deliberate gaps from the cue list (R-20261106-4).
- Ducking has no standard: 6-12 dB, attack 30-80 ms, release 250-700 ms as a start (R-223).
- Temp tracks are analysed into descriptors, never uploaded as references unless owned (R-224).

## Open questions

- Answered 2026-11-03: the loudness-curve fit is `mw.py curve` (C-20261103-1). Not yet judged on real cues: whether 2 LU and 4 LU are the right lines.
- Video-to-music models (Sonilo partner node, Foley-Omni) for first drafts.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `film scoring AI music workflow 2026`; ComfyUI video-to-music nodes
- Netflix and broadcast delivery specs for music and dialogue

Tooling:

- `path:SKILL.md "film scoring AI"` on GitHub code search, sorted by recently updated; `npx skills find "film scoring AI"` and skills.sh weekly installs
- `https://registry.modelcontextprotocol.io/v0/servers?search=film scoring AI`; fallback `"film scoring AI" mcp server site:glama.ai OR site:pulsemcp.com`
- `"film scoring AI" skill OR plugin OR "mcp server" 2026 site:github.com`; supersession sweep `"film scoring AI" skill deprecated OR archived 2026`

Practice:

- `"claude code" OR codex OR cursor "film scoring AI" "my workflow" 2026`; hn.algolia.com `search_by_date?query=film scoring AI`
- Reddit r/aimusic, r/WeAreTheMusicMakers, r/gamedev RSS (reading through RSS only)

Testing:

- `music to picture sync evaluation` 2026
- mw.py join and duck tests

Best sources: practitioner scoring texts, delivery specs, tool docs. Noisy: SEO 'best AI music generator' listicles and scraped directories.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261106-4 · 2026-11-06 · Karlin and Wright read
- Summary: Karlin and Wright, *On the Track* 2nd ed.: experts see a two-frame error, one frame is very hard to see, errors show only on sharp events, and late beats early (ch. 8); start at a shift of emphasis and exit at the next, with tail or hard out (ch. 4); gaps are structure (ch. 4, 10); play through, phrase or hit (ch. 10); texture under speech, voice-over strictest (ch. 10); too low is also a failure (ch. 19); what the director likes in a temp (ch. 3). The authors' general rule, no study cited, 20 years old, orchestral sessions; untested on AI output. Replaces the one-frame tolerance and the sound-or-cut entry rule.
- Track: practice
- Sources: the book, by chapter
- Magnitude: 2 (changes what the skill decides)
- Applied: SKILL.md Steps 1, 2, 4; references/spotting.md

### R-20261017-1 · 2026-10-17 · Scoring, first pass
- Summary: Spotting, hit maths, ducking rules of thumb, temp tracks: ai-docs/research/03-music-fundamentals.md R-221 to R-224. Lessons from earlier film work on this setup: a continuous score beats per-section music; movements with their own captions carry a mood arc that one caption cannot.
- Track: subject
- Sources: https://tryuncle.com/learn/davinci-resolve/how-to-duck-background-music-under-dialogue-in-davinci-resolve, https://backlothelp.netflix.com/hc/en-us/articles/360001794307
- Magnitude: n/a (initial)
- Applied: C-20261017-1

### R-20261105-4 · 2026-11-05 · Round two, group 10: spotting

artofcomposing.com/how-to-spot-a-film and web.pdx.edu/~jnewton/assignments/60nt_no_one_trains/index.html, through a fetch tool's extraction: tempo search for hits, into spotting.md. Music Theory 21c film chapter: covered.
