---
name: musicwright-curate
description: "Use to keep and use everything learned about music making: record a listener's verdict on a take, turn verdicts into a taste profile (what they like and reject, and why), save lessons, dead ends and working recipes, promote a judged recipe into mw.py's recipes, answer 'what have I learned about music', 'what do I like', 'which settings worked', and file new research or notes in the studio or the plugin. Use on 'remember that I liked this', 'I didn't like the drone', 'note that cfg 7 sounds harsh', 'what music have I made', 'update my music notes', 'add this to the music knowledge'. Making music is the other musicwright skills. Also 'refresh musicwright-curate'."
---

# musicwright-curate

The memory of the plugin. Two stores:

- **The studio** (private, per person): `MUSICWRIGHT_HOME`, default `~/.musicwright`. Verdicts,
  taste, lessons, recipes, ideas, host config. Point it at a private notes folder or vault if
  the person keeps one, so it is backed up with their other notes.
- **The plugin** (shared, public): skill references, `recipes.json`, LEARNINGS and RESEARCH files.
  Only general knowledge goes here: no names, paths, projects or machines.

Layout and file formats: [references/studio.md](references/studio.md).

## Step 1: capture (whenever it happens, not at the end)

| Heard | Do |
|---|---|
| a verdict on a take ("keep 2", "too harsh", "loved the breathy start") | `mw.py verdict <take> keep\|reject\|maybe --note "<their words>"` |
| a standing preference ("I like flute leads", "never static or hiss") | `mw.py note taste "<preference, in their words>" --source "<project or date>"` |
| a lesson or dead end (a setting failed, a workaround) | `mw.py note lesson "<what happened, the fix>"`; if it is general, also add an L- entry to the right skill's LEARNINGS.md |
| a recipe that produced a kept take | `mw.py note recipe "<recipe, caption, settings, seed>"`; promote it (Step 3) |
| an idea for later | `mw.py note idea "<idea>"` |

Use their words. Paraphrase loses the detail that makes taste usable.

## Step 2: distil taste

When `verdicts.jsonl` has new entries (or the person asks "what do I like"):

1. Read `verdicts.jsonl` and `taste.md`.
2. Group kept against rejected by what differs: model and recipe, cfg and sampler, tempo, key,
   instruments, caption words, length.
3. Rewrite the "Profile" section at the top of `taste.md`: 5-15 short lines, each with its
   evidence (how many keeps or rejects, which projects). Mark guesses as guesses.
4. Other musicwright skills read the profile before writing a brief or caption.

## Step 3: promote what is proven

- A recipe whose takes were kept twice or more (or once, explicitly praised) goes into the hub's
  `references/recipes.json` with a `source` line that names the kind of run, not the person
  or project. Log the change in that skill's CHANGELOG.md.
- A lesson that holds beyond one project goes into the owning skill's LEARNINGS.md (L- entry with
  Trigger and Hypothesis), and into the SKILL.md or a reference when it changes what the skill
  tells agents to do (with a CHANGELOG entry).
- Research findings with sources go to the owning skill's RESEARCH.md, never into a SKILL.md
  from memory.

## Step 4: answer from the record

"What have I learned / made / liked": read `taste.md`, `lessons.md`, `recipes.md`, the
verdicts, and the project ledgers listed in `studio/projects.md` (if kept). Answer from them,
with dates and file paths, and say what is missing (takes nobody judged, recipes never tried).

## Rules

- Private stays private: names, paths, machines, other people's projects and opinions about
  people never go into the plugin's public files.
- Never invent a verdict. "Unjudged" is a valid state and `mw.py ledger` lists them.
- Append, do not rewrite, verdicts and notes; only the Profile section is rewritten.
- One fact, one home: when moving a lesson into a skill, leave a pointer in the studio note.

## References

- [references/studio.md](references/studio.md): studio files, formats, the Profile section, the knowledge map of where each kind of fact lives.

## Maintenance

Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md),
[LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evergreen.json`.
