# Log

Append-only. Newest last.

## 2026-10-17

- Owner's request: an evergreen music plugin that researches AI music making and music making in general, the skills and plugins people use and which models do what, and centralises everything already learned and still to learn about music. Then: a public repo with the full set-up (CI, release workflow, SECURITY.md, banner, wiki).
- Started from a one-minute solo flute request: three ACE-Step 1.5 XL takes rendered through ComfyUI; spectrograms showed one take with a low drone under the flute and one with a 19 s silent tail. That run became the first test of `mw.py sheet` and `measure`.
- Four research agents: an inventory of the owner's existing music work (kept private), models and licences (research 01), agent tools and workflows (02), music fundamentals with tested ffmpeg recipes (03). Originals with machine details are in the owner's private notes; the repository copies are generalised.
- Corrections the research forced on earlier notes: ACE-Step 1.5 is MIT (not Apache 2.0); MiniMax Music 3 is open weights under its own community licence (not CC BY-NC); YuE2 and Stable Audio 3 have native ComfyUI nodes.
- Named it musicwright (songwright and tunewright are taken). Design: decisions/2026-10-17-hub-studio-and-take-loop.md.
- Built mw.py (doctor, new, gen, measure, sheet, master, edit, join, loop, seam, duck, analyze, verdict, ledger, note), seven skills with references, evergreen companions and eval suites.
- Verified on real takes: master to -14 LUFS landed at -14.1 / -1.0 dBTP (loudnorm fell back to dynamic and mw.py said so); an 8-bar loop at 66 bpm came out at exactly 29.0909 s with seam ratio 0.04; OGG loop tags written and read back.
- Banner: Z-Image Turbo on ComfyUI, 1536x640, seed 101 of four candidates (101, 202, 303, 404; the others had duplicated headphones or a robot hand with no body). Workflow and prompt in .github/images.
- Repository infrastructure modelled on polywright: plugin and marketplace manifests, AGENTS.md (CLAUDE.md imports it), LICENSE, SECURITY.md, .gitignore, .gitattributes, root CHANGELOG, dependabot, tests and release workflows (ffmpeg from apt, Homebrew and Chocolatey; an analyze job with librosa), `tests/check_skills.py` (adds recipe and preset checks, a LAN-address guard, and allows the owner handle only as the GitHub `m4bwav/` slug), `tests/test_mw.py` (49 tests on synthetic ffmpeg audio, `gen` against a fake local ComfyUI and ACE-Step host) and `scripts/budget.py` (all descriptions green at 7 x 700 characters). No check_discovery.py: ffmpeg is found on PATH or by MUSICWRIGHT_FFMPEG, which test_mw.py covers.
- mw.py bugs the tests found and fixed: `Path.write_text(newline=)` broke `new` and `note` on Python 3.9 (now `write_lf`); `loop --out x.ogg --ogg` re-encoded the file onto itself (tags now go in the first pass); an `ok: false` result such as `analyze` without librosa exited 0 although references/cli.md promises exit 1; the `--no-wait` hint named a `gen --collect` option that does not exist (the hint now says what is true; adding `--collect` is open).
- Repository: public m4bwav/musicwright with CI (Linux, macOS, Windows; Python 3.9 and 3.14), release workflow, dependabot, secret scanning and push protection, wiki enabled. Installed locally as musicwright@mark-local.
- CI caught ffmpeg portability bugs Windows hid (PR #1): positional atrim arguments, amix/concat behaviour on ffmpeg 6.1, no libvorbis in Homebrew. The loop crossfade now runs on raw float samples in Python (L-001).
- Agent evals, headless claude -p, one fresh run per case: T-20261017-1 40/42 (the hub's two triggers went to generate and game; every decoy passed; every action case ran its real command); after sharper generate and game descriptions, T-20261017-2 24/24 on hub, generate, game and compose. A guard refused generation scripts and ComfyUI posts during the runs; one decoy in the first pass still rendered two images through the user's own image skill before the guard was widened. The harness is kept in the owner's private notes.
- Wiki published (17 pages) after the owner saved its first page; every example was run on Windows and Linux first. The verification found ten mw.py bugs and three doc mismatches, listed in HANDOFF.md.
- The owner retired the earlier private acestep-music and comfyui-music skills in favour of musicwright; pointers now send music work here from the image-generation plugin and the owner's game project.
- First listener verdicts on the flute takes: the take the sheet flagged for a low drone was rejected ("bass a flute can't make"); the preferred take was one the sheet had ranked second for its silent tail. Recorded as L-002.
- Released v0.1.0 on the owner's go-ahead.

## 2026-10-18

- Listener verdicts on the stage-2 layering mixes: the 2B base lego seed 8101 kept, the ducked mix best overall and the plain one liked; seed 8303 ducked slightly over plain, both below 8101. Recorded with `mw.py verdict --by`; recipe `acestep-rest-lego` added from the kept take.
- Stage 3 built: the kept mix plus a percussion lego take at -8 and -12 dB, and the plain mix at -8 dB. Sheets show no clipping or dropouts. Not yet heard.
- Wrote up the layers findings (R-20261017-6, L-001 in generate and produce, REST server version and VRAM, generate Step 5) and added `mw.py pulse` and `mw.py answer`, which reproduced last session's hand measurements on the real takes (the solo reads no pulse; the 66 bpm percussion take reads steady at 66.3; ducking moved the kept part 4.4 dB toward the lead's rests).
- Owner's request: feed musicwright notation or tabs and get music, and the reverse. A research pass (R-20261018-1 in compose) found no maintained Python tab parser and no MIDI input on ACE-Step, so the readers and writers were written in stdlib Python (`scripts/notation.py`) behind `render`, `notate` and `transcribe`, with FluidSynth, SoundFonts, librosa and basic-pitch as the user's optional tools. Kept in musicwright-compose instead of an eighth skill to hold the always-loaded description budget.
- Bugs caught on real files before commit: ABC octaves one low (C is middle C), a one-line transcription writing chords when two notes snapped to one slot, pyin and basic-pitch writing notes into a take's silent tail (fixed with a level gate and range filter), and the note splitter missing a semitone step reached by a smooth slide (the anchor is now the note's median).

## 2026-10-23

- Books track 8 (Oltheten, *Mixing With Impact*; DeSantis, *Making Music*), branch books-8. Built `mw.py mixcheck`, `compare`, `preview`, `monobass`, `mix --shelves --automate`, `master --peak`, an `lra_hint` per preset and melody hints in `render --check`, and wrote the craft into all seven skills. Rulings and what was not built: decisions/2026-10-23-books-track8.md.
- Calibrated on 78 real AI renders (mix flags fire on 1% to 18%; 43 raise none); the three judged flute takes (BELOW-RANGE: -4.0 dB on the rejected take, -25.1 and -33.3 on the kept ones); 18 public-domain tunes against six random walks (melody flags 0/18 and 6/6; the single-top-note rule fired on 12 of 18 and was dropped as a flag).
- Corrections on real data: MUDDY needed a bass part (produce L-002); the first monobass (subtract a low-passed side) widened the lows, a Linkwitz-Riley crossover fixed it (hub L-003); one ACE-Step render loses 10 LU in mono (produce L-003).
- Evals T-20261023-1: 33/33 in a repository clone and 15/15 in a fixtures-only folder; baselines 5/5 in a clone (they read the repository) and 1/5 fixtures-only. Three apparent failures were evidence regexes that missed a script called through a shell variable or options split over lines. One passing run found that `preview --blind` wrote its key into the listening folder; it now goes beside it (hub L-004).
- 82 unit tests; 19 mutations, each caught by its test. Installed skills 446 KB (yellow; green line 400).
- Books track 9 (Rogers, *Level Up!*), branch books-9: musicwright-game Step 1 takes the cue list from a beat chart or LEVEL-PLAN.md; adaptive.md gains mystery, warning, chase and villain-motif cues and rules on rotation, energy, the title piece, silence, stinger direction and a visual twin. Rulings M1-M6 in [decisions/2026-10-23-books-track9.md](decisions/2026-10-23-books-track9.md).
- Size: six sibling MAINTENANCE.md files were identical copies of the hub's; they now point at it. Installed skills 446 KB to 422 KB (still yellow: scripts are 168 KB).
- Not built: a `mw.py cues` neighbour-repeat check (no real beat chart to calibrate on, and games repeat a level theme on purpose; M2).
- Evals T-20261023-1 (game): outcome-2 3/3 against a baseline 0/3 (no warning cue, no visual twin); triggers and decoys 3/3 except trigger-2, 2/3 once it had a fixture, classed harness (game L-001).
- Books track 11 (DeSantis, *Making Music*, the items track 8 left for librosa), branch books-11: `mw.py analyze` reports tuning against A440 (offset, spread, trend), each later file's gap from the first, a repetition share, and `--sections` (automatic, a count, or tags) with boundaries on the nearest beat. Flags OFF-A440, DRIFT, REPEATS, TUNING-GAP. Rulings N1-N9 in [decisions/2026-10-23-books-track11.md](decisions/2026-10-23-books-track11.md).
- librosa stays optional (N1): CI does not install it, the new tests skip without it, `MUSICWRIGHT_REQUIRE_LIBROSA=1` runs them. 86 tests green here with librosa 1.0.0; 11 mutations, each caught.
- Calibrated on 111 AI renders and layers and 11 human recordings from Wikimedia Commons (kept in the session's scratch folder only): OFF-A440 6/111 and 4/11 (strings and a 1920 band sit sharp), REPEATS 5/111 (all 10-minute beds) and 0/11, DRIFT 0 everywhere. Window spread is bends and effects, not drift (produce L-004). Sections on 24 spliced composites: 85% of boundaries within 3 s (compose L-003).
- Records fix: track 8's produce L-002, L-003 and compose L-002 had been inserted inside the LEARNINGS template comment; the comment now starts at the template.
- Evals T-20261023-2: produce and compose action-4 (hold-outs) 3/3 each, baselines 0/1. A passing run's note about fractional bars led to the beat snap.
## [2026-10-23] index | rebuilt (3 entries)
## [2026-10-23] index | rebuilt (3 entries)
## [2026-10-23] index | rebuilt (4 entries)
## [2026-10-23] index | rebuilt (5 entries)
## [2026-10-23] index | rebuilt (5 entries)
