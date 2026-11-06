# Changelog

Plugin versions. Reasoned changes per skill are in each `skills/<name>/CHANGELOG.md`.

## Unreleased

- musicwright-produce: mixing.md gains reverb and delay by job, a render treated as premixed audio, and a referencing order, from Senior, *Mixing Secrets* (2nd ed.).
- `mw.py analyze` reports `harmony` (changes per minute, longest one-chord span, top-two share), not flagged and uncalibrated.
- musicwright-game: fixed the intro-then-loop recipe. Cut the intro at S+L, not at S: on real takes the old cut jumped 0.17-0.58 at the join against a typical step near 0.01; the new one stays within about two steps. Stems now get one gain, never a master each.
- musicwright-game: new references/interactive.md (choosing a technique, transitions, stinger kinds, layers, repetition, an implementation check), plus cue rows, game genres and loop types in adaptive.md, from Phillips and Sweet.
- `mw.py gen --recipe yue2-3b-int8 --task cover`: sings new style and lyrics over a melody SheetSage2 transcribes from the source. No listener verdict yet.

## 0.1.12 (2026-11-05)

- Research round two, group 7: acestep.md gains ACE-Step community reports on captions, chords, endings, keyscale and cover; licences.md notes an unanswered rights question.
- Research round two, group 8: the YuE2 melody-cover route and the Stable Audio 3 caption shape.
- Research round two, group 9: corrected the YuE2 memory figure in models.md.
- Research round two, groups 10 and 11: prompting notes for YuE2, Stable Audio 3 and ACE-Step vocals; tempo search for hits; a delay before state changes; cadence, borrowed-chord and sentence notes.

## 0.1.11 (2026-11-04)

- Second-round listening: recipe source notes record that Stable Audio 3 can miss a calm brief, a second kept YuE2 take and the preferred MiniMax Music 3 seed. The extract docs mention one slight leak in the drums. No setting changed.

## 0.1.10 (2026-11-03)

- `mw.py doctor` reports the askwright `ask.py` (`MUSICWRIGHT_ASKWRIGHT`, `askwright` in the studio config.json, or the plugin cache). The sound-test rule now reaches produce, generate, score and compose, after an eval showed the hub-only rule was missed.

## 0.1.9 (2026-11-03)

- The take loop puts sound tests on an askwright page when that plugin is installed, reads the answers back and records them with `mw.py verdict`. Chat stays the fallback.
- RESEARCH.md notes the SongEval run: not adopted.

## 0.1.8 (2026-11-03)

- New recipes from a listener's keeps: `stable-audio3-medium` and `yue2-3b-int8`, through `mw.py gen`. YuE2 needs lyrics and saves its ABC plan beside the take. `doctor` also looks for checkpoints. `mw.py gen --task cover` in ComfyUI now follows the source's semantic hints unless `--strength` is given (behaviour change: the old default was denoise 0.6), after a blind listening pair; the docs lead with ComfyUI for cover, repaint and extract.
- `mw.py gen --task extract` without a caption sends an empty text, where ComfyUI would have read the caption as the word "None". `mw.py curve` no longer prints a zero-length span when two shape points land on one time. The `acestep-rest` recipe's `use` line no longer says ComfyUI lacks the source tasks. Found by the 0.1.7 wiki run.

## 0.1.7 (2026-11-03)

- `mw.py curve FILES --shape 0:-30,20:-18,50%:-14,end:-24 [--absolute]` ranks takes against a target loudness shape for film cues: per-second short-term loudness against the interpolated shape, rms error after the level offset, correlation, worst second and mean error per span. Test added.

- `mw.py gen --recipe acestep-xl-base --task extract --track NAME` runs ACE-Step 1.5 extract inside ComfyUI on the XL base checkpoint, through two nodes (MWAceStep15TaskTextEncode, MWAceStep15ExtractGuider) vendored from ComfyUI_RyanOnTheInside at 52daf66 (MIT) into comfy_nodes/musicwright_nodes/acestep15; the upstream import-time mask patch is left out. New recipe acestep-xl-base; sft recipes refuse extract. Dry-run test.
- `mw.py gen --task cover --hints` covers inside ComfyUI from the source's semantic hints (decoded 5 Hz codes) through a new MWAceStep15CoverGuider node and the vendored extract_semantic_hints (same pack, MIT), at denoise 1; refused with `--strength` or on REST. Dry-run test.

## 0.1.6 (2026-11-02)

- `pulse --threshold adaptive`: a moving-median onset threshold (median plus spread over a 3 s window) for tracks whose level changes; the global threshold missed a quiet intro's hits once a loud section raised it (Lerch, *An Introduction to Audio Content Analysis*, 2nd ed., sec. 9.3.2). Default stays global, so earlier readings hold. Rows say which threshold ran. Test added.
- `analyze` reports `key_margin` (top key profile score minus the runner-up) and `runner_up_relation` (relative, parallel, fifth), and flags `KEY-AMBIGUOUS` under 0.05 (Lerch sec. 7.5.2: Krumhansl profiles score near keys close together). Test for the relation helper.

Earlier unreleased work, now in 0.1.6:


- `gen --task cover|repaint` on the ACE-Step ComfyUI recipes: uploads `--src` to ComfyUI and runs cover as LoadAudio -> VAEEncodeAudio -> KSampler at denoise 1 - strength (default 0.4), repaint through the new AudioLatentRepaintMask node shipped in `skills/musicwright/comfy_nodes/` (checked on the host first). Measured on the PC: a 10-20 s repaint of a 30 s take in 35 s, source kept outside the window (0.99-1.00). Three tests on the fake server.
- Generate: listen for a known tune before releasing any cue, not only after a reference or cover (Hands-On Generative AI ch. 9).
- `fluidsynth` key in the studio config.json, read after `MUSICWRIGHT_FLUIDSYNTH` (as `soundfont` already was), with a test.
- `gen --no-wait` logs each queued ComfyUI job as a `queued` ledger row (recipe, caption, seed, prompt id); `gen --collect DIR` downloads, measures and logs the jobs that have finished, reports the pending ones and logs failed ones once. `--no-wait` on the REST route is now an error. Three tests.
- `mixcheck` and `compare` read integrated loudness and true peak from the file as it is, like `measure`: a mono file read 3 dB low in true peak (-13.5 against -10.5 dBTP) because the stereo layout spread back up the filter graph. After the padded retry the short-term contour drops the seconds that reach into the padding. Test added.

## 0.1.5 (2026-11-01)

- Compose: a "Rhythm and groove" section in theory.md (DeSantis, *Making Music*: unequal loop lengths, the 3+3+2 backbone, groove offsets and ghost notes, silence or a bed between notes, breadth before depth), the strategies the 2026-10-22 book pass had left out.

## 0.1.4 (2026-11-01)

- Book learnings (Foster, Generative Deep Learning 2e, ch. 11; approved by the owner): `render --check` adds `key_fit`, the pitch-class histogram against the declared (or estimated) key with out-of-key notes on strong beats listed and short passing notes allowed, with tests. Compose: MIDI and ABC header rule (key and time signature) and events over grids for triplets, repeated notes and dynamics. Generate: temperature ladder and melody-copy check rows, and an ACE-Step control map (global, per section, per stem).

## 0.1.3 (2026-10-25)

- Fixes found by the 0.1.2 wiki verification: on ffmpeg builds that abort with `best_input` (static 7.0.2), `mixcheck` and `compare` still measure the padded copy for bands, stereo and contour, but take integrated loudness and true peak from the original file, since the padding's silence lowered loudness (a 3.5 s 44.1 kHz tone now reads -21.8 LUFS on 7.0.2 and on 9.0.1). `mixcheck` `duration_s` is the file's length, not a count of whole-second blocks (3.5, not 4). `pulse` sets `tempo_bpm`, `grid_deviation` and `grid_chance` to null when it says `none`.

## 0.1.2 (2026-10-25)

- Fixes found by the 0.1.1 wiki verification: `mixcheck` and `compare` no longer stop on ffmpeg builds that abort with `Assertion best_input >= 0` (static 7.0.2) when a file does not end on a whole second at 48 kHz (44.1 and 8 kHz inputs among them): mw.py pads a copy to whole seconds and measures again. `seam` reads the level jump from a robust line through the window levels at the seam, so a loop cut on a kick over a swelling bed reads clean (3.5 dB before, about 1.3 now) while a real level step still reads as a seam. `pulse` reports `onset_rise_db` and says `none` when onsets rise under 1 dB (a swelling tone with no beat was called steady at 120 bpm).
- Correction to 0.1.1 below: the six `MAINTENANCE.md` pointers took the installed skills from 446 KB to 422 KB when they were added; tracks 11, the 0.1.1 fixes and these fixes brought the total to 450 KB (`scripts/budget.py`, yellow).

## 0.1.1 (2026-10-23)

- Listening checks (blind, matched level; decisions 2026-10-23-listening-checks): REPEATS is no longer a flag, `repetition.share` is still reported (a bed at 0.98 sounded less stuck than one at 0.13); TUNING-GAP fires over 30 cents, not 15 (a layer 27.6 cents off was heard as in tune; now 0 of 14 real layers); BRIGHT reads as a fatigue pointer (a take at -7.6 dB was slightly tiring, not harsh); the density section-tag advice is marked as not shown to help on one pair.
- Fixes: `--host` without `http://` works; `seam` no longer calls a loop that starts on a drum hit a level jump; `master` with only `--lufs`/`--tp` is named `custom`, and its dynamic-mode warning no longer blames peaks on a source with no loudness range; `new` refuses an unknown `--preset`; `verdict` fails on a missing file and records an unlogged take by its stem; `gen` through ComfyUI says when it sent the recipe's bpm and key and that MiniMax Music 3 ignores `--bpm`/`--key`.
- Docs: seam ratio 2 or less is clean; argument errors exit 2 with usage on stderr; `created` in the music.json table.
- Also in this release, from the Unreleased list of tracks 8, 9 and 11:

- `mw.py analyze` (librosa, still optional) reports tuning against A440 (offset, spread and trend over 10 s windows), each later file's tuning gap from the first, the share of the track that repeats an earlier 8 s block, and with `--sections` the section boundaries in seconds and bars (an automatic count, a number, or tag names). Flags OFF-A440, DRIFT, REPEATS and TUNING-GAP, set on 111 AI renders and 11 human recordings; rates in musicwright-produce's references/mixing.md. Tempo and key are unchanged.
- `mw.py mixcheck`: one ffmpeg pass gives each band's level against the whole, peak-to-loudness ratio, a short-term loudness contour, stereo correlation, mono-fold loss and low-end width, with flags (OVER-LIMITED, FLAT, MUDDY, BRIGHT, MONO-LOSS, LOW-WIDE, and BELOW-RANGE with `--lowest NOTE`). Thresholds set on 78 real AI renders, rates in musicwright-produce's references/mixing.md. `mw.py compare take ref` sets two files side by side.
- `mw.py preview`: loudness-matched copies for listening, `--blind` (shuffled take_A, take_B and a key file), `--as phone` and `--as quiet`. The hub's take loop hands these over instead of the raw takes.
- `mw.py monobass` (Linkwitz-Riley crossover, lows to mono); `mw.py mix --shelves` and `--automate` (per-file high shelf and gain envelopes); `mw.py master --peak` (gain-only pre-master, no limiter) and an `lra_hint` per loudness preset.
- `mw.py render --check` gives melody hints per line (leap share, returning rhythm), calibrated on public-domain tunes against random walks.
- Craft from Oltheten, *Mixing With Impact*, and DeSantis, *Making Music*: fixes for AI renders (produce), melody, harmonic rhythm, arrangement and endings and a five-field reference (compose), section tags that say who plays and a stop rule (generate), a "Tired of" list (curate), never-repeating beds and layers by subtraction (game), a presence check for cues under dialogue (score).
- Notation: `mw.py render` plays ABC, ASCII guitar and bass tab, MusicXML and MIDI (FluidSynth and a SoundFont when installed, otherwise a built-in sketch synth) and checks bar lengths; `mw.py notate` converts between ABC, MusicXML, MIDI and tab; `mw.py transcribe` turns a recording into MIDI, ABC, MusicXML or tab (librosa pyin for one instrument, basic-pitch for several), with a level gate and a range filter. The readers and writers are standard-library Python in `scripts/notation.py`. musicwright-compose owns the route (Step 4, references/notation.md).
- `mw.py pulse` (is there a beat: onsets, inter-onset spread, autocorrelation, grid fit) and `mw.py answer` (does a layered part sit in the lead's rests), both standard library.
- Recipe `acestep-rest-lego`: one part added to a kept take on the 2B base checkpoint, kept by a listener with the part ducked under the lead.
- Adding a part is a step in musicwright-generate; the REST reference names the server version that fixes base-model noise (DCW) and the measured VRAM per model.
- `mw.py mix`: layer stems with per-file gain, offset and pan into one file, with aligned stems.
- `mw.py gen --task cover|repaint|lego|complete|extract --src F --track T`: work from existing audio on the ACE-Step REST server (lego, complete and extract need a base checkpoint); the source is uploaded and the planner is turned off so the new part hears it.
- `mw.py duck` keeps the music's length when the key is shorter, and `--stem` writes the ducked music alone.
- master, edit, join, loop, duck and sheet create a missing `--out` folder; gen validates before creating one and no longer creates it on dry runs; the REST route sends `--cfg`, `--steps`, `--shift` and `--set`, and lists options it cannot use.
- Game cues from the level plan (musicwright-game, after Rogers, *Level Up!*): the cue list comes from a beat chart or `LEVEL-PLAN.md` when there is one; new cue types mystery, warning, chase and a villain motif; rules on rotating two tracks per area, energy for action cues, the title piece, silence as an event, stinger direction and a visual twin for cues that carry information.
- Six skills' `MAINTENANCE.md` files point at the hub's identical copy, which takes the installed skills from 446 KB to 420 KB.

## 0.1.0 (2026-10-17)

First release.

- Seven evergreen skills: musicwright (hub: brief, route, the take loop for an agent that cannot listen, the project contract), musicwright-generate (models, licences, captions, seeds, fixing takes), musicwright-compose (theory, motifs, prompt vocabulary, notes-first routes), musicwright-produce (loudness, mastering, formats, stems, mixing fixes), musicwright-game (seamless loops, layers, stingers, Unity import), musicwright-score (spotting, hit points, movements, ducking under dialogue) and musicwright-curate (verdicts, taste, lessons, recipes).
- `mw.py` (standard-library Python 3.9+, needs ffmpeg): doctor, new, gen (ACE-Step 1.5 XL and MiniMax Music 3 through ComfyUI, the ACE-Step REST server; `--dry-run` prints the graph or payload), measure (LUFS, LRA, true peak, head and tail silence, clipping), sheet (spectrogram and waveform contact sheet), master (two-pass loudness to a preset), edit, join (crossfades on hit points), loop (bar-exact, tail crossfaded into head, OGG loop tags), seam, duck (under dialogue or a video's sound, remuxing the video), analyze (tempo and key with librosa), verdict, ledger and note.
- Four generation recipes in `recipes.json` and eight loudness presets in `loudness.json`, each with its source.
- `tests/check_skills.py` (structure, companions, manifests, recipes and presets, links, public-safety guards), `tests/test_mw.py` (every command on synthetic audio, `gen` against a fake local host) and `scripts/budget.py`; CI on Ubuntu, macOS and Windows with ffmpeg.
- Research notes of 2026-10-17 in `ai-docs/research`.
