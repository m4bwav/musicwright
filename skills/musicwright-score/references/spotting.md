# Spotting, hits and ducking

## Spotting notes

One line per cue:

```
1M1  0.0-24.0  hit; dread: low strings and piano, slow; must not compete with the opening voice-over
     hits: 11.5 (cut to the wreck), 24.0 (sunrise: hand over to 1M2)
1M2  24.0-38.0 play through; dawn: lighter strings and winds, D major
     says: she has decided to stay (the picture only shows a sunrise); knows: same
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

Cue function (Hill, *Scoring the Screen*, ch. 3 and 11):

- `says:` what the cue adds that picture and dialogue do not: a character's inner state, subtext,
  what is coming, the nature of the world. Music cannot show objects, only the feeling behind them.
  "Sad scene, sad music" restates the image: rewrite it, or leave the scene unscored. Hill's rule is
  a critic's ideal and Karlin and Wright allow plain mood support, so treat redundancy as a warning.
- `knows:` `same`, `audience ahead` or `audience behind`. The same shot of a stranger is scored
  plainly, as sinister, or neutral with a hint of a trap, depending on what the audience knows. An
  `audience ahead` cue names a tension device in its caption (low register, dissonance, a pulse),
  not only the character's mood.
- Throughline: before rendering, watch the scene and sketch its tension over time; write it as the
  `mw.py curve --shape` target. A cue that stays flat while the scene turns (surprise, realisation,
  grief) fails the drama.
- Palette: one per film in `brief.md`. List the cut's dominant sounds first (ask the film or sfx
  plugin for its sound list) and carry one or two into the score as timbre or pulse (a ticking
  ostinato, cricket-like pizzicato, wind-like woodwind flurries). Score the film, not the scene.

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

Hit style (Hill ch. 13-14): mark each hit `integrated` (played by an instrument already in the
texture: a pizzicato answering a knock) or `stinger` (an effect laid on top). Prefer integrated;
many stingers on small actions read as mickey-mousing. With generated audio, integrated means
picking a take whose own accent falls on the hit (the tempo search below); a stinger is an overlaid
sound from sfxwright. In a `play through` cue under cross-cut action, hit the story turns, not every
cut.

Cutting rhythm (Bordwell, *Film Art*, p. 282): picture and music tempos need not match, and cuts
can land on phrases rather than beats (about one cut per 5 s over a fast track). Decide whether the
cutting follows the beat, the bar or the phrase before matching cuts to the grid.

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
- Do not count on caption words to clear a cue for speech. ACE-Step XL with smooth legato, sustained,
  mid register, even dynamics, simple, against the same caption without them, blind on two seeds: the
  plain take got in the way clearly less on one, the worded take slightly less on the other. Listen
  with the voice in. Voice-over needs the strictest treatment, with no lips to help (Karlin and
  Wright ch. 10).
- Sort lines into critical (story, instructions, anything the player must hear) and background (barks, crowd chatter). Duck only under critical lines; a narrow cut on the music around 1.7-3 kHz while they play can clear the words without a big level drop (Zdanowicz and Bambrick, book rule, unverified).
- Too low also fails: music needs enough level to do its job. After `duck`, check `mw.py preview
  --as phone` and `--as quiet` copies of the mix, and ask whether the words are clear and the music
  still works (Karlin and Wright ch. 19).

## Temp tracks

A temp track sets mood and pace while cutting. Risks: the director falls for it, and with AI it
tempts copying. Analyse it (`mw.py analyze --sections` for tempo, key and where its sections change; the sheet for density and swells)
and write a caption from the descriptors. Ask what the director likes and dislikes in it, usually one
instrument or feeling, and caption from that. Do not use it as an audio reference unless the user
owns it or has a licence.

Knock-off trap (Hill ch. 11): one famous temp piece pulls every new cue towards a copy of it.
Describe the temp's function (`says:`, throughline, palette), not its surface, and check with
`mw.py analyze` that the final take does not match it on tempo, key and lead instrument all at once.
