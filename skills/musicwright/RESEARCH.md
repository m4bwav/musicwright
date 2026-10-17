# Research: musicwright

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md. The first research pass is in the repository's [ai-docs/research](../../ai-docs/research/index.md).

Topic: Routing music work for agents: brief, route, the take loop for an agent that cannot listen, mw.py, the project contract. Tier `fast`. Last refresh 2026-10-17; next due per `evergreen.json`.

## Current understanding

- An agent cannot hear: every music workflow that works (oaustegard's listening-to-music, bitwize's QC gate) renders, measures and shows a picture, then asks a person. The take loop (several seeds, sheet, numbers, verdict) is the core of this hub. Confidence: high (R-108, R-141 in ai-docs research 02).
- Spectrogram sheets separate takes well on what they can show: a solo line versus an added drone, trailing silence, loudness. Tested on three 60 s flute takes on 2026-10-17: the sheet flagged a low drone under one take and a 19 s silent tail on another.
- The local default for making audio is ACE-Step 1.5 XL through ComfyUI (MIT); MiniMax Music 3 is the second local engine; hosted APIs (Lyria 3.5, ElevenLabs) cost money and carry plan limits.
- CLI first, MCP optional: a stdlib script with one JSON object per command works from any agent (pattern from Producer Pal and TwelveTake, R-117, R-119).
- Seamless game loops are covered poorly by other tools (R-123), so mw.py loop and seam are a differentiator.

## Open questions

- Whether a learned audio-quality scorer (Audiobox Aesthetics, SongEval) adds useful signal to the sheet for ranking takes.
- Whether an MCP wrapper over mw.py is worth its install cost.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `"AI music" agent workflow 2026`, `"music generation" "claude code" OR "agent skill"`
- ComfyUI release notes (github.com/comfyanonymous/ComfyUI releases) for audio nodes; forum: github.com/comfyanonymous/ComfyUI/discussions

Tooling:

- `path:SKILL.md "music agent"` on GitHub code search, sorted by recently updated; `npx skills find "music agent"` and skills.sh weekly installs
- `https://registry.modelcontextprotocol.io/v0/servers?search=music agent`; fallback `"music agent" mcp server site:glama.ai OR site:pulsemcp.com`
- `"music agent" skill OR plugin OR "mcp server" 2026 site:github.com`; supersession sweep `"music agent" skill deprecated OR archived 2026`

Practice:

- `"claude code" OR codex OR cursor "music agent" "my workflow" 2026`; hn.algolia.com `search_by_date?query=music agent`
- Reddit r/aimusic, r/WeAreTheMusicMakers, r/gamedev RSS (reading through RSS only)

Testing:

- `"music" agent evaluation listening OR spectrogram OR "audio QC" 2026`
- `SongEval OR "Audiobox Aesthetics" music quality metric`

Best sources: ai-docs research 00-02 (first pass), ComfyUI releases, the repos named in references/tools.md. Noisy: SEO 'best AI music generator' listicles and scraped directories.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261017-2 · 2026-10-17 · Sheet test on real takes
- Summary: mw.py sheet on three ACE-Step XL flute takes (2026-10-17) showed one clean solo line, one take with a low drone band from about 20 s, one with a 19 s silent tail; mw.py measure agreed (tail silence, gaps). Confirms the sheet as the agent's ranking signal, with a person's ear as the verdict.
- Track: testing
- Sources: local run 2026-10-17
- Magnitude: n/a (initial)
- Applied: C-20261017-1

### R-20261017-1 · 2026-10-17 · First pass: four research reports (existing practice, models, agent tools, fundamentals)
- Summary: Agent tools for music split into DAW bridges (Ableton, REAPER, Logic MCP servers), code music (Strudel, mostly AGPL), hosted generator wrappers, and a few render-and-measure skills. None covers the generate, judge and finish loop with a memory of the listener's taste. The hub is built on that gap. Details and sources: ai-docs/research/02-agent-tools-and-workflows.md (R-101 to R-149).
- Track: tooling
- Sources: https://github.com/oaustegard/claude-skills, https://github.com/bitwize-music-studio/claude-ai-music-skills, https://news.ycombinator.com/item?id=47999656
- Magnitude: n/a (initial)
- Applied: C-20261017-1

