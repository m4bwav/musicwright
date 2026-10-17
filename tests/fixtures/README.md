# Test fixtures

Small synthetic signals for the agent eval cases in `skills/*/evals/evals.json` (made with ffmpeg `aevalsrc`, 8 kHz mono):

- `tone.wav`: 12 s A-major triad (220, 277.18, 329.63 Hz).
- `a.wav`, `b.wav`: 8 s tones (G3, D4) with a slow swell, for join cases.
- `take_s1.flac`: `a.wav` as FLAC, standing in for a generated take.

`tests/test_mw.py` makes its own signals in a temporary folder and does not use these.
