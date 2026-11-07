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

### R-20261106-8 · 2026-11-06 · Blind pair: one level or one gain across three cues

One listener, blind, levels matched overall (LRA 2.5 equal, 8.6 kept), calm, combat and town renders 20 s each with raw levels -18.7, -11.6, -13.6 LUFS. Slightly preferred the side keeping those differences, with no note. Slight, one pair, one cue order, not played in a game. The tested side used one gain plus a light limiter at 0.89; `master --shared-gain` uses gain only.

### R-20261106-7 · 2026-11-06 · Braddock, Waddell and Lerch read; Spotify page rechecked
- Summary: Normalisation is not universal, so a louder master is not always merely turned down (Braddock ch. 14). The mix beating the master at matched level points at the last dynamic or low-end change (ch. 14). Fades after dynamics (Braddock ch. 4, Waddell ch. 10); lossy from the highest-resolution file (Braddock ch. 16, Waddell ch. 2, 12); rate conversion can create intersample peaks and asymmetry is not DC (Waddell ch. 7). Structure scores about 50-70% pairwise F (Lerch 9.7.3.3); the 85% here is recall on splices. Spotify's page confirms Loud -11, a limiter at -1 dB sample values, 5 ms attack, 100 ms decay, and no normalisation on the web player and third-party devices; a -14 master with PLR over 10 dB therefore reaches it (arithmetic). Open disagreements are in ai-docs/HANDOFF.md.
- Track: subject
- Sources: Braddock, *Audio Mastering*; Waddell, *Complete Audio Mastering* (2013); Lerch, *An Introduction to Audio Content Analysis*, 2nd ed. (2023); https://support.spotify.com/us/artists/article/loudness-normalization/
- Magnitude: minor
- Applied: C-20261106-4

### R-20261106-3 · 2026-11-06 · Katz and Senior read
- Summary: Katz, *Mastering Audio* 3rd ed.: lowering level does not remove clipping in the file, and a limiter can sound worse (ch. 16); filters and lossy coding can raise peaks (ch. 16, 18); section moves go before the loud entry, never during a build (ch. 5); tails and heads (ch. 3); judge at the loudest passage (ch. 4). Senior, *Mixing Secrets*: several lossless, lightly limited references (ch. 4); side effects of loudness processing, buildups beyond level and a consumer play-through (ch. 19); crossovers can colour. Practitioner opinion, nothing tested on AI renders. The PLR limits for `linear` (13 dB for `streaming` and so on) are not in Katz: they are arithmetic from loudness.json on his target-plus-PLR method (p. 255 read on the page image). On synthetic files `master --preset streaming` went dynamic at PLR 14.9 and linear at 7.5. Preset numbers unchanged. The premixed-render, referencing and three-points lines came in with 0.1.14 and are not repeated.
- Track: practice
- Sources: the two books, by chapter
- Magnitude: 2 (corrects the source-clipping fix and the monobass claim)
- Applied: SKILL.md Steps 1, 1b, 3, 4; references/mixing.md; references/loudness.md

### R-20261103-3 · 2026-11-03 · Dean (ed.), Oxford Handbook of Computer Music; Zölzer, Digital Audio Signal Processing (sources pass 14)
- Summary: no copy of either book on disk; read from publisher and library listings. Dean (OUP 2011): histories, composition and improvisation, sounding out, performance modes, cognition and computation (Wiggins, Pearce, Müllensiefen: statistical expectation models such as IDyOM), cultural issues; a survey with nothing an agent can run, IDyOM-style melodic surprise a candidate only for melody checks. Zölzer (Wiley, 3rd ed. 2022): quantization and dither, AD/DA, audio processing systems, filters, room simulation, dynamics, sample rate conversion, audio coding, machine learning for audio. Dither and resampling are already in mw.py and produce references (ffmpeg.md, loudness.md); no gap. No skill change.
- Track: subject
- Sources: https://www.schweitzer-online.de/en/buch/Dean/Oxford-Handbook-Computer-Music/9780199792030/A1073080/, https://oreilly.com/library/view/digital-audio-signal/9781119832676, https://katalog.ub.uni-heidelberg.de/titel/69056401 (read 2026-11-03)
- Magnitude: 0 (candidates only)
- Applied: none

### R-20261106-1 · 2026-11-06 · Müller's book read; supersedes R-20261103-1 on what to build
- Summary: the owner's copy of *Fundamentals of Music Processing* 2nd ed. was read for one question, with a local test on real renders. Chord labels as a check: no (best F about 0.74 on one catalogue, a one-triad answer scores 0.551). Harmonic change rate: yes, reported, not flagged, since it needs no correct label. DTW cost as a follows-the-source score: no (no threshold in the book; a shuffled self at 0.083 overlapped unrelated pairs at 0.079). HPSS: no. Local alignment for cover against source stays a spike until a real cover set exists. R-20261103-1 said no copy was on disk and called chords the one to build; both are now out of date.
- Track: practice
- Sources: Müller 2nd ed., notes in Ai/books/plugin-learnings/music-round4-muller.md
- Magnitude: 1 (new report field)
- Applied: C-20261106-1

### R-20261103-1 · 2026-11-03 · Müller, Fundamentals of Music Processing, through the FMP notebooks (sources pass 12)
- Summary: no copy of the book on disk, so the free FMP notebooks (the book's companion, text CC BY-NC-SA 4.0, libfmp code MIT) stood in. mw.py already covers C4 structure (Foote checkerboard novelty in `analyze --sections`), C5's key half (chroma template correlation) and C6 onsets and tempo (`pulse`, adaptive threshold since 0.1.6). Not covered: C5 chord recognition (chroma templates plus HMM smoothing; would let a check say whether a take follows the asked progression), C3 DTW alignment (take against a rendered MIDI sketch), C8 harmonic/percussive separation. None is a wrong statement in the skills, so no skill change; chord recognition is the one worth building if a cue ever needs its progression checked (librosa has the pieces, libfmp is MIT).
- Track: practice
- Sources: https://www.audiolabs-erlangen.de/resources/MIR/FMP/C0/C0.html (read 2026-11-03)
- Magnitude: 0 (candidates only)
- Applied: none

### R-20261102-6 · 2026-11-02 · r/SunoAI and r/udiomusic, top of the month (sources pass 6)
- Summary: forum anecdotes, low confidence. Suno v6 users report a muffled or "radio static" high band and mix drift in long rock tracks; one popular thread hands ChatGPT a spectral-subtraction recipe (quietest 12% of frames as the noise profile, about 7 dB at most, bass below 350 Hz left alone). ffmpeg afftdn does the same locally: tested on a synthetic tone plus 5 kHz+ pink noise (band -55.9 to -60.9 dB, tone unchanged), row added to mixing.md. Uploads of own recordings and public-domain carols flagged as copyrighted by Suno: noted in hosted.md. Udio: walled garden, downloads blocked, nothing for the skills.
- Track: practice
- Sources: https://www.reddit.com/r/SunoAI/top/.rss?t=month, https://www.reddit.com/r/udiomusic/top/.rss?t=month (read 2026-11-02), local ffmpeg run
- Magnitude: 0.1 (one new fix row)
- Applied: produce references/mixing.md, generate references/hosted.md

### R-20261102-1 · 2026-11-02 · Demucs, torchaudio and librosa today (sources pass 1)
- Summary: torchaudio is in maintenance since 2.9: load and save are TorchCodec wrappers. Demucs 4.1.0 on PyPI no longer imports torchaudio, so that change does not touch it, but the package leaves out numpy: a bare `uvx demucs` fails, `uvx --with numpy demucs` separates a 10 s clip in 3 s on CPU (torch 2.15, Python 3.14). librosa is still 0.11.0 (March 2025), nothing that touches mw.py. stems.md commands fixed.
- Track: tooling
- Sources: https://docs.pytorch.org/audio/stable/torchaudio.html, https://pypi.org/project/demucs-torchcodec, https://pypi.org/project/demucs-infer/, https://librosa.org/doc/latest/changelog.html, local run 2026-11-02
- Magnitude: 0.1 (one broken command)
- Applied: stems.md, generate models.md

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

### R-20261105-4 · 2026-11-05 · Round two, group 10: mastering

sageaudio.com/articles/how-to-limit-your-master and masteringthemix.com/blogs/learn/advanced-limiting-techniques disagree on true-peak detection and show no tests; no tested limiter comparison found. No change.
