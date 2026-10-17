---
name: musicwright-produce
description: "Use whenever music audio exists and must be finished or checked: loudness to a destination (streaming -14 LUFS, game music, web video, broadcast EBU R128) with true peak, two-pass mastering, trimming and fades, formats and sample rates (WAV, FLAC, OGG, why MP3 breaks loops), clipping, silence and mono checks, stems with Demucs or RoFormer, mixing fixes for AI output, reference mastering. Runs mw.py measure, master, edit, analyze. Use on 'master this', 'how loud should it be', 'normalise to -14', 'is this clipping', 'convert to ogg', 'split the stems', 'it's too quiet'. Loops for games are musicwright-game; fitting to a video is -score. Also 'refresh musicwright-produce'."
---

# musicwright-produce

Finishing and checking. Everything here is measured, never guessed: run the number before and
after every change and report both. Script: `mw.py` in the musicwright hub's `scripts/` folder.

## Step 1: measure

`mw.py measure <files>` gives duration, sample rate, integrated loudness (LUFS), loudness range
(LRA), true peak, head and tail silence, interior gaps, clipping signs and warnings.
`mw.py analyze <files>` adds tempo and key when librosa is available (it prints the `uv run`
line when it is not). Picture: `mw.py sheet <files> --out <png>`, then look at it.

## Step 2: pick the destination preset

| Preset | LUFS | True peak | When |
|---|---|---|---|
| `streaming` | -14 | -1 | personal listening, Spotify, YouTube uploads |
| `apple` | -16 | -1 | Apple Music, AES streaming guidance |
| `web-video` | -16 | -1.5 | score or bed under web video, one level for every cue in a film |
| `game-music` | -18 | -1 | every music asset in one game, mastered to the same level |
| `game-console-mix` / `game-mobile-mix` | -24 / -18 | -1 | the whole game mix, not a single file |
| `broadcast` / `broadcast-us` | -23 / -24 | -1 / -2 | EBU R128 / ATSC A/85 |

Game targets apply to the whole mix: master all music files of one game to one level and
balance against SFX in the engine's mixer. Sources and caveats: [references/loudness.md](references/loudness.md).

## Step 3: fix, then master last

Order: trim and fade (`mw.py edit`), then any repair, then loudness (`mw.py master`).

- Silence at the end (common in AI renders): `mw.py edit <in> --end <t> --fade-out 2-4 --out <out>`.
- Too quiet or too loud: `mw.py master <in> --preset <p> --out <out>`. It runs two-pass loudnorm,
  linear when possible, resamples to 48 kHz and reports before and after. "dynamic" in the result
  means the target needed more headroom than the file had and dynamics were changed: say so,
  or choose a lower target.
- Clipping or harsh peaks in the source: a lower target, or a gentle limiter in a DAW; never
  stack more compression on AI output, which is usually already dense.
- Muddy (200-500 Hz), harsh (2-5 kHz), dull (nothing above 16 kHz): describe it and suggest EQ
  moves from [references/mixing.md](references/mixing.md); the agent cannot judge by ear.
- Stems for layers, removing AI vocals, or checking an artefact: [references/stems.md](references/stems.md).

## Step 4: formats

- Work and archive in WAV (24-bit) or FLAC at the source rate; 48 kHz for games and video.
- OGG Vorbis (q6) for engines; MP3 only for distribution, never for loops (encoder padding adds
  silence: measured +1,728 samples when the gapless tag is missing).
- Never upsample AI output to look better; it does not add detail.
- Convert with `mw.py edit <in> --out <name>.<ext>` (codec from the extension).

## Step 5: report and record

Report every deliverable with its path and the after numbers, plus what you could not check by ear.
Add it to `music.json` deliverables (hub references/contract.md). A lesson worth keeping
(a preset that suited a destination, a fix that worked) goes to musicwright-curate.

## Rules

- Measure before and after every change; never claim an improvement without the numbers.
- Master last, once. Re-mastering a mastered file stacks artefacts.
- Keep the original take untouched in `takes/`; write results to `out/`.
- Tools that are GPL or AGPL (Matchering, Essentia) are called as separate programs, never vendored.

## References

- [references/loudness.md](references/loudness.md): targets by destination with sources, loudnorm details.
- [references/mixing.md](references/mixing.md): frequency map, EQ, compression, reverb and stereo rules, scripted QC checks.
- [references/ffmpeg.md](references/ffmpeg.md): tested ffmpeg recipes for everything mw.py does and a few it does not.
- [references/stems.md](references/stems.md): Demucs and RoFormer separation, and when to use them.

## Maintenance

Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md),
[LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evergreen.json`. Platform loudness targets
can change: refresh when due.
