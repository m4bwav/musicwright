# Loudness targets (checked 2026-10-17)

Integrated loudness per ITU-R BS.1770 (LUFS = LKFS), true peak in dBTP. The presets live in the
hub's references/loudness.json; change a number there only with a source.

| Destination | Integrated | True peak | Source |
|---|---|---|---|
| Spotify | normalises to -14 (Loud -11, Quiet -19) | below -1; below -2 if louder than -14 | https://support.spotify.com/us/artists/article/loudness-normalization/ |
| Apple Music | Sound Check at about -16 (secondary sources) | 1 dB headroom, send 24-bit | Apple Digital Masters brief |
| YouTube | turns loud tracks down to about -14, never up (not officially documented) | -1 (practice) | |
| AES TD1008 | music streams -16 | | |
| EBU R128 v5.0 (Nov 2023) | -23 ±0.5 LU (±1 live) | -1 | https://tech.ebu.ch/publications/r128 |
| ATSC A/85 (US broadcast) | -24 ±2 | -2 | |
| Netflix | -27 ±2 dialogue-gated | -2 | https://backlothelp.netflix.com/hc/en-us/articles/360001794307 |
| Console games (Sony ASWG, IESD) | -24 ±2 over a long capture | -1 | IESD Mix Reference Levels |
| Handheld and mobile games | -18 ±2 (PlayStation portable) or -16 (IESD) | -1 | sources conflict |
| Xbox, Steam/PC | no published target found | | |
| Cinema | calibrated playback, not a LUFS target | | |

Game and film targets describe the whole mix. A single music asset for a game is mastered
consistently (the `game-music` preset, -18 LUFS) and balanced in the engine. For one track to
listen to or upload, -14 LUFS and -1 dBTP is the safe single target.

## loudnorm details (verified 2026-10-17)

- Defaults are I=-24, LRA=7, TP=-2: always set them.
- It resamples to 192 kHz internally: always add `-ar 48000` (or the source rate) on output.
- Two passes with the measured values and `linear=true` apply one static gain. When the target
  needs more true-peak headroom than the file has, it falls back to dynamic mode: check
  `normalization_type` in the second pass (mw.py reports it).
- pyloudnorm agrees with ffmpeg within 0.1 LU.
