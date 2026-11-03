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

### R-20261103-6 · 2026-11-03 · Coursera music-production syllabi; Kaggle Learn (sources pass 17)
- Summary: Berklee's Music Production Capstone (mixing philosophies, techniques, mixing and mastering checklists) and Malachi's Mixing and Completing Your Music Production (critical listening, loudness standards, metadata) are covered by produce mixing.md, mastering presets and ffmpeg.md tagging. Kaggle Learn has no audio course; the Hugging Face Audio Course is speech and classification, outside scope. No skill change; group 6 done.
- Track: subject
- Sources: https://www.coursera.org/learn/music-production-capstone, https://www.coursera.org/learn/mixing-and-completing-your-music-production, https://huggingface.co/learn/audio-course (searched 2026-11-03)
- Magnitude: 0
- Applied: none

### R-20261103-5 · 2026-11-03 · Ableton Learning Music; Soundfly (sources pass 16)
- Summary: Ableton Learning Music chapters (beats and tempo by genre, backbeats, pitch, keys and scales, triads and progressions, basslines, melodies, song structure; advanced: modes, pentatonic, whole tone, octatonic, pelog, 19-tone, inversions, voicings, sevenths) are all in theory.md or below what the agent needs; pelog and 19-tone are not, but models do not take microtonal captions reliably, so not a gap. Soundfly's course list returned 403; skipped. No skill change.
- Track: subject
- Sources: https://learningmusic.ableton.com/ (read 2026-11-03), https://soundfly.com/courses (403)
- Magnitude: 0
- Applied: none

### R-20261103-4 · 2026-11-03 · Dodge and Jerse, Computer Music; Foster, Generative Deep Learning (sources pass 15)
- Summary: no copy of either on disk; read from contents lists. Dodge and Jerse (2nd ed. 1997): synthesis (oscillators, FM, subtractive, granular, physical modelling), reverberation and localisation, composition with computers (conditional probabilities, random walks, fractional 1/f noise, motivic and canonic transforms), real-time performance. Synthesis is the AI models' job and mw.py's sketch synth is enough for previews; ch. 11 adds 1/f melodies to the Nierhaus candidate (R-20261103-2), still not a gap. Foster (2nd ed. 2023) ch. 11: symbolic Transformers, polyphonic tokenisation, MuseGAN on Bach chorales; superseded for this plugin by audio models, and MidiTok is already noted (R-20261102-2 in generate). No skill change; group 5 done.
- Track: subject
- Sources: https://lib.ecu.edu/catalog-preview/catalog/648316, https://www.oreilly.com/library/view/generative-deep-learning/9781098134174/part03.html, https://obalkyknih.cz/file/toc/844250/pdf (read 2026-11-03)
- Magnitude: 0 (candidates only)
- Applied: none

### R-20261103-2 · 2026-11-03 · Farnell, Designing Sound; Nierhaus, Algorithmic Composition (sources pass 13)
- Summary: no copy of either book on disk; read from library tables of contents. Farnell (MIT Press 2010; parts Theory, Tools, Technique, Practicals, all in Pure Data) is procedural sound effects, not music: out of scope here, at most a pointer for a future game SFX plugin. Nierhaus (Springer 2009) surveys Markov models, generative grammars, transition networks, chaos and self-similarity, genetic algorithms, cellular automata, neural networks and rule-based AI. The compose skill names none of these, but the agent writes notes directly and AI models make the audio, so a Markov or grammar generator is not a gap; a candidate only if a user wants endless seeded variations of a motif without a model (a small Markov over intervals in mw.py would do). No skill change.
- Track: subject
- Sources: https://vufind.daystar.ac.ke/Record/138154/TOC, https://ocw.mit.edu/courses/21m-380-music-and-technology-sound-design-spring-2016/pages/readings-and-assignments, https://find.library.upatras.gr/Record/978-3-211-75540-2/TOC?lng=en (read 2026-11-03)
- Magnitude: 0 (candidates only)
- Applied: none

### R-20261023-1 · 2026-10-23 · Making Music: melody, arrangement by subtraction, endings, the reference catalogue
- Summary: DeSantis, *Making Music: 74 Creative Strategies for Electronic Music Producers* (Ableton, 2015), read for the plugin: describe a reference in five fields (ch. 5), an avoidance list of one's habits (6), foreground, middle and background (31), blurred section edges (32), loops of unequal length (37), kick and bass as one line (44), tuned drums (46), melody contour and motifs (49-51), lyric stress (54), harmonic rhythm (59), arrangement by subtraction and the arc (63, 66-72), endings (73, 75), unique events (74), a stop rule (76, 78), feedback at matched loudness (77). The contour rules were tested as checks before use (L-002).
- Track: practice
- Sources: the book, chapters as cited; reading notes kept by the owner
- Magnitude: 0.3 (new sections in theory.md and vocabulary.md, melody hints in render --check)
- Applied: C-20261023-1

### R-20261018-1 · 2026-10-18 · Notation to audio and back: tools, licences, what works
- Summary: FluidSynth 2.6.1 (2026-09-19, LGPL-2.1; Windows zip 2.7 MB, Scoop current, Chocolatey stale at 2.4.7, brew `fluid-synth`), render with `fluidsynth -ni -q -g G -r 48000 -F out.wav sf2 in.mid` (default gain 0.2 is quiet). GeneralUser GS 2.0.3 (32 MB) allows private or commercial use in your own music; MuseScore_General is MIT. music21 10.5.0 (BSD-3, Python 3.11+); abcMIDI GPL-2.0; MuseScore Studio 4.7.5 exports PDF and audio from the command line. PyGuitarPro reads GP3-5 only; alphaTab reads GP6/7. No maintained Python ASCII-tab parser exists, so mw.py has its own. ACE-Step 1.5 takes no MIDI; `cover` with `audio_cover_strength` (1.0 strong, 0.5 balanced, 0.1 loose) on a synth render is the route to a performed sound, tried upstream (PR #795) and reverted the same day (#798), with no published results. basic-pitch 0.4.0 (Apache-2.0) supports Python 3.8-3.11 only; tested here 2026-10-18 on Windows: it runs through uv on Python 3.11 only with numpy<2 and setuptools<81. Demucs moved to adefossez/demucs (4.1.0, MIT). ADTOF drum transcription is CC BY-NC-SA. ABC-Eval (2025) finds models write valid ABC syntax but reason poorly about structure, so generated ABC must be parsed and checked. Local test on a 41 s free-time solo flute: pyin and basic-pitch agreed on pitch in 72% of frames where both heard a note (81% on pitch class); both read hiss in the silent tail as notes until a level gate was added, and pyin jumped octaves until the range was narrowed.
- Track: tooling
- Sources: https://github.com/FluidSynth/fluidsynth/releases, https://github.com/FluidSynth/fluidsynth/blob/master/doc/wiki/UserManual.md, https://github.com/mrbumpy409/GeneralUser-GS/blob/main/documentation/LICENSE.txt, https://pypi.org/project/music21/, https://github.com/sshlien/abcmidi, https://github.com/musescore/MuseScore/releases, https://pypi.org/project/PyGuitarPro/, https://github.com/CoderLine/alphaTab, https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INFERENCE.md, https://github.com/ace-step/ACE-Step-1.5/pull/795, https://pypi.org/project/basic-pitch/, https://github.com/spotify/basic-pitch/issues/201, https://github.com/adefossez/demucs, https://github.com/MZehren/ADTOF, https://arxiv.org/abs/2509.23350
- Magnitude: 0.4 (a new capability: notation rendered and transcribed by mw.py)
- Applied: C-20261018-1

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

