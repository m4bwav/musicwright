# The studio and the knowledge map

## Studio files (`MUSICWRIGHT_HOME`, default `~/.musicwright`)

| File | Written by | Holds |
|---|---|---|
| `config.json` | the person or setup | `{"comfyui": "http://host:port,...", "acestep_rest": "http://host:port"}` |
| `verdicts.jsonl` | `mw.py verdict` | every verdict with the take's recipe (route, model, seed, caption, lyrics, params, duration) |
| `taste.md` | `mw.py note taste`, then curated | a Profile section at the top (rewritten), then dated raw notes (append-only) |
| `lessons.md` | `mw.py note lesson` | dated lessons and dead ends |
| `recipes.md` | `mw.py note recipe` | recipes that worked, with seeds |
| `ideas.md` | `mw.py note idea` | music to make later |
| `projects.md` | by hand or curate | one line per music project folder (path, use, status) |

## taste.md Profile shape

```markdown
# Taste notes

## Profile (rewritten <date> from <n> verdicts)
- Bright, melodic mid-tempo electronica over dark ambient (8 keeps, 1 reject).
- Flute leads, virtuosic in solo sections (kept in 3 projects).
- Harsh top end rejected: cfg 7 on ACE-Step XL "harsh"; cfg 4.5 kept (guess from 2 batches).
- Noise textures (static, hiss, beeps) rejected as foreground.

## Tired of (rewritten <date>)
- A tempo band, timbre, drum sound or section shape the listener has heard too often, with what
  to try instead (after DeSantis, *Making Music* ch. 6); musicwright-generate reads it before a
  caption. Drop a line when a piece needs that thing anyway.

## Notes
- 2026-10-17: ... (source: ...)
```

## Where each kind of fact lives

| Fact | Home |
|---|---|
| a person's taste, verdicts, their projects and hosts | studio (private) |
| a general lesson ("short renders go quiet at the end") | owning skill's LEARNINGS.md (L-), then its SKILL.md or reference |
| a sourced, dated finding about a model, price, licence or platform | owning skill's RESEARCH.md (R-) |
| a change to what a skill says | owning skill's CHANGELOG.md (C-) |
| a judged recipe | hub `references/recipes.json` |
| loudness targets | hub `references/loudness.json` with sources |
| a first-pass research report | the repository's ai-docs/research/ |

Owning skill by subject: models, prompts, licences → musicwright-generate; theory, vocabulary,
notation → -compose; loudness, mixing, formats, stems → -produce; loops, engines, adaptive →
-game; film, hits, ducking → -score; the take loop, mw.py, the contract → musicwright (hub).
