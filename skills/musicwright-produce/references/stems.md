# Stem separation (checked 2026-11-02)

Use it to: make game layers from one track (drums only for a combat layer), remove AI vocals
from an instrumental, check which stem an artefact sits in, or feed a remix. Separated stems
carry bleed and artefacts; fine for game layers at moderate levels, not for exposed solos.

| Tool | Licence | Notes |
|---|---|---|
| Demucs v4 (`adefossez/demucs`, v4.1.0 on PyPI) | MIT | upstream archived; the fork is the home, little maintenance. 4.1.0 no longer imports torchaudio, so the torchaudio 2.9 TorchCodec change does not touch it; the `demucs-torchcodec` and `demucs-infer` forks are not needed. Models `htdemucs` (default), `htdemucs_ft` (about 4x slower, a bit better), `htdemucs_6s` (adds guitar and piano; piano weak), `mdx_extra` |
| BS-RoFormer / Mel-RoFormer | MIT code, weights vary | best vocal separation; through `python-audio-separator`, ZFTurbo Music-Source-Separation-Training, or the UVR GUI |
| Meta SAM Audio | SAM Licence, gated | separate by a text prompt ("the flute"); read the licence first |
| ACE-Step `extract` | MIT | from the generator itself (base model, REST server) |
| ElevenLabs, Suno, Mureka | plan terms | stems from the hosted service when the track came from there |

Commands (run 2026-11-02 on Windows: demucs 4.1.0, torch 2.15 CPU, Python 3.14; a 10 s clip in 3 s on CPU). The package does not declare numpy, so a bare `uvx demucs` fails with `No module named numpy`:

```bash
uvx --with numpy demucs --two-stems=vocals song.wav      # vocals + accompaniment
uvx --with numpy demucs -n htdemucs_ft song.wav          # drums, bass, other, vocals
```

uv installs the CPU build of torch from PyPI. For the GPU, add `--with torch --index https://download.pytorch.org/whl/cu128` (unchecked) or run it in a venv that already has CUDA torch, and pass `-d cuda`.

After separating, `mw.py measure` each stem: all layers of one piece must share length, tempo
and key, and should be mastered to the same preset.
