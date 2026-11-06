# Spotting, hits and ducking

## Spotting notes

One line per cue:

```
1M1  0.0-24.0  hit; dread: low strings and piano, slow; must not compete with the opening voice-over
     hits: 11.5 (cut to the wreck), 24.0 (sunrise: hand over to 1M2)
1M2  24.0-38.0 play through; dawn: lighter strings and winds, D major
1M3  38.0-46.0 phrase; resolve: flute and trumpets; ring out under the title
no music: 46.0-52.0, the closing line must land
```

Rules (Karlin and Wright, *On the Track*, ch. 4, 10):

- Treatment: play through (one mood), phrase (acknowledge each shift, often by colour or an added
  instrument rather than a new theme) or hit. How much to hit is a style decision; settle it early.
- Start at a shift of emphasis: new emotion or subject in the dialogue, a camera move, a new action,
  a reaction. A cut is fine if it coincides, and starting between cuts works too. Soft or accented is
  a choice.
- End at the next shift, tail under the next line, or go hard out on action and tension cues. Leave
  mid-scene when the cue has run long enough, must return soon and silence will help, or would hurt
  the scene by staying.
- Stopping is a statement, so gaps are part of spotting. If nobody can say what a cue is for, question it.
- The first and last seconds are the most noticed. Name the hits that must land and the moments
  that must stay quiet.

## Tempo and hits

- First ask whether a tempo fits the emotion, the dialogue and the cutting rhythm: the search below
  finds tempos that land hits, not ones that suit the scene.
- bpm = 60 x beats / seconds between two hits. Hits 7.5 s apart with 16 beats → 128 bpm.
- One bar at 120 bpm in 4/4 = 2 s. Plan sections as whole bars between hits.
- Frame rates 24, 25, 29.97, 30, 60; one frame at 24 fps = 41.7 ms. Aim within 2 frames (83 ms)
  on sharp events such as a door slam or a hard cut; softer moments need less. If it must miss, miss
  late: about 100 ms early reads as wrong. A general rule from Karlin and Wright ch. 8, no study cited.
- Fitting after rendering: cut or repeat at bar lines; time-stretch up to about ±5% before it
  sounds processed.

With several hits, try tempos in 0.25 bpm steps around the felt tempo, count how many frames each hit misses the nearest beat, and weight the critical hits. Changing one bar's meter (3/4, 5/4) can put a hit on a downbeat. From one practitioner and one course handout.

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
- Keep the foreground steady under dialogue: a sudden burst at 2-5 kHz pushes the voice back and
  the ear is slow to settle again (after Oltheten, *Mixing With Impact* 5.4). Check every cue that
  plays under speech with `mw.py mixcheck`: BRIGHT or a high `presence_db` means it competes with
  the voice; pick another take or duck it.
- Caption cues under speech positively: smooth legato, sustained, mid register, even dynamics, simple.
  Voice-over needs the strictest treatment, with no lips to help (Karlin and Wright ch. 10). Whether
  models obey is untested.
- Too low also fails: music needs enough level to do its job. After `duck`, check `mw.py preview
  --as phone` and `--as quiet` copies of the mix, and ask whether the words are clear and the music
  still works (Karlin and Wright ch. 19).

## Temp tracks

A temp track sets mood and pace while cutting. Risks: the director falls for it, and with AI it
tempts copying. Analyse it (`mw.py analyze --sections` for tempo, key and where its sections change; the sheet for density and swells)
and write a caption from the descriptors. Ask what the director likes and dislikes in it, usually one
instrument or feeling, and caption from that. Do not use it as an audio reference unless the user
owns it or has a licence.
