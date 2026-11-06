# Research: musicwright-generate

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md. The first research pass is in the repository's [ai-docs/research](../../ai-docs/research/index.md).

Topic: AI music generation: models, licences, hosted APIs, ACE-Step and MiniMax prompting and parameters, re-roll strategy. Tier `fast`. Last refresh 2026-10-17; next due per `evergreen.json`.

## Current understanding

- ACE-Step 1.5 (2B, XL 4B) is MIT and its model card allows commercial use of outputs; XL sft through ComfyUI peaks about 12.9 GB on 16 GB; v0.1.8 (2026-05-18) is the latest release. Confidence high (R-013, R-014).
- MiniMax Music 3 open weights (2026-08) run natively in ComfyUI; licence needs on-product attribution and AI disclosure, free under USD 20M revenue (R-011, R-012).
- YuE2 (native nodes, ABC score layer) and Stable Audio 3 (licensed data, loops and SFX) are the next local engines to measure; neither is measured on 16 GB yet (R-015, R-021).
- Hosted: Lyria 3.5 USD 0.08 a song with SynthID; ElevenLabs Music USD 0.15 a minute, Enterprise needed for film, TV and studio games; Suno has no public API and caps downloads; Udio downloads are off (R-001 to R-009).
- Adding a part to an existing track: ACE-Step `lego` on a base checkpoint through the REST server (`mw.py gen --task lego --src --track`); native ComfyUI cannot. Source tasks must run with the planner off and, on base checkpoints, with DCW off (R-20261017-4, R-20261017-5, R-20261017-6). Lego plays along with the lead rather than answering it; `duck --stem` keyed by the lead shapes the answer, and a listener kept that route (R-20261017-6).
- Prompting: caption = sound, lyrics/sections = time; tempo and key in their fields; one caption holds one colour, so mood arcs are rendered as movements; cfg 4.5 er_sde linear_quadratic was preferred over cfg 7 euler by a listener (ACE-Step tutorial; local verdicts).
- Ownership: purely AI output is not copyrightable in the US; vendor 'you own it' clauses are contract terms (R-085, R-086).

## Open questions

- YuE2 and Stable Audio 3 Medium VRAM and time on 16 GB.
- MiniMax Music 3 against ACE-Step XL in a listening test.
- Can a caption or setting make lego answer in the rests rather than play along? (R-20261017-6: it plays along; ducking shapes the answer afterwards.)
- Tencent SongGeneration and SongBloom licences and homes.

## Search plan

Four tracks; every refresh runs at least one query on each, scoped to the time since the last refresh.

Subject:

- github.com/ace-step/ACE-Step-1.5 releases, docs/en/Tutorial.md and API.md; huggingface.co/MiniMaxAI/MiniMax-Music3; github.com/multimodal-art-projection/YuE; stability.ai news
- ai.google.dev/gemini-api/docs/music-generation and /pricing; elevenlabs.io/pricing/api; suno.com/pricing and /legal/terms
- `AI music lawsuit OR settlement OR licensing 2026` (Suno, Udio, GEMA); copyright.gov/ai
- Forums: github.com/ace-step/ACE-Step-1.5/discussions and issues; ComfyUI discussions (audio)

Tooling:

- `path:SKILL.md "AI music generation"` on GitHub code search, sorted by recently updated; `npx skills find "AI music generation"` and skills.sh weekly installs
- `https://registry.modelcontextprotocol.io/v0/servers?search=AI music generation`; fallback `"AI music generation" mcp server site:glama.ai OR site:pulsemcp.com`
- `"AI music generation" skill OR plugin OR "mcp server" 2026 site:github.com`; supersession sweep `"AI music generation" skill deprecated OR archived 2026`

Practice:

- `"claude code" OR codex OR cursor "AI music generation" "my workflow" 2026`; hn.algolia.com `search_by_date?query=AI music generation`
- Reddit r/aimusic, r/WeAreTheMusicMakers, r/gamedev RSS (reading through RSS only)

Testing:

- `music generation benchmark OR evaluation 2026` (SongEval, WildSongBench, MusicCaps)
- local timing and VRAM runs recorded in the ledger

Best sources: model cards and repos, vendor pricing and terms pages, court and regulator pages; trade press only as leads. Noisy: SEO 'best AI music generator' listicles and scraped directories.

## Findings log

### R-20261103-1 · 2026-11-03 · Quiet check

- Summary: ACE-Step-1.5 still at v0.1.8; no MiniMax Music successor; nothing new on YuE2 or ComfyUI audio nodes; Suno/Udio unchanged (no API, Udio downloads off). ElevenLabs Music list price still USD 0.15/min (a 50% OpenRouter launch discount ended 2026-10-19). Aggregator lists Stable Audio 3.0 hosted at USD 0.26/generation and Google tiers as 'Lyria 3 Pro' (USD 0.08/song) and 'Lyria 3 Clip' (USD 0.04/30 s): open question whether the main file's 'Lyria 3.5' name is right; confirm on ai.google.dev pricing. Tooling: nothing new. Testing: CMI-RewardBench v2 (arxiv 2603.00610) shows Gemini-2.5-Pro under 80% agreement with human preference, so LLM judges of takes stay a pre-sort only.
- Track: subject, tooling, testing
- Sources: github.com/ace-step/ACE-Step-1.5/releases; cometapi.com/ai-music-api-pricing; openrouter.ai audio collection; arxiv.org/html/2603.00610v2
- Magnitude: 0.15
- applied: none (note only)

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261017-6 · 2026-10-18 · Lego on base checkpoints: DCW, base against XL, percussion over free time
- Summary: (1) On ACE-Step servers that force DCW on, lego on a base checkpoint returns noise (issue #1259); PRs #1273 and #1282 resolve DCW from the model config and expose `dcw_enabled` in the API, so mw.py sends `dcw_enabled: false` for base-only tasks and the server should be at or after commit ca1e85f. (2) After the fix, lego on the 2B base returns the new part alone and centres on the source's tonal centre (the flute source sat in D although A minor was asked for). It does not answer in the rests: the part is about as loud in the lead's rests as under its notes, follows the lead's dynamics and plays on into the lead's silent tail. Ducking the part under the lead (`duck --stem`, ratio 3, threshold 0.02, attack 80 ms, release 700 ms) moved it about 4-5 dB toward the rests (`mw.py answer`: -4.8 dB to -0.4 dB for the kept seed). mw.py's REST route reproduced a direct-API take for the same seed. (3) XL base with `ACESTEP_OFFLOAD_TO_CPU=true` on a 16 GB card: 530 s for three 60 s takes including the load, peak 13.5 GB; one of its three seeds held a single tone for the whole take. 2B base: 16-25 s per 60 s take, peak 7.5 GB. (4) Percussion lego over a free-time solo invents its own grid: with bpm 66 in the metadata one seed held a steady 66 bpm, one was gridded at another tempo, one was sparse; without bpm it chose 83-112 bpm. No take followed the lead's note onsets better than chance (`mw.py pulse` reads the solo as no pulse). A beat under a free-time take needs a tempo-locked base (re-render the lead at a fixed bpm) or accents placed on phrases. (5) A listener kept both the plain and the ducked mix of the 2B base seed 8101 (the ducked one best) over the other seeds and over a part rendered without the source (which pulled in a bass and rhythm section or ignored the lead's breaths).
- Track: testing
- Sources: https://github.com/ace-step/ACE-Step-1.5/issues/1259, https://github.com/ace-step/ACE-Step-1.5/pull/1273, https://github.com/ace-step/ACE-Step-1.5/pull/1282, local runs 2026-10-17/18 on a 16 GB RTX 5060 Ti (ledger and verdicts in the owner's studio)
- Magnitude: moderate (a server-version requirement, a new step for adding a part, a kept recipe)
- Applied: C-20261018-1

### R-20261017-5 · 2026-10-17 · Adding a part to an existing track: routes
- Summary: ACE-Step 1.5 `lego` on a base checkpoint is the only open route found that generates a new stem conditioned on the user's own audio. Tasks by checkpoint: turbo and sft do text2music, cover and repaint; only `acestep-v15-base` (2B, 4.79 GB on Hugging Face) and `acestep-v15-xl-base` (4B, 19.95 GB as fp32 shards; about 10 GB as Comfy-Org's bf16 file) do `extract`, `lego` and `complete`. The docs put XL base at 24 GB or more; on 16 GB it needs CPU offload. REST fields: `task_type`, `track_name` (one of woodwinds, brass, fx, synth, strings, percussion, keyboard, guitar, bass, drums, backing_vocals, vocals; a flute is `woodwinds`), `track_classes` for complete, `repainting_start`/`repainting_end` as the window, `audio_cover_strength` for cover, `model`, `inference_steps` (server default 8, base wants 50), `guidance_scale` (default 7.0). The server refuses absolute `src_audio_path` values outside its temp folder, so the source is uploaded as multipart field `src_audio`; the other fields can travel as one JSON `param_obj` form field. Native ComfyUI has no source tasks: `ReferenceTimbreAudio` only attaches timbre latents, and the Comfy tutorial says cover and repaint are not supported. ComfyUI_RyanOnTheInside has `ACEStep15NativeLegoGuider` (needs a restart and a base file in ComfyUI's format); ComfyUI-AceMusic wraps ACE-Step v1 and has no lego. YuE2 edits regenerate the whole recording (CC BY-NC weights); Stable Audio 3 inpaints and continues but has no stem conditioning; MiniMax Music 3 takes no audio. Hosted: Suno Studio (Premier) adds parts to imported audio; ElevenLabs inpainting replaces sections and does not layer; Lyria takes no audio; Udio downloads are off. Lego history: noise and unsynced output in issues #311, #369, #1048, #1255; fixes #810 (2026-03) and #1287 (2026-08-16).
- Track: subject
- Sources: github.com/ace-step/ACE-Step-1.5 docs/en/INFERENCE.md (Lego, Complete), docs/en/API.md, docs/en/Tutorial.md (DiT selection), acestep/constants.py (TRACK_NAMES, TASK_INSTRUCTIONS), acestep/api/http/release_task_audio_paths.py; huggingface.co/api/models/ACE-Step/acestep-v15-base and -xl-base; docs.comfy.org/tutorials/audio/ace-step/ace-step-v1-5; github.com/ryanontheinside/ComfyUI_RyanOnTheInside; github.com/hiroki-abe-58/ComfyUI-AceMusic; help.suno.com/en/articles/7940161; elevenlabs.io/docs/eleven-api/guides/how-to/music/inpainting (all checked 2026-10-17)
- Magnitude: moderate (new capability: mw.py gen --task)

### R-20261017-4 · 2026-10-17 · Lego ignores the source when the planner runs (before #1287)
- Summary: with `thinking` true, servers older than ACE-Step PR #1287 (merged 2026-08-16) let the 5Hz LM write audio codes from the text alone for `lego` and `complete`; those codes pre-empt the source ("Audio codes provided, ignoring src_audio"), so the new part never hears the track. #1287 skips the LM for both tasks as an interim default. A client can get the same effect on any server version by sending `thinking: false` with `use_cot_caption` and `use_cot_language` false; mw.py does this for every source task.
- Track: subject
- Sources: github.com/ace-step/ACE-Step-1.5 commit 14c0211 (PR #1287) message and tests (checked 2026-10-17)
- Magnitude: moderate

### R-20261017-3 · 2026-10-17 · Recipe check on a solo-instrument brief
- Summary: Three seeds of the default XL recipe for an unaccompanied flute: two came out solo, one added a low drone. Seed variance, not the caption, decided it; keep the fish-then-lock workflow.
- Track: testing
- Sources: local run 2026-10-17
- Magnitude: n/a (initial)
- Applied: C-20261017-1

### R-20261017-2 · 2026-10-17 · Tooling: official vendor skills and MCP servers
- Summary: ElevenLabs ships an official music skill and MCP (music_v2_5); MiniMax ships an MCP; ace-step publishes ace-step-skills; calesthio/generative-media-skills covers several providers. Every Suno MCP is unofficial. See research 02 R-131 to R-136.
- Track: tooling
- Sources: https://github.com/elevenlabs/skills, https://github.com/ace-step/ace-step-skills
- Magnitude: n/a (initial)
- Applied: C-20261017-1

### R-20261017-1 · 2026-10-17 · Model landscape, first pass
- Summary: Full table of models by task, licence, 16 GB fit and ComfyUI support, plus legal and platform rules: ai-docs/research/01-models-landscape.md (R-001 to R-097). Changes to earlier local notes: ACE-Step 1.5 is MIT, not Apache 2.0; MiniMax Music 3 is open weights under its own community licence, not CC BY-NC.
- Track: subject
- Sources: https://github.com/ace-step/ACE-Step-1.5, https://huggingface.co/MiniMaxAI/MiniMax-Music3/blob/main/LICENSE, https://ai.google.dev/gemini-api/docs/music-generation
- Magnitude: n/a (initial)
- Applied: C-20261017-1


### R-20261102-2 · 2026-11-02 · Sources pass 2: Essentia, MidiTok, AudioCraft, Stable Audio API

- Essentia: PyPI still ships only 2.1b6 dev builds; AGPL rule in models.md stands; nothing it adds over librosa and beat_this for mw.py today.
- MidiTok 3.1.0 (Python >=3.10): a tokenizer for training symbolic models; no use in a plugin that does not train. No change.
- AudioCraft 1.3.0: MusicGen weights still CC BY-NC; models.md row correct. No change.
- Stable Audio 3 Large: API-only; resellers list about USD 0.02 a take (WaveSpeed text-to-audio, async poll). Stability's own price page not found. Added to the models.md row.
- Hugging Face transformers audio docs: not read this pass (moved to pass 3).


### R-20261102-3 · 2026-11-02 · Sources pass 3: Hugging Face transformers audio docs, IT-JIM blog

- transformers text-to-audio docs: the `"text-to-audio"` pipeline now leads with speech models (CSM, Dia, Bark, VITS); its install line needs `torchcodec`, matching research 04's torchaudio 2.9 note. MusicGen through transformers carries the same CC BY-NC weights as AudioCraft. No change.
- IT-JIM blog: no post on ACE-Step, LeVo or YuE found by search; the list's claim is unverified. Skipped.
- Gap noted, not acted on: LeVo (Tencent SongGeneration) is absent from models.md; a SongEval leaderboard (wizwand.com) puts it level with YuE. Add a row only after its licence and a local run are checked.

### R-20261102-4 · 2026-11-02 · Sources pass 4: Torin Hopkins, MusicMakerApp, Kingy AI

- Torin Hopkins (CU Boulder ATLAS): a researcher (AIMC 2023 papers on AI jam partners, AR drumming), not a resources page; nothing on model use or prompting. Skipped.
- MusicMakerApp: a hosted Suno-style text and lyrics to song app; no "Creation Lab" or vendor prompt guide found. Skipped.
- Kingy AI (kingy.ai): tool profiles and video summaries of Suno, Udio, Mureka, Musick AI, MusicGen; self-described as partly sponsored. Nothing the hosted-model notes lack. No change.

### R-20261102-5 · 2026-11-02 · Sources pass 5: Artlist, Mubert, Artificial Analysis

- Artlist help and blog: text-to-music runs Google Lyria 3; prompt template genre + mood + instruments + tempo/energy + structure + use case (matches the caption guidance); licence per plan, official licence text not found. Row added to hosted.md.
- Mubert: API v3 with Company_ID and License_Token, 150+ channels; royalty-free and sub-licensing claimed by the vendor (github.com/MubertAI/skills, mubert.com blog). Third-party tutorials still show the retired v2 endpoint. Row added to hosted.md.
- Artificial Analysis Music Arena v1.1 (instrumental): Suno v6 1148 leads, Lyria 3.5 1078, Stable Audio 3 Large 1014, MiniMax Music 3.0 1000; ACE-Step and YuE absent. Added as an outside ranking in hosted.md, dated.

### R-20261102-7 · 2026-11-02 · Sources pass 7: awesome-ai-music lists, r/ArtificialInteligence

- GitHub lists: Curated-Awesome-Lists/awesome-ai-music-generation (503 stars, mostly old research repos) and wildminder/awesome-ai-music (per-model pages with ComfyUI node packs, quants and LoRAs; the better index). New to models.md, each checked at its repo or HF card: DiffSynth-Music (Apache 2.0, control templates on ACE-Step 1.5), acestep.cpp and the official acestep.vst3 (MIT), ACE-Step Transcriber (MIT). Neither list names a ComfyUI node pack with ACE-Step extract, so item 7 extract is unchanged.
- r/ArtificialInteligence search RSS for music (top of month) returned nothing. Hugging Face audio discussions skipped: no single forum; the per-model community tabs are covered by the model checks.

### R-20261102-8 · 2026-11-02 · Sources pass 8: Gearspace, Kaggle, Stability audio news

- Gearspace AI subforum and Kaggle audio forums: searches found no relevant threads (KVR threads instead, opinion only). One vendor-blog figure (raw Suno export near -11 LUFS short-term against -7 to -8 for a commercial rock master) adds nothing the produce loudness presets lack.
- Stable Audio 3 (released 2026-05-20, arXiv 2026-05-18): the Medium HF card says it supports inpainting and continuation, through stable-audio-tools `generate_diffusion_cond_inpaint`; the card shows no mask input and no ComfyUI route. Added to the models.md row as a possible second repaint route, untested.

### R-20261102-9 · 2026-11-02 · Sources pass 9: Meta AI, Google Magenta, Hugging Face audio posts

- Meta AI: no audio or music model since AudioCraft/MusicGen; the MusicGen row (CC BY-NC weights) stands.
- Google Magenta: Magenta RealTime 2 (2026-06-04, google/magenta-realtime-2, CC BY 4.0, 2.4B Base and 230M Small, 48 kHz stereo, ~200 ms control latency, text/audio/MIDI steering) is already in models.md; HF API confirms the licence tag. Lyria stays hosted only.
- Hugging Face blog: no 2026 music post found. LeVo 2 (Tencent SongGeneration v2-large, released 2026-03-01) surfaced again; its licence is a custom Tencent file ("Other" on HF) that could not be read (GitHub 404, HF 401 without login), and third parties disagree on commercial use. No models.md row until the licence is read from the source.

### R-20261102-10 · 2026-11-02 · Sources pass 10: OpenAI research, Sound on Sound, Music Business Worldwide

- OpenAI: no released music model; only October 2025 reports (The Information) of one in development (text and audio prompts, Juilliard score annotation). No models.md row.
- Sound on Sound: no AI mastering or separation article surfaced; search returned vendor blogs only. No change.
- Music Business Worldwide: Udio licensed by UMG (2025-10), Warner (2025-11), Merlin, Kobalt (2026-04) and NMPA (2026-06); Sony none; downloads still off, licensed platform not launched (2026-11). Suno: Warner deal 2025-11 (licensed models promised in 2026), UMG and Sony talks stalled (FT 2026-04). hosted.md Udio and Suno rows updated.

### R-20261102-11 · 2026-11-02 · Sources pass 11: Towards Data Science audio, Synthtopia

- Towards Data Science: the music and audio pieces found are 2023-2024 explainers (Landschoot's audio diffusion intro and Tiny Audio Diffusion, a MusicLM overview); nothing on current models. No change.
- Synthtopia: AI items are instruments and synth tools (SPIN on MusicGen, Combobulator, sonicLAB Fundamental 4.1 with text-to-preset and an MCP server, MicroMusic), not music generators. No change; group 4 blogs done.

### R-20261105-1 · 2026-11-05 · Round two, group 7: ACE-Step community

Read: 13 of the 70 most-commented issues (400 listed), 11 of 112 discussions, DCW.md and the start of ALT_VAE.md, and keyword scans (not full reads) of Tutorial.md, the Musician's Guide and INFERENCE.md.

- Issues #424, #677: planner rewrites captions; #1277: no chord control; #972, discussions #1250, #1252: cover does not keep a melody. Into acestep.md.
- Discussion #1268 (one user's A/B day, 1-3 runs per condition, Apple Silicon): static harmony on EDM captions, keyscale clearing clashes, duration padding. Into acestep.md as reports, untested here. Also, not added: `use_adg` is implemented for xl-sft though docs say base only; INFERENCE.md gives shift both ways for sft, and seeds outweighed it; `retake_seed` with `retake_variance` 0.3 explores near a good seed. Candidates if the REST route needs them; `--set` can already pass them.
- Issues #1259, #1288, #1299: noise from sft and base through ACE-Step's own pipeline is DCW, fixed by #1273 and #1282. ComfyUI was unaffected. Fits the ComfyUI-first ruling.
- Discussions #1256, #1364: rights questions unanswered by maintainers. The repository LICENSE, two model cards and the Space LICENSE are MIT with no output clause; the clause the askers quote was not found, and may sit somewhere not read. Noted in licences.md.
- ALT_VAE.md: ScragVAE, an MIT community VAE selectable on the Python route. Discussion #1366: latent-init reference in ComfyUI matches the cover denoise route. No change; ScragVAE is a listening-test candidate. Discussion #1372 is a vendor's demo: skipped. Issue #1280: the maintainer says the project is still maintained; latest tagged release v0.1.8, 2026-05-18, against commits since.
- Not read: the remaining issues, mostly install, LoRA and GPU reports; LoRA training is outside the skill.
