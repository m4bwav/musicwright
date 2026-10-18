# Changelog

Plugin versions. Reasoned changes per skill are in each `skills/<name>/CHANGELOG.md`.

## Unreleased

- Notation: `mw.py render` plays ABC, ASCII guitar and bass tab, MusicXML and MIDI (FluidSynth and a SoundFont when installed, otherwise a built-in sketch synth) and checks bar lengths; `mw.py notate` converts between ABC, MusicXML, MIDI and tab; `mw.py transcribe` turns a recording into MIDI, ABC, MusicXML or tab (librosa pyin for one instrument, basic-pitch for several), with a level gate and a range filter. The readers and writers are standard-library Python in `scripts/notation.py`. musicwright-compose owns the route (Step 4, references/notation.md).
- `mw.py pulse` (is there a beat: onsets, inter-onset spread, autocorrelation, grid fit) and `mw.py answer` (does a layered part sit in the lead's rests), both standard library.
- Recipe `acestep-rest-lego`: one part added to a kept take on the 2B base checkpoint, kept by a listener with the part ducked under the lead.
- Adding a part is a step in musicwright-generate; the REST reference names the server version that fixes base-model noise (DCW) and the measured VRAM per model.
- `mw.py mix`: layer stems with per-file gain, offset and pan into one file, with aligned stems.
- `mw.py gen --task cover|repaint|lego|complete|extract --src F --track T`: work from existing audio on the ACE-Step REST server (lego, complete and extract need a base checkpoint); the source is uploaded and the planner is turned off so the new part hears it.
- `mw.py duck` keeps the music's length when the key is shorter, and `--stem` writes the ducked music alone.
- master, edit, join, loop, duck and sheet create a missing `--out` folder; gen validates before creating one and no longer creates it on dry runs; the REST route sends `--cfg`, `--steps`, `--shift` and `--set`, and lists options it cannot use.

## 0.1.0 (2026-10-17)

First release.

- Seven evergreen skills: musicwright (hub: brief, route, the take loop for an agent that cannot listen, the project contract), musicwright-generate (models, licences, captions, seeds, fixing takes), musicwright-compose (theory, motifs, prompt vocabulary, notes-first routes), musicwright-produce (loudness, mastering, formats, stems, mixing fixes), musicwright-game (seamless loops, layers, stingers, Unity import), musicwright-score (spotting, hit points, movements, ducking under dialogue) and musicwright-curate (verdicts, taste, lessons, recipes).
- `mw.py` (standard-library Python 3.9+, needs ffmpeg): doctor, new, gen (ACE-Step 1.5 XL and MiniMax Music 3 through ComfyUI, the ACE-Step REST server; `--dry-run` prints the graph or payload), measure (LUFS, LRA, true peak, head and tail silence, clipping), sheet (spectrogram and waveform contact sheet), master (two-pass loudness to a preset), edit, join (crossfades on hit points), loop (bar-exact, tail crossfaded into head, OGG loop tags), seam, duck (under dialogue or a video's sound, remuxing the video), analyze (tempo and key with librosa), verdict, ledger and note.
- Four generation recipes in `recipes.json` and eight loudness presets in `loudness.json`, each with its source.
- `tests/check_skills.py` (structure, companions, manifests, recipes and presets, links, public-safety guards), `tests/test_mw.py` (every command on synthetic audio, `gen` against a fake local host) and `scripts/budget.py`; CI on Ubuntu, macOS and Windows with ffmpeg.
- Research notes of 2026-10-17 in `ai-docs/research`.
