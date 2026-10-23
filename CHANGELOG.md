# Changelog

Plugin versions. Reasoned changes per skill are in each `skills/<name>/CHANGELOG.md`.

## Unreleased

- `mw.py analyze` (librosa, still optional) reports tuning against A440 (offset, spread and trend over 10 s windows), each later file's tuning gap from the first, the share of the track that repeats an earlier 8 s block, and with `--sections` the section boundaries in seconds and bars (an automatic count, a number, or tag names). Flags OFF-A440, DRIFT, REPEATS and TUNING-GAP, set on 111 AI renders and 11 human recordings; rates in musicwright-produce's references/mixing.md. Tempo and key are unchanged.
- `mw.py mixcheck`: one ffmpeg pass gives each band's level against the whole, peak-to-loudness ratio, a short-term loudness contour, stereo correlation, mono-fold loss and low-end width, with flags (OVER-LIMITED, FLAT, MUDDY, BRIGHT, MONO-LOSS, LOW-WIDE, and BELOW-RANGE with `--lowest NOTE`). Thresholds set on 78 real AI renders, rates in musicwright-produce's references/mixing.md. `mw.py compare take ref` sets two files side by side.
- `mw.py preview`: loudness-matched copies for listening, `--blind` (shuffled take_A, take_B and a key file), `--as phone` and `--as quiet`. The hub's take loop hands these over instead of the raw takes.
- `mw.py monobass` (Linkwitz-Riley crossover, lows to mono); `mw.py mix --shelves` and `--automate` (per-file high shelf and gain envelopes); `mw.py master --peak` (gain-only pre-master, no limiter) and an `lra_hint` per loudness preset.
- `mw.py render --check` gives melody hints per line (leap share, returning rhythm), calibrated on public-domain tunes against random walks.
- Craft from Oltheten, *Mixing With Impact*, and DeSantis, *Making Music*: fixes for AI renders (produce), melody, harmonic rhythm, arrangement and endings and a five-field reference (compose), section tags that say who plays and a stop rule (generate), a "Tired of" list (curate), never-repeating beds and layers by subtraction (game), a presence check for cues under dialogue (score).
- Notation: `mw.py render` plays ABC, ASCII guitar and bass tab, MusicXML and MIDI (FluidSynth and a SoundFont when installed, otherwise a built-in sketch synth) and checks bar lengths; `mw.py notate` converts between ABC, MusicXML, MIDI and tab; `mw.py transcribe` turns a recording into MIDI, ABC, MusicXML or tab (librosa pyin for one instrument, basic-pitch for several), with a level gate and a range filter. The readers and writers are standard-library Python in `scripts/notation.py`. musicwright-compose owns the route (Step 4, references/notation.md).
- `mw.py pulse` (is there a beat: onsets, inter-onset spread, autocorrelation, grid fit) and `mw.py answer` (does a layered part sit in the lead's rests), both standard library.
- Recipe `acestep-rest-lego`: one part added to a kept take on the 2B base checkpoint, kept by a listener with the part ducked under the lead.
- Adding a part is a step in musicwright-generate; the REST reference names the server version that fixes base-model noise (DCW) and the measured VRAM per model.
- `mw.py mix`: layer stems with per-file gain, offset and pan into one file, with aligned stems.
- `mw.py gen --task cover|repaint|lego|complete|extract --src F --track T`: work from existing audio on the ACE-Step REST server (lego, complete and extract need a base checkpoint); the source is uploaded and the planner is turned off so the new part hears it.
- `mw.py duck` keeps the music's length when the key is shorter, and `--stem` writes the ducked music alone.
- master, edit, join, loop, duck and sheet create a missing `--out` folder; gen validates before creating one and no longer creates it on dry runs; the REST route sends `--cfg`, `--steps`, `--shift` and `--set`, and lists options it cannot use.
- Game cues from the level plan (musicwright-game, after Rogers, *Level Up!*): the cue list comes from a beat chart or `LEVEL-PLAN.md` when there is one; new cue types mystery, warning, chase and a villain motif; rules on rotating two tracks per area, energy for action cues, the title piece, silence as an event, stinger direction and a visual twin for cues that carry information.
- Six skills' `MAINTENANCE.md` files point at the hub's identical copy, which takes the installed skills from 446 KB to 420 KB.

## 0.1.0 (2026-10-17)

First release.

- Seven evergreen skills: musicwright (hub: brief, route, the take loop for an agent that cannot listen, the project contract), musicwright-generate (models, licences, captions, seeds, fixing takes), musicwright-compose (theory, motifs, prompt vocabulary, notes-first routes), musicwright-produce (loudness, mastering, formats, stems, mixing fixes), musicwright-game (seamless loops, layers, stingers, Unity import), musicwright-score (spotting, hit points, movements, ducking under dialogue) and musicwright-curate (verdicts, taste, lessons, recipes).
- `mw.py` (standard-library Python 3.9+, needs ffmpeg): doctor, new, gen (ACE-Step 1.5 XL and MiniMax Music 3 through ComfyUI, the ACE-Step REST server; `--dry-run` prints the graph or payload), measure (LUFS, LRA, true peak, head and tail silence, clipping), sheet (spectrogram and waveform contact sheet), master (two-pass loudness to a preset), edit, join (crossfades on hit points), loop (bar-exact, tail crossfaded into head, OGG loop tags), seam, duck (under dialogue or a video's sound, remuxing the video), analyze (tempo and key with librosa), verdict, ledger and note.
- Four generation recipes in `recipes.json` and eight loudness presets in `loudness.json`, each with its source.
- `tests/check_skills.py` (structure, companions, manifests, recipes and presets, links, public-safety guards), `tests/test_mw.py` (every command on synthetic audio, `gen` against a fake local host) and `scripts/budget.py`; CI on Ubuntu, macOS and Windows with ffmpeg.
- Research notes of 2026-10-17 in `ai-docs/research`.
