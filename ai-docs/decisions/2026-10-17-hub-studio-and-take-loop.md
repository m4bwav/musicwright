---
kind: decision
status: active
date: 2026-10-17
title: Hub, six siblings, one CLI, the take loop and a private studio (read before adding a skill, an mw.py command, a recipe or an MCP server)
tags: architecture,hub,mw.py,studio,take-loop
---

# Decision: a hub, six siblings, one CLI, a take loop and a private studio

Date: 2026-10-17. Status: adopted for v0.1.0.

## Context

The owner makes AI music for an indie card game, AI short films and personal listening, has
strong taste and no formal training, and had music knowledge scattered over two private skills,
a best-practices note, batch scripts and film-project notes, with recipes and preferences that
contradicted each other (research 00, private). Research (ai-docs/research) found DAW bridges,
code-music tools and hosted-generator wrappers, but nothing that runs the generate, judge and
finish loop for an agent that cannot hear, or that remembers what the listener liked.

## Decision

- One hub skill (`musicwright`): brief, route, the take loop (several seeds → spectrogram sheet
  and numbers → the listener's verdict → ledger), the project folder and `music.json`.
- Six siblings by job, not by model: generate (models, prompting, licences), compose (theory,
  vocabulary, notes-first), produce (loudness, mastering, QC, stems), game (loops, engines,
  adaptive), score (film), curate (verdicts, taste, lessons, recipe promotion).
- One stdlib CLI (`mw.py`) with ffmpeg underneath: doctor, new, gen (ComfyUI and ACE-Step
  REST), measure, sheet, master, edit, join, loop, seam, duck, analyze, verdict, ledger, note.
  One JSON object per command, fail soft.
- Recipes and loudness presets live in data (`recipes.json`, `loudness.json`) with sources; a
  recipe enters only after a listener kept a take made with it.
- A private studio (`MUSICWRIGHT_HOME`, default `~/.musicwright`) holds verdicts, taste,
  lessons, recipes and host config; the public plugin holds only general knowledge.
- No MCP server in v0.1.0: CLI first, as Producer Pal and TwelveTake show.

## Rejected

- One skill per model (an ACE-Step skill, a Suno skill): models churn monthly; jobs do not.
  The earlier ACE-Step skills are folded into generate.
- Automating Suno or Udio: no public API, terms forbid other channels, Udio downloads are off.
- A learned quality scorer in v0.1.0: unproven on this material; the spectrogram plus a
  person's ear is the judged signal for now (open question in the hub's RESEARCH.md).
- The names songwright (an iPhone app and a marketplace use it) and tunewright (an audio
  tagger uses it).

## Consequences

- Every take is reproducible from the ledger, and every verdict feeds taste across projects.
- The plugin says "unheard" until a person listens; it never claims a take sounds good.
- Game loops (bar-exact, crossfaded, seam-checked) are a first-class output.
