# Changelog

Plugin versions. Reasoned changes per skill are in each `skills/<name>/CHANGELOG.md`.

## 0.1.0 (2026-10-17)

First release.

- Seven evergreen skills: musicwright (hub: brief, route, the take loop for an agent that cannot listen, the project contract), musicwright-generate (models, licences, captions, seeds, fixing takes), musicwright-compose (theory, motifs, prompt vocabulary, notes-first routes), musicwright-produce (loudness, mastering, formats, stems, mixing fixes), musicwright-game (seamless loops, layers, stingers, Unity import), musicwright-score (spotting, hit points, movements, ducking under dialogue) and musicwright-curate (verdicts, taste, lessons, recipes).
- `mw.py` (standard-library Python 3.9+, needs ffmpeg): doctor, new, gen (ACE-Step 1.5 XL and MiniMax Music 3 through ComfyUI, the ACE-Step REST server; `--dry-run` prints the graph or payload), measure (LUFS, LRA, true peak, head and tail silence, clipping), sheet (spectrogram and waveform contact sheet), master (two-pass loudness to a preset), edit, join (crossfades on hit points), loop (bar-exact, tail crossfaded into head, OGG loop tags), seam, duck (under dialogue or a video's sound, remuxing the video), analyze (tempo and key with librosa), verdict, ledger and note.
- Four generation recipes in `recipes.json` and eight loudness presets in `loudness.json`, each with its source.
- `tests/check_skills.py` (structure, companions, manifests, recipes and presets, links, public-safety guards), `tests/test_mw.py` (every command on synthetic audio, `gen` against a fake local host) and `scripts/budget.py`; CI on Ubuntu, macOS and Windows with ffmpeg.
- Research notes of 2026-10-17 in `ai-docs/research`.
