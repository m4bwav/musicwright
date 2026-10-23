# Looking at music you cannot hear

The agent cannot listen. It can look at a spectrogram, read numbers and ask the listener the
right questions. This file says how to do each well, and what to tell the listener.

## Reading an `mw.py sheet`

Each take is two rows: a spectrogram (time left to right, frequency bottom to top on a log
scale up to 8 kHz by default, brightness = energy) and a waveform.

| You see | It usually means |
|---|---|
| one bright wavy line with fainter copies above it | one melodic voice (a solo) and its harmonics |
| several bright lines moving independently | several melodic parts, or chords |
| broad vertical stripes, regular in time | drums or percussion; the spacing gives the beat |
| a wide steady band near the bottom | a drone, pad or bass under everything; for a "solo" brief it is an intruder |
| dark columns | silence or a pause (breaths in a solo, a break) |
| a dark block at the end | the render went quiet early: trim it or re-roll |
| a hard ceiling where everything stops | a low-pass or codec cut-off (dull top end) |
| an even haze across all frequencies | noise, hiss or reverb wash |
| a thick waveform pinned to the top and bottom | loud and compressed, possibly clipped (check `measure`) |

Rank in this order: parts the brief excluded (a drone or bass under a solo, drums in a bed), then the
melodic line, then the ending; a silent tail is a trim, not a fault (L-002). Compare takes against each
other, not against an ideal: the picture ranks them, it does not
grade music. It cannot show melody quality, timing feel, vocal artefacts, or whether the tune
sounds like a known song.

## Numbers that matter (`mw.py measure`)

- `lufs_i` against the destination preset (musicwright-produce); `true_peak_dbtp` at or below -1.
- `tail_silence_s` over about 3 s, or `head_silence_s` over 1 s: trim or re-roll.
- `gaps`: interior silences. Fine for a breathy solo, wrong for a bed that should not stop.
- `warnings`: clipping signs, a true peak too high, silence.
- `lra` (loudness range): high for a dynamic solo or film cue, low for a steady game bed.
- Optional `mw.py analyze`: tempo (may read double or half) and key (pentatonic and modal music
  often reads as its relative major or minor).

## Numbers that point at the mix (`mw.py mixcheck`)

- `bands_db`: each band against the whole. Compare them with each other and with another take,
  never with a target curve. A spectrum hides timing, and copying one mix's spectrum onto another
  does not make them sound alike (after Oltheten, *Mixing With Impact* 3.3, 4.4).
- `plr_db`: true peak minus integrated loudness. Low means squashed; a squashed master is turned
  down by streaming services and then only sounds duller.
- `contour`: short-term loudness over time. `spread_lu` under 2 on a long piece means no
  section is louder or quieter than another; `by_tenth_lufs` shows where it builds and falls.
- `stereo`: `correlation` under 0 means more side than mid, and `mono_fold_db` is what a phone
  speaker loses; `low_correlation` under 0.7 means the bass is wide.
- `flags`: what to ask the listener to listen for. Each fired on a minority of 78 real AI renders
  (musicwright-produce: references/mixing.md); none of them says a take is good or bad.

## What to tell the listener

For each take: the file path, one line on what the sheet shows, the key numbers, any warning.
Then your ranking and why. Give the listener loudness-matched copies (`mw.py preview`), since a
copy even slightly louder is heard as better. End with what you could not check and what to
listen for:

1. The first 5 seconds: a real start, or mid-phrase? A click?
2. Instruments that were asked to stay out (a pad under a solo, drums in an ambient bed).
3. Melody: does it develop or repeat one bar? Does it sound like a song they know?
4. Artefacts: metallic or phasey vocals, smeared drums, warbling held notes, sizzle.
5. Timing: does the tempo drift, does the beat flip to half time?
6. The ending: resolved, faded, or cut off?
7. Fit: would it tire after 20 loops? Does it leave room for dialogue or sound effects?
8. Small speaker and low level: does it still work from `mw.py preview --as phone` and `--as
   quiet`? Is the bass still implied, the lead still clear?
9. Front to back: listen once through without stopping, half attending, and note where it
   loses you. Loops of a few bars hide what a whole play reveals.

Record their answer with `mw.py verdict` in their words. A verdict like "too harsh" or "loved
the breathy start" is the most valuable data this plugin collects.

## Checks a script can add

Built: mono compatibility and phase (`mw.py mixcheck`), loop seam (`mw.py seam`). Still by hand
(ai-docs/research/03-music-fundamentals.md R-226): DC offset (`astats`), tempo drift (beat
interval trend), tuning drift between takes that will be layered.
