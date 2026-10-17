# Research: musicwright-compose

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md. The first research pass is in the repository's [ai-docs/research](../../ai-docs/research/index.md).

Topic: Music theory for prompting and judging, caption vocabulary, notes-first routes (MIDI, ABC, MusicXML, code music, DAW MCP servers). Tier `moderate`. Last refresh 2026-10-17; next due per `evergreen.json`.

## Current understanding

- Theory used for prompting and judging is stable: modes and moods, pentatonic and world scales, progressions by mood, tempo ranges, forms, motif development and ranges (R-201 to R-208, research 03).
- Models respond better to mood words plus a mode name than to the mode alone; tempo and key belong in fields, not captions (ACE-Step tutorial).
- No living artists in prompts: Suno strips names, Spotify removes voice imitation, ACE-Step warns about stylistic similarity (R-210).
- Notes-first routes need no model: write MIDI or ABC, then render and look. DAW MCP servers (Producer Pal, TwelveTake REAPER, mcp-score) handle session chores well and taste badly; always read back after a write (R-139 to R-144).
- Motif continuity across separate AI renders is weak; cover or repaint from one render is the workaround (R-207).

## Open questions

- Whether any model reliably follows a written melody (YuE2's ABC layer is the best candidate).
- Strudel's stance on AI tooling and where its docs live after the Codeberg move.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- ACE-Step Tutorial (caption dimensions, tags); Open Music Theory; Hooktheory TheoryTab
- MuseScore, LilyPond, music21, mido release notes

Tooling:

- `path:SKILL.md "music theory for AI music"` on GitHub code search, sorted by recently updated; `npx skills find "music theory for AI music"` and skills.sh weekly installs
- `https://registry.modelcontextprotocol.io/v0/servers?search=music theory for AI music`; fallback `"music theory for AI music" mcp server site:glama.ai OR site:pulsemcp.com`
- `"music theory for AI music" skill OR plugin OR "mcp server" 2026 site:github.com`; supersession sweep `"music theory for AI music" skill deprecated OR archived 2026`

Practice:

- `"claude code" OR codex OR cursor "music theory for AI music" "my workflow" 2026`; hn.algolia.com `search_by_date?query=music theory for AI music`
- Reddit r/aimusic, r/WeAreTheMusicMakers, r/gamedev RSS (reading through RSS only)

Testing:

- `ABC OR MusicXML OR MIDI validation parse render agent` 2026
- oaustegard listening-to-music skill updates

Best sources: theory texts and pedagogy sites, library docs, the MCP server repos. Noisy: SEO 'best AI music generator' listicles and scraped directories.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261017-2 · 2026-10-17 · DAW and notation bridges
- Summary: Producer Pal (GPL-3.0), ahujasid/ableton-mcp (MIT), TwelveTake REAPER (MIT), mcp-score (MIT) are the usable bridges; Strudel tools are mostly AGPL. Research 02 R-115 to R-130.
- Track: tooling
- Sources: https://github.com/adamjmurray/producer-pal, https://github.com/TwelveTake-Studios/reaper-mcp, https://github.com/tskovlund/mcp-score
- Magnitude: n/a (initial)
- Applied: C-20261017-1

### R-20261017-1 · 2026-10-17 · Fundamentals, first pass
- Summary: Modes, world scales, progressions, tempo, meter, form, motif development, ranges and caption vocabulary: ai-docs/research/03-music-fundamentals.md R-201 to R-210.
- Track: subject
- Sources: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md, https://www.hooktheory.com/theorytab/common-chord-progressions, https://www.flutopedia.com/scales.htm
- Magnitude: n/a (initial)
- Applied: C-20261017-1

