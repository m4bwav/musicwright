# musicwright-compose changelog, entries before 2026-11-10

Newer entries: [skills/musicwright-compose/CHANGELOG.md](../../skills/musicwright-compose/CHANGELOG.md).

### C-20261123-1 · 2026-11-23 · Caption/tag pairs and four lyric checks
- because: user request (harvest of the ACE-Step 1.5 Tutorial, MIT, rows T6 and T10)
- files: references/vocabulary.md (Failure modes, Lyrics that sing)
- Docs only; evals not re-run (no trigger change).

### C-20261120-1 · 2026-11-20 · Voice-led chords, chord_fit and cadence hints, blues scale and layout
- because: R-20261120-1
- files: SKILL.md (Step 3 check paragraph), references/notation.md (input table), references/theory.md (Progressions, Root movement and voicing), references/scales.md (Pentatonic and world scales); hub notation.py and mw.py
- Chord symbols now play voice-led (`--root-chords` for the old root-position blocks); `render --check` adds `chord_fit` and `cadence`. Six-note blues scale, the 12-bar layout and the three-voice V7 line, in our own words. Evals not re-run (no trigger change).

### C-20261118-3 · 2026-11-18 · .mws part presets and arrange; scales.md split out
- because: user request (arranger helper; size budget back to green)
- files: references/notation.md (Score text), references/scales.md (new: Pentatonic and world scales, Modes as intervals over a drone moved whole from theory.md), references/theory.md (pointer), SKILL.md (References)
- No text lost; theory.md fell under the 3,500-token reference budget. Evals not re-run (no trigger change).

### C-20261118-2 · 2026-11-18 · Score text (.mws)
- because: user request (technique harvest from vitaminclaude/voidstruck, ideas only)
- files: references/notation.md (Score text an agent can write, input table)
- Chord symbols with slash bass and melody strings (+ stacks, > slides, - rests) read by notation.py parse_mws and played by `mw.py render`.

### C-20261118-1 · 2026-11-18 · Small-group jazz form
- because: R-20261118-1
- files: references/theory.md (Form)
- One line: intro, head, solo choruses over the whole form, head, tag; medleys at one tempo.

### C-20261117-2 · 2026-11-17 · Vocal delivery words
- because: R-20261117-1
- files: references/vocabulary.md (new Vocal delivery words)

A soft-to-screaming delivery table with volume and range checks, and an effects list with style pairings. Book rule, unverified; caption words untested on any model. Evals not re-run (no trigger change).

### C-20261117-1 · 2026-11-17 · Per-bar summed-length rule
- because: technique harvest D3, [piropipo](https://github.com/miyo-hime/piropipo) README (positions written per note so a wrong length cannot shift later bars)
- files: SKILL.md (after the validate paragraph); hub mw.py render --check gains `bar_lengths` and `--roll`. Writing ABC now sums each bar and reads the lint.

### C-20261113-1 · 2026-11-13 · Slides render as glides
- because: user request; L-guitar-slide-bends in the hub's LEARNINGS
- files: references/notation.md (Play notation or tabs, new Slides), references/vocabulary.md (new Slide guitar words)

mw.py render now plays tab slides and vibrato as one pluck with a pitch-bend glide (RPN 0 = +-12) or the string model; slide programming rules and prompt candidates added. Evals not re-run (no trigger change).

### C-20261109-1 · 2026-11-09 · From Hill, Scoring the Screen
- because: R-20261109-1
- files: references/theory.md (Root movement, voicing and extended chords)

Contextual harmony and four Western film signs added. Evals not re-run.

### C-20261107-8 · 2026-11-07 · Expressive rendering of notes
- because: book distillation, Boulanger (ed.), The Csound Book ch. 6 (Beck) and ch. 7 (Dobson) (everscout ai-music beat)
- files: references/symbolic.md (Rendering notes so they do not sound flat)

Velocity should move brightness as well as level, register and pitch should change attack and decay, and a solo line wants one envelope with pitch steps; also a listening check for AI takes. Untested here.

### C-20261107-7 · 2026-11-07 · Synth voice words for captions
- because: book distillation, Wilson, Make: Analog Synthesizers ch. 3 (everscout downtempo beat)
- files: references/vocabulary.md (Period electronic sound)

Added waveform character and modulation words (pulse-width modulation, resonant sweep, sample and hold, ring mod, hard sync); whether models honour them is untested.

### C-20261107-6 · 2026-11-07 · Half and double tempo, quantized triplets
- because: book distillation, Roads, The Computer Music Tutorial 2e (everscout ai-music beat)
- files: references/notation.md (Transcribe a recording)

Added the book's failure modes as a short check; not tested on generated audio.

### C-20261107-5 · 2026-11-07 · Prediction is not quality; audio by matching
- because: book distillation, Dean (ed.), The Oxford Handbook of Computer Music (everscout ai-music beat)
- files: references/symbolic.md (Generating notes by rule; Audio by matching). Book claims, untested here.

### C-20261107-4 · 2026-11-07 · Generating notes by rule
- because: book distillation, Collins, Introduction to Computer Music (everscout ai-music beat)
- files: references/symbolic.md (Generating notes by rule). Markov order, noise sources, repetition against change, simple performance timing; book claims, untested here.

### C-20261107-3 · 2026-11-07 · Root movement, voicing, extended chords, modes over a drone, additive rhythm, stepped arpeggios
- because: book distillation, Hewitt, Music Theory for Computer Musicians (everscout ai-music beat)
- files: references/theory.md (Root movement, voicing and extended chords; Modes as intervals over a drone; Rhythm and groove)

### C-20261107-2 · 2026-11-07 · Period electronic sound by mechanism; song-form failure mode
- because: book distillation, Manning, Electronic and Computer Music (everscout ai-music beat)
- files: references/vocabulary.md (Period electronic sound, Failure modes)

### C-20261105-9 · 2026-11-05 · Cadence, borrowed-chord and sentence notes
- because: R-20261105-4
- files: references/theory.md (Progressions, Form)

Cadence, borrowed-chord and sentence notes, from round-two reading; see the RESEARCH entry for how strong each source is.

### C-20261107-1 · 2026-11-07 · Under-speech words removed; lyric form test recorded
- because: R-20261107-1
- files: references/vocabulary.md (opening list, Lyrics that sing)

The under-speech caption line failed its blind test and is gone. The bar-mapping note now says what the lyric form test showed and did not.

### C-20261106-1 · 2026-11-06 · Found sound as signpost or hidden layer
- because: user request (book distilled into a beat); Murphy, Ears to the Ground (2024), artists' reports, untested
- files: references/theory.md

One line on the two jobs of a found sound and letting its movement set the form.


### C-20261106-4 · 2026-11-06 · Polyphonic transcription is a sketch
- because: R-20261106-8
- files: references/notation.md (Transcribe a recording)
- SKILL.md already says a transcription is a draft, so only the polyphonic caveat is added.

### C-20261106-3 · 2026-11-06 · Pattison: lyrics by stress, section jobs, stability table
- because: R-20261106-5
- files: SKILL.md (step 4), references/vocabulary.md (Space and placement list, Lyrics that sing), references/theory.md (Form, Arrangement, Density and register)
- Replaces "read aloud" with stresses marked in writing, adds word jobs and a table, notes Senior's three beside 3-5.

### C-20261103-9 · 2026-11-03 · Sound tests point at the askwright page
- because: user request; T-20261103-1 (0/3: the hub-only rule was missed when this skill handled the request)
- files: SKILL.md
- One line sends listening tests to an askwright page when `mw.py doctor` reports the script.

### C-20261101-2 · 2026-11-01 · Theory: rhythm and groove from DeSantis
- because: user request (book run for the everscout downtempo beat found five *Making Music* strategies not applied on 2026-10-22: ch. 30, 37, 39-40, 42, 47)
- files: references/theory.md (new "Rhythm and groove")
- Unequal loop lengths, the 3+3+2 backbone, groove offsets and ghost notes, silence or a bed between notes, breadth before depth.

### C-20261101-1 · 2026-11-01 · Key-fit hint and the notation header rule
- because: user request (book learnings from Foster, Generative Deep Learning 2e, ch. 11)
- files: SKILL.md (Step 3), references/symbolic.md (Formats and libraries)
- `--check` now reports `key_fit`; MIDI and ABC must carry key and time signature; events over grids when a part has triplets, repeated same-pitch notes or dynamics.

### C-20261023-2 · 2026-10-23 · A reference's form from mw.py analyze --sections
- because: L-003, T-20261023-2, decisions 2026-10-23-books-track11
- files: SKILL.md (Step 2 item 6), evals/evals.json (action-4, hold-out)
- The reference step now takes the form (sections in seconds and bars) from `mw.py analyze REF --sections` on a recording the user owns, after DeSantis, *Making Music* (borrowing a formal skeleton).

### C-20261023-1 · 2026-10-23 · Melody, harmonic rhythm, arrangement and endings; the five-field reference
- because: R-20261023-1, L-002, T-20261023-1
- files: SKILL.md (Step 2 items 6-7; Step 3; References), references/theory.md (Melody; Harmonic rhythm and the low end; Arrangement; Endings), references/vocabulary.md (Depth, Low end, Describing a reference, Lyrics that sing), evals/evals.json (action-3)
- `mw.py render --check` reports melody hints; the reference becomes five fields that map onto caption, key, tempo and sections.

### C-20261018-1 · 2026-10-18 · Notation to audio and back (mw.py render, notate, transcribe)
- because: user request ("feed musicwright musical notation or tabs and have it produce the music, and the reverse"), R-20261018-1, L-001
- files: SKILL.md (description, Step 1, Step 3 table, Step 4: notation to audio and back, References), references/notation.md (new), references/symbolic.md (Formats and libraries, Models that write notes), evals/evals.json (trigger-3, trigger-4, action-2)
- The skill now plays ABC, tabs, MusicXML and MIDI through mw.py, converts between them, and transcribes recordings to MIDI, ABC, MusicXML and tab. The description names these; nothing else moved.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
