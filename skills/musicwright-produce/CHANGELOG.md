# Changelog: musicwright-produce

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-20261120-1 · 2026-11-20 · stems.md points to mw.py stemcheck
- because: user request (technique harvest, arXiv:2610.17821, adopt-partly)
- files: references/stems.md (one line after the commands)
- Run stemcheck after separating; generative separators need it most. SKILL.md unchanged, evals not re-run.

### C-20261118-2 · 2026-11-18 · Reverb recipe measured; flag tables to flags.md
- because: user request (turn the recipe into a measured result; size budget back to green)
- files: references/mixing.md (Reverb and delay by job: measured RT60 and tail, afir irnorm=2), references/flags.md (new: mixcheck and analyze flag tables moved whole), SKILL.md (one line shortened)
- `mw.py reverb` runs the recipe. With afir's default IR norm the wet path sat about 43 dB under the dry; irnorm=2 fixes it. Not judged by ear yet. Evals not re-run.

### C-20261107-2 · 2026-11-07 · Stretch, varispeed and formant notes
- because: book distillation, Roads, The Computer Music Tutorial 2e (everscout ai-music beat)
- files: references/ffmpeg.md (time-stretch note)

Added the book's failure modes as a short check; not tested on generated audio.

### C-20261118-1 · 2026-11-18 · Synthesised reverb impulse
- because: user request (technique harvest from vitaminclaude/voidstruck, ideas only)
- files: references/mixing.md (Reverb and delay by job)
- Seeded noise, power-law decay and a falling one-pole lowpass as a recipe; not judged by ear.

### C-20261114-1 · 2026-11-14 · Roughness, quiet playback, stretch stems
- because: book distillation, Loy, Musimathics vols. 1-2 (R-20261114-1)
- files: references/mixing.md (one line), references/ffmpeg.md (one sentence)

Book rules, untested on generated audio.

### C-20261113-1 · 2026-11-13 · Rubber Band for pitch shifts
- because: user request (slide guitar study, ai-docs/research/2026-11-13-slide-guitar-study.md)
- files: references/ffmpeg.md (Stretching)

Rubber Band R3 with --formant and pitch or time maps over resampling, Audacity or librosa. Evals not re-run.

### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.


Older entries: [ai-docs/changelog-archive/musicwright-produce.md](../../ai-docs/changelog-archive/musicwright-produce.md).
