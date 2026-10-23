# Mixing rules of thumb and scripted checks

The agent cannot hear; use these to describe a problem the listener reports, or to suggest a
fix to try in a DAW. Practitioner sources (e.g. Mike Senior, Mixing Secrets for the Small Studio).

## Frequency map

sub 20-60 Hz · bass 60-250 · mud 200-500 · body/honk 500-1k · presence 1-4k (ear most
sensitive; harshness 2-5k) · sibilance 5-8k · air 10-16k.

## Moves

- EQ: cut before boost; narrow cuts, wide gentle boosts; high-pass everything that is not bass
  (pads about 100-200 Hz, reverb returns 200-300 Hz).
- Masking: carve the rival (dip the pad at the lead's 2-3 kHz), pan apart, or sidechain bass to kick.
- Compression: bus 1.5:1-2:1 with 1-3 dB reduction; vocals 3:1-4:1 with 3-6 dB; slow attack
  (10-30 ms) keeps transients.
- Reverb: pre-delay 10-30 ms; rooms intimate, 2-4 s halls epic; little on bass and kick.
- Stereo: kick, bass and lead centred; below about 100-150 Hz mono.
- AI output: gentle EQ, a limiter, loudness normalisation. It is usually dense already: add no
  compression.

## Layering a new part over a kept take

- Keep every layer as its own file and build each stage as a mix: `mw.py mix base.flac part.wav
  --gains 0,-4 --pans -0.2,0.25 --stems stems/ --out stage2.wav`. The aligned stems let the
  listener judge a part alone and re-balance it in a DAW.
- Two instruments in one register (two flutes) mask each other: set the new part 3-6 dB under the
  lead, pan them apart (about -0.2 and +0.3) and let the answer sit in the lead's rests.
- Before adding anything on a beat (tambourine, shaker, drums), check the base has a pulse:
  `mw.py pulse base.flac` (steady, weak or none, with a tempo and a grid fit). A free-time (rubato) take gives tempos that disagree from
  window to window and onsets that land on a beat grid barely better than chance. Percussion on
  a grid will drift against it; use phrase-placed accents (a hit or swell at phrase starts) or
  re-render a tempo-locked base.
- A layer generated separately (its own seed, same bpm and key) does not know where the lead
  breathes; expect to slide it with `--offsets` and still hear two players ignoring each other.
- To make an added part answer the lead, duck it under the lead (`mw.py duck part.wav --under
  base.flac --stem --out answer.wav`, ratio 3, attack 80 ms, release 700 ms as a start) and check
  with `mw.py answer answer.wav --lead base.flac`: `rests_minus_under_db` above 0 means it now sits
  in the rests. A listener preferred the ducked mix of a lego part over the plain one.

## AI renders: what goes wrong and what to run

A render arrives finished and dense: every part clear, bright and close. Mixing books treat that
as the problem to solve, not a strength. The flags come from `mw.py mixcheck`; the moves after
Oltheten, *Mixing With Impact* (2018) and DeSantis, *Making Music* (2015).

| You see | Do |
|---|---|
| FLAT, or sections that do not contrast | sections with their own density in the prompt (musicwright-compose); with stems, 1-3 dB of section moves on chosen stems: `mw.py mix drums.wav bass.wav other.wav --automate 1:0=-3,58=-3,60=0`; never raise the whole level instead |
| everything equally bright, no depth | pick the foreground part; darken the rest with `--shelves 0,-4,-3` (one value per stem, 3 kHz corner) and give only the darkened stems a short shared reverb in a DAW; reverb reads as depth only against something dry and close |
| BRIGHT (2-5 kHz most of the time) | listen for fatigue at a moderate level; lower the stem that owns the band (usually vocals or "other"), or lower cfg on the next render |
| MUDDY | cut 250-500 Hz on the pad or keys, not the bass; ask the next prompt for fewer sustained low-mid parts |
| LOW-WIDE | `mw.py monobass` (below) |
| MONO-LOSS | the mix plays quieter and thinner on a phone or a mono speaker: check with `mw.py preview --as phone`; re-roll if it must work there |
| OVER-LIMITED | master to the destination preset without more limiting; a louder master is turned down by streaming services and only sounds duller |
| BELOW-RANGE on a solo brief | a drone or bass the instrument cannot play: re-roll the seed |
| a louder take keeps winning | rank on `mw.py preview` copies |

Bass to mono: `mw.py monobass in.wav --out out.wav` splits at 160 Hz with a Linkwitz-Riley
crossover, keeps the high part's stereo and puts the low part of the mid signal in both channels.
On four real renders with wide lows the low-end correlation went from -0.46, -0.1, 0.07 and 0.41 to
0.88-1.0 (0.96-1.0 at `--hz 200`). Bass that is purely out of phase cancels in mono and is gone
afterwards, which is what a mono speaker would play anyway.

## Arrangement density

3-5 focal elements at once, each in its own register. A good track has at least two density
levels. Under dialogue or busy SFX: no busy 1-4 kHz lead.

## Scripted checks

| Check | How | Flag when |
|---|---|---|
| loudness, LRA, true peak | `mw.py measure` (ebur128) | off the preset; TP above -1 |
| mix balance and stereo | `mw.py mixcheck` (one ffmpeg pass; table below) | any flag: listen for it |
| clipping | `astats` peak level and flat factor (in `mw.py measure`) | peak at 0 dBFS with a high flat factor (a +30 dB clipped test jumped from 8.4 to 41.3) |
| silence | `silencedetect` (in `mw.py measure`) | over 0.2 s at the start, over 1 s at the end of a one-shot, any in a loop |
| DC offset | `astats` DC offset | absolute value over 0.001 |
| mono compatibility | `mixcheck` `mono_fold_db`; by hand, fold with `dualmono=true` so a mono-safe file reads 0 | more than 3 dB lost (MONO-LOSS) |
| phase | `mixcheck` `correlation` (mid against side energy; agrees with `aphasemeter`) | below 0 (cancellation); 0.3-0.9 is normal stereo |
| tempo and key | `mw.py analyze` | far from the brief (beware double or half tempo) |
| tuning, repetition | `mw.py analyze` (librosa; table below) | any flag: listen for it |
| spectrum | `mw.py sheet` | hard ceiling, holes, a constant whine |
| loop seam | `mw.py seam` | ratio over about 3, or a level jump over 3 dB |

## mixcheck flags and how often they fire

Fire rates on 78 real AI renders (ACE-Step 1.5 and MiniMax Music 3 takes, film scores and layered
mixes, 14 s to 10 min); 43 raised no flag. No listener labels exist for most of them, so each
threshold sits where a minority fires; they are heuristics, not verdicts.

| Flag | Fires when | Rate | Note |
|---|---|---|---|
| OVER-LIMITED | true peak minus integrated loudness (PLR) under 8 dB | 1/78 | after Oltheten 5.5, 14.5 |
| FLAT | longer than 90 s and short-term loudness spread (10th to 90th percentile) under 2 LU | 4/78 | fine for a steady game bed |
| MUDDY | 250-500 Hz more than 3 dB over the bass and mid bands' average, with a bass part present | 5/78 | without the bass condition it fired on both kept flute solos |
| BRIGHT | 2-5 kHz against 200 Hz-2 kHz above -10 dB for half the playing time | 5/78 | uncalibrated: the one render a listener called harsh read -19.8 and did not fire; flute leads fire it |
| MONO-LOSS | more side than mid energy (correlation under 0), so mono loses over 3 dB | 13/78 | real: one render loses 10 LU folded, confirmed with `aphasemeter` |
| LOW-WIDE | correlation under 0.7 below 120 Hz | 14/78 | fixed by `monobass` |
| BELOW-RANGE | with `--lowest NOTE`: energy a whole tone under the note above -15 dB against the whole | 1/3 flute solos | the take a listener rejected for "bass a flute can't make" read -4.0; the two kept takes -25.1 and -33.3 |

Not built: sibilance spikes (no vocal material to calibrate on) and a codec-ceiling check (the
sheet shows it).

## analyze flags and how often they fire

Rates on 111 AI renders and layered parts and on 11 human recordings (public domain and CC BY:
orchestra, string quartet, solo cello, a piano roll, a 1920 dance band, loop-built electronic
pieces). 100 of the AI files raise none. No listener has judged tuning or repetition yet.

| Flag | Fires when | AI | Human | Note |
|---|---|---|---|---|
| OFF-A440 | tuning 15 cents or more from A440 | 6/111 | 4/11 | a layering warning: strings and old recordings sit sharp on purpose |
| TUNING-GAP | a later file 15 cents or more from the first | | | real lego layers sat 0.4 to 14 cents from their lead; a separate render 28 |
| DRIFT | the last third 15 cents from the first, on 90 s or more | 0/111 | 0/11 | no real file drifts; proved on a synthetic step |
| REPEATS | 90% of a track of 60 s or more repeats an earlier 8 s block | 5/111 | 0/11 | all five are 10-minute beds; the human maximum is 0.61, a scherzo with written repeats |

Window spread (`spread_cents`) is not flagged: bends, vibrato and pitch effects raise it (L-004).
Sections (`--sections`) found 85% of known boundaries in spliced real renders (compose L-003).
