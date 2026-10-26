# Handoff

State on 2026-10-25: 0.1.2 released (the four wiki-verification fixes from #13); wiki republished at 0.1.2 (wiki commit ce0d323, verified on Windows and on Linux with the static ffmpeg 7.0.2 build, where mixcheck and compare now pass).

Candidates for 0.1.3, found by the wiki run: (1) the padded retry on ffmpeg 7.0.2 measures the padding too (a 3.5 s 44.1 kHz file read -9.1 LUFS against -8.9 unpadded on 9.0.1); take loudness from the unpadded file. (2) `mixcheck` `duration_s` counts whole-second blocks (4 for 3.5 s). (3) `pulse` still prints `tempo_bpm` and grid numbers beside `none`; null or label them. Earlier state follows below.

## Listening checks and 0.1.1 (2026-10-23)

- Four blind pairs judged by the owner: REPEATS dropped as a flag (share still reported), TUNING-GAP over 30 cents, BRIGHT is a fatigue pointer, density section tags not shown to help. Rulings P1-P5 and the bug fixes: [decisions/2026-10-23-listening-checks.md](decisions/2026-10-23-listening-checks.md). The old item 7 bug list is fixed (92 tests, ten mutations caught).
- Release: tag `v0.1.1` runs release.yml. Then republish the wiki (item 5) and reinstall the plugin.

## Books track 11 (2026-10-23)

- `mw.py analyze`: tuning (offset, spread, trend, gap from the first file), repetition share, `--sections`; flags OFF-A440, DRIFT, REPEATS, TUNING-GAP. librosa stays optional and CI skips these tests. Rulings N1-N9: [decisions/2026-10-23-books-track11.md](decisions/2026-10-23-books-track11.md). Listener verdicts: see the section above. Installed skills 433 KB (yellow).

## Books track 9 (2026-10-23)

- musicwright-game builds its cue list from a beat chart or LEVEL-PLAN.md and adaptive.md has four new cue types and rules after Rogers, *Level Up!*; six MAINTENANCE.md files point at the hub's. Rulings M1-M6 and what was not built (`mw.py cues`): [decisions/2026-10-23-books-track9.md](decisions/2026-10-23-books-track9.md). Evals T-20261023-1 in the game TESTS.md (outcome-2 3/3, baseline 0/3).

## Books track 8 (2026-10-23)

- Built on branch books-8: `mw.py mixcheck`, `compare`, `preview` (matched, `--blind`, `--as phone|quiet`), `monobass`; `mix --shelves --shelf-hz --automate`; `master --peak`; `lra_hint` per preset; melody hints in `render --check`; prose in produce, hub, compose, generate, curate, game and score. Rulings K1-K11 and what was not built: [decisions/2026-10-23-books-track8.md](decisions/2026-10-23-books-track8.md).
- Calibration: 78 real AI renders on the owner's machine (mix flags fire on 1% to 18%; 43 raise none), the three judged flute takes (BELOW-RANGE separates the rejected one by 21 dB), 18 public-domain tunes against six random walks (melody flags 0/18 and 6/6). Rates are in musicwright-produce references/mixing.md and compose references/theory.md.
- Not built: a dynamic-EQ harshness repair, sibilance spikes, kick-bass onset coincidence, a codec-ceiling flag. Each needs material or labels this machine does not have yet.
- Evals T-20261023-1 (produce, hub, compose, generate TESTS.md): run action baselines in a folder holding only the fixtures, since a baseline in a clone finds mw.py. Density tags and BRIGHT were judged by ear on 2026-10-23 (above). Research: [research/index.md](research/index.md).

## Done

- Public repository m4bwav/musicwright: seven skills with references, evergreen companions and eval suites; mw.py with 15 commands; 49 unit tests on synthetic audio and a fake ComfyUI and ACE-Step server; check_skills.py and budget.py green; CI green on Linux, macOS and Windows (Python 3.9 and 3.14); release workflow; dependabot; secret scanning and push protection.
- Real runs: three ACE-Step XL flute takes sheeted and measured; master, loop with OGG tags and seam on real audio.
- Agent evals: T-20261017-1 40/42 over all seven skills, T-20261017-2 24/24 on hub, generate, game and compose after the routing fix.

## Owed

1. Evals: baselines without the plugin, three runs per case, and a re-run of the generate action case with its new prompt (it no longer names the plugin). The compose and generate suites changed on 2026-10-18 (compose trigger-3, trigger-4, action-2); see their TESTS.md for the run after the plugin was reinstalled.
2. Not yet run on real hardware: the MiniMax Music 3 and REST recipes through `mw.py gen`, REST cover, repaint and extract, YuE2 and Stable Audio 3 (download, measure VRAM and time; add recipes only after a listener keeps a take).
3. `mw.py gen --collect` for `--no-wait` jobs: needs the queued recipe saved (a ledger row with status queued) so collected takes are measured and logged.
4. A loudness-curve fit for film cues and an optional learned quality score: open questions in the hub's RESEARCH.md.
5. Wiki: republished for 0.1.1 on 2026-10-23 (wiki commit e35cc91, 17 pages, live check clean; every example rerun on Windows and on Linux under WSL 2 against tag v0.1.1). The four bugs that run found (mixcheck/compare abort on static ffmpeg 7.0.2, seam on a downbeat loop, pulse on a swelling tone, the 420 KB claim) are fixed under Unreleased (log 2026-10-23, L-005); the wiki's Errors page still describes them until 0.1.2 ships. Next release: rerun the verification and republish with the publish script in the owner's private notes (wiki-build/publish.sh).
6. v0.1.0 released 2026-10-17; 0.1.1 carries tracks 8, 9, 11, the listening checks and the old item 7 bug list. Bump plugin.json, mw.py VERSION and CHANGELOG.md together.

## Notation (2026-10-18)

- `mw.py render` (ABC, ASCII tab, MusicXML, MIDI to MIDI and audio; FluidSynth and a SoundFont when found, else a built-in sketch synth; `--check` lists bars that do not add up), `mw.py notate` (between ABC, MusicXML, MIDI and tab), `mw.py transcribe` (librosa pyin or basic-pitch; level gate and range filter). Readers and writers are stdlib in `scripts/notation.py`. musicwright-compose owns the route (Step 4, references/notation.md, R-20261018-1, L-001). Tests: 71, green on Python 3.9 and 3.14 locally.
- Verified here: FluidSynth 2.6.1 Windows zip with GeneralUser GS renders ABC, tab and transcriptions; basic-pitch runs only through `uv tool run --python 3.11 --from basic-pitch --with "numpy<2" --with "setuptools<81"` and needs PYTHONIOENCODING=utf-8 on Windows (mw.py sets it); pyin and basic-pitch agreed on 72% of frames on a solo flute take.
- Not yet done: the cover-for-realism route (render, then ACE-Step cover at 0.5-0.9) has not been run on hardware; Guitar Pro files are not read (export MusicXML from MuseScore or TuxGuitar); MuseScore CLI export is unverified here.

## Next steps

Start from INDEX.md, or paste [next-session-prompt.md](next-session-prompt.md). Run `python tests/check_skills.py`, `python tests/test_mw.py`, `python scripts/budget.py` before every commit; work through pull requests on main and merge your own once CI is green.
