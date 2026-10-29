# Research: musicwright-game

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md. The first research pass is in the repository's [ai-docs/research](../../ai-docs/research/index.md).

Topic: Game music: seamless loops, intro plus loop, layers, Unity import and scheduling, FMOD and Wwise, disclosure. Tier `moderate`. Last refresh 2026-10-17; next due per `evergreen.json`.

## Current understanding

- A loop is whole bars (samples = bars x beats x 60 / bpm x rate), flows musically, has no fades or silence, and crossfades its tail into its head; the seam check scored a hard cut 80 and a crossfaded loop 0.9 (R-216, R-229).
- Unity: Streaming + Vorbis for music; no loop import setting; OGG loop tags ignored; intro then loop needs two clips and PlayScheduled (R-216 to R-218).
- Adaptive music: horizontal re-sequencing, vertical layering, stingers, one intensity parameter; Wwise and FMOD have free indie tiers (R-219).
- Long-session games fight fatigue: 2-4 min loops with variation, room for SFX, silence between fights (R-220).
- Steam's Content Survey covers AI-made sound that ships with a game (R-094).

## Open questions

- FMOD documentation pages (client-rendered) not read directly.
- Godot's handling of OGG loop tags.
- Whether the WebGL loop bug still exists in Unity 6.x.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- docs.unity3d.com AudioClip and PlayScheduled; issuetracker.unity.com audio loop
- fmod.com/docs, audiokinetic.com courses and blog; forum: discussions.unity.com (Audio)
- partner.steamgames.com content survey

Tooling:

- `path:SKILL.md "game music loops"` on GitHub code search, sorted by recently updated; `npx skills find "game music loops"` and skills.sh weekly installs
- `https://registry.modelcontextprotocol.io/v0/servers?search=game music loops`; fallback `"game music loops" mcp server site:glama.ai OR site:pulsemcp.com`
- `"game music loops" skill OR plugin OR "mcp server" 2026 site:github.com`; supersession sweep `"game music loops" skill deprecated OR archived 2026`

Practice:

- `"claude code" OR codex OR cursor "game music loops" "my workflow" 2026`; hn.algolia.com `search_by_date?query=game music loops`
- Reddit r/aimusic, r/WeAreTheMusicMakers, r/gamedev RSS (reading through RSS only)

Testing:

- `seamless loop detection OR loop point finder` (crosslooper, PyMusicLooper)
- mw.py seam on known-good and known-bad loops

Best sources: Unity manual and issue tracker, middleware docs and courses, Steam partner docs. Noisy: SEO 'best AI music generator' listicles and scraped directories.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261029-1 · 2026-10-29 · Practice: code-synthesised loop, gapless AAC on the web
- Track: practice
- A web puzzle dev had Claude Code synthesise a 21 s loop in Node (four chords at 92 BPM, each instrument a function of time), mixing into a circular buffer so tails wrap to the start (no click), rendering three candidates in about 1.5 s, checking clipping and equal loudness by numbers, and checking that Chrome decodes the AAC to exactly the rendered sample count, which kept the WebAudio loop gapless. A person chose the winner by ear. Single maker report, not tested here.
- Sources: https://www.reddit.com/r/aigamedev/comments/1xic6d6/i_had_claude_code_synthesise_my_web_games_music/
- Applied: references/loops.md (Web paragraph)

 · 2026-10-17 · mw.py loop on a real take
- Summary: An 8-bar loop at 66 bpm cut from a flute take came out at exactly 29.0909 s with seam ratio 0.04 and level jump -1.7 dB (clean); OGG carried LOOPSTART=0, LOOPLENGTH=1396364.
- Track: testing
- Sources: local run 2026-10-17
- Magnitude: n/a (initial)
- Applied: C-20261017-1

### R-20261017-1 · 2026-10-17 · Game music, first pass
- Summary: Loops, Unity import, adaptive techniques, conventions and lengths: ai-docs/research/03-music-fundamentals.md R-216 to R-220; Steam disclosure from research 01 R-094.
- Track: subject
- Sources: https://docs.unity3d.com/Manual/class-AudioClip.html, https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html, https://partner.steamgames.com/doc/gettingstarted/contentsurvey
- Magnitude: n/a (initial)
- Applied: C-20261017-1

