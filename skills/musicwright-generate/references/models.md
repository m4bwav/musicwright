# Music models by task (checked 2026-10-17)

"16 GB" = runs on a 16 GB consumer GPU (measured where marked). ComfyUI: native = core node,
partner = paid API node, custom = third-party pack. Sources and finding numbers (R-0xx) are in
ai-docs/research/01-models-landscape.md.

## Full songs and instrumentals

| Model | Open | Licence (outputs) | 16 GB | ComfyUI | Notes |
|---|---|---|---|---|---|
| ACE-Step 1.5 2B / XL 4B (base, sft, turbo) | yes | MIT; model card allows commercial use of outputs | yes, measured: 2B 10.4 GB, XL 12.9 GB peak | native | 10 s-10 min; cover, repaint; extract/lego/complete on base; LoRA; v0.1.8 (2026-05-18) |
| MiniMax Music 3 | open weights | MiniMax-Music3 Community Licence: free under USD 20M revenue, show "MiniMax-Music3" in the product UI, disclose AI output | yes (int8 text encoder, dynamic loading) | native | up to 5 min, 32 kHz; text-to-music only; takes often come back shorter than asked |
| YuE2-3B | open weights | CC BY-NC 4.0 plus creator permission: individuals may sell outputs, companies need a licence | unmeasured (24 GB stated) | native | lyrics + style through an editable ABC score; covers via SheetSage2 |
| Stable Audio 3 Small / Small-SFX / Medium | open weights (Large API-only) | Stability Community Licence: free under USD 1M revenue, you own outputs | likely (0.46B / 1.4B) | native | licensed training data; instrumental and SFX up to 6:20; no vocals |
| HeartMuLa-oss-3B | yes | Apache 2.0 | unknown | custom | songs, MuLaCover covers |
| DiffRhythm 1.2 / 2 | yes | Apache 2.0 | v1 yes (8 GB chunked) | custom | full songs; repo quiet |
| MusicGen | weights NC | CC BY-NC 4.0 | yes | custom | non-commercial: not a default |
| Magenta RealTime 2 | yes | CC BY 4.0 weights, no claim on outputs | offline on NVIDIA | none | real-time only on Apple Silicon |
| Tencent SongGeneration, SongBloom | unclear | official repos gone or 404 | | custom | do not depend on them |
| Lyria 3.5 / 3 Clip / RealTime | hosted | Gemini API terms, SynthID watermark | n/a | none | USD 0.08 a song, 0.04 a 30 s clip; RealTime experimental, instrumental |
| ElevenLabs Music v2.5 | hosted | paid plans commercial, but film, TV and studio games need Enterprise | n/a | partner (SFX and speech only) | USD 0.15 a minute; stems, inpainting |
| Suno v6 / v6-wild / v6-mini | hosted | paid tiers get rights within a monthly download cap; remixes non-commercial | n/a | none | no public API; downloads capped (Pro 20, Premier 60 a month) |
| Udio | hosted | downloads disabled since 2025-10-29 | n/a | none | |

Local default order: ACE-Step XL, then MiniMax Music 3, YuE2 for score-led songs, Stable Audio 3
for loops and SFX.

## Editing and analysis

| Task | Tool | Licence | Note |
|---|---|---|---|
| Stems | adefossez/demucs v4 (`htdemucs`, `htdemucs_ft`, `htdemucs_6s`) | MIT | upstream archived; the fork is the home, little maintenance |
| Stems, best vocals | BS-RoFormer / Mel-RoFormer via python-audio-separator, ZFTurbo MSST, UVR | MIT code, weights vary | |
| Separate by text prompt | Meta SAM Audio | SAM Licence, gated | read the licence before commercial use |
| Voice conversion | RVC WebUI, Applio | MIT | never convert into a real singer's voice without consent |
| Singing synthesis | DiffSinger | Apache 2.0 | |
| Transcription to MIDI | MuScriptor (2026-07, weights licence unstated), MT3, basic-pitch | Apache 2.0 (MT3, basic-pitch) | |
| Beats, tempo, key | beat_this (MIT), librosa, Essentia (AGPL: call it, never vendor it) | | |
| Captioning | Music Flamingo, Qwen3-Omni, ACE-Step's LM | research licences | |
| Mastering | Matchering 2 (GPL-3.0, reference mastering), ffmpeg loudnorm | | |
| Sound effects | Stable Audio 3 Small-SFX, MMAudio (video to SFX), ElevenLabs SFX (USD 0.12 a minute) | | |

## ComfyUI audio nodes (0.38.2)

Native: ACE-Step 1.0 and 1.5 (`TextEncodeAceStepAudio1.5`, `EmptyAceStep1.5LatentAudio`,
`ReferenceTimbreAudio`), YuE2 (`YuE2GenerateABC`, `YuE2GenerateMusic`, `SheetSage2AudioToABC`),
MiniMax Music 3 (`MiniMaxMusic3TextEncode`, `EmptyMiniMaxMusic3LatentAudio`), Stable Audio;
LoadAudio, SaveAudio (FLAC), SaveAudioMP3, SaveAudioOpus, TrimAudioDuration, AudioConcat,
VAEDecodeAudioTiled. Partner: ElevenLabs (no music node), Sonilo (music). No Lyria, Suno or
Udio nodes. Templates ship for every native model (`audio_*` in the workflow templates).

## Not yet measured here

YuE2 and Stable Audio 3 Medium on 16 GB; MiniMax Music 3 timings with recorded settings;
any side-by-side listening test of ACE-Step against MiniMax. Add a recipe when one is run and judged.
