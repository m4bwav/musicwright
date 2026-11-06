# ACE-Step 1.5 prompting and parameters

Applies to the XL models through ComfyUI (`acestep-xl-sft`) and the 2B model through the REST
server. Upstream guide: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md

## Caption (ComfyUI `tags`, REST `prompt`)

Dimensions the model reads: style/genre, emotion, instruments, timbre texture, era and
production, vocal character, speed/rhythm feel, structure hints ("fade-out ending", "slow build").

- Comma-separated tags work well. Aim for 4+ dimensions, 15-35 tags.
- Repeat the most important element in other words ("solo flute ... single melodic line ...
  unaccompanied") so it survives.
- Contradictions get fused badly: "dark ambient" plus "happy pop" gives mush. Put contrast in time
  (sections or separate movements).
- Over-stacked tags can be sung as lyrics in vocal tracks. Keep vocal captions lean.
- Write the caption yourself. The planner's main job is audio codes, and the maintainer points people at custom mode or a bigger model for words; its "Enhance Caption" and simple mode have changed genre and language in several reports (issues #424, #677).
- EDM and house captions can sit on one chord for minutes. Adding "evolving sections, varied and moving chord harmony" fixed it in one user's A/B test, while seed, strength and guidance did not (discussion #1268; small sample, not tried here).
- A chord progression in the caption or lyrics gives no reliable bar-level control, says the maintainer (issue #1277). For exact chords use notation and `mw.py render`, then cover.
- Leaving an instrument out by asking is unreliable (discussion #1071, one report): name what plays instead.

Examples that a listener kept:

```
melodic mid-tempo electronica, clean bright electric guitar melodies, warm analog synth pads,
round bass, organic electronic drums, sunny, nostalgic, hopeful, hi-fi, polished, smooth,
expressive flute lead throughout, instrumental
```
(bpm 96-112, major keys, 180 s, six sections ending "[Outro - fade out]")

```
solo flute, unaccompanied Native American cedar flute, shakuhachi-inspired breathy wooden tone,
single melodic line, pentatonic melody, ornamental grace notes, gentle breath vibrato, long
sustained notes with pauses, natural canyon reverb, intimate close-miked recording, meditative,
serene, spacious, contemplative, instrumental
```
(66 bpm, A minor, 60 s; one of three seeds still slipped a low drone under the flute: re-roll seeds)

## Lyrics field (`lyrics`)

- Instrumental: `[Instrumental]`, or a section map such as `[Intro - guitar swells]` blank line
  `[Groove - drums enter]` ... `[Outro - fade out]`.
- Tags the model knows: [Intro] [Verse] [Pre-Chorus] [Chorus] [Bridge] [Outro] [Build] [Drop]
  [Breakdown] [Instrumental] [Guitar Solo] [Piano Interlude] [Fade Out] [Silence]; one modifier
  after a hyphen.
- Vocals: 6-10 syllables a line, sections tagged, 50+ languages; stressed syllables on strong
  beats (musicwright-compose: vocabulary.md, "Lyrics that sing").
- Tags that say who plays carry the arrangement: `[Intro - pad and kick only]`, `[Build - layers
  enter]`, `[Breakdown - drums drop out]`, `[Drop - full band]`, `[Outro - layers leave in reverse
  order]`, with the outro mirroring the intro. From the arrangement books (DeSantis ch. 72, 75);
  not yet compared against mood-only tags in a listening test here.
- For a real ending inside one render, ask for 10-15 s more than the target and name the ending in the caption; an exact `duration` cut off mid-fade twice in one user's test (discussion #1268).
- An ending holds up better as its own short render with an ending in its caption, joined with
  `mw.py join`, than as a trim of a render that just stops.
- How much section tags steer is disputed: they helped 3-minute instrumentals, but did not shape
  a 48 s mood arc or a 2-minute loudness curve. Shape short cues in post.

## Parameters (ComfyUI graph)

| Node / field | Default (`acestep-xl-sft`) | Effect |
|---|---|---|
| KSampler cfg | 4.5 | adherence vs harshness; 7 is the template default and can sound harsh |
| sampler / scheduler | er_sde / linear_quadratic | smoother than euler/simple at the same steps |
| steps | 50 | XL sft/base; turbo uses 8 |
| ModelSamplingAuraFlow shift | 3.0 | higher = firmer, lower = looser |
| planner (clip_name2) | qwen_1.7b_ace15 | 0.6B fast, 4B smarter but crowds a 16 GB card beside the XL DiT |
| LM cfg_scale | 2.0 | raise to 3 when the caption is ignored |
| LM temperature | 0.85 | 1.0 for more variety |
| bpm, keyscale, timesignature | set by brief | 30-300 bpm accepted; extremes unstable; 4/4 most reliable. Set keyscale even when it does not matter to the brief: it cleared major against minor clashes between parts in one user's test (discussion #1268) |
| duration | 10-600 s | 2-4 min is the stable zone |

## Control map: change only the wrong level

| Level | Controls | Use when |
|---|---|---|
| global | caption (`tags` / `prompt`), style words, bpm, keyscale, LM temperature | the whole take is off-brief |
| per section | section tags in `lyrics`, `repaint` with `--start`/`--end` | one passage is wrong, the rest is kept |
| per stem | `lego`, `complete`, `extract` with `--track` ([acestep-rest.md](acestep-rest.md)) | one part is wrong or missing |

Fix at the narrowest level that is wrong: re-captioning a whole take to mend one bar throws away
what worked (after Foster, *Generative Deep Learning* 2e, ch. 11, on separate control levels).

## Timing (16 GB RTX 5060 Ti)

XL sft: about 80-100 s per 180 s track; 60 s takes in well under a minute each once loaded; a
600 s track about 10 min. The first job after a server start also loads about 10 GB of weights.
If the planner crawls (about 1.6 s per token in the server log instead of about 0.1), VRAM is
degraded: restart ComfyUI when nobody else is using it, then requeue.

## Audio as input

- Timbre/style reference (ComfyUI, native): LoadAudio → VAEEncodeAudio → `ReferenceTimbreAudio`
  between the text encoder and the KSampler, with `generate_audio_codes` false. Copies the sound,
  not the melody. Untested here.
- Cover, repaint, extend, extract: REST server ([acestep-rest.md](acestep-rest.md)). In ComfyUI: cover and repaint on the XL recipes, extract on `acestep-xl-base` (`mw.py gen --recipe acestep-xl-base --task extract --src mix.wav --track drums`) through the MW nodes vendored in `comfy_nodes/musicwright_nodes/acestep15` (MIT, from ComfyUI_RyanOnTheInside). 15 s warm for 30 s. The source must hold the part: on a mix with no clear drums or vocals both takes came out nearly the same (correlation 0.97); on a punk mix with both they separated (0.02) and a listener rated each as mostly that part alone (2026-11-03), though near the end of the drums the cymbals sounded a little too much like a synth note, heard as a leak (2026-11-04), so listen to the end of a take before relying on it. Cover follows the source's semantic hints unless `--strength` is given (MWAceStep15CoverGuider; see acestep-rest.md).
- Cover keeps structure and feel, not the tune: the maintainer says it does not preserve a melody note for note (issue #972), and users report either a near copy or a different song (discussions #1250, #1252). To keep a melody, try the hint cover, compare strengths on one seed, and judge by ear. YuE2 has a route built for it: ComfyUI's `audio_yue2_music_cover` template transcribes the melody with SheetSage2 into an editable ABC score, then sings new style and lyrics over it (non-commercial terms for companies, not run here, not in `mw.py gen`).
- Only use reference audio the user owns or has licensed.
