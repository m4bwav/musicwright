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
- Vocals: 6-10 syllables a line, sections tagged, 50+ languages.
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
| bpm, keyscale, timesignature | set by brief | 30-300 bpm accepted; extremes unstable; 4/4 most reliable |
| duration | 10-600 s | 2-4 min is the stable zone |

## Timing (16 GB RTX 5060 Ti)

XL sft: about 80-100 s per 180 s track; 60 s takes in well under a minute each once loaded; a
600 s track about 10 min. The first job after a server start also loads about 10 GB of weights.
If the planner crawls (about 1.6 s per token in the server log instead of about 0.1), VRAM is
degraded: restart ComfyUI when nobody else is using it, then requeue.

## Audio as input

- Timbre/style reference (ComfyUI, native): LoadAudio → VAEEncodeAudio → `ReferenceTimbreAudio`
  between the text encoder and the KSampler, with `generate_audio_codes` false. Copies the sound,
  not the melody. Untested here.
- Cover, repaint, extend, extract: REST server ([acestep-rest.md](acestep-rest.md)).
- Only use reference audio the user owns or has licensed.
