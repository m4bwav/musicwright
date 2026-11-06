# Music models by task (checked 2026-10-17)

"16 GB" = runs on a 16 GB consumer GPU (measured where marked). ComfyUI: native = core node,
partner = paid API node, custom = third-party pack. Sources and finding numbers (R-0xx) are in
ai-docs/research/01-models-landscape.md.

## Full songs and instrumentals

| Model | Open | Licence (outputs) | 16 GB | ComfyUI | Notes |
|---|---|---|---|---|---|
| ACE-Step 1.5 2B / XL 4B (base, sft, turbo) | yes | MIT; model card allows commercial use of outputs | yes, measured: 2B 10.4 GB, XL 12.9 GB peak | native | 10 s-10 min; cover, repaint; extract/lego/complete on base only (REST server; in ComfyUI cover through stock nodes, repaint through musicwright's AudioLatentRepaintMask node, `mw.py gen --task` on the XL recipes, and extract on acestep-xl-base through the vendored MW extract nodes, isolation unproven); LoRA; v0.1.8 (2026-05-18) |
| MiniMax Music 3 | open weights | MiniMax-Music3 Community Licence: free under USD 20M revenue, show "MiniMax-Music3" in the product UI, disclose AI output | yes (int8 text encoder, dynamic loading) | native | up to 5 min, 32 kHz; text-to-music only; takes often come back shorter than asked |
| YuE2-3B | open weights | CC BY-NC 4.0 plus creator permission: individuals may sell outputs, companies need a licence | unmeasured (24 GB stated) | native | lyrics + style through an editable ABC score; covers via SheetSage2 |
| Stable Audio 3 Small / Small-SFX / Medium | open weights (Large API-only) | Stability Community Licence: free under USD 1M revenue, you own outputs | likely (0.46B / 1.4B) | native | licensed training data; instrumental and SFX up to 6:20; no vocals; Large through resellers about USD 0.02 a take (WaveSpeed, 2026-11; Stability's own price unchecked); inpainting and continuation through stable-audio-tools `generate_diffusion_cond_inpaint` (HF card), no ComfyUI route seen, untested here |
| HeartMuLa-oss-3B | yes | Apache 2.0 | unknown | custom | songs, MuLaCover covers |
| DiffRhythm 1.2 / 2 | yes | Apache 2.0 | v1 yes (8 GB chunked) | custom | full songs; repo quiet |
| DiffSynth-Music (DiffSynth-Studio) | yes | Apache 2.0 | low-VRAM offload stated, unmeasured | none (Python, DiffSynth-Studio) | control templates on the ACE-Step 1.5 backbone: beats (click track), keep vocals and write the band, keep the band and write vocals, prosody, reference; ships its own track separator; HF card 2026-09 |
| MusicGen | weights NC | CC BY-NC 4.0 | yes | custom | non-commercial: not a default |
| Magenta RealTime 2 | yes | CC BY 4.0 weights, no claim on outputs | offline on NVIDIA | none | real-time only on Apple Silicon |
| ACE-Step 1.5 in C++ | acestep.cpp (MIT, GGML: CPU, CUDA, ROCm, Metal, Vulkan; text + lyrics to 48 kHz WAV or MP3) and acestep.vst3 (MIT, official, a DAW plugin built on it) | | | none | for a machine without Python or a DAW-side draft; unmeasured here |
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
| Stems | adefossez/demucs v4 (`htdemucs`, `htdemucs_ft`, `htdemucs_6s`) | MIT | upstream archived; the fork is the home, little maintenance; `uvx --with numpy demucs` (the package leaves numpy out) |
| Stems, best vocals | BS-RoFormer / Mel-RoFormer via python-audio-separator, ZFTurbo MSST, UVR | MIT code, weights vary | |
| Separate by text prompt | Meta SAM Audio | SAM Licence, gated | read the licence before commercial use |
| Voice conversion | RVC WebUI, Applio | MIT | never convert into a real singer's voice without consent |
| Singing synthesis | DiffSinger | Apache 2.0 | |
| Lyrics and captions from audio | ACE-Step Transcriber (HF ACE-Step/acestep-transcriber, MIT, audio-text-to-text) | MIT | untested here |
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

## Measured here

Measured 2026-11-02 on the RTX 5060 Ti 16 GB (weights from Comfy-Org/stable-audio-3 and Comfy-Org/YuE2,
ungated): Stable Audio 3 Medium, 8 steps lcm/simple cfg 1, a 60 s take in 9 s, exactly 60.0 s, -16.3 LUFS,
-1.9 dBTP. YuE2 3B int8 with ABC planning (template settings), 90 s asked, 78 s returned in 33 s, about
8.5 GB VRAM, -14.7 LUFS and +0.1 dBTP (master before use). A listener kept one take of each on 2026-11-03, so both are recipes
(`stable-audio3-medium`, `yue2-3b-int8`). Still unmeasured: any side-by-side listening test of ACE-Step against
MiniMax, or between these models.

## Stable Audio 3 captions

ComfyUI's template expands short ideas into one sentence in this order: genre and adjectives, main instruments, supporting layers, rhythm and percussion, mood woven in, then `BPM: X. Length: Y seconds`. It has separate versions for music, instrument, SFX and one-shot. Follow that shape by hand; not yet compared here by ear.
