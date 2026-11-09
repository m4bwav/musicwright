---
name: musicwright-score
description: "Use whenever music must fit a video or film cut: spotting (where cues start and stop and what they must hit), choosing a tempo so hits land on beats (bpm = 60 x beats / seconds), rendering movements with their own mood and key and joining them on hit points, one continuous score instead of per-shot music, shaping loudness to the scenes, ducking under dialogue, temp tracks, delivery loudness. Runs mw.py join, duck, edit, master. Use on 'score this video', 'music for my short film', 'the music cuts abruptly between scenes', 'make it build to the reveal', 'duck the music under the voice'. Sound design and dialogue belong to the film plugin. Also 'refresh musicwright-score'."
---

# musicwright-score

Music written to picture. The cut is the boss: every decision starts from the timeline. Script:
`<this folder>/../musicwright/scripts/mw.py` (the sibling hub folder). When a film plugin owns the whole sound mix, this skill delivers
the music stem it asks for and lets that plugin mix.

## Step 1: spot the cut

Watch or read the cut and write a cue list in `brief.md`: for each cue its start and end (seconds),
purpose (emotion, tension, transition), treatment (`play through`, `phrase` or `hit`), the hits
that must land (a reveal, a cut, a door slam), and what it must not do (fight dialogue, give away a
twist). Cue names 1M1, 1M2. Name where music stays out and why (realism, a line that must land,
saving the next entry), and settle this before rendering: it sets how many movements you need.
Enter at a shift of emphasis (dialogue, camera, action, reaction), on a cut or between cuts, soft or
accented; exit at the next shift, tail under the next line, or go hard out on action and tension.
Give every cue a `says:` line, what the music tells the audience that picture and dialogue do not
(inner state, subtext, what is coming); a `says:` that restates the image is redundant, so rewrite
it or leave the scene unscored. Add `knows:` (`same`, `audience ahead`, `audience behind`) and mark
each hit `integrated` or `stinger`. Before rendering, sketch the scene's tension over time and keep
it as the `mw.py curve --shape` target. Method: [references/spotting.md](references/spotting.md).

## Step 2: one score, in movements

- Across a sequence, prefer one continuous score over separate music per shot: per-shot music
  re-attacks at every cut and sounds broken. Keep the gaps the cue list names; a director's standing
  preference for unbroken music wins. Render the video without its own music when the
  video tool offers that.
- One caption holds one colour. A cue that travels (dread → dawn → triumph) is rendered as
  movements, each with its own caption, key and length, a few seconds longer than its slot.
- Tempo for hits: bpm = 60 x beats / seconds between hits (7.5 s for 16 beats → 128 bpm); aim within
  2 frames (83 ms at 24 fps) on sharp events, softer moments need less, and if it must miss, miss
  late. Generated music cannot be told where hits are:
  choose the bpm, then cut at bar lines.
- One `palette:` per film in `brief.md` (instrument families, harmonic colour, density,
  attitude), taken partly from the cut's own sound world (machinery, crickets, wind): every cue
  caption draws from it, and a cue that leaves it says why.
- Period or classical films: name period instruments and forms in the caption (musicwright-compose
  vocabulary.md); "gentle, tender" pulls a modern sound.

Generate the movements through musicwright-generate (several seeds each), look at the sheets,
let the director listen (on an askwright page when `mw.py doctor` reports `askwright`; hub Step 3), record verdicts.

## Step 3: assemble

- Join on the hit points: `mw.py join m1.flac m2.flac m3.flac --lengths 24,10,12 --xfade 2
  --fade-out 1.5 --out out/score.wav`. Each part holds its length, then crossfades (equal power)
  into the next; `crossfade_centres_s` in the result are the hit points.
- Trim or extend at bar boundaries; small tempo nudges with `atempo` up to about ±5%
  (musicwright-produce ffmpeg.md).
- Loudness shape: section tags rarely shape a cue's dynamics. Shape it after rendering, with
  gain changes per section in a DAW or the film plugin, rather than re-rolling for it. To pick
  the take that already follows the arc, rank them against the target shape:
  `mw.py curve t1.flac t2.flac --shape 0:-30,20:-18,50%:-14,end:-24` (rms_error_lu under about
  2 follows it; spans say where a take is too loud or quiet; short-term loudness lags up to 3 s).

## Step 4: sit it under the picture

- Dialogue: duck the music 6-12 dB while people speak (attack 30-80 ms, release 250-700 ms):
  `mw.py duck out/score.wav --under <video or dialogue> --out <out.mp4 or out.wav>`. It remuxes
  the video when the output is a video file. Tune by ear; no standard depth exists.
- Too low also fails: make `mw.py preview --as phone` and `--as quiet` copies of the mix and ask the
  director whether the words are clear and the music still does its job.
- Master the final mix (or the music stem, if a film plugin mixes) to `web-video` (-16 LUFS,
  -1.5 dBTP) for the web, `broadcast` for EBU delivery.

## Step 5: hand over

Report the score file, the cue list with hit times, the numbers, and what nobody has listened to
yet. Record the director's notes as verdicts (`mw.py verdict`), and their standing preferences
("one continuous score", "classical, not modern") through musicwright-curate.

## Rules

- Temp tracks guide pace and mood only: analyse them (tempo, key, instruments, density, where it
  swells) and write a caption from that. Never upload someone else's music as a reference.
- Never name a living composer or artist in a prompt.
- Keep the music stem separate from the mix so it can be re-balanced later.

## References

- [references/spotting.md](references/spotting.md): spotting notes, hit maths, frame rates, ducking numbers, temp-track analysis.

## Maintenance

Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md),
[LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evergreen.json`.
