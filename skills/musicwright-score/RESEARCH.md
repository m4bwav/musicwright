# Research: musicwright-score

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md. The first research pass is in the repository's [ai-docs/research](../../ai-docs/research/index.md).

Topic: Scoring to picture: spotting, hit maths, movements, ducking, temp tracks. Tier `moderate`. Last refresh 2026-10-17; next due per `evergreen.json`.

## Current understanding

- Spot first: cue list with starts, ends, hits and what music must not do (R-221).
- Hits land when bpm = 60 x beats / seconds; tolerance about one frame (R-222).
- One caption holds one colour: render movements and join on hit points; per-shot music re-attacks at cuts, so one continuous score is preferred.
- Ducking has no standard: 6-12 dB, attack 30-80 ms, release 250-700 ms as a start (R-223).
- Temp tracks are analysed into descriptors, never uploaded as references unless owned (R-224).

## Open questions

- A loudness-curve fit (rank takes against a target shape per section) worth adding to mw.py.
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

### R-20261017-1 · 2026-10-17 · Scoring, first pass
- Summary: Spotting, hit maths, ducking rules of thumb, temp tracks: ai-docs/research/03-music-fundamentals.md R-221 to R-224. Lessons from earlier film work on this setup: a continuous score beats per-section music; movements with their own captions carry a mood arc that one caption cannot.
- Track: subject
- Sources: https://tryuncle.com/learn/davinci-resolve/how-to-duck-background-music-under-dialogue-in-davinci-resolve, https://backlothelp.netflix.com/hc/en-us/articles/360001794307
- Magnitude: n/a (initial)
- Applied: C-20261017-1

