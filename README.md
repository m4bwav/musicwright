# musicwright

![A small white robot setting a wooden music note on a page of handwritten sheet music, beside a wooden flute, black headphones, a colourful pad controller and a laptop showing a colourful spectrogram, on a sunlit wooden desk with studio speakers and a plant](https://raw.githubusercontent.com/m4bwav/musicwright/main/.github/images/banner.jpg)

Seven self-maintaining ("evergreen") skills and one command-line tool that let an AI agent make music with you:
generate it with local or hosted AI models, judge takes it cannot hear, finish them to the right loudness, cut
seamless game loops, fit a score to a film cut, and remember what you liked. Written 2026-10-17 for Claude Code,
GitHub Copilot, Cursor and Codex, from a research pass on AI music models and licences, the agent tools people use
for music, and music fundamentals, whose dated notes are in [ai-docs/research](ai-docs/research/index.md).

You stay the author. musicwright sketches, renders, measures and organises; you listen and decide.

## What it does

Ask for music and the hub skill writes a brief, picks a route, and runs the take loop:

1. **Render several takes** with recorded seeds: ACE-Step 1.5 XL or MiniMax Music 3 on your own ComfyUI, the
   ACE-Step REST server for fast drafts, or a hosted API (Lyria, ElevenLabs) when you approve the cost.
2. **Look, because it cannot listen**: one spectrogram contact sheet for all takes, plus loudness, peaks and
   silences for each. The agent ranks them on what the picture and numbers show and says what it could not check.
3. **You listen and give a verdict**, which goes into the project ledger and your private studio, so the next brief
   starts from your taste.
4. **Finish**: master to a destination (streaming, game, web video, broadcast), cut a bar-exact loop with a
   checked seam, or join movements on a film's hit points and duck them under dialogue.
5. **Notes in, notes out**: play ABC, guitar or bass tab, MusicXML or MIDI as audio, convert between them, and
   transcribe a recording into MIDI, ABC, MusicXML or tab (`mw.py render`, `notate`, `transcribe`).

A real example, "a 1 minute flute solo, no other instruments", three takes of ACE-Step 1.5 XL on a 16 GB GPU:

![Three spectrogram and waveform rows, one per take: the top take has a wide low band under the flute from about a third of the way in, the middle take goes dark for its last third, the bottom take shows a single clean melodic line with breaths between phrases](https://raw.githubusercontent.com/m4bwav/musicwright/main/.github/images/demo-flute-sheet.jpg)

The sheet showed what a text reply would have hidden: the first take slipped a drone under the flute, the second
went silent for its last 19 seconds, the third is one clean melodic line. The third is in
[.github/samples](.github/samples/flute-solo-s63389.mp3) (ACE-Step 1.5 XL, MIT, seed 63389).

## The skills

| Skill | Job | Tier |
|---|---|---|
| [`musicwright`](skills/musicwright/SKILL.md) | The hub: brief, route, the take loop, the project folder and ledger, and `mw.py` | fast |
| [`musicwright-generate`](skills/musicwright-generate/SKILL.md) | Which model for which job and licence, captions and section tags, fishing with seeds, fixing harsh or off-brief takes, long pieces from movements | fast |
| [`musicwright-compose`](skills/musicwright-compose/SKILL.md) | Theory for prompting and judging: modes, world scales, progressions, tempo, form, motifs, ranges; caption vocabulary; MIDI, ABC, MusicXML, code music and DAW bridges; notation and tabs played as audio, recordings transcribed to notes | moderate |
| [`musicwright-produce`](skills/musicwright-produce/SKILL.md) | Loudness targets with sources, two-pass mastering, formats, clipping and silence checks, mixing rules, stems | moderate |
| [`musicwright-game`](skills/musicwright-game/SKILL.md) | Seamless loops, intro then loop, layers, stingers, Unity import and scheduling, FMOD and Wwise, Steam disclosure | moderate |
| [`musicwright-score`](skills/musicwright-score/SKILL.md) | Scoring to picture: spotting, tempo for hits, movements joined on hit points, ducking, temp tracks | moderate |
| [`musicwright-curate`](skills/musicwright-curate/SKILL.md) | Your verdicts, taste profile, lessons and proven recipes, kept in a private studio; general lessons promoted into the skills | slow |

Each skill folder holds `SKILL.md` plus its evergreen companions: `RESEARCH.md` (dated findings and a four-track
search plan), `CHANGELOG.md`, `LEARNINGS.md`, `TESTS.md` with `evals/evals.json`, `MAINTENANCE.md` and
`evergreen.json` (tier, due date, history). The skills follow whichever evergreen plugin is installed
([evergreen-protocol](https://github.com/m4bwav/evergreen-protocol)) and work without it.

## mw.py

`skills/musicwright/scripts/mw.py` is standard-library Python 3.9+ on top of ffmpeg. It prints one JSON object
per command, so an agent reads numbers instead of ffmpeg logs.

```
python mw.py doctor                                   # ffmpeg, ComfyUI hosts and their music models, ACE-Step REST, recipes that can run
python mw.py new music/menu --name "Main menu" --use game-loop --duration 150
python mw.py gen --caption "warm melodic electronica, ..." --duration 150 --bpm 96 --key "D major" --takes 3 --name menu --out music/menu/takes
python mw.py sheet music/menu/takes/*.flac --out music/menu/sheets/menu.png --measure
python mw.py verdict music/menu/takes/menu_s4021.flac keep --note "bright, not tiring"
python mw.py loop music/menu/takes/menu_s4021.flac --start 8 --bars 32 --bpm 96 --out music/menu/out/menu_loop.wav --ogg
python mw.py master music/menu/out/menu_loop.wav --preset game-music --out music/menu/out/menu_loop_master.wav
python mw.py join m1.flac m2.flac m3.flac --lengths 24,10,12 --xfade 2 --out score.wav
python mw.py duck score.wav --under cut.mp4 --out cut_scored.mp4
python mw.py render riff.txt --bpm 100 --out riff.wav        # ASCII tab, ABC, MusicXML or MIDI to audio
python mw.py transcribe solo.flac --out solo.mid --to abc,musicxml --lowest C4 --highest A5
python mw.py pulse solo.flac                                 # is there a beat to put percussion on?
```

Full list: [skills/musicwright/references/cli.md](skills/musicwright/references/cli.md). The contract other
plugins use (folder layout, `music.json`, ledger): [contract.md](skills/musicwright/references/contract.md).

## Install

The skills install nothing and spend nothing on their own. ffmpeg, ComfyUI and its model weights, the ACE-Step
server, FluidSynth and a SoundFont, librosa or basic-pitch for transcription, hosted APIs and DAW bridges are yours to install or pay for; `mw.py doctor` says what is missing.

As a Claude Code plugin:

    /plugin marketplace add m4bwav/musicwright
    /plugin install musicwright@musicwright

As plain skills for any agent that reads Agent Skills, clone the repository and link every folder under `skills/`
into the agent's skills directory. Keep all seven together, because the siblings use the hub's `scripts/`.

    git clone https://github.com/m4bwav/musicwright
    # Windows (junctions need no admin rights)
    foreach ($s in Get-ChildItem musicwright\skills -Directory) { New-Item -ItemType Junction -Path "$HOME\.claude\skills\$($s.Name)" -Target $s.FullName }
    # macOS / Linux
    for s in musicwright/skills/*/; do ln -s "$PWD/$s" ~/.claude/skills/; done

Needs: Python 3.9+ and ffmpeg. For generating: ComfyUI with ACE-Step 1.5 XL (or MiniMax Music 3) weights, or the
ACE-Step REST server. Optional: librosa for tempo and key (`mw.py analyze` prints a one-line `uv run` that needs
no install). Hosts: `MUSICWRIGHT_COMFYUI` and `MUSICWRIGHT_ACESTEP`, or `config.json` in your studio
(`MUSICWRIGHT_HOME`, default `~/.musicwright`).

## Verified (2026-10-17, Windows 11, ffmpeg 9.0.1, ComfyUI 0.38.2, RTX 5060 Ti 16 GB)

From real runs, not from a model's say-so:

- The flute run above: three 60 s ACE-Step 1.5 XL takes through ComfyUI, measured and sheeted by `mw.py`.
- `mw.py master` took a -15.7 LUFS take to -14.1 LUFS and -1.0 dBTP, and reported that loudnorm had to switch to
  dynamic mode.
- `mw.py loop --bars 8 --bpm 66` produced exactly 29.0909 s with a seam ratio of 0.04 (clean) and OGG loop tags
  that read back.
- The research agents tested the ffmpeg recipes in `musicwright-produce` on generated signals: loudness, clipping
  detection, MP3 padding (+1,728 samples without the gapless tag), the crossfaded loop and its seam check.
- `tests/test_mw.py` runs every command on synthetic audio in CI on Linux, macOS and Windows.

Not verified yet: YuE2, Stable Audio 3 and MiniMax Music 3 timings with recorded settings; the ACE-Step REST cover,
repaint and extract tasks; hosted APIs; agent evals run three times per case. Details in each skill's TESTS.md.

## Testing

CI (`.github/workflows/tests.yml`) on Linux, macOS and Windows: `tests/check_skills.py` (frontmatter, description
limits, companions, manifests, relative links, public-safety guards), `tests/test_mw.py` (every command on
synthetic audio, no network), and `scripts/budget.py` (what every session loads and the installed size stay green).

## Privacy

musicwright has no server and collects nothing. `mw.py` runs on your machine and only talks to the network when a
command needs it: `gen` and `doctor` talk to the ComfyUI hosts and the ACE-Step server you configure (default
localhost). Hosted APIs are only called when you ask and approve. Your verdicts and taste notes stay in your studio
folder.

## If you are an agent asked to analyse this suite

Read, roughly in order: `skills/musicwright/SKILL.md` (routing and the take loop), `skills/*/SKILL.md`,
`skills/*/RESEARCH.md` (dated sources), `skills/musicwright/references/recipes.json` and `loudness.json` (data with
sources), and `tests/`. The rule running through all of it: the agent cannot hear, so it reports what numbers and
a picture show and lets a person decide. Repository rules: [AGENTS.md](AGENTS.md).

License: MIT. Security: [SECURITY.md](SECURITY.md). The banner was made with ComfyUI; its prompt and seed are in
`.github/images/`. The sample is AI-generated with ACE-Step 1.5 XL (MIT).
