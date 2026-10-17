# Spotting, hits and ducking

## Spotting notes

One line per cue:

```
1M1  0.0-24.0  dread: low strings and piano, slow; must not compete with the opening voice-over
     hits: 11.5 (cut to the wreck), 24.0 (sunrise: hand over to 1M2)
1M2  24.0-38.0 dawn: lighter strings and winds, D major
1M3  38.0-46.0 resolve: flute and trumpets; ring out under the title
```

Rules: music starts under a sound or on a cut, not in silence; it stops on a hit or rings out;
the first and last seconds are the most noticed. Name the hits that must land and the moments
that must stay quiet.

## Tempo and hits

- bpm = 60 x beats / seconds between two hits. Hits 7.5 s apart with 16 beats → 128 bpm.
- One bar at 120 bpm in 4/4 = 2 s. Plan sections as whole bars between hits.
- Frame rates 24, 25, 29.97, 30, 60; one frame at 24 fps = 41.7 ms: the tolerance for a hit.
- Fitting after rendering: cut or repeat at bar lines; time-stretch up to about ±5% before it
  sounds processed.

## Movements

Render each movement a few seconds longer than its slot (short renders often fade early), pick
the best take of each, then `mw.py join ... --lengths a,b,c --xfade 2`. The crossfade begins at
each hit point. A 2 s equal-power crossfade suits a mood change; use 0.5-1 s for a hard cut.

## Ducking under dialogue (rules of thumb; no standard found)

- Duck 6-12 dB, attack 30-80 ms, release 250-700 ms; or set music 10-15 LU below the dialogue
  while someone speaks.
- Web video dialogue sits around -16 to -20 LUFS short-term.
- `mw.py duck` defaults: threshold 0.03, ratio 4, attack 40 ms, release 500 ms. Raise the ratio
  for a deeper duck.
- Music under a line ruins pitch tracking of that line: measure or tune voices alone.

## Temp tracks

A temp track sets mood and pace while cutting. Risks: the director falls for it, and with AI it
tempts copying. Analyse it (`mw.py analyze` for tempo and key; the sheet for density and swells)
and write a caption from the descriptors. Do not use it as an audio reference unless the user
owns it or has a licence.
