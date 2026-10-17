# Stem separation (checked 2026-10-17)

Use it to: make game layers from one track (drums only for a combat layer), remove AI vocals
from an instrumental, check which stem an artefact sits in, or feed a remix. Separated stems
carry bleed and artefacts; fine for game layers at moderate levels, not for exposed solos.

| Tool | Licence | Notes |
|---|---|---|
| Demucs v4 (`adefossez/demucs`, v4.1.0) | MIT | upstream archived; the fork is the home, little maintenance. Models `htdemucs` (default), `htdemucs_ft` (about 4x slower, a bit better), `htdemucs_6s` (adds guitar and piano; piano weak), `mdx_extra` |
| BS-RoFormer / Mel-RoFormer | MIT code, weights vary | best vocal separation; through `python-audio-separator`, ZFTurbo Music-Source-Separation-Training, or the UVR GUI |
| Meta SAM Audio | SAM Licence, gated | separate by a text prompt ("the flute"); read the licence first |
| ACE-Step `extract` | MIT | from the generator itself (base model, REST server) |
| ElevenLabs, Suno, Mureka | plan terms | stems from the hosted service when the track came from there |

Commands (not run here yet):

```bash
uvx demucs --two-stems=vocals song.wav      # vocals + accompaniment
uvx demucs -n htdemucs_ft song.wav          # drums, bass, other, vocals
```

After separating, `mw.py measure` each stem: all layers of one piece must share length, tempo
and key, and should be mastered to the same preset.
