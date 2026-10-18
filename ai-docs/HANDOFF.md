# Handoff

State on 2026-10-18, end of the layers-2 and notation session.

## Done

- Public repository m4bwav/musicwright: seven skills with references, evergreen companions and eval suites; mw.py with 15 commands; 49 unit tests on synthetic audio and a fake ComfyUI and ACE-Step server; check_skills.py and budget.py green; CI green on Linux, macOS and Windows (Python 3.9 and 3.14); release workflow; dependabot; secret scanning and push protection.
- Research pass in ai-docs/research (models and licences, agent tools, fundamentals).
- Real runs: three ACE-Step XL flute takes sheeted and measured; master, loop with OGG tags and seam on real audio.
- Agent evals: T-20261017-1 40/42 over all seven skills, T-20261017-2 24/24 on hub, generate, game and compose after the routing fix.

## Owed

1. Evals: baselines without the plugin, three runs per case, and a re-run of the generate action case with its new prompt (it no longer names the plugin). The compose and generate suites changed on 2026-10-18 (compose trigger-3, trigger-4, action-2); see their TESTS.md for the run after the plugin was reinstalled.
2. Not yet run on real hardware: the MiniMax Music 3 and REST recipes through `mw.py gen`, REST cover, repaint and extract, YuE2 and Stable Audio 3 (download, measure VRAM and time; add recipes only after a listener keeps a take).
3. `mw.py gen --collect` for `--no-wait` jobs: needs the queued recipe saved (a ledger row with status queued) so collected takes are measured and logged.
4. A loudness-curve fit for film cues and an optional learned quality score: open questions in the hub's RESEARCH.md.
5. Wiki: live since 2026-10-17 (17 pages, sidebar, footer, every example verified on Windows and Linux against main 62231a9). After the bug fixes below, re-run the verification and republish with the publish script kept in the owner's private notes (wiki-build/publish.sh).
7. Bugs found while verifying the wiki (fix with tests, one PR):
   - master, edit, join, loop and duck fail with a raw ffmpeg error when the --out folder does not exist (sheet, new and gen create it).
   - duck cuts the music to the length of --under and returns the mix, not a music stem; add a --stem or keep-length option and say which it returns.
   - master's "dynamic" warning blames peaks even when loudnorm went dynamic because the measured LRA was 0 (steady tones and drones).
   - gen sends 90 bpm and C major when --bpm/--key are omitted, against the brief's "leave to the model"; minimax-music3 ignores --bpm/--key and acestep-rest ignores --cfg/--steps/--sampler/--scheduler/--shift/--planner/--set without saying so.
   - new accepts an unknown --preset; master --lufs/--tp without --preset reports "streaming"; gen creates --out before validating, leaving empty folders on dry or failed runs.
   - verdict accepts a missing file and, for a take gen never logged, records the name with its extension so ledger never matches it.
   - seam's level jump uses the first and last 50 ms, so a loop starting on a drum hit reads "check by ear" with a smooth seam.
   - Docs: cli.md and the game skill say a seam ratio of "about 1 or less" is clean while the code says up to 2; argument errors exit 2 with usage on stderr, not JSON; contract.md omits music.json's `created`.
6. v0.1.0 released 2026-10-17. The next release (0.1.1) should carry the bug fixes in item 7; bump plugin.json, mw.py VERSION and CHANGELOG.md together.

## Layers (2026-10-17/18, done)

- PR #5: `mw.py mix`, `gen --task lego|complete|extract|cover|repaint`, `duck --stem`, `--out` folders, `dcw_enabled: false` for base-only tasks.
- Branch `layers-2`: R-20261017-6 written (DCW, base against XL, percussion invents its grid), L-001 in generate and produce, the REST reference names the server version and VRAM per model, generate Step 5 (add a part: pulse, lego, duck --stem, mix), recipe `acestep-rest-lego` (a listener kept the 2B base seed 8101 mix, the ducked one best), `mw.py pulse` and `mw.py answer` with tests.
- Stage 3 (percussion over the kept stage-2 mix) is built and waits for the listener; the percussion takes had no pulse to follow, so a tempo-locked re-render of the lead is the better route if the listener wants a beat.

## Notation (2026-10-18)

- `mw.py render` (ABC, ASCII tab, MusicXML, MIDI to MIDI and audio; FluidSynth and a SoundFont when found, else a built-in sketch synth; `--check` lists bars that do not add up), `mw.py notate` (between ABC, MusicXML, MIDI and tab), `mw.py transcribe` (librosa pyin or basic-pitch; level gate and range filter). Readers and writers are stdlib in `scripts/notation.py`. musicwright-compose owns the route (Step 4, references/notation.md, R-20261018-1, L-001). Tests: 71, green on Python 3.9 and 3.14 locally.
- Verified here: FluidSynth 2.6.1 Windows zip with GeneralUser GS renders ABC, tab and transcriptions; basic-pitch runs only through `uv tool run --python 3.11 --from basic-pitch --with "numpy<2" --with "setuptools<81"` and needs PYTHONIOENCODING=utf-8 on Windows (mw.py sets it); pyin and basic-pitch agreed on 72% of frames on a solo flute take.
- Not yet done: the cover-for-realism route (render, then ACE-Step cover at 0.5-0.9) has not been run on hardware; Guitar Pro files are not read (export MusicXML from MuseScore or TuxGuitar); MuseScore CLI export is unverified here.
- Size: tracked repository 2082 KB, over the 2048 KB green line (yellow); installed skills 390 KB of a 400 KB green line. The next addition that grows the installed size should trim something first.

## Next steps

Start from INDEX.md, or paste [next-session-prompt.md](next-session-prompt.md). Run `python tests/check_skills.py`, `python tests/test_mw.py`, `python scripts/budget.py` before every commit; work through pull requests on main and merge your own once CI is green.
