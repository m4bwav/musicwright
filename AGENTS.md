# Agent rules for musicwright

Rules for any AI agent (Claude Code, Copilot, Cursor, Codex, Gemini CLI) working in this repository. `CLAUDE.md` imports this file and `.github/copilot-instructions.md` points here.

Read [README.md](README.md) first. The seven skills live under [skills/](skills/); the hub is `skills/musicwright`, which also holds the CLI (`scripts/mw.py`), the generation recipes (`references/recipes.json`) and the loudness presets (`references/loudness.json`). Each skill is an evergreen unit with its companions beside it: RESEARCH, CHANGELOG, LEARNINGS, TESTS, `evals/evals.json`, MAINTENANCE and `evergreen.json`. The first research pass is in [ai-docs/research/](ai-docs/research/).

## Rules

- Evergreen units in pointer mode: before editing a skill, read its `evergreen.json`. If `next_due` has passed or `contradiction` is set, say so and refresh after the task (the evergreen plugin's `evergreen-refresh`, otherwise the skill's `MAINTENANCE.md`). Every edit to a SKILL.md gets a CHANGELOG entry with its reason (`R-`, `L-` or `T-` ids, or "user request"). Re-run that skill's `evals/evals.json` (evergreen-test) when the change alters what the skill triggers on, decides or does.
- Research beats recall. Music models, their licences and node names, hosted prices and terms, store disclosure rules and loudness targets move monthly. Never change a model name, version, licence, price, ComfyUI node or loudness number from memory: cite the source in the skill's RESEARCH.md (an `R-` entry) and log the change in CHANGELOG.md.
- `mw.py` stays standard-library Python 3.9+, prints exactly one JSON object per command, fails soft (`ok: false` with `error`), and runs on Windows, macOS and Linux. It needs ffmpeg and ffprobe for audio work; `analyze` alone may use librosa, and prints the one-liner that runs it when librosa is missing. Every new command or option gets a test in `tests/test_mw.py`.
- Recipes go into `skills/musicwright/references/recipes.json` only after a listener kept a take made with them, and each recipe's `source` says which run and when. A recipe nobody has judged says so in its `source`.
- Loudness presets live in `skills/musicwright/references/loudness.json`; change a number only with a source, and keep each `note` saying where it came from.
- The agent cannot listen. Spectrogram sheets and loudness numbers rule takes out (silence, clipping, a render that went quiet); only a listener's verdict says a take is good. Never write that a take sounds good, and never promote a recipe on numbers alone.
- Never name a living artist, band or composer in a prompt, caption, recipe or example; describe the style in words (instruments, tempo, era, production). Never upload someone else's recording as a reference without the user saying they hold the rights.
- Skills stay under 200 lines, with a description of at most 1,024 characters (Agent Skills spec; this repository's budget is 700) that says what the skill does and names the sibling that owns nearby requests.
- The skills install nothing on their own and spend nothing: ffmpeg, ComfyUI, model weights, the ACE-Step REST server, librosa, hosted generators and DAW or notation MCP servers are the user's to install, download or pay for, after being told what each is for and what it costs.
- Before committing, run from the repository root: `python tests/check_skills.py` (structure, companions, manifests, links, public-safety guards), `python tests/test_mw.py` (skips when ffmpeg is not on PATH) and `python scripts/budget.py`. CI runs them on three operating systems with ffmpeg installed.
- Size budget: `scripts/budget.py` sets green, yellow and red limits on what every session loads (descriptions) and on the installed size. Red fails CI. Say so when a change crosses yellow.
- This is a public repository. Nothing in it names a person other than the author credit, a private project, a machine or its LAN address, an absolute path on someone's machine, or a credential. A lesson learned on a particular machine or project is generalised here ("a 16 GB card", "a game's combat loop"); the specifics belong in the owner's private notes, never in a commit. The studio (`MUSICWRIGHT_HOME`, default `~/.musicwright`) holds a listener's verdicts and taste and never enters the repository. `tests/check_skills.py` guards home-folder paths, the owner's own paths and private network addresses.
- Versions: when a packaged file changes, bump `.claude-plugin/plugin.json`, `VERSION` in `mw.py` and the root CHANGELOG.md, and tag `vX.Y.Z`. The release workflow checks the tag against the manifest, runs the checks, zips `skills/` and publishes a GitHub release.
- Work on `main` through pull requests; delete merged branches.
- No AI attribution anywhere: no Co-Authored-By trailers and no "generated with" lines in commits, pull requests or files.

## everlast (session knowledge, load on demand)

- `ai-docs/INDEX.md` lists what past sessions learned here. At the start of a task, scan it and open only the entries that match; read `ai-docs/HANDOFF.md` when continuing unfinished work.
- Before finishing a task that hit a dead end, verified a non-obvious command or made a design choice, record it in `ai-docs/` and rewrite `HANDOFF.md` when work is left unfinished. Say "nothing to record" when that is true.
- Anything naming a person, an internal host or name, a credential, or an opinion about people goes to the owner's private notes, never here.
- Link documents with relative markdown links. Every markdown folder has an index that links its files. No wikilinks in the repository.
