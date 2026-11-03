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
