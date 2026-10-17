# Research: musicwright-curate

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md. The first research pass is in the repository's [ai-docs/research](../../ai-docs/research/index.md).

Topic: Keeping music knowledge: verdicts, taste profile, lessons, recipe promotion, the studio and the knowledge map. Tier `slow`. Last refresh 2026-10-17; next due per `evergreen.json`.

## Current understanding

- Verdicts in the listener's words are the most valuable data the plugin collects; mw.py verdict copies each with its recipe to the studio (design, 2026-10-17).
- Taste is distilled from kept versus rejected takes into a short Profile with evidence; guesses are marked.
- Private (studio) and public (plugin) knowledge are kept apart; only general lessons are promoted, with CHANGELOG entries.

## Open questions

- Whether automatic taste distillation (clustering verdicts by recipe) beats a periodic manual rewrite.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- `personal music preference profile LLM agent memory` 2026

Tooling:

- `path:SKILL.md "music taste memory"` on GitHub code search, sorted by recently updated; `npx skills find "music taste memory"` and skills.sh weekly installs
- `https://registry.modelcontextprotocol.io/v0/servers?search=music taste memory`; fallback `"music taste memory" mcp server site:glama.ai OR site:pulsemcp.com`
- `"music taste memory" skill OR plugin OR "mcp server" 2026 site:github.com`; supersession sweep `"music taste memory" skill deprecated OR archived 2026`

Practice:

- `"claude code" OR codex OR cursor "music taste memory" "my workflow" 2026`; hn.algolia.com `search_by_date?query=music taste memory`
- Reddit r/aimusic, r/WeAreTheMusicMakers, r/gamedev RSS (reading through RSS only)

Testing:

- curate evals: a verdict recorded, a Profile line with evidence

Best sources: the plugin's own ledgers and studio files; agent-memory practice posts. Noisy: SEO 'best AI music generator' listicles and scraped directories.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261017-1 · 2026-10-17 · Design from existing practice
- Summary: Before musicwright, taste lived in scattered skill notes (a preferred recipe, rejected noise textures, a request for one continuous film score). Centralising verdicts with their recipes makes those preferences reusable across projects.
- Track: practice
- Sources: local notes, 2026-10-17
- Magnitude: n/a (initial)
- Applied: C-20261017-1

