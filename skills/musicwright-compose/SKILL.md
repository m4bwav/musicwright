---
name: musicwright-compose
description: "Use for the musical thinking behind a piece: keys, modes and scales by mood (pentatonic, Japanese in and yo, maqam), chord progressions, tempo by genre, song form, motifs and how to develop them, instrument ranges and timbre words, the genre and mood vocabulary music models respond to, describing a reference without naming the artist, and notes-first routes (MIDI, ABC, MusicXML, LilyPond, Strudel, DAW and MuseScore MCP servers). Use on 'what key sounds heroic', 'chords for a sad cue', 'write a motif', 'make a MIDI', 'describe this style for a prompt', 'teach me music theory'. Rendering audio from a caption is musicwright-generate. Also 'refresh musicwright-compose'."
---

# musicwright-compose

Theory an agent needs to write a better brief, a better caption, or the notes themselves, and to
explain music to someone with taste but no training. Keep answers practical: a rule of thumb, a
number, an example they can hear.

## Step 1: what is being asked

- **A prompt or brief** (most often): turn the user's words or a reference into caption
  vocabulary, a key, a tempo and a section plan, then hand to musicwright-generate.
- **Notes**: a motif, chord chart, MIDI file, score or live-code pattern. Go to Step 3.
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
6. A reference track or artist: translate it into those descriptors. Never put a living artist's
   name in a prompt, and never upload someone else's recording as a reference.

Write the result into the project's `brief.md` (Decisions list) so the choice is kept.

## Step 3: notes first

Choose the lightest format that does the job ([references/symbolic.md](references/symbolic.md)):

| Want | Format | Render or check with |
|---|---|---|
| a melody to show or hum | ABC notation | abcjs link or abc2midi; parse it back |
| a MIDI file for a DAW or game | MIDI via mido or pretty_midi | re-read and print bars and notes; FluidSynth + a SoundFont to hear it |
| a printable score | MusicXML (music21) or LilyPond | MuseScore CLI or LilyPond to PDF/PNG, then look at the page |
| a looping pattern | Strudel or Sonic Pi code | a strudel.cc share link; the user presses play |
| the user's own DAW | a DAW MCP server (Ableton, REAPER, Logic) | read back the project after every write |

Always validate what you wrote by parsing it back and, when possible, rendering it to audio or an
image you can look at. Motif continuity across separate AI renders is weak: when a theme must
return in other cues, keep its notes here and use cover or repaint from one render rather than
hoping a caption reproduces it.

## Rules

- Explain with the user's words first, the term second ("the dreamy raised fourth, called Lydian").
- No living artist names in prompts; long-dead composers and historical styles are fine
  ("baroque", "in the manner of Debussy").
- For world scales, name instruments and the scale, not a people or a sacred practice ("native
  american flute, minor pentatonic", never a tribe or ceremony). The double harmonic "exotic"
  scale reads as a stereotype: use it sparingly.
- Install nothing (MuseScore, LilyPond, FluidSynth, a DAW bridge) without saying what it is for.

## References

- [references/theory.md](references/theory.md): modes, world scales, progressions, tempo, meter, form, motif development, ranges.
- [references/vocabulary.md](references/vocabulary.md): caption vocabulary, describing a reference, failure modes.
- [references/symbolic.md](references/symbolic.md): MIDI, ABC, MusicXML, LilyPond, Strudel, DAW and notation MCP servers, learning path.

## Maintenance

Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md),
[LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evergreen.json`. Theory is stable; the
tools section moves: refresh when due.
