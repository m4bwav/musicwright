---
kind: decision
status: active
date: 2026-10-23
title: Books track 9 rulings: game cues from a level plan, new cue types, one MAINTENANCE file
tags: game,cues,beat-chart,level-plan,rotation,accessibility,size-budget
---

# Decision: game cues from the level plan, and a smaller install

Date: 2026-10-23. Status: adopted on branch books-9 (not released).

## Context

Rogers, *Level Up!* (3rd edition) was read for the game plugins. For musicwright-game the notes
proposed taking the cue list from a level's beat chart or room plan, four missing cue types
(mystery, warning, chase, a villain motif) and rules on energy, rotation, the title piece,
silence, stinger direction and a visual twin for cues that carry information. None of it was
in the skill before. The installed skills were 446 KB, over the 400 KB green line, so the
install had to shrink before anything was added.

## Rulings

- M1. Six of the seven `MAINTENANCE.md` files were the evergreen pointer template, identical
  apart from their title (38 KB together). They now point at the hub's copy and list their own
  files. musicwright installs only as a whole plugin, and no evergreen script reads the file's
  content, so nothing loses the fallback rules. Installed size 446 KB to 420 KB after the
  additions; still yellow, because the rest is scripts (168 KB) and evergreen records.
- M2. No `mw.py cues` check for the same track in neighbouring areas. It would be a field the
  planner sets, but no real beat chart or cue sheet exists to calibrate on, and classic games
  reuse one level theme across neighbouring levels on purpose, so a repeat is not a defect by
  itself. The rule ships as prose that asks the plan to say when a repeat is meant.
- M3. The new cue rows give no lengths in seconds or minutes ("loop, like combat", "a stinger or
  a layer"): the book gives none, and AGENTS.md forbids numbers from recall.
- M4. The energy rule ("a notch above the screen") covers action and traversal cues only. Long
  map, deck-building and ambient beds keep the low-fatigue rules of Step 1, which the notes
  flagged as being in tension with it.
- M5. The description names "cue lists (from a level plan or beat chart)" and drops "and
  lengths", so it stays at 691 of 700 characters.
- M6. The eval fixture `tests/fixtures/LEVEL-PLAN.md` is an invented six-stage plan with a
  repeated track in stages 2 and 3, two new enemies and a boss first seen two stages early, so
  one case can grade rotation, warning cues, a motif and the visual twin from the output file.
