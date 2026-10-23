# Changelog: musicwright

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261023-4 · 2026-10-23 · 0.1.1: listening-check flags and bug fixes in mw.py; cli and contract corrections
- because: decisions 2026-10-23-listening-checks
- files: scripts/mw.py (hosts, seam, master, new, verdict, gen, analyze), references/cli.md (errors; seam; analyze), references/contract.md (music.json)
- Hosts without a scheme work; seam's level jump uses a median over half a second; master names a custom target and words dynamic mode on a flat source correctly; new checks the preset; verdict refuses a missing file; gen reports filled-in or ignored bpm and key; analyze drops REPEATS and moves TUNING-GAP to 30 cents.

### C-20261023-3 · 2026-10-23 · analyze reports tuning, repetition and sections
- because: decisions 2026-10-23-books-track11; T-20261023-2 (produce, compose)
- files: scripts/mw.py (analyze), references/cli.md (analyze row), references/listening.md (what analyze's numbers mean)
- `analyze` gains tuning against A440 (offset, spread, trend), a gap from the first file, a repetition share, `--sections` (automatic, a count, or tags) and the flags OFF-A440, DRIFT, REPEATS and TUNING-GAP. librosa stays optional.

### C-20261023-2 · 2026-10-23 · One MAINTENANCE.md for the plugin
- because: size budget (installed skills 446 KB, green line 400); decisions 2026-10-23-books-track9 M1
- files: MAINTENANCE.md of compose, curate, game, generate, produce and score
- The six sibling copies were the same pointer template as this one; they now point here and list their own files. This file is unchanged.

### C-20261023-1 · 2026-10-23 · Hand over loudness-matched copies; mixcheck in the look step; new mw.py commands
- because: R-20261023-1 (musicwright-produce), L-003, L-004, T-20261023-1
- files: SKILL.md (Step 3), references/listening.md (Numbers that point at the mix; questions 8-9; Checks a script can add), references/cli.md, references/loudness.json (lra_hint per preset), scripts/mw.py (mixcheck, compare, preview, monobass; mix --shelves, --shelf-hz, --automate; master --peak; doctor checks the new filters), scripts/notation.py (melody_hints), evals/evals.json (action-2)
- The take loop now gives the listener matched copies, because a louder take wins on loudness alone; listening.md explains the mixcheck numbers and replaces a mono rule that would have flagged a mono-safe file measured without dual-mono.

### C-20261017-4 · 2026-10-17 · mw.py: mix, source tasks on the REST route, duck keeps the music length, --out folders
- because: user request (add parts to a kept take); HANDOFF bugs (missing --out folders, duck cut the music to the key's length, REST ignored --cfg/--steps/--set, gen made --out on dry runs); R-20261017-4, R-20261017-5 in musicwright-generate
- files: scripts/mw.py (mix, gen --task/--src/--track/--start/--end/--strength/--model, duck --stem, out_file), references/cli.md (gen, duck, mix rows)
- `mix` layers stems with gain, offset and pan, sums in Python (L-001) and writes aligned stems; `gen` uploads a source for cover, repaint, lego, complete and extract with the planner off; `duck` pads the key so the music keeps its length and `--stem` returns the music alone; master, edit, join, loop, duck and sheet create their output folder; gen validates before creating anything.

### C-20261017-3 · 2026-10-17 · Ranking order for takes judged from sheets
- because: L-002
- files: references/listening.md (Reading an mw.py sheet)
- Rank on excluded parts first, then melody, then the ending; a silent tail is a trim.

### C-20261017-2 · 2026-10-17 · mw.py loop and OGG output made portable across ffmpeg builds
- because: L-001
- files: scripts/mw.py (cmd_loop, out_codec, join)
- The loop crossfade runs on raw float samples in Python; atrim options are named; .ogg falls back to ffmpeg's built-in Vorbis encoder when libvorbis is missing.

### C-20261017-1 · 2026-10-17 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `fast`, interval 14d. See R-20261017-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
