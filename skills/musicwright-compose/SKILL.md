---
name: musicwright-compose
description: "Use for the notes and the musical thinking behind a piece: keys, modes and scales by mood, chord progressions, tempo by genre, song form, motifs, instrument ranges, the vocabulary music models respond to, describing a reference without naming the artist; and notation: write MIDI, ABC, MusicXML or tabs, play notation or a guitar tab as audio (mw.py render), convert between them (notate), transcribe a recording into notes, sheet music or tab (transcribe). Use on 'what key sounds heroic', 'chords for a sad cue', 'play this tab', 'turn this ABC into audio', 'write down the melody in this recording'. Captions to audio are musicwright-generate. Also 'refresh musicwright-compose'."
---

# musicwright-compose

Theory an agent needs to write a better brief, a better caption, or the notes themselves, and to
explain music to someone with taste but no training. Keep answers practical: a rule of thumb, a
number, an example they can hear.

## Step 1: what is being asked

- **A prompt or brief** (most often): turn the user's words or a reference into caption
  vocabulary, a key, a tempo and a section plan, then hand to musicwright-generate.
- **Notes**: a motif, chord chart, MIDI file, score or live-code pattern. Go to Step 3.
- **Notation or tabs to hear, or a recording to write down**: Step 4.
- **A question about music**: answer with the tables in the references, and point to one thing
  to listen for. Offer the learning path when they want more.

## Step 2: from feeling to settings

1. Mood → mode and progression ([references/theory.md](references/theory.md)): wonder = Lydian
   (I-II), heroic = Mixolydian (I-bVII-IV-I), menace = Phrygian (i-bII), sad = vi-IV-I-V,
   epic = i-VI-III-VII.
2. Use and genre → tempo range (ambient 60-80, card and strategy beds 80-110, combat 130-170).
3. Form: verse-chorus for songs, through-composed for film, A-B-A'-C for game loops (never one
   8-bar loop), 2-4 bars of section per tag.
4. Instruments by register and colour (ranges in theory.md), 3-5 focal parts at once.
5. Words: build the caption from [references/vocabulary.md](references/vocabulary.md): genre +
   era/production + instruments + mood + vocal or "instrumental" + structure hint.
6. A reference track or artist: fill the five reference fields in vocabulary.md (sound, harmony,
   melody, rhythm, form) and build the caption from them. Never put a living artist's name in a
   prompt, and never upload someone else's recording as a reference.
7. Arrangement and ending: densest section first, others by subtraction; sections that differ in
   who plays; an ending planned as its own section ([references/theory.md](references/theory.md)).

Write the result into the project's `brief.md` (Decisions list) so the choice is kept.

## Step 3: notes first

Choose the lightest format that does the job ([references/symbolic.md](references/symbolic.md)):

| Want | Format | Render or check with |
|---|---|---|
| a melody to show or hum | ABC notation | `mw.py render tune.abc --check`, then `--out tune.wav` |
| a MIDI file for a DAW or game | ABC rendered to MIDI by mw.py, or mido | `mw.py render` writes the .mid beside the audio |
| a printable score | MusicXML (`mw.py notate tune.abc --out tune.musicxml`) or LilyPond | MuseScore or LilyPond to PDF/PNG, then look at the page |
| a looping pattern | Strudel or Sonic Pi code | a strudel.cc share link; the user presses play |
| the user's own DAW | a DAW MCP server (Ableton, REAPER, Logic) | read back the project after every write |

Always validate what you wrote by parsing it back and, when possible, rendering it to audio or an
image you can look at. `--check` also gives melody hints for each line (too many leaps, no rhythm
that returns): rules of thumb, so fix or keep them knowingly. Motif continuity across separate AI renders is weak: when a theme must
return in other cues, keep its notes here and use cover or repaint from one render rather than
hoping a caption reproduces it.

## Step 4: notation to audio and back

([references/notation.md](references/notation.md) has the formats, tools and limits.)

1. **Play it**: `mw.py render <file> --check` reads ABC, ASCII tab, MusicXML or MIDI and lists
   bars that do not add up; fix those (usually a wrong note length), then
   `mw.py render <file> --out out/x.wav` (FluidSynth with a SoundFont when installed, otherwise a
   built-in sketch synth). Tabs carry no rhythm: say the tempo (`--bpm`) and check the step it chose.
2. **Make it sound performed**: the render is a fine source for an ACE-Step cover (strength
   0.5-0.9, a caption naming the real instrument). That route is experimental, so the listener picks.
3. **Write it down**: `mw.py transcribe take.flac --out notes/take.mid --to abc,musicxml,tab`
   with `--lowest`/`--highest` set to the instrument's range. One line: pyin. Several notes at once:
   `--engine basic-pitch`, on stems for a full mix. Free time: run `mw.py pulse` and pass `--bpm`.
4. Render the transcription back and let the listener compare it with the recording; open the
   MusicXML in MuseScore to read or correct it. Say that a transcription is a draft.

## Rules

- Explain with the user's words first, the term second ("the dreamy raised fourth, called Lydian").
- No living artist names in prompts; long-dead composers and historical styles are fine
  ("baroque", "in the manner of Debussy").
- For world scales, name instruments and the scale, not a people or a sacred practice ("native
  american flute, minor pentatonic", never a tribe or ceremony). The double harmonic "exotic"
  scale reads as a stereotype: use it sparingly.
- Install nothing (MuseScore, LilyPond, FluidSynth, a DAW bridge) without saying what it is for.

## References

- [references/theory.md](references/theory.md): modes, world scales, progressions, tempo, meter, form, motif development, melody, harmonic rhythm, arrangement, endings, ranges.
- [references/vocabulary.md](references/vocabulary.md): caption vocabulary, describing a reference, failure modes.
- [references/symbolic.md](references/symbolic.md): MIDI, ABC, MusicXML, LilyPond, Strudel, DAW and notation MCP servers, learning path.
- [references/notation.md](references/notation.md): render, notate and transcribe: what each format reads, FluidSynth and SoundFonts, pyin and basic-pitch, limits.

## Maintenance

Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md),
[LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evergreen.json`. Theory is stable; the
tools section moves: refresh when due.
