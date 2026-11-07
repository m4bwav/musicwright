---
name: musicwright-produce
description: "Use whenever music audio exists and must be finished or checked: loudness to a destination (streaming -14 LUFS, games, web video, EBU R128) with true peak, mastering, trims and fades, formats (WAV, FLAC, OGG; MP3 breaks loops), a mix check (muddy, harsh, flat, mono, wide bass, a drone under a solo), loudness-matched comparisons, stems, fixes for AI output. Runs mw.py measure, mixcheck, compare, preview, master, monobass. Use on 'master this', 'how loud should it be', 'is this clipping', 'is it muddy', 'why does mine sound smaller than', 'check it in mono', 'convert to ogg', 'split the stems'. Game loops: musicwright-game; fitting to video: -score. Also 'refresh musicwright-produce'."
---

# musicwright-produce

Finishing and checking. Everything here is measured, never guessed: run the number before and
after every change and report both. Script: `<this folder>/../musicwright/scripts/mw.py` (the sibling hub folder).

## Step 1: measure

`mw.py measure <files>` gives duration, sample rate, integrated loudness (LUFS), loudness range
(LRA), true peak, head and tail silence, interior gaps, clipping signs and warnings.
`mw.py analyze <files>` adds tempo, key, tuning and repetition when librosa is available (it
prints the `uv run` line when it is not); give the lead first and a layer's `cents_from_first`
says whether they will beat. A `KEY-AMBIGUOUS` flag (`key_margin` under 0.05) means the runner-up
(often the relative minor or major) is nearly as likely: name both in a brief. Picture: `mw.py sheet <files> --out <png>`, then look at it.

`mw.py mixcheck <files>` measures what a mix engineer listens for: each band's level against the
whole, peak-to-loudness ratio (PLR), a loudness contour, stereo correlation, the mono-fold loss
and how wide the lows are. It flags OVER-LIMITED, FLAT, MUDDY, BRIGHT, MONO-LOSS and LOW-WIDE,
and BELOW-RANGE with `--lowest C4` when the brief names a solo instrument. Flags say what to listen
for, not whether it is good; how often each fired on 78 real AI renders is in
[references/mixing.md](references/mixing.md). `mw.py compare take.wav ref.wav` sets a take beside
a reference the user owns ("why does mine sound smaller?"); use the reference for the idea, never
to copy its spectrum. Cut the biggest section from both with `mw.py edit` first; use two or three
lossless, lightly limited references, and say so when one's PLR is far below the take's (Senior ch. 4).

## Step 1b: compare at one loudness

People hear the louder of two copies as better, even at 0.3 dB (after Oltheten, *Mixing With
Impact* 5.3). Before a listener ranks takes or judges a fix, write matched copies:
`mw.py preview <files> --out <dir>` (one LUFS for all, lowered when a copy would need a limiter).
`--blind` names them take_A, take_B in a shuffled order and keeps the key in a file you open only
after the ranking; `--as phone` (mono, 300 Hz-6 kHz) and `--as quiet` (20 dB down) are the small
speaker and low-level checks. A sound test goes on an askwright page, not in chat, when `mw.py doctor` reports `askwright` (hub Step 3).

When asking for a judgement, give times for the loudest and quietest passages, read by eye from
`mw.py sheet`, since harshness shows at the loudest. The listener sets the volume once and plays each
passage through rather than switching quickly (Katz ch. 4, 19). Before delivery, ask for one full
play-through with no screen and a snag list; fix only those that hold across `--as phone`,
`--as quiet` and normal, unless that one check is the destination. Compare the final with the
untouched take on blind `preview` copies, because a chain of fixes can end up worse (Senior ch. 19). If the take wins, suspect the last dynamic or low-end change first (Braddock ch. 14).

## Step 2: pick the destination preset

| Preset | LUFS | True peak | When |
|---|---|---|---|
| `streaming` | -14 | -1 | personal listening, Spotify, YouTube uploads |
| `apple` | -16 | -1 | Apple Music, AES streaming guidance |
| `web-video` | -16 | -1.5 | score or bed under web video, one level for every cue in a film |
| `game-music` | -18 | -1 | every music asset in one game, mastered to the same level |
| `game-console-mix` / `game-mobile-mix` | -24 / -18 | -1 | the whole game mix, not a single file |
| `broadcast` / `broadcast-us` | -23 / -24 | -1 / -2 | EBU R128 / ATSC A/85 |

Game targets apply to the whole mix: one level, or one gain to keep calm under
combat (`mw.py master a b c --shared-gain`); balance against SFX in the engine. Sources and caveats: [references/loudness.md](references/loudness.md).

## Step 3: fix, then master last

Order: trim and fade (`mw.py edit`), then any repair, then loudness (`mw.py master`). If no flag
fires and the listener has no complaint, apply the destination gain only: no EQ, no repair (Katz ch. 4).

- Silence at the end: `mw.py edit <in> --end <t> --fade-out 2-4 --out <out>`.
  Put `--end` after the audible decay ends (read `mw.py sheet`) and make the fade longer than the decay
  left; never fade across a ringing tail to reach a length. When trimming a head, keep the sound before
  the first attack and fade in briefly (Katz ch. 3).
- Too quiet or too loud: `mw.py master <in> --preset <p> --out <out>`. It runs two-pass loudnorm,
  linear when possible, resamples to 48 kHz and reports before and after. "dynamic" in the result
  means the target needed more headroom than the file had and dynamics were changed: say so and
  ask the listener about pumping, softer drums, muddy bass and lifted tails (Senior ch. 19), or choose
  a lower target. `linear` needs a PLR of at most true-peak target minus LUFS target: 13 dB for
  `streaming`, 14.5 `web-video`, 15 `apple`, 17 `game-music`. Above that prefer the lower target;
  unused headroom is no fault (Katz ch. 17).
- Clipping in the source: a lower target only prevents new overs after encoding and removes nothing
  already in the render; a limiter is no repair and can sound worse (Katz ch. 16). Re-roll, or use a
  declipper in a DAW. Harsh peaks: the EQ moves below. Never stack more compression on AI output,
  which is usually already dense.
- LOW-WIDE: `mw.py monobass <in> --out <out>` folds the lows to mono under a 160 Hz crossover
  (`--hz 200` for a fully mono low end up to about 120 Hz) and keeps the stereo above the split.
  A crossover can colour the sound: have a listener compare result and input on `preview` copies (Senior ch. 19).
- Any filter (`monobass`, `--shelves`, EQ) or later rate conversion can raise peaks, even a cut: measure again before delivery (Katz ch. 16, 18).
- FLAT on a piece that should build, or everything equally bright: a build needs a drop before it.
  With stems, in order: mute or lower stems ahead of the peak, darken background stems while the lead
  stays bright (`--shelves 0,-4,-3`), then 1-3 dB section moves (`mw.py mix <stems> --automate
  2:0=-3,58=-3,60=0`). With no stems, `mw.py mix take.wav --automate 1:...` rides the whole render and
  leaves transients alone: the last resort. Lower in the quieter bars before a loud entry, never during
  a build, ramping over several seconds; level moves survive a `linear` master and may not survive a
  `dynamic` one (Katz ch. 5, Senior ch. 19). Recipes in
  [references/mixing.md](references/mixing.md) "AI renders".
- Muddy (250-500 Hz), harsh (2-5 kHz), dull (nothing above 16 kHz) without stems: describe it and
  suggest EQ moves from [references/mixing.md](references/mixing.md); the agent cannot judge by ear.
- Fades: before `master` when it reports `linear`; after it when it reports `dynamic` or after any DAW compressor or limiter, because
  level-dependent processing changes how a fade sounds (after DeSantis, *Making Music* 75).
- For a human mastering engineer: `mw.py master <in> --peak -6 --out <out>` (gain only, peaks at
  -6 dBFS, no limiter, source rate). `master` also prints the preset's `lra_hint`.
- Stems for layers, removing AI vocals, or checking an artefact: [references/stems.md](references/stems.md).

## Step 4: formats

- Work and archive in WAV (24-bit) or FLAC at the source rate; 48 kHz for games and video.
- OGG Vorbis (q6) for engines; MP3 only for distribution, never for loops (encoder padding adds
  silence: measured +1,728 samples when the gapless tag is missing).
- Never upsample AI output to look better; it does not add detail.
- Convert with `mw.py edit <in> --out <name>.<ext>` (codec from the extension), from the 24-bit or float master, never a 16-bit or lossy copy.
- Run `mw.py measure` on the OGG, MP3 or M4A too, since lossy coding can raise peaks. At 0 dBTP or
  above, lower the source and re-encode rather than add a limiter (Katz ch. 16).

## Step 5: report and record

Report every deliverable with its path and the after numbers, plus what you could not check by ear.
Add it to `music.json` deliverables (hub references/contract.md). A lesson worth keeping
(a preset that suited a destination, a fix that worked) goes to musicwright-curate.

## Rules

- Never claim an improvement without before and after numbers.
- Never let a listener compare copies at different loudness: preview them matched first.
- Master last, once. Re-mastering a mastered file stacks artefacts.
- Keep the original take untouched in `takes/`; write results to `out/`.
- Tools that are GPL or AGPL (Matchering, Essentia) are called as separate programs, never vendored.

## References

- [references/loudness.md](references/loudness.md): targets by destination, loudnorm details.
- [references/mixing.md](references/mixing.md): frequency map, mix moves, scripted checks.
- [references/ffmpeg.md](references/ffmpeg.md): tested ffmpeg recipes.
- [references/stems.md](references/stems.md): Demucs and RoFormer separation.

## Maintenance

Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md),
[LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evergreen.json`. Platform loudness targets
can change: refresh when due.
