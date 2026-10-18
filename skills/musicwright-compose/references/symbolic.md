# Notes-first routes (checked 2026-10-17)

## Formats and libraries

| Format | Write with | Check by | Good for |
|---|---|---|---|
| ABC | plain text | `mw.py render --check` (stdlib), abcjs (browser link), `abc2midi` | short melodies, sharing a tune in chat |
| MIDI | `mido`, `pretty_midi` (Python) | re-read, print notes per bar; FluidSynth + a General MIDI SoundFont to render | DAWs, game engines, sketches |
| MusicXML | `music21` | MuseScore's command line (`<MuseScore executable> -o out.pdf in.musicxml`; the executable is `mscore` on Linux, `MuseScore4` on Windows and macOS; unverified here) or verovio to PNG, then look | scores to print or edit |
| LilyPond | `.ly` text | `lilypond` to PDF/PNG | engraved scores |
| Strudel | JavaScript patterns | a strudel.cc share link (the code fits in the URL) | loops, live coding |
| Sonic Pi / SuperCollider | Ruby / sclang | Sonic Pi over OSC; SuperCollider non-real-time render to a file | generative and live code |

Run Python music libraries without installing them: `uv run --no-project --python 3.12 --with
music21 --with mido python script.py`.

A shared events list keeps formats in step: `{layer, start_beat, end_beat, midi, velocity}`
converts to MIDI, MusicXML, ABC and Strudel.

## Models that write notes

- YuE2's ABC layer: generate or edit the melody and chord plan as ABC, then render audio (ComfyUI
  native `YuE2GenerateABC`, `YuE2GenerateMusic`).
- Anticipatory Music Transformer (Apache 2.0): infilling and accompaniment over MIDI. MIDI-LLM:
  text to multitrack MIDI (Llama 3.2 licence). Text2midi (MIT) is the common baseline.
- Transcription back to notes: `mw.py transcribe` (pyin or basic-pitch, Apache 2.0; see notation.md);
  YourMT3+ (GPL-3.0) for multi-instrument; MuScriptor (2026-07, weights licence unstated).
- Often no model is needed: write the MIDI or ABC directly, then render and look.

## DAW and notation bridges (MCP servers)

| Software | Server | Licence | Note |
|---|---|---|---|
| Ableton Live | adamjmurray/producer-pal (MCP + REST + skills) | GPL-3.0 | most complete; Max for Live |
| Ableton Live | ahujasid/ableton-mcp | MIT | most starred; Remote Script setup is the usual trouble; has telemetry |
| REAPER | TwelveTake-Studios/reaper-mcp | MIT | stock REAPER, file bridge, workflow tools (sidechain in one call) |
| Logic Pro | MongLong0214/logic-pro-mcp | MIT | macOS, fail-closed |
| FL Studio | karl-andres/fl-studio-mcp | MIT | early |
| MuseScore | tskovlund/mcp-score | MIT | MusicXML plus live editing |
| Wwise | BilkentAudio/Wwise-MCP | Apache-2.0 | experimental |

What works through them: organising and renaming big sessions, track layouts, writing MIDI,
sidechain and routing chores, sample search. What fails: taste, and writes that report success
but change nothing. Read the project back after every write, and keep steps small to avoid
timeouts. Anthropic's own Ableton connector only answers from documentation; it controls nothing.

## Learning path (free)

1. Ableton Learning Music (learningmusic.ableton.com): beats, scales, chords, basslines, song
   structure in a browser, one evening.
2. Hooktheory TheoryTab and 8-bit Music Theory (YouTube): put names to what you already like.
3. musictheory.net, Open Music Theory, MIT OCW 21M.051 for depth.
4. Cambridge-MT free multitracks for mixing practice.
5. Wwise and FMOD free courses when a game outgrows the engine's own mixer.
