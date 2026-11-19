# Mixing rules of thumb and scripted checks

The agent cannot hear; use these to describe a problem the listener reports, or to suggest a
fix to try in a DAW. Practitioner sources.

## Frequency map

sub 20-60 Hz · bass 60-250 · mud 200-500 · body/honk 500-1k · presence 1-4k (ear most
sensitive; harshness 2-5k) · sibilance 5-8k · air 10-16k.

## Moves

- EQ: cut before boost; narrow cuts, wide gentle boosts; high-pass everything that is not bass
  (pads about 100-200 Hz, reverb returns 200-300 Hz). Senior: shelves before peaks, a boost in one band and under 6 dB, high-pass slopes no steeper than about 18 dB/octave and not resonant, and judge every setting in the mix, not solo.
- Masking: carve the rival (dip the pad at the lead's 2-3 kHz), pan apart, or sidechain bass to kick.
- Compression: bus 1.5:1-2:1 with 1-3 dB reduction; vocals 3:1-4:1 with 3-6 dB; slow attack
  (10-30 ms) keeps transients.
- Compression exists to steady a balance: if a part sits at one fader position, leave it alone (Senior ch. 9).
- Reverb: pre-delay 10-30 ms; rooms intimate, 2-4 s halls epic; little on bass and kick. Name the job first (table below).
- Stereo: kick, bass and lead centred; below about 100-150 Hz mono.
- Rough or grating stacks: two layers whose main partials fall a small part of a critical band apart (about 100 Hz wide low down, near a third of an octave higher) beat as roughness; retune, thin or move one. A mix that sounds thin at low volume is equal-loudness, not EQ: judge balance at a moderate level (Loy, *Musimathics* vol. 1, ch. 6; book rule, unverified).
- A low cut set in the dense section may fail where the part is exposed: recheck it there (Senior ch. 19).
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

## Reverb and delay by job

One reverb does five jobs at once. Pick the job, then the settings (Senior, *Mixing Secrets*, 2nd ed. 2018, ch. 16-17).

| Job | Preset | Pre-delay | Use |
|---|---|---|---|
| blend (same room) | natural, tail cut short | 10-20 ms | many parts, after the balance is set |
| size (bigger space) | natural, soft onset | 50 ms or more | many parts, after the balance is set |
| tone | unnatural, tail cut short | set by ear | one or two parts, while balancing |
| sustain | unnatural, soft onset | 25 ms or more | one or two parts, while balancing |
| spread (width) | bland, uncoloured | set by ear | when a part is too narrow |

A delay does the same jobs and masks less. A delay on the tempo sinks into the mix; one off the tempo pops out, so keep it for effects.

**Synthesised impulse when there is no room to convolve with** (a browser game's ConvolverNode, an ffmpeg `afir` pass, a built-in render). Build the impulse from noise instead of shipping a recorded one:

1. Seeded white noise, one channel per side (different seeds give width), 1.5 to 4 s long.
2. Decay as a power of what is left: gain = (1 - t/T)^p with p near 2 to 2.5. It falls slowly, then fast, so the tail ends at zero without a click and no fade is needed.
3. Darken as it decays: a one-pole lowpass (y += a(x - y)) whose cutoff glides from about 8-10 kHz at the start to 1-2 kHz at the end, as air and walls eat the highs first.
4. Normalise the impulse, keep the reverb send low (wet 10-25 %), and put a gentle bus compressor after it (about -6 dB threshold, 6:1) so a loud hit does not swamp the tail.

The seed makes it repeatable: the same seed is the same room every run. `mw.py reverb IN --out OUT` does all four steps. Measured on a 10.4 s built-in-synth phrase (2026-11-18; seed 7, 2.5 s, p 2.2, wet 0.2): impulse RT60 2.85 s (Schroeder T30); the tail sits about 14 dB under the last bar 0.25 s after the music stops, falls about 17 dB a second (the power law speeds up late) and reaches silence 2.25 s after, with no click. In ffmpeg `afir`, set `irnorm=2`: with the default norm the wet path came out about 43 dB under the dry, so a 0.2 send was inaudible. Idea from vitaminclaude/voidstruck (PolyForm Strict: our own words, no code); not yet judged by ear.

## A render is premixed audio

A stereo render has the problem of a sample from a finished record: it was made to stand alone and leaves no room. Senior's rebalancing moves (ch. 15.2) carry over; applying them to AI renders is our inference, untested. Stems (stems.md) come first when separation is clean.

- Adding a part: high-pass the render when a new bass goes in, and cut whatever the new part needs; low-pass it if hiss or crackle keeps a new lead from coming forward.
- One part too loud: a narrow peak on its pitch for a tonal part; fast high-band limiting for a loud tambourine or hat; if it is panned, process that side or the mid or side alone.
- One bad hit: paste a clean hit from elsewhere in the take.
- If none of it works, re-roll: Senior's own last resort is to replace the part rather than salvage it (ch. 12).

## Referencing a take

Senior ch. 4, 19.2-19.3. The agent sets up the comparison; the listener answers. Make loudness-matched copies (`mw.py preview`, `mw.py compare`), judge the side effects and not the level gain, and ask in this order: overall tone; level and dynamics of the main parts; tone of the main parts; reverb and delay length and level; stereo image. Compare the loudest section first, since it should be the peak, using lossless, lightly limited references; a heavily limited one differs by processing. Do not match a reference's spectrum curve: mixes differ by key and arrangement. If most references have less in one region (say 300-500 Hz), try a cut there. Last pass: a written snag list after a night's rest, the whole track, eyes off the displays.

## AI renders: what goes wrong and what to run

A render arrives finished and dense: every part clear, bright and close. Mixing books treat that
as the problem to solve, not a strength. The flags come from `mw.py mixcheck`; the moves after
Oltheten, *Mixing With Impact* (2018) and DeSantis, *Making Music* (2015).

| You see | Do |
|---|---|
| FLAT, or sections that do not contrast | sections with their own density in the prompt (musicwright-compose); a build needs a drop before it, so with stems mute or lower them ahead of the peak, darken them, then 1-3 dB of section moves: `mw.py mix drums.wav bass.wav other.wav --automate 1:0=-3,58=-3,60=0`; with no stems `mw.py mix take.wav --automate 1:...` rides the render, the last resort. Lower before a loud entry, never during a build. Level moves may not survive a `dynamic` master (Katz ch. 5, Senior ch. 19) |
| everything equally bright, no depth | pick the foreground part; darken the rest with `--shelves 0,-4,-3` (one value per stem, 3 kHz corner) and give only the darkened stems a short shared reverb in a DAW; reverb reads as depth only against something dry and close |
| BRIGHT (2-5 kHz most of the time) | listen for fatigue at a moderate level; lower the stem that owns the band (usually vocals or "other"), or lower cfg on the next render |
| MUDDY | cut 250-500 Hz on the pad or keys, not the bass; ask the next prompt for fewer sustained low-mid parts |
| LOW-WIDE | `mw.py monobass` (below) |
| MONO-LOSS | the mix plays quieter and thinner on a phone or a mono speaker: check with `mw.py preview --as phone`; re-roll if it must work there |
| OVER-LIMITED | master to the preset without more limiting; a normalising service only turns a louder master down, but some players do not normalise, so confirm the destination |
| BELOW-RANGE on a solo brief | a drone or bass the instrument cannot play: re-roll the seed |
| hiss or "radio static" in the highs (users report it on Suno v6 renders) | a light FFT denoise before mastering: `ffmpeg -i in.wav -af "afftdn=nr=7:nf=-50:tn=1" out.wav` (about 7 dB at most, noise floor tracked); on a sine plus 5 kHz+ pink noise it took the band from -55.9 to -60.9 dB and left the tone at -21.2/-21.3 dB; listen for swirly artefacts and back off `nr` if they appear |
| a louder take keeps winning | rank on `mw.py preview` copies |

Bass to mono: `mw.py monobass in.wav --out out.wav` splits at 160 Hz with a Linkwitz-Riley
crossover, keeps the high part's stereo and puts the low part of the mid signal in both channels.
On four real renders with wide lows the low-end correlation went from -0.46, -0.1, 0.07 and 0.41 to
0.88-1.0 (0.96-1.0 at `--hz 200`). Bass that is purely out of phase cancels in mono and is gone
afterwards, which is what a mono speaker would play anyway. A crossover can colour the sound near
the split, and side changes shift the apparent balance, so have a listener compare result and input
on `preview` copies (Senior ch. 19).

## Arrangement density

3-5 focal elements at once, each in its own register. A good track has at least two density
levels. Under dialogue or busy SFX: no busy 1-4 kHz lead. Senior's stricter test is three main points of interest at a time, which may change from moment to moment, with each section given its own sound and a fill when a part repeats more than three times (ch. 7). Use it to write or judge prompts, not as a flag. A single small mono speaker makes balance errors easier to hear (ch. 2).

## Scripted checks

| Check | How | Flag when |
|---|---|---|
| loudness, LRA, true peak | `mw.py measure` (ebur128) | off the preset; TP above -1 |
| encoded deliverable | `mw.py measure` on the OGG, MP3 or M4A; any filter or codec can raise peaks (Katz ch. 16, 18) | TP at 0 or above: lower the source, re-encode |
| mix balance and stereo | `mw.py mixcheck` (one ffmpeg pass; table below) | any flag: listen for it |
| clipping | `astats` peak level and flat factor (in `mw.py measure`) | peak at 0 dBFS with a high flat factor (a +30 dB clipped test jumped from 8.4 to 41.3) |
| silence | `silencedetect` (in `mw.py measure`) | over 0.2 s at the start, over 1 s at the end of a one-shot, any in a loop; cut after the audible decay, not across it (Katz ch. 3) |
| DC offset | `astats` DC offset | absolute value over 0.001; a lopsided wave alone is not DC |
| mono compatibility | `mixcheck` `mono_fold_db`; by hand, fold with `dualmono=true` so a mono-safe file reads 0 | more than 3 dB lost (MONO-LOSS) |
| phase | `mixcheck` `correlation` (mid against side energy; agrees with `aphasemeter`) | below 0 (cancellation); 0.3-0.9 is normal stereo |
| tempo and key | `mw.py analyze` | far from the brief (beware double or half tempo) |
| tuning, repetition, harmonic change | `mw.py analyze` (librosa; table below) | any flag: listen for it |
| spectrum | `mw.py sheet` | hard ceiling, holes, a constant whine |
| loop seam | `mw.py seam` | ratio over about 3, or a level jump over 3 dB |

## Flags: rates and calibration

How often each mixcheck and analyze flag fires on real renders, and the listener checks that moved the thresholds: [flags.md](flags.md).

`mw.py diff BEFORE AFTER --out diff.wav` writes what a master or edit changed, so it can be heard. Both files must start together. Level is matched first unless `--raw`.
