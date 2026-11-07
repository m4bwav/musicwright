# Seamless loops

## Checklist

1. Whole bars: samples = bars x beats per bar x 60 / bpm x sample rate. At 120 bpm in 4/4 at 48 kHz,
   8 bars = 768,000 samples. `mw.py loop --bars --bpm` computes it.
2. Musical flow: the end leads back to the start (same chord, or a dominant into it), with the same
   instruments, volume and tempo. Reverse any palette change before the loop point. Nothing stands out
   unless it recurs. Joins that hide well: a vamp at both ends, a phrase's second half at the start and
   first half at the end, one progression split across the join.
3. Technical seam: crossfade the tail past the loop end into the head (best for AI audio with
   reverb), or cut both ends at rising zero crossings (sparse single loops only: a snap changes the
   length, so synchronized layers drift further apart each pass; the slope must match too).
4. No audible fade of the whole mix and no silence at the file edges or loop boundary. Composed rests
   mid-loop are fine, and a fade of a few samples at each end of a sparse hard cut is fine.
5. Test: `mw.py seam` (ratio 2 or less is clean; a hard cut on a test tone scored 80, the
   crossfaded loop 0.9), on the encoded file you ship as well as the WAV, then have someone listen to
   it three times through.

## How `mw.py loop` builds it

Source window S..E where E = S + loop length + X (X = crossfade). Output = (tail E-X..E fading out,
mixed with head S..S+X fading in) followed by S+X..E-X. Length = E - S - X = exactly the loop
length. The end of the file runs straight into the start of the file, because the start already
contains the tail. Equal-power (`qsin`) fades.

## Choosing the start

- Skip the intro swell: the first 5-15 s of an AI take is often a build.
- Prefer a downbeat. In the sheet, drum stripes give the beat spacing; at a known bpm, beats fall
  every 60 / bpm seconds from the first strong stripe.
- Transients hide a seam; legato exposes it. Prefer a start on a percussive hit, avoid a crash or long
  note crossing the point. Rhythmic takes loop easily; an ambient take that fails needs a longer
  crossfade rather than another start.
- Cut every loop of a set at the same musical place.
- A wrapped tail has no source on the first pass, so it can read as dissonance when the end and start
  chords differ. Matching pitch and instrument at both ends cures it.
- Try two or three starts and keep the best seam score; then ask a person.

## Intro then loop

Unity cannot play an intro once and then loop from file metadata. Ship two files, `intro.wav` and
`loop.wav`, and stitch them with `PlayScheduled` (unity.md). Make both from one take, with L the loop
length in seconds: `mw.py loop <take> --start <S> --bars N --bpm B --out loop.wav`, then
`mw.py edit <take> --end <S+L> --out intro.wav`. The loop file opens on the take's own audio at S+L
crossfading into S, so the join with an intro cut there is continuous and the first pass is the
untouched take. An intro cut at S instead hits the loop's fading-in head and foreign tail. It costs
one pass of file size.

## Layers from one piece

Vertical layering needs stems that share length and tempo: separate one master take with Demucs
or RoFormer (musicwright-produce references/stems.md), then cut every stem with the same
`--start --bars --bpm --xfade`. Check each stem's seam. **Never master stems one by one:** loudness
normalisation breaks their balance. Master the full mix, take that gain from `mw.py measure` before and
after, and apply the one gain to every stem. Design rules for layers: interactive.md.

## Engines and tags

OGG `LOOPSTART` / `LOOPLENGTH` Vorbis comments are in samples (`mw.py loop --ogg` writes them).
RPG Maker reads them; Unity does not; Godot reportedly honours only a custom start. A
`music.json` deliverable entry carries the same numbers for any engine script.

Web (WebAudio): loop with `AudioBufferSourceNode.loop`, not an `<audio loop>` element. Lossy files
carry encoder padding, so decode the shipped file in the target browser (`decodeAudioData`) and check
the buffer length equals the rendered loop's sample count; any extra samples are a gap at the seam.
One maker shipped a gapless 21 s AAC loop this way in Chrome (2026-10-29, RESEARCH R-20261029-1).
For loops synthesised in code, mix notes into a circular buffer so tails wrap into the head, and run
reverb and filters over two passes for the same reason.

`mw.py seam FILE --chords` also compares the notes in the last and first second. It is uncalibrated: a low similarity can still be a good chord change, so use it to choose what to listen to. `mw.py loop --bits 24` writes 24-bit WAV; the default 16-bit is dithered.
