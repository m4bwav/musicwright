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
