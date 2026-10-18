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

