# Notation to audio and back (checked 2026-10-18)

`mw.py render`, `notate` and `transcribe` turn written music into sound and recordings into
written music. The readers and writers are standard-library Python (`scripts/notation.py` beside
mw.py). The sound and the pitch tracking come from optional tools the user installs. Research:
R-20261018-1 in [../RESEARCH.md](../RESEARCH.md).

## Play notation or tabs

```bash
mw.py render tune.abc --check                       # read it, list bars that do not add up
mw.py render tune.abc --out out/tune.wav            # + out/tune.mid
mw.py render riff.txt --bpm 112 --out out/riff.wav  # ASCII guitar or bass tab
mw.py render song.musicxml --program flute --transpose -2 --out out/song.flac
```

| Input | Read | Not read (reported, never guessed) |
|---|---|---|
| ABC (`.abc`, or text with X: and K:) | ABC 2.1 notes, accidentals and key signatures with modes, lengths, rests, ties, chords `[CEG]`, broken rhythm `>` `<`, tuplets `(3`, repeats `|: :|` with endings `[1 [2`, voices `V:`, `%%MIDI program`, inline fields, chord symbols (`--chords` plays them) | grace notes, lyrics, decorations as sound, `%%` directives other than MIDI program |
| ASCII tab (`.txt`) | 4 to 8 string lines (`e|--0--3--|`), multi-digit frets, labelled tunings, bar lines; `--tuning` for others (dropd, dadgad, openg, bass, bass5, guitar7, ukulele, or `E2,A2,D3,G3,B3,E4`) | rhythm (tabs carry none: the usual gap between notes counts as an eighth note unless `--tab-step` says), bends and slides as pitch changes |
| MusicXML (`.musicxml`, `.xml`, `.mxl`) | partwise scores: parts with their MIDI programs, chords, backup and forward (several voices), ties, repeats and endings, tempo marks | timewise scores, grace and cue notes |
| MIDI (`.mid`) | format 0 and 1, tempo map, time and key signature, programs, the drum channel | SMPTE timing |
| Guitar Pro | not read: open it in MuseScore (free) or TuxGuitar and export MusicXML | |

Sound:

- **FluidSynth + a SoundFont** (General MIDI instruments): used when both are found. FluidSynth
  2.6.1 is LGPL-2.1, a 2.7 MB zip on Windows (Scoop `extras/fluidsynth`; Chocolatey lags behind),
  `brew install fluid-synth`, or the Linux package. GeneralUser GS (32 MB) allows use in your own
  music, private or commercial; MuseScore_General is MIT. Point mw.py at them with
  `MUSICWRIGHT_FLUIDSYNTH` and `--sf2`, `MUSICWRIGHT_SOUNDFONT`, or `"soundfont"` in the studio
  `config.json`. Renders come out quiet (about -20 to -26 LUFS); master them afterwards.
- **Built-in synth** otherwise: plucked strings for guitars, basses and harps, a soft wind
  tone, bells and an organ. It is a sketch, good enough to check notes and to use as a source.
- **Make it sound performed**: use the render as the source of an ACE-Step cover,
  `mw.py gen --recipe acestep-rest --task cover --src out/tune.wav --strength 0.6 --caption "..."`.
  ACE-Step has no MIDI input; its docs give strength 1.0 strong, 0.5 balanced, 0.1 loose, with
  examples at 0.7-0.8. Nobody has published results for synth renders as cover sources (an
  upstream attempt was reverted the day it merged), so sweep 0.5-0.9 and let the listener pick.

Models writing ABC: benchmarks find good syntax but weak structure, so always run
`mw.py render --check` on ABC an agent wrote. A bar that is too long or too short almost always
means a wrong note length. Fix it before rendering.

## Write notation from MIDI, ABC, MusicXML or tab

```bash
mw.py notate take.mid --bpm 66 --out score.musicxml   # open in MuseScore to read, fix, print
mw.py notate tune.abc --out tune.txt --tuning guitar  # tab (frets up to --max-fret 15)
mw.py notate riff.txt --out riff.abc
```

Notes snap to a sixteenth grid (`--grid 2` for eighths), so triplets and free rhythm come out
approximate. On a MIDI file `--bpm` keeps every note where it sounds and counts it in that tempo,
which is what a performance needs; on ABC, MusicXML and tab it sets the playing speed.

## Transcribe a recording

```bash
mw.py transcribe flute.flac --out notes/flute.mid --to abc,musicxml --lowest C4 --highest A5 --bpm 66
mw.py transcribe band.wav --engine basic-pitch --out notes/band.mid --to musicxml
```

- **pyin** (default) follows one line: one instrument, one note at a time. It uses librosa;
  without it mw.py prints the `uv run` line that brings it in for one run.
- **basic-pitch** (Apache-2.0) handles several notes at once, but works best on one instrument
  at a time. It does not install on Python 3.12 or newer. On Windows with Python 3.11 it also
  needs NumPy below 2 and setuptools below 81 (tested 2026-10-18):
  `uv tool install --python 3.11 basic-pitch --with "numpy<2" --with "setuptools<81"`. It is a few
  hundred MB with TensorFlow. `MUSICWRIGHT_BASIC_PITCH` can name a wrapper.
- For a full mix, split stems first (Demucs 4.1.0 from adefossez/demucs, MIT; the original
  facebookresearch repository is archived), or ACE-Step `extract` on a base checkpoint, then
  transcribe each stem.
- Both engines read hiss and hum in the rests as notes, and pyin jumps octaves on breathy
  tones. So mw.py drops notes more than `--gate` dB (default 35) under the loud passages and
  outside `--lowest`/`--highest`. Set the range to the instrument's real range.
- On a free-time take the rhythm is a guess against `--bpm`. Check `mw.py pulse` first.
- Measured on a 41 s breathy solo flute: where both engines heard a note, they agreed on the
  pitch 72% of the time and on the pitch class 81%. Treat a transcription as a draft to read and
  fix in MuseScore, then render it back and compare by ear.
- Not covered: drum transcription (the usual model, ADTOF, is non-commercial), guitar audio
  straight to tab (models exist in papers; no maintained code found), piano-specific models.

## Bridges and other tools

MuseScore Studio 4.7 (free) opens MusicXML and MIDI and exports PDF, PNG and audio:
`MuseScore4 -o out.pdf in.musicxml` (unverified here). music21 (BSD-3, Python 3.11+), abcMIDI
(GPL-2.0) and alphaTab (Guitar Pro in JavaScript) are alternatives when the stdlib readers fall
short. Notation MCP servers (mcp-musescore, music21-mcp-server, midi-mcp-server) are in
[symbolic.md](symbolic.md).
