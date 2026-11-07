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

Header rule: every MIDI file carries key signature and time signature meta events, and every ABC
tune its `K:` and `M:` lines. Without them a reader (or `mw.py render --check`, whose `key_fit`
compares the notes with the declared key) has to guess, and a model trained on notes loses the
context it reads first (after Foster, *Generative Deep Learning* 2e, ch. 11).

Events or grid: a fixed step grid (one cell per sixteenth) cannot hold triplets, cannot tell one
long note from the same pitch struck again, and has no room for dynamics. Use the events list
above (start, end, pitch, velocity) whenever a part has triplets, repeated same-pitch notes or
dynamics; a grid is fine for straight drum patterns (same source).

## Generating notes by rule (Collins 2010, untested here)

Rules are worth trying when a model will not obey or a piece must vary on each run. These come from Collins, *Introduction to Computer Music*, sec. 8.3 and 9.4 to 9.6.

- Markov chain over notes: a low order wanders and a high order quotes the source. Order three to four is the book's reported trade-off. A small source needs a lower order, and a token with no onward transition needs a jump or a relaxed match.
- Random source: white noise sounds unrelated, a random walk (Brownian) sounds too tied to the last note, and 1/f sits between them. The book presents 1/f as a baseline, not a guarantee of good music.
- Repetition and change: music sits between constant surprise and constant repeat, across several timescales. Vary one parameter while another repeats.
- Performance: small random timing jitter is the quick fix for a stiff sequence, and rules fitted by trying them and listening go further. Very fine timing tends to be heard as expression, not as rhythm.
- Keep the hand edits: record which outputs were picked and changed, because that human choice is part of the method when judging it.

Better prediction is not a better piece: in one study (Oxford Handbook of Computer Music, ch. 19) sixteen judges rated Bach's chorale melodies about 6 and generated ones about 3, and the system best at predicting unseen melodies scored no clear gain. It covers one style and statistical models of pitch, so take the warning, not the numbers: judge by listening, not by a model's fit.

## Audio by matching (same book, ch. 20, untested here)

Soundspotting cuts a source library into segments and, for each piece of a target, joins the closest one. It keeps the target's music and the source's sound, the split a cover or timbre reference is after.

- Match on features tied to hearing, or the result sounds random. In the book's system, low cepstral coefficients select for timbre and high ones for pitch.
- Segment length is the trade-off: at 0.01 s the source vanishes, and from about 0.25 s it is recognisable but matches get worse. A larger library wins matches back.
- Only use source audio the user owns or has licensed.

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
