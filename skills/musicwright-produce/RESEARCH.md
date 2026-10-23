# Research: musicwright-produce

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md. The first research pass is in the repository's [ai-docs/research](../../ai-docs/research/index.md).

Topic: Finishing music: loudness targets, mastering, formats, QC checks, mixing rules, stem separation. Tier `moderate`. Last refresh 2026-10-17; next due per `evergreen.json`.

## Current understanding

- Targets: Spotify -14 LUFS / -1 dBTP (-2 when louder); EBU R128 v5.0 -23 LUFS; console game mixes -24 ±2, handheld -18 or -16 (sources conflict); Netflix -27 dialogue-gated. Game targets are for the whole mix (R-213).
- loudnorm: set I, TP, LRA explicitly; add -ar 48000; linear two-pass or it falls back to dynamic (verified 2026-10-17, R-227).
- MP3 padding breaks loops when the gapless tag is ignored: +1,728 samples measured (R-215).
- AI output is usually dense: master with a limiter and normalisation, no added compression (R-212).
- Stems: Demucs lives on in the adefossez fork with little maintenance; RoFormer models lead vocal separation (R-030, R-031, R-232).

## Open questions

- Apple Music and YouTube targets have no primary source.
- Any Xbox or Steam loudness guidance.
- Whether to add a true-peak limiter step to mw.py master for loud sources.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- support.spotify.com loudness normalization; tech.ebu.ch/publications/r128; Apple Digital Masters brief
- Sony ASWG / IESD game loudness; audiokinetic blog (loudness)
- ffmpeg changelog (loudnorm, ebur128)

Tooling:

- `path:SKILL.md "music mastering loudness"` on GitHub code search, sorted by recently updated; `npx skills find "music mastering loudness"` and skills.sh weekly installs
- `https://registry.modelcontextprotocol.io/v0/servers?search=music mastering loudness`; fallback `"music mastering loudness" mcp server site:glama.ai OR site:pulsemcp.com`
- `"music mastering loudness" skill OR plugin OR "mcp server" 2026 site:github.com`; supersession sweep `"music mastering loudness" skill deprecated OR archived 2026`

Practice:

- `"claude code" OR codex OR cursor "music mastering loudness" "my workflow" 2026`; hn.algolia.com `search_by_date?query=music mastering loudness`
- Reddit r/aimusic, r/WeAreTheMusicMakers, r/gamedev RSS (reading through RSS only)

Testing:

- `audio QC loudness true peak check script` 2026
- pyloudnorm and ffmpeg ebur128 agreement

Best sources: standards bodies, platform help pages, ffmpeg docs; practitioner books for mixing. Noisy: SEO 'best AI music generator' listicles and scraped directories.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261023-1 · 2026-10-23 · Mixing With Impact: matched loudness, relative balance, mono lows, dynamics survive normalisation
- Summary: Oltheten, *Mixing With Impact* (Routledge, 2018), read for the plugin: compare only at matched loudness (5.3); balance is relative and analysers hide timing (3.3, 4.4); masking rules (4.2); a low-mid excess and over-bright sources as the usual faults (4.4, 11.2); lows centred, correlation as the translation check (11.4); normalisation rewards dynamics and the loudness range should suit the destination (14.5); a hand-off to mastering with peaks well below 0 and no limiter (14.3). Turned into `mw.py mixcheck`, `compare`, `preview`, `monobass`, `master --peak` and the presets' `lra_hint`, with thresholds set on 78 real renders.
- Track: practice
- Sources: the book (2018 English edition), sections as cited; reading notes kept by the owner
- Magnitude: 0.3 (the produce skill now runs checks and fixes it used to describe)
- Applied: C-20261023-1

### R-20261017-2 · 2026-10-17 · mw.py master on a real take
- Summary: A -15.7 LUFS flute take mastered to -14 / -1 came out at -14.1 / -1.0, with loudnorm in dynamic mode (the take had 2.5 dB of true-peak headroom). mw.py reports the mode so the change is never silent.
- Track: testing
- Sources: local run 2026-10-17
- Magnitude: n/a (initial)
- Applied: C-20261017-1

### R-20261017-1 · 2026-10-17 · Loudness and finishing, first pass
- Summary: Targets, formats, MP3 padding, mixing rules and scripted checks with tested ffmpeg recipes: ai-docs/research/03-music-fundamentals.md R-211 to R-215, R-225 to R-232.
- Track: subject
- Sources: https://support.spotify.com/us/artists/article/loudness-normalization/, https://tech.ebu.ch/publications/r128, https://backlothelp.netflix.com/hc/en-us/articles/360001794307
- Magnitude: n/a (initial)
- Applied: C-20261017-1

