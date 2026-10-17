---
name: musicwright
description: "Start here for any music task no sibling clearly owns: make a track, theme, loop, score cue, song or solo with AI (local ACE-Step or MiniMax Music 3 through ComfyUI, or hosted Lyria, ElevenLabs), judge takes the agent cannot hear (spectrogram sheets, loudness numbers, then the listener's verdict), and keep every take's recipe and verdict. Runs mw.py (doctor, gen, sheet, measure, master, loop, join, duck, verdict). Use on 'make me a song', 'a 1 minute flute solo', 'music for my game', 'soundtrack for this video', 'which take is best'. Siblings: musicwright-generate, -compose, -produce, -game, -score, -curate. Also 'refresh musicwright'."
---

# musicwright

The hub for music work. It turns a request into a brief, picks the route, runs the take loop
(render several, look, measure, let a person listen, record the verdict) and hands the finishing
to the right sibling. The siblings hold the depth.

Script: `scripts/mw.py` in this skill folder (Python 3.9+, standard library, ffmpeg on PATH; one
JSON object per command). Run `python <this folder>/scripts/mw.py doctor` once per session: it finds
ffmpeg, ComfyUI hosts and the music models on them, the ACE-Step REST server, librosa and the
studio folder, and lists the recipes that can run here. Commands: [references/cli.md](references/cli.md).

## Step 1: the brief (ask only what you cannot infer)

- **Use**: `game-loop`, `game-cue` (stinger, victory), `film-cue`, `listening`, `song` (vocals).
- **Length** in seconds, and for film the hit times. For loops, bars at a tempo.
- **Sound**: genre, era and production, 3-5 instruments, 2-3 mood words, vocals or instrumental,
  and what must stay out ("no drums", "flute only").
- **References** are described in words, never by naming a living artist or uploading someone
  else's recording (musicwright-compose: references/vocabulary.md shows how).
- **Destination**: where it plays sets the loudness preset and format (musicwright-produce).
- **Licence needs**: commercial game, YouTube, streaming, personal. This narrows the models.

Scaffold: `mw.py new <dir> --name <Name> --use <use> --duration <s>`. Folder: `brief.md`,
`music.json` (the manifest other plugins read, [references/contract.md](references/contract.md)),
`takes/`, `out/`, `sheets/`, `ledger.jsonl` (every take's recipe and every verdict).

## Step 2: route

| Route | When | Owner |
|---|---|---|
| **generate** | audio from a text brief: beds, themes, solos, songs | musicwright-generate |
| **compose** | notes first: motifs, MIDI, ABC or MusicXML, code music, DAW control, theory questions | musicwright-compose |
| **produce** | the audio exists: master, fix loudness, stems, format, QC | musicwright-produce |
| **game** | loops, intro plus loop, layers, stingers, Unity, FMOD or Wwise | musicwright-game |
| **score** | music fitted to a cut: hit points, movements, ducking | musicwright-score |
| **curate** | remember a verdict, taste, lesson or recipe; "what have I learned" | musicwright-curate |

Most requests run generate, then one of produce, game or score.

## Step 3: the take loop (the agent cannot listen)

1. Render several takes, three by default, with recorded seeds: `mw.py gen --recipe <r> --caption ...
   --duration <s> --takes 3 --name <slug> --out <dir>/takes`. The ledger gets one line per take.
   Shared GPU: queue behind other jobs and never cancel someone else's.
2. Look before you report: `mw.py sheet <takes> --out <dir>/sheets/<slug>.png --measure`, then open
   the PNG. Reading it: [references/listening.md](references/listening.md). Check what the
   picture can show: one melodic line or several, drums or none, a drone where none was asked
   for, silence at the end, clipping, a loudness that misses the destination.
3. Report to the listener, ranked: each take's path, what the sheet shows, the numbers, and
   your pick with the reason. Say plainly that you have not heard them. Never write "sounds great".
4. Record what they say: `mw.py verdict <take> keep|reject|maybe --note "<their words>"`. It
   goes to the project ledger and the studio, where musicwright-curate turns verdicts into taste.
5. Re-roll or change one knob at a time (musicwright-generate's cheat-sheet), then finish.

## Step 4: finish and hand over

The chosen take goes to its finishing sibling. Every deliverable lands in `out/` with its
measure numbers, and `music.json` lists it with model, licence, seed and the disclosure line
(musicwright-generate: references/licences.md).

## Step 5: keep what was learned

A verdict, a new preference or a recipe that worked goes to musicwright-curate: never only into
this conversation. The studio folder (`MUSICWRIGHT_HOME`, default `~/.musicwright`) holds taste,
lessons, recipes and every verdict across projects.

## Rules

- The listener decides. Report what the numbers and the picture show and what you could not check.
- Seeds, captions and settings go in the ledger, so any take can be made again.
- No living artist's name in a prompt, even where a model allows it. Describe the sound.
- Pick a model whose licence fits the use before rendering, and say which licence applies.
- One GPU-heavy job at a time on a shared card. Never kill or cancel other jobs, and stop
  processes only by their own PID.
- Install nothing and spend nothing without asking: models, servers and hosted credits are the
  user's to approve.

## Gotchas

- Short renders often go quiet in their last seconds. Render longer than you need, then trim.
- MP3 adds silence at the start and end, which breaks loops. Keep WAV or FLAC until the delivery step.
- High guidance (cfg 7 on ACE-Step XL) sounds harsh to some listeners. The default recipe uses 4.5.
- `mw.py` reports "dynamic" normalisation when a loudness target needs more headroom than the
  file has. Accept the change knowingly, or lower the target.

## References

- [references/cli.md](references/cli.md): every mw.py command and option.
- [references/listening.md](references/listening.md): reading a sheet, the critique checklist, what to tell the listener.
- [references/contract.md](references/contract.md): the project folder, `music.json` and ledger fields for other plugins.
- [references/tools.md](references/tools.md): other skills, MCP servers and DAW bridges, and when to use them.
- [references/recipes.json](references/recipes.json), [references/loudness.json](references/loudness.json): data mw.py reads.

## Maintenance

Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md),
[LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evergreen.json`. Read `evergreen.json` at the
start; if it is past `next_due` or has a contradiction, say so and refresh after the task.
