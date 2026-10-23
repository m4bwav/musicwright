# Seamless loops

## Checklist

1. Whole bars: samples = bars x beats per bar x 60 / bpm x sample rate. At 120 bpm in 4/4 at 48 kHz,
   8 bars = 768,000 samples. `mw.py loop --bars --bpm` computes it.
2. Musical flow: the end leads back to the start (same chord, or a dominant into it).
3. Technical seam: crossfade the tail past the loop end into the head (best for AI audio with
   reverb), or cut both ends at rising zero crossings (sparse material only).
4. No fade-in, fade-out or silence inside the loop file.
5. Test: `mw.py seam` (ratio 2 or less is clean; a hard cut on a test tone scored 80, the
   crossfaded loop 0.9), then have someone listen to it three times through.

## How `mw.py loop` builds it

Source window S..E where E = S + loop length + X (X = crossfade). Output = (tail E-X..E fading out,
mixed with head S..S+X fading in) followed by S+X..E-X. Length = E - S - X = exactly the loop
length. The end of the file runs straight into the start of the file, because the start already
contains the tail. Equal-power (`qsin`) fades.

## Choosing the start

- Skip the intro swell: the first 5-15 s of an AI take is often a build.
- Prefer a downbeat. In the sheet, drum stripes give the beat spacing; at a known bpm, beats fall
  every 60 / bpm seconds from the first strong stripe.
- Try two or three starts and keep the best seam score; then ask a person.

## Intro then loop

Unity cannot play an intro once and then loop from file metadata. Ship two files: `intro.wav`
(ends exactly where the loop begins) and `loop.wav`, and stitch them with `PlayScheduled`
(unity.md). Make both from one take: `mw.py edit <take> --end <S> --out intro.wav` and
`mw.py loop <take> --start <S> --bars N --bpm B --out loop.wav`. Note the intro then has no
crossfade into the loop: start the loop on a clear downbeat.

## Layers from one piece

Vertical layering needs stems that share length and tempo: separate one master take with Demucs
or RoFormer (musicwright-produce references/stems.md), then cut every stem with the same
`--start --bars --bpm --xfade`. Check each stem's seam.

## Engines and tags

OGG `LOOPSTART` / `LOOPLENGTH` Vorbis comments are in samples (`mw.py loop --ogg` writes them).
RPG Maker reads them; Unity does not; Godot reportedly honours only a custom start. A
`music.json` deliverable entry carries the same numbers for any engine script.
