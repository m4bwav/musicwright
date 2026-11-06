---
kind: research
status: active
date: 2026-11-02
title: Sources to mine for improvements (read before a mining pass or a skill refresh's search plan)
tags: research,sources,mining
---

# Sources to mine

The owner handed over a list of forums, tutorial sites, books, blogs and docs on AI music generation on 2026-11-02 (written by another AI, unverified) and asked that they be mined for improvements. Each pass takes a few sources, reads what is new, and records findings as numbered R- entries in a research note or a skill's RESEARCH.md, with a change in a skill only when a finding names something the skills lack or get wrong. Mark sources done below with the date.

Already covered by earlier passes (research 01 to 03): Demucs, Essentia, Magenta, Stability's models, Suno and Udio terms. Mine those only for what changed.

## Access

- Reddit: only the public RSS feeds work (`https://www.reddit.com/r/<sub>/top/.rss?t=month`), one request every 30 to 60 s; JSON and WebFetch are refused. Never use Arctic Shift.
- Discord servers (Suno, Udio, AudioCraft): not readable from here. Skip unless the owner pastes threads.
- Paywalled books: use the owner's copies through readwright if he has them; otherwise tables of contents and publisher samples only.

## Order (most likely to pay off first)

1. Docs that touch code musicwright runs or could run: Hugging Face transformers audio docs, torchaudio docs (note: 2.9 needs TorchCodec, research 04), Demucs, librosa, Essentia, MidiTok, AudioCraft, Stable Audio API.
2. Tutorial and technical sites: IT-JIM blog (ACE-Step, LeVo, YuE tests), Torin Hopkins' AI music resources, MusicMakerApp Creation Lab, Kingy AI, Artlist and Mubert guides (licensing, prompt structure), Artificial Analysis audio benchmarks.
3. Forums: r/SunoAI, r/udiomusic (the list's "r/UdIO"; check the real name), r/ArtificialInteligence music threads, Hugging Face audio discussions, GitHub awesome-ai-music lists, Gearspace AI subforum, Kaggle audio forums.
4. Blogs: Stability Audio, Meta AI, Google Magenta, Hugging Face audio posts, OpenAI research, Sound on Sound tech, Music Business Worldwide (law and licensing; feeds generate's licence notes), Towards Data Science audio tag, Synthtopia.
5. Books, most relevant first: Müller, *Fundamentals of Music Processing*; Farnell, *Designing Sound*; Nierhaus, *Algorithmic Composition*; Dean (ed.), *The Oxford Handbook of Computer Music*; Zölzer, *Digital Audio Signal Processing*; Dodge, *Computer Music*; Foster, *Generative Deep Learning*. Low value for this plugin: Müller and Guido, Géron, Petzold's *Code*.
6. Courses (Coursera, Kaggle Learn, Soundfly, Ableton Learning Music): skim the syllabus for any check or technique the skills lack; do not take them.

## Round two (queued 2026-11-05, owner's request)

Round one was shallow: several sites had nothing, Reddit was one top-of-month read of two subs, and most books were judged from contents lists. Round two goes deeper, in this order, a few sources per session. Same rules: findings as R- entries, skill changes only for real gaps, each source marked done below with what was actually read. "Not found" or "blocked" is recorded as that, never as "no gaps".

7. ACE-Step community: GitHub issues and discussions on the ACE-Step 1.5 repository (settings, failures, fixes), then its docs and tutorials.
8. ComfyUI music: workflows and tutorials for ACE-Step, Stable Audio and YuE2, ComfyUI's own docs and blog, community workflow sites; compare with the recipes and `comfy_nodes`.
9. Reddit through RSS at the pace above, top of the month and top of the year where the feed allows: r/comfyui, r/StableDiffusion, r/LocalLLaMA (music threads), r/SunoAI and r/udiomusic again (prompt craft), r/mixingmastering, r/audioengineering, r/GameAudio, r/WeAreTheMusicMakers. Check each sub exists and is active; drop dead ones. Then see whether an everscout beat already covers AI music. If none does, set the case out for the owner in HANDOFF; do not create one unasked.
10. Tutorial sites, found afresh by search instead of from the old list: prompt and lyric-tag guides for local models, game-audio sites on loops and adaptive music, film-scoring and mastering tutorials. Prefer sites showing settings and results over sponsored roundups.
11. Free textbooks: Open Music Theory for compose; anything else open found during 10.
12. Books the owner obtains, through readwright and the books process in the owner's private notes. Wanted, in order: Muller, *Fundamentals of Music Processing* (settles the chord, DTW and HPSS candidates); Phillips, *A Composer's Guide to Game Music*; Sweet, *Writing Interactive Music for Video Games*; Karlin and Wright, *On the Track*; Katz, *Mastering Audio*; Senior, *Mixing Secrets for the Small Studio*; Pattison, *Writing Better Lyrics*. Waits on the owner; do what is on disk and carry on without the rest. Never download a pirated copy.

## Done

- 2026-11-02: torchaudio, Demucs, librosa (R-20261102-1 in the produce RESEARCH.md: `uvx demucs` needs `--with numpy`). Next in group 1: Hugging Face transformers audio docs, Essentia, MidiTok, AudioCraft, Stable Audio API.
- 2026-11-02: Essentia, MidiTok, AudioCraft, Stable Audio API (R-20261102-2 in the generate RESEARCH.md; one models.md line). Next: HF transformers audio docs, then group 2 (IT-JIM blog first).
- 2026-11-02: HF transformers audio docs, IT-JIM blog (no matching post found) (R-20261102-3). Next: group 2 from Torin Hopkins.
- 2026-11-02: Torin Hopkins (a researcher, no resources page), MusicMakerApp (no guide found), Kingy AI (partly sponsored roundups) (R-20261102-4). Next: Artlist and Mubert guides, Artificial Analysis.
- 2026-11-02: Artlist, Mubert, Artificial Analysis Music Arena (R-20261102-5; Mubert and Artlist rows and the arena ranking in hosted.md). Group 2 done; next: group 3 (forums: r/SunoAI via RSS first).
- 2026-11-02: r/SunoAI and r/udiomusic top-of-month RSS (R-20261102-6 in the produce RESEARCH.md: afftdn row in mixing.md; Suno upload flagging in hosted.md). Next: r/ArtificialInteligence music threads, Hugging Face audio discussions, awesome-ai-music lists.
- 2026-11-02: awesome-ai-music lists (wildminder's is the useful one), r/ArtificialInteligence (no music threads this month), HF audio discussions (no single forum; skipped) (R-20261102-7: DiffSynth-Music, acestep.cpp/.vst3, ACE-Step Transcriber rows in generate models.md). Next: Gearspace AI subforum, Kaggle audio forums, then group 4 blogs.
- 2026-11-02: Gearspace, Kaggle (nothing found; group 3 done), Stability audio news (R-20261102-8: SA3 inpainting and continuation in the models.md row). Next: Meta AI, Google Magenta, Hugging Face audio posts.
- 2026-11-02: Meta AI (nothing new), Google Magenta (MRT2 already covered), Hugging Face audio posts (none in 2026) (R-20261102-9; LeVo 2 licence unreadable, no row). Next: OpenAI research, Sound on Sound tech, Music Business Worldwide.
- 2026-11-02: OpenAI research (no released model), Sound on Sound (nothing found), Music Business Worldwide (label deals into hosted.md) (R-20261102-10). Next: Towards Data Science audio tag, Synthtopia, then group 5 books.
- 2026-11-02: Towards Data Science audio (2023-24 explainers only), Synthtopia (synth tools, no generators); group 4 done (R-20261102-11). Next: group 5 books, Müller first (readwright on the owner's copy if he has one, else table of contents).
- 2026-11-03: Müller via the FMP notebooks (no copy owned; R-20261103-1 in the produce RESEARCH.md: chord recognition, DTW and HPSS are candidates, no skill change). Next: Farnell, *Designing Sound* (table of contents and samples).
- 2026-11-03: Farnell (procedural SFX in Pure Data, out of scope) and Nierhaus (Markov, grammars, GA, CA: not a gap while the agent writes notes) from tables of contents (R-20261103-2 in the compose RESEARCH.md, no skill change). Next: Dean (ed.), *The Oxford Handbook of Computer Music*, then Zölzer.
- 2026-11-03: Dean (survey; IDyOM-style expectation a melody-check candidate only) and Zölzer (dither, resampling already covered) from listings (R-20261103-3 in the produce RESEARCH.md, no skill change). Next: Dodge, *Computer Music*, then Foster, *Generative Deep Learning*.
- 2026-11-03: Dodge and Jerse (synthesis is the models' job; 1/f and random-walk melodies join the Nierhaus candidate) and Foster (symbolic Transformers, MuseGAN: superseded) from contents lists (R-20261103-4 in the compose RESEARCH.md, no skill change). Group 5 done; next: group 6 course syllabi (Ableton Learning Music, Soundfly first).
- 2026-11-03: Ableton Learning Music (covered by theory.md) and Soundfly (403, skipped) (R-20261103-5 in the compose RESEARCH.md, no skill change). Next: Coursera music-production syllabi, Kaggle Learn (audio), which ends group 6.

- 2026-11-03: Coursera syllabi (Berklee capstone, Malachi mixing course: covered) and Kaggle Learn (no audio course) (R-20261103-6 in the compose RESEARCH.md, no skill change). Group 6 done; all groups mined unless the list grows.
- 2026-11-05: group 7, ACE-Step community (R-20261105-1 in the generate RESEARCH.md: 13 issues, 11 discussions, DCW.md read; Tutorial, Musician's Guide and INFERENCE.md keyword-scanned only). Seven notes in acestep.md, one in licences.md. Next: group 8.
