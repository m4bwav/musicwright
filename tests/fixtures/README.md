# Test fixtures

Small synthetic signals for the agent eval cases in `skills/*/evals/evals.json` (made with ffmpeg `aevalsrc`, 8 kHz mono):

- `tone.wav`: 12 s A-major triad (220, 277.18, 329.63 Hz).
- `a.wav`, `b.wav`: 8 s tones (G3, D4) with a slow swell, for join cases.
- `take_s1.flac`: `a.wav` as FLAC, standing in for a generated take (its G3 sits under a flute's range, for the mixcheck `--lowest` case).

- `tune.abc`: an original 4-bar tune in G with a repeat, first and second endings, a broken rhythm, a triplet and chord symbols, for render and notate cases.
- `riff.txt`: an original two-bar ASCII tab in drop D with a two-digit fret.
- `wander.abc`: a random walk of leaps with a rhythm that never repeats, for the melody-check case (both melody hints fire).

`tests/test_mw.py` makes its own signals in a temporary folder and uses only the two notation files.
