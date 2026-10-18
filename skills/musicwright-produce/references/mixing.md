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

## Arrangement density

3-5 focal elements at once, each in its own register. A good track has at least two density
levels. Under dialogue or busy SFX: no busy 1-4 kHz lead.

## Scripted checks

| Check | How | Flag when |
|---|---|---|
| loudness, LRA, true peak | `mw.py measure` (ebur128) | off the preset; TP above -1 |
| clipping | `astats` peak level and flat factor (in `mw.py measure`) | peak at 0 dBFS with a high flat factor (a +30 dB clipped test jumped from 8.4 to 41.3) |
| silence | `silencedetect` (in `mw.py measure`) | over 0.2 s at the start, over 1 s at the end of a one-shot, any in a loop |
| DC offset | `astats` DC offset | absolute value over 0.001 |
| mono compatibility | fold to mono, compare loudness | mono 1.5-3 LU or more quieter than stereo |
| phase | `aphasemeter` mean | below 0 (cancellation); 0.3-0.9 is normal stereo |
| tempo and key | `mw.py analyze` | far from the brief (beware double or half tempo) |
| spectrum | `mw.py sheet` | hard ceiling, holes, a constant whine |
| loop seam | `mw.py seam` | ratio over about 3, or a level jump over 3 dB |
