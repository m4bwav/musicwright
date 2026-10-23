---
name: musicwright-game
description: "Use for the game side of music: seamless loops (bar-exact length, tail crossfaded into the head, seam check), intro-then-loop, vertical layers and stems, stingers, cue lists (from a level plan or beat chart), menu, map, combat and boss conventions, fatigue in long sessions, Unity AudioClip import (Streaming, Vorbis, PlayScheduled), OGG loop tags, FMOD and Wwise basics, Steam's AI disclosure. Runs mw.py loop and seam. Use on 'make this loop seamless', 'combat music with layers', 'import music into Unity', 'why does my loop click', 'intro then loop'. A new piece of game music from a brief starts at musicwright; generating audio is musicwright-generate. Also 'refresh musicwright-game'."
---

# musicwright-game

Music that plays for hours behind a game: it must loop without a seam, leave room for sound
effects, not tire the player, and import cleanly. Script: `mw.py` in the musicwright hub.

## Step 1: plan the set

- When the game has a level plan (a beat chart with one column per level, a `LEVEL-PLAN.md` from
  madnesswright-scenes, a design one-pager), build the cue list from it, not from genre defaults:
  its music row gives the track per area in play order, its big and small moments set the
  intensity, a new enemy's first room gets a warning cue, a rest room gets silence or a rest cue.
  Read across the row and flag the same track in two neighbouring areas, and any area long enough
  to tire of that has one track only. Rules: adaptive.md "Cues from the level plan".
- With no plan, list the cues by game state: menu, map or deck building, combat, boss, shop or
  rest, victory, defeat, stingers. Lengths and conventions: [references/adaptive.md](references/adaptive.md).
- A turn-based or card game runs for hours: fatigue is the enemy. Prefer 2-4 min loops with A/B
  variation, several tracks per area, no hook every 20 s, a sparse 1-4 kHz range for SFX, and
  silence between fights.
- One main theme reused across menu, map, boss and victory (different tempo, mode, instruments)
  makes the set feel authored. Keep the motif's notes in the brief (musicwright-compose).
- Decide the tempo and bars per loop now. Loop length in seconds = bars x beats per bar x 60 / bpm
  (at 96 bpm in 4/4, 32 bars = 80 s).

## Step 2: generate for looping

Ask musicwright-generate for a take at the planned bpm and key, longer than the loop (loop
length + 10-20 s): a steady caption with no intro or ending words ("steady loop, no intro, no
ending", never "epic finale"), WAV or FLAC only.

## Step 3: cut the loop

`mw.py loop <take> --start <s> --bars <N> --bpm <bpm> --xfade 1.5 --out out/<name>_loop.wav [--ogg]`

- `--start` past any intro swell, on a downbeat if you can find one (look at the sheet; the
  spacing of drum stripes gives the beat).
- The tail after the loop end is crossfaded into the head, so reverb tails carry over instead
  of cutting off. The result is exactly N bars.
- Read `seam`: ratio about 1 or less and level jump under 3 dB is "clean"; "audible seam likely"
  means another start point, a longer crossfade, or another take.
- The loop must also flow musically (the last bar leads back to the first chord). Only a person
  can judge that: ask them to play it three times through and listen at the seams.
- Master after looping, to the `game-music` preset, so every track in the game sits at one level:
  `mw.py master out/<name>_loop.wav --preset game-music --out out/<name>_loop_master.wav`. Re-run
  `mw.py seam` on the mastered file.

Full method, intro plus loop, and layers: [references/loops.md](references/loops.md).

## Step 4: into the engine

Unity: [references/unity.md](references/unity.md) (Streaming + Vorbis for music, Loop on the
AudioSource, intro then loop with two sources and `PlayScheduled`). Unity ignores OGG loop
tags; they still document the loop for other engines (RPG Maker reads them). FMOD and Wwise:
adaptive.md.

## Step 5: record and disclose

Each deliverable goes into `music.json` with its loop data (bars, bpm, length) and model. Steam's
Content Survey covers AI-made sound that ships with the game: put the disclosure line from
musicwright-generate's references/licences.md on the store page.

## Rules

- No MP3 anywhere in the loop chain: its padding adds a gap.
- No fades or silence inside a loop file.
- Every music file of one game at one loudness; balance against SFX in the engine mixer.
- Layers of one piece share length, tempo and key: render them from one take (stems) or one
  seed, never from separate unrelated renders.

## References

- [references/loops.md](references/loops.md): loop math, crossfade method, seam check, intro plus loop, layers from stems.
- [references/unity.md](references/unity.md): import settings, looping, PlayScheduled stitching, mixer snapshots.
- [references/adaptive.md](references/adaptive.md): cue list and lengths, cues from a level plan, horizontal and vertical techniques, FMOD and Wwise terms.

## Maintenance

Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md),
[LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evergreen.json`.
