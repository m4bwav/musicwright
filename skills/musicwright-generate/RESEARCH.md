# Research: musicwright-generate

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md. The first research pass is in the repository's [ai-docs/research](../../ai-docs/research/index.md).

Topic: AI music generation: models, licences, hosted APIs, ACE-Step and MiniMax prompting and parameters, re-roll strategy. Tier `fast`. Last refresh 2026-10-17; next due per `evergreen.json`.

## Current understanding

- ACE-Step 1.5 (2B, XL 4B) is MIT and its model card allows commercial use of outputs; XL sft through ComfyUI peaks about 12.9 GB on 16 GB; v0.1.8 (2026-05-18) is the latest release. Confidence high (R-013, R-014).
- MiniMax Music 3 open weights (2026-08) run natively in ComfyUI; licence needs on-product attribution and AI disclosure, free under USD 20M revenue (R-011, R-012).
- YuE2 (native nodes, ABC score layer) and Stable Audio 3 (licensed data, loops and SFX) are the next local engines to measure; neither is measured on 16 GB yet (R-015, R-021).
- Hosted: Lyria 3.5 USD 0.08 a song with SynthID; ElevenLabs Music USD 0.15 a minute, Enterprise needed for film, TV and studio games; Suno has no public API and caps downloads; Udio downloads are off (R-001 to R-009).
- Prompting: caption = sound, lyrics/sections = time; tempo and key in their fields; one caption holds one colour, so mood arcs are rendered as movements; cfg 4.5 er_sde linear_quadratic was preferred over cfg 7 euler by a listener (ACE-Step tutorial; local verdicts).
- Ownership: purely AI output is not copyrightable in the US; vendor 'you own it' clauses are contract terms (R-085, R-086).

## Open questions

- YuE2 and Stable Audio 3 Medium VRAM and time on 16 GB.
- MiniMax Music 3 against ACE-Step XL in a listening test.
- Current field names for REST cover, repaint and extract (API.md moves).
- Tencent SongGeneration and SongBloom licences and homes.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- github.com/ace-step/ACE-Step-1.5 releases, docs/en/Tutorial.md and API.md; huggingface.co/MiniMaxAI/MiniMax-Music3; github.com/multimodal-art-projection/YuE; stability.ai news
- ai.google.dev/gemini-api/docs/music-generation and /pricing; elevenlabs.io/pricing/api; suno.com/pricing and /legal/terms
- `AI music lawsuit OR settlement OR licensing 2026` (Suno, Udio, GEMA); copyright.gov/ai
- Forums: github.com/ace-step/ACE-Step-1.5/discussions and issues; ComfyUI discussions (audio)

Tooling:

- `path:SKILL.md "AI music generation"` on GitHub code search, sorted by recently updated; `npx skills find "AI music generation"` and skills.sh weekly installs
- `https://registry.modelcontextprotocol.io/v0/servers?search=AI music generation`; fallback `"AI music generation" mcp server site:glama.ai OR site:pulsemcp.com`
- `"AI music generation" skill OR plugin OR "mcp server" 2026 site:github.com`; supersession sweep `"AI music generation" skill deprecated OR archived 2026`

Practice:

- `"claude code" OR codex OR cursor "AI music generation" "my workflow" 2026`; hn.algolia.com `search_by_date?query=AI music generation`
- Reddit r/aimusic, r/WeAreTheMusicMakers, r/gamedev RSS (reading through RSS only)

Testing:

- `music generation benchmark OR evaluation 2026` (SongEval, WildSongBench, MusicCaps)
- local timing and VRAM runs recorded in the ledger

Best sources: model cards and repos, vendor pricing and terms pages, court and regulator pages; trade press only as leads. Noisy: SEO 'best AI music generator' listicles and scraped directories.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261017-3 · 2026-10-17 · Recipe check on a solo-instrument brief
- Summary: Three seeds of the default XL recipe for an unaccompanied flute: two came out solo, one added a low drone. Seed variance, not the caption, decided it; keep the fish-then-lock workflow.
- Track: testing
- Sources: local run 2026-10-17
- Magnitude: n/a (initial)
- Applied: C-20261017-1

### R-20261017-2 · 2026-10-17 · Tooling: official vendor skills and MCP servers
- Summary: ElevenLabs ships an official music skill and MCP (music_v2_5); MiniMax ships an MCP; ace-step publishes ace-step-skills; calesthio/generative-media-skills covers several providers. Every Suno MCP is unofficial. See research 02 R-131 to R-136.
- Track: tooling
- Sources: https://github.com/elevenlabs/skills, https://github.com/ace-step/ace-step-skills
- Magnitude: n/a (initial)
- Applied: C-20261017-1

### R-20261017-1 · 2026-10-17 · Model landscape, first pass
- Summary: Full table of models by task, licence, 16 GB fit and ComfyUI support, plus legal and platform rules: ai-docs/research/01-models-landscape.md (R-001 to R-097). Changes to earlier local notes: ACE-Step 1.5 is MIT, not Apache 2.0; MiniMax Music 3 is open weights under its own community licence, not CC BY-NC.
- Track: subject
- Sources: https://github.com/ace-step/ACE-Step-1.5, https://huggingface.co/MiniMaxAI/MiniMax-Music3/blob/main/LICENSE, https://ai.google.dev/gemini-api/docs/music-generation
- Magnitude: n/a (initial)
- Applied: C-20261017-1

