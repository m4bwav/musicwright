---
kind: decision
status: active
date: 2026-10-23
title: Listening checks on BRIGHT, TUNING-GAP, REPEATS and density section tags; the 0.1.1 bug fixes
tags: listening,calibration,bright,tuning,repetition,sections,release,bugs
---

# Decision: what four blind listening checks changed, and what 0.1.1 fixes

Date: 2026-10-23. Status: adopted for 0.1.1.

## Context

Tracks 8 and 11 shipped four rules that no listener had judged: BRIGHT (uncalibrated), TUNING-GAP
at 15 cents, REPEATS at a share of 0.9, and section tags that say who plays. The owner judged one
blind pair for each. Every pair was made with `mw.py preview --blind` (one loudness, letters
shuffled, the key kept away from the listening folder) and asked as one question with fixed
answers.

| Check | Pair | Answer |
|---|---|---|
| REPEATS | minutes 3-6 of two 10-minute ACE-Step beds: share 0.98 (flagged) and 0.13 | the flagged bed was "probably less repetitive"; both middling |
| TUNING-GAP | the kept solo flute with a separately rendered jazz flute 27.6 cents sharp (flagged), and with one 2.5 cents off | both "reasonably in tune"; the flagged mix "sounded better overall" |
| Sections | ACE-Step 1.5 XL SFT, one caption and seed, 180 s: density tags against mood-only tags | the mood take "seemed solid"; neither reached a full-orchestra chorus, "especially not" the density take |
| BRIGHT | one caption and seed at cfg 9 (presence -7.6 dB, flagged) and cfg 4.5 (-11.8) | neither harsh; the cfg 9 take "slightly harder to listen to" |

## Rulings

- P1. REPEATS is gone as a flag. `repetition.share` is still reported. One pair is thin, but it
  pointed the wrong way, and the flag only ever fired on ambient beds, which repeat a texture on
  purpose. The published rate becomes "reported, not flagged".
- P2. TUNING-GAP fires over 30 cents (was 15 or more). A 27.6-cent layer was heard as in tune.
  Re-measured on the 14 real layers against their lead: 0 fire (was 1, the pair above). Where a
  gap becomes audible above 30 is untested; two held unison notes would show it sooner than two
  moving lines.
- P3. BRIGHT keeps its -10 dB line (5 of 78 renders) and the flag points in the right direction.
  The text now says what the check found: at -7.6 dB a take was slightly tiring, not harsh. The
  label changed from "uncalibrated" to a fatigue pointer, so the rate is unchanged.
- P4. Density section tags stay in musicwright-generate as book craft, marked as not shown to help
  on one pair. Name added instruments in the caption as well (generate L-002).
- P5. cfg 9 against 4.5 on the same seed raised presence by 4.2 and 2.5 dB on two seeds: the
  recipe's 4.5 stays.

## Bug fixes in 0.1.1 (HANDOFF item 7 and one found this session)

- `--host 127.0.0.1:8199` without `http://` read as "unreachable (URLError)"; hosts now get the
  scheme added (found queuing these renders).
- `seam` takes the level jump from the median of 50 ms windows over half a second each side, so a
  loop that starts on a drum hit reads clean.
- `master`: `--lufs`/`--tp` without `--preset` is named `custom` (file `<stem>_custom.wav`, no
  preset note); dynamic mode on a source with LRA under 1 no longer blames peaks.
- `new --preset` refuses an unknown preset before creating any folder.
- `verdict` on a missing file that is not a logged take fails; an unlogged file is recorded by
  its stem, so `ledger` can match it.
- `gen` through ComfyUI says when the recipe's bpm and key were sent because none were given
  (`filled_in`; the ACE-Step text encoder needs both), and that MiniMax Music 3 ignores `--bpm`
  and `--key` (`ignored`).
- Docs: the seam line is a ratio of 2 or less (cli.md, game SKILL.md, loops.md), argument errors
  exit 2 with usage on stderr (cli.md), `created` is in contract.md's music.json table.

Ten mutations, one per fix, each caught by its new test.

## Not changed

- No eval re-run: the skill wording changes are flag notes and one hedge in a bullet, not routing
  or steps.
- The listening files stay outside the repository (owner's output folder); the answer keys were
  kept in the session's scratch folder until the answers were in.
