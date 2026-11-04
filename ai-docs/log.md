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

## [2026-10-23] listening | four blind checks and the 0.1.1 fixes
- Owner judged four blind, level-matched pairs (preview --blind): a 0.98-share bed sounded less stuck than a 0.13 one, so REPEATS is no longer a flag; a layer 27.6 cents off was heard as in tune, so TUNING-GAP fires over 30 cents (0 of 14 real layers); a cfg 9 take with BRIGHT at -7.6 dB was slightly tiring, not harsh; density section tags did no better than mood words on one orchestral pair. Rulings P1-P5 in [decisions/2026-10-23-listening-checks.md](decisions/2026-10-23-listening-checks.md); produce L-005, generate L-002.
- Fixed HANDOFF item 7 plus hosts without `http://`; 92 tests, ten mutations caught. Version 0.1.1.
## [2026-10-23] index | rebuilt (6 entries)
## [2026-10-23] ci | ffmpeg on Ubuntu from a static build
- `apt-get install ffmpeg` stalled 20-40 minutes on several runs (the analyze job of #10 took 40 min, books-9 hung twice). Ubuntu jobs and release.yml now download BtbN's static ffmpeg 9.0 build (GitHub release, 3-minute limit) and fall back to apt; macOS and Windows unchanged. Owner's go-ahead 2026-10-23.
## [2026-10-23] wiki | republished for 0.1.1 (wiki e35cc91): ten new commands, the 0.1.1 changes and four findings (HANDOFF item 5); examples rerun against v0.1.1 on Windows and Linux
## [2026-10-23] fix | three wiki-verification bugs for 0.1.2 (Unreleased, not tagged)
- mixcheck/compare: reproduced the `best_input >= 0` abort with the static 7.0.2 build in WSL; it fires whenever the 48 kHz stream does not end on a whole second (a native 48 kHz file of 20.37 s too), and padding inside the filter graph does not help. mw.py now pads a copy (s16 for s16 sources, else f32, since the filters run in the input's format and f32 moved quiet bands by up to 3 dB) and measures again; the full suite passes on 7.0.2 and 9.0.1.
- seam: Theil-Sen line through the 50 ms levels each side, read at the seam (L-005). pulse: `onset_rise_db`, none under 1 dB (52 real renders measured 2.4 dB or more). CHANGELOG's 446-to-420 KB line corrected (422 then, 446 at 0.1.1, 450 with these fixes, yellow). 97 tests; five mutations caught.
## [2026-10-23] index | rebuilt (6 entries)
## [2026-10-25] fix | 0.1.3: the three candidates from the 0.1.2 wiki run
- mixcheck/compare: after the best_input retry, a plain `aresample,ebur128=peak=true` pass over the original gives integrated loudness and true peak (the padded copy still gives bands, stereo and contour). A 3.5 s 44.1 kHz tone reads 3.5 s, -21.8 LUFS, -21.1 dBTP on static 7.0.2 (WSL) and 9.0.1 alike. `duration_s` from ffprobe, not the per-second block count. pulse: tempo_bpm, grid_deviation, grid_chance null when pulse is none. Retry test now uses a part-second 44.1 kHz file; three mutations caught; 97 tests on both builds. L-006.
## [2026-10-25] wiki | 0.1.3 wiki republished
- Verification (vault kit wiki-build/wiki-verify.py) rerun against tag v0.1.3 on Windows (ffmpeg 9.0.1) and WSL (static 7.0.2): all three 0.1.3 fixes show (pulse nulls, duration_s floats and 3.5 for a 3.5 s file, -21.8 LUFS on both builds). New case `mixcheck short`. 97 tests on both (5 librosa skips on Linux). Installed skills 452 KB, repo 2,269 KB (yellow).
- Found: mono true peak differs by 3 dB between mixcheck's normal pass and the retry (take_s1.flac -13.5 vs -10.5), and the contour still reads the padding on short files. Both listed in HANDOFF as 0.1.4 candidates.
## [2026-11-01] decision | flute-solo stage 3 and transcriptions (askwright notation-stage3)
- Owner's answers: best stage 3 mix is the answer lead with percussion at -12 dB (matched the guess); all three were "ok, lets just move on for now", so stage 3 is closed; no fixed-bpm re-render, the lead stays free-time (guess was yes: the owner accepts a loose percussion bed over a locked beat); basic-pitch is the closer transcription (matched); FluidSynth and the SoundFont go in the vault studio folder (guess was a tools folder for size).
- Done: FluidSynth 2.6.1 (win10-x64-cpp11) and GeneralUser-GS.sf2 downloaded to the studio folder `fluidsynth/` (38 MB, git-ignored in the private overlay so the vault repo stays small), `soundfont` set in studio config.json, MUSICWRIGHT_FLUIDSYNTH set with setx. Verdicts logged in the flute-solo ledger. Not verified: a render through the new binary (the auto-mode classifier refused to run a downloaded executable); run `mw.py doctor` and one `mw.py render` in a new shell.
- Tooling idea: mw.py reads `soundfont` from the studio config but FluidSynth only from env or PATH; a `fluidsynth` config key would match.

## [2026-11-01] verify | FluidSynth from the studio folder, and a `fluidsynth` config key
- `mw.py doctor` lists the studio FluidSynth 2.6.1 and GeneralUser GS; an 8-bar ABC render used `synth: fluidsynth` (7.98 s, -23.9 LUFS, -13.7 dBTP). Note: the setx variable is not in shells started before it was set, so the Bash tool saw none; the config key fixes that.
- `fluidsynth_bin()` reads `fluidsynth` from studio config.json after the env var; test added (101 tests), AGENTS.md, notation.md and CHANGELOG Unreleased updated. Studio config gained the key.

## [2026-11-01] fix | mixcheck mono true peak and padded contour (Unreleased)
- A mono 0.3 sine read -13.5 dBTP in mixcheck against -10.5 in measure: the aformat=stereo after one asplit set the layout for the ebur128 branch too. Each branch now resamples on its own after [0:a]asplit; test_mono_file_reads_like_measure (102 tests). After the best_input retry the per-second short-term list is cut to the file's whole seconds. Not rerun under WSL 7.0.2.

## [2026-11-01] eval | WSL padding check and generate action-1 rerun
- Static ffmpeg 7.0.2 under WSL: 102 tests OK (5 skips), so the padded-contour fix holds on both builds.
- generate action-1 with the reworded prompt, three runs (T-20261101-1): 3/3 on the trace, 0/3 Skill calls; the clone exposes mw.py. Fixtures-only rerun and baselines still owed (HANDOFF item 1).

## [2026-11-02] eval | generate action-1 fixtures-only and baseline
- Harness gained EVAL_MODE (clone, fixtures = empty folder plus case fixtures, baseline = fixtures with musicwright@mark-local disabled in the --settings file). action-1: 3/3 fixtures-only with the Skill tool each time; baseline 1/3 (one found the plugin cache mw.py by searching). T-20261102-1.
- Found: no sibling skill said where mw.py sits in an install, so runs used the dev clone path. game, generate, produce and score now name `<this folder>/../musicwright/scripts/mw.py`.

## [2026-11-02] eval | baselines for the other action cases
- EVAL_MODE=baseline, three runs each of twelve action cases (T-20261102-2); musicwright absent from every init. 6/36 passed: compose action-1 and action-2 3/3 each (file evidence met by a plain script), the other ten 0/3. evals.json baseline fields filled.
- Harness (vault eval-harness run_evals.py): fixtures-only folders now get the tests/fixtures files the prompt names, keeping their path. Skipped compose action-4 and produce action-4: their audio is not kept.

## [2026-11-02] eval | compose action-1 and action-2 need mw.py
- Evidence is now a trace of `mw.py render` (action-1 also `notate`, and motif.abc or motif.mid) instead of the output file. Kept baseline traces rescored 0/3 each; fixtures-only with the plugin (T-20261102-3): action-1 2/3, action-2 3/3. The action-1 miss never loaded the skill: a 'MIDI file' prompt can still skip compose.

## [2026-11-02] eval | action-4 baselines on stand-in audio
- Harness: EVAL_AUDIO copies bare audio names in a prompt from a stand-in folder (vault eval-harness/audio: reference.flac from spacey_album 01, lead/part.flac from flute takes s52203/s41017). T-20261102-4: compose action-4 and produce action-4 baseline 0/3 each, with the plugin 3/3 each. Owed item 1 (baselines) is closed.

## [2026-11-02] build | gen --collect, and MiniMax Music 3 on real hardware
- `gen --no-wait` writes a `queued` ledger row per ComfyUI job; `gen --collect DIR` downloads, measures and logs finished ones, lists pending, logs failures once; REST --no-wait now errors. 105 tests. Checked live: queued a 90 s take, collect said pending, then logged it.
- MiniMax Music 3 via mw.py gen (PC ComfyUI 8199): 60 s -> 43 s in 105 s; 90 s -> 63 s in 140 s; peak 15.3 GB VRAM. Recipe timing note updated. Takes in Ai/Music/hw-checks await a listener.

## [2026-11-02] hardware | Stable Audio 3 Medium and YuE2 on the PC
- Weights from Comfy-Org/stable-audio-3 (medium + t5gemma_b_b_ul2) and Comfy-Org/YuE2 (3B int8 + sheetsage2) into D:/ComfyUI/models; nodes were already native. Standalone graphs from the bundled templates in Ai/Music/hw-checks/run_native.py (not in mw.py: no take judged yet).
- SA3 Medium: 60 s in 9 s, 60.0 s, -16.3 LUFS, -1.9 dBTP. YuE2: 90 s asked, 78 s in 33 s, ~8.5 GB, -14.7 LUFS, +0.1 dBTP; its ABC plan saved beside the take. Both await a listener.
- ACE-Step REST: no server on either host; ACE-Step-1.5 cloned to D:/AI/ACE-Step-1.5 but `uv sync` was refused by the auto-mode classifier (runs downloaded code). Mark runs `uv sync && uv run acestep-api` there, then REST, cover, repaint and extract can be measured.

## [2026-11-02] research | Audiobox Aesthetics on the judged takes (Owed item 4, half)
- Item 2 still blocked: no ACE-Step venv (uv sync is Mark's), takes unheard. Ran audio-aes via uv tool run (pins: requests, soundfile, torch/torchaudio<2.9) on 16 files in 50 s. CE matched the owner on the s52203/s41017 keep/reject and the s8101 over s8303 mixes; noise on slight gaps; PQ ranked the reject higher. Not added to mw.py. Note: ai-docs/research/04-learned-quality-score.md; raw scores in Ai/Music/aes-check/out.jsonl.

## [2026-11-02] hardware | ACE-Step REST through mw.py gen (Owed item 2)
- Mark ran uv sync and started acestep-api (8001). Freed ComfyUI VRAM via /free first. acestep-rest recipe: text2music 30 s in 190 s cold (-15.6 LUFS, 3.25 s silent tail); cover (strength 0.6, violin), repaint 10-20 s, extract track vocals each ~9 s warm. Repaint: correlation with source 1.0 outside the window, -0.08 inside. Cover: ~0.1 (new material). Extract on a solo-flute source returned nearly the source (0.98), so it is not a real stem test; rerun on a mixed source. Takes rest_* in Ai/Music/hw-checks, unheard.

## [2026-11-02] hardware | cover through stock ComfyUI nodes (Mark: move ComfyUI-native source tasks ahead of the loudness curve)
- Graph: the mw.py XL text2music graph with EmptyAceStep1.5LatentAudio swapped for LoadAudio -> VAEEncodeAudio, generate_audio_codes off, KSampler denoise < 1 (Ai/Music/hw-checks/native_cover.py). 30 s source rest_t2m_s3501: denoise 0.5 and 0.7 each ~2 min (REST server also resident). Log-spectrogram correlation to the source: 0.48 (d0.5), 0.42 (d0.7), REST cover 0.62. Unheard.
- No stock node masks a 1D audio latent by time (SetLatentNoiseMask takes an image mask), so repaint needs a small custom node (time-range mask over the ACE-Step 1.5 latent); extract needs the ACE-Step task instruction, which no stock node passes. Plan in HANDOFF item 7.

## [2026-11-02] plan | sources to mine
- Mark's list of 50 forums, tutorial sites, books, blogs and docs filed as research 05 with an order and access limits (Reddit RSS only, Discord unreadable); HANDOFF item 8, after item 7 (ComfyUI-native source tasks).

## [2026-11-02] hardware | repaint inside ComfyUI with a custom node (Owed item 7)
- Stock KSampler already blends a latent noise_mask each step, and comfy.utils.reshape_mask takes [B,1,T] for 1D latents, so repaint needs only a mask builder: AudioLatentRepaintMask (comfy_nodes/musicwright_nodes, installed in D:/ComfyUI/custom_nodes). Graph LoadAudio -> VAEEncodeAudio -> mask -> KSampler denoise 1 (Ai/Music/hw-checks/native_repaint.py).
- 10-20 s of rest_t2m_s3501: 54 s cold, 15 s warm. Per-2 s correlation to the source (seg_corr.py): outside the window waveform 0.96-1.00 (a VAE round trip, not bit-identical like REST); inside, spectral 0.50-0.70 against REST 0.58-0.81, so it follows the context less. A 0.5 s fade changed little. Unheard: native_repaint_10_20_f0/f5 in hw-checks.
- Extract: no stock route. Community packs (ComfyUI-AceMusic, the official ace-step/ACE-Step-ComfyUI, RyanOnTheInside, kaola-ace-step) claim cover/repaint, extract only partly; installing one runs downloaded code, so it waits on Mark. comfyui-gen gained references/custom-nodes.md (PR #159, L-225: restart the PC server from its cmd file, the scheduled task did not restart it).

## [2026-11-02] build | gen --task cover and repaint through ComfyUI (Owed item 7)
- check_task lets cover and repaint through on acestep15-graph recipes; gen_comfy uploads --src via /upload/image (input/musicwright) and rewrites the graph (source_graph): cover = VAEEncodeAudio latent, denoise 1 - strength (default 0.4); repaint = AudioLatentRepaintMask window (no --end: to the source end), checked via /object_info first. Node moved to skills/musicwright/comfy_nodes so it installs with the plugin. 107 tests.
- Real run on the PC: 10-20 s repaint of rest_t2m_s3501 in 35 s; seg_corr outside the window 0.99-1.00, inside waveform ~0, spectral 0.69-0.83. Take mwgen_repaint_s3601 in Ai/Music/hw-checks, unheard.

## [2026-11-02] research | sources pass 1 (Owed item 8): torchaudio, Demucs, librosa
- PC ComfyUI busy (another session's Flux job, 13.5 GB, 97%), so item 7's cover runs (strength 0.7, audio codes) waited; did item 8 instead.
- Demucs 4.1.0 on PyPI no longer uses torchaudio; bare `uvx demucs` fails on missing numpy, `uvx --with numpy demucs` works (10 s clip, 3 s CPU). stems.md and generate models.md fixed; R-20261102-1 in produce RESEARCH.md. librosa still 0.11.0. Research 05 Done list started.

## [2026-11-02] hardware | ComfyUI cover at strength 0.7 and 0.85 (Owed item 7)
- Queued behind another session's Flux job with `gen --no-wait`, collected by a background loop (Mark: queue and wait instead of stopping on a busy GPU). Source rest_t2m_s3501, seed 3701, caption solo violin.
- seg_corr per 2 s against the source: 0.7 spectral 0.77-0.91, waveform 0.1-0.8 (structure kept, new sound; more than REST cover 0.6 at 0.62); 0.85 spectral 0.93-0.98, waveform ~0.92 (nearly a copy, true peak 0.0 dBTP, clipping warning). Both 3.25 s silent tail, inherited from the source. Guidance in acestep-rest.md: 0.5-0.75 on ComfyUI. Takes mwgen_cover_st07/st085_s3701 unheard. Cover with source audio codes not run: no mw.py or stock-node route feeds codes.

## [2026-11-02] research | sources pass 2 (Owed item 8)
- Essentia, MidiTok, AudioCraft, Stable Audio API: no real gaps; SA3 Large reseller price added to models.md (R-20261102-2). Item 7 remainder: extract waits on Mark choosing a community node pack; cover with audio codes needs a node route (not started). Next pass: HF transformers audio, then IT-JIM.

## [2026-11-02] tool | easy_piano.py beginner sheets (outside the plugin)
- Ai/Music/piano-kids/easy_piano.py: clip -> ffmpeg -> mw.py transcribe -> top line, eighth grid, easy key, C4-G5 -> ABC + printable abcjs HTML with letter names. README there. Candidate for a future `mw.py` option if Mark uses it.
- Fix: easy_piano.py finds the uv-installed basic-pitch (~/.local/bin) and stops on transcribe errors.

## [2026-11-02] research | sources pass 3 (Owed item 8)
- HF transformers text-to-audio docs: speech-first, needs torchcodec; no gap. IT-JIM ACE-Step/LeVo/YuE post not found. LeVo missing from models.md, noted only (R-20261102-3). Next pass: Torin Hopkins, MusicMakerApp, Kingy AI.

## [2026-11-02] research | sources pass 4 (Owed item 8)
- Torin Hopkins, MusicMakerApp, Kingy AI: nothing usable, no skill change (R-20261102-4). Fixed the HANDOFF title line split by an earlier insert. Next pass: Artlist and Mubert guides, Artificial Analysis audio benchmarks.

## [2026-11-02] research | sources pass 5 (Owed item 8)
- Artlist (runs Lyria 3; prompt template), Mubert (API v3, vendor-claimed sub-licensing) and the Artificial Analysis Music Arena v1.1 (Suno v6 leads instrumental; ACE-Step and YuE unranked) added to generate references/hosted.md (R-20261102-5). Group 2 done. Next pass: group 3 forums.

## [2026-11-02] research | sources pass 6 (Owed item 8)
- r/SunoAI and r/udiomusic top-of-month RSS: Suno v6 hiss/"radio static" complaints led to an ffmpeg afftdn row in produce mixing.md (tested on a synthetic tone plus high-band noise); Suno flagging users' own and public-domain uploads noted in hosted.md (R-20261102-6). Next pass: r/ArtificialInteligence, HF audio discussions, awesome-ai-music lists.

## [2026-11-02] research | sources pass 7 (Owed item 8)
- wildminder/awesome-ai-music is the useful list (per-model ComfyUI packs, quants, LoRAs). Added to generate models.md after checking each source: DiffSynth-Music (Apache 2.0 control templates on ACE-Step 1.5: keep vocals or band, beats, prosody), acestep.cpp and acestep.vst3 (MIT), ACE-Step Transcriber (MIT). No list names an ACE-Step extract node pack. r/ArtificialInteligence music RSS empty; HF discussions skipped (R-20261102-7). Next pass: Gearspace, Kaggle, then blogs.

## [2026-11-02] research | sources pass 8 (Owed item 8)
- Gearspace and Kaggle: no relevant threads; group 3 done. Stable Audio 3 HF card: inpainting and continuation via stable-audio-tools (no ComfyUI route), noted in generate models.md as a possible repaint route, untested (R-20261102-8). Next pass: Meta AI, Google Magenta, HF audio posts.

## [2026-11-02] research | sources pass 9 (Owed item 8)
- Meta AI: nothing since AudioCraft. Magenta RealTime 2 already in models.md (licence confirmed via HF API). No 2026 HF music blog post. LeVo 2 licence is a custom Tencent file that could not be fetched, so no row (R-20261102-9). Next pass: OpenAI research, Sound on Sound, Music Business Worldwide.

## [2026-11-02] research | sources pass 10 (Owed item 8)
- OpenAI: no released music model. Sound on Sound: nothing found. MBW: label deals with Udio (no platform launch yet) and Suno added to generate hosted.md (R-20261102-10). Next pass: Towards Data Science audio, Synthtopia, then books.

## [2026-11-02] research | sources pass 11 (Owed item 8)
- Towards Data Science audio: only 2023-24 explainers. Synthtopia: synth and preset tools, no generators. No skill change; group 4 done (R-20261102-11). No open askwright questions. Next pass: group 5 books, Müller first.

## [2026-11-03] research | sources pass 12 (Owed item 8)
- Müller's book not on disk; FMP notebooks read instead. Structure, key and tempo already in mw.py; chord recognition, DTW alignment and HPSS noted as candidates, no skill change (R-20261103-1). The Music/notation-stage3/ask folder has no questions.json (nothing open). Next pass: Farnell, then Nierhaus.


## [2026-11-03] research | sources pass 13 (Owed item 8)
- Farnell, *Designing Sound*: procedural SFX in Pure Data, out of scope. Nierhaus, *Algorithmic Composition*: Markov, grammars, GA, CA; not a gap while the agent writes notes, Markov-over-intervals variations a candidate only. Tables of contents only, no copies on disk (R-20261103-2). Next pass: Dean, then Zolzer.

## [2026-11-03] research | sources pass 14 (Owed item 8)
- Dean, *Oxford Handbook of Computer Music*: survey, IDyOM-style expectation a candidate only. Zölzer, *Digital Audio Signal Processing*: dither and resampling already covered. Listings only, no skill change (R-20261103-3). Next pass: Dodge, then Foster.

## [2026-11-03] research | sources pass 15 (Owed item 8)
- Dodge and Jerse, *Computer Music*: synthesis out of scope, ch. 11 1/f melodies a candidate only. Foster, *Generative Deep Learning* ch. 11: symbolic models superseded. No skill change; group 5 done (R-20261103-4). Next pass: group 6 course syllabi.

## [2026-11-03] research | ACE-Step node packs (Owed item 7)
- Cloned three packs for research (not installed). RyanOnTheInside has native extract, lego and semantic-hint cover guiders (MIT); official pack and AceMusic have no extract. Ruling: vendor the guiders into comfy_nodes rather than install the heavy pack (research 06). Next: build the extract route.

## [2026-11-03] build | ComfyUI extract route (Owed item 7)
- Vendored the RyanOnTheInside ACE-Step 1.5 extract guider, its common helpers and the lazy model/tokenizer patches (MIT, 52daf66) into comfy_nodes/musicwright_nodes/acestep15, with two MW-prefixed nodes; dropped the upstream import-time reshape_mask patch so AudioLatentRepaintMask keeps stock behaviour. Recipe acestep-xl-base (downloaded acestep_v1.5_xl_base_bf16, 9.97 GB, from Comfy-Org/ACE-Step-1.5). `mw.py gen --task extract` builds a SamplerCustomAdvanced graph with the guider.
- Real run on the PC (ComfyUI restarted by PID from run_comfy_8199_hidden.cmd; patches logged as applied): source rest_t2m_s3501, drums and vocals, seed 3801, 45 s cold / 15 s warm for 30 s. Both takes nearly identical (waveform correlation 0.97, 0.66-0.69 to the source), no energy above 5 kHz (sibilance and air bands about -53 dB). The REST extract of the same source is not isolated either, and the source may hold no vocals. Isolation unproven: listening owed (mwgen_extract_drums/vocals_s3801 in Ai/Music/hw-checks); retry on a source with clear drums and vocals.

## [2026-11-03] research | sources pass 16 (Owed item 8)
- Ableton Learning Music: every chapter already in theory.md (pelog, 19-tone not, models do not take microtonal captions). Soundfly 403. No skill change (R-20261103-5). Next pass: Coursera, Kaggle Learn; then the semantic-hint cover guider (item 7).


## [2026-11-03] research | sources pass 17 (Owed item 8)
- Coursera music-production syllabi covered by produce; Kaggle Learn has no audio course. No skill change; group 6 done (R-20261103-6). Next: the semantic-hint cover guider (item 7).

## [2026-11-03] build | ComfyUI cover from semantic hints (Owed item 7)
- Vendored extract_semantic_hints (RyanOnTheInside ace_step_utils.py, 52daf66, MIT) and added MWAceStep15CoverGuider; `mw.py gen --task cover --hints` swaps KSampler for SamplerCustomAdvanced with the guider at denoise 1 and the task text encoder (task_type cover), as the upstream example workflow does. Refused with --strength or on REST. 109 tests. PR #62 merged.
- Real run on the PC (ComfyUI restarted; a Stop-Process + Start-Process inside a timed-out PowerShell call left the server dead, Start-ScheduledTask "ComfyUI server (8199)" brought it back): source rest_t2m_s3501, caption jazz piano trio, seed 3901. hintcover_s3901 loudness-envelope correlation to the source 0.29 (waveform 0.11) against plaincover_s3901 at strength 0.3 (denoise 0.7) 0.03 (0.03). Hint take peaks 0 dBTP. Unheard; listening owed.

## [2026-11-03] build | loudness-curve fit (Owed item 4)
- `mw.py curve FILES --shape 0:-30,20:-18,50%:-14,end:-24 [--absolute]`: per-second short-term loudness (ebur128 frame log, needs `-v verbose` on ffmpeg 9) against the interpolated shape, skipping the first 3 s and silence; rms error after the level offset, correlation, worst second, mean error per span; takes ranked. Synthetic test: a rising tone 2.1 LU, a flat one 6.7. On four hw-checks takes with a rise-and-fall shape: 3.8 to 7.3 LU, none follows it. PR #64 merged. Next: item 8 group 7.

## [2026-11-03] build | extract retry on a clear mix (Owed item 7)
- Source vocalsrc_s4001 (acestep-xl-sft, punk rock, loud drums, shouted male vocal, 30 s). `mw.py gen --recipe acestep-xl-base --task extract --track drums|vocals --seeds 4002`. Takes correlate 0.02 with each other and 0.25/0.17 with the source; band shares: drums sub -6.8, mid -13.9 dB; vocals sub -33.8, presence -8.5 dB. Isolation shown by numbers; unheard, listening owed. Item 8 closed (six groups, all mined).

## [2026-11-03] release | 0.1.7, wiki, listening page
- Tagged v0.1.7 (PR #67), installed. Wiki republished from 0.1.3 to 0.1.7 (a8f0c25), verified on Windows and on static ffmpeg 7.0.2 in WSL. Its findings are fixed under Unreleased: extract without a caption sent null, which ComfyUI would read as the word "None"; curve printed a zero-length span; a stale recipe line.
- Real rerun with the empty caption (same source, seed 4002): drums correlate 0.99 and vocals 0.85 with the earlier takes, and 0.035 with each other, so separation holds. extract3_* in Ai/Music/hw-checks; the listening page still plays extract2_*.
- Listening page: askwright set hw-checks-listening with extract, blind cover, repaint, MM3, SA3 and YuE2. Unanswered.

## [2026-11-03] build | listening verdicts applied, 0.1.8
- All seven hw-checks-listening questions answered: extract clean, hint cover won blind (key opened after), ComfyUI repaint better than REST, MM3, SA3 and YuE2 kept. Rulings in decisions/2026-11-03-listening-verdicts.md. Ten verdicts recorded with `mw.py verdict`.
- `mw.py gen`: graphs and recipes stable-audio3-medium and yue2-3b-int8, YuE2 saves its ABC; hosts and doctor look in checkpoints too; ComfyUI cover defaults to hints. Real runs: SA3 20 s in 26 s cold, YuE2 30 s in 20 s. 112 tests pass.
## [2026-11-03] index | rebuilt (7 entries)

## [2026-11-03] release | wiki at 0.1.8; SongEval blocked
- Wiki republished at 0.1.8 (407dd49, 17 pages, live clean), verified on Windows and on static ffmpeg 7.0.2 in WSL; no new bugs. The verify script assumed every ComfyUI recipe has a unet; fixed in the private notes.
- SongEval read but not run: the install of its requirements was refused by the permission check. 23 verdicts exist, so it is otherwise ready (research 04).

## [2026-11-03] research | SongEval run, not adopted (Owed item 4)
- Owner allowed the install. 20 judged files on CPU, 63 s. Backwards on flute keep vs reject and hint vs plain cover, right on repaint and stage 2 s8101 vs s8303, noise on slight pairs; score mostly tracks material (YuE2 song 4.35, flute about 1.5). Not adopted, item 4 closed (research 04). Needed torchaudio==2.7.0 and transformers==4.50.3 on Windows. Test folder deleted.
