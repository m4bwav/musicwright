---
kind: decision
date: 2026-11-06
title: "SFT wide test and level pair: default unchanged, pack for calm and combat, master --shared-gain added"
tags: [listening, recipes, sft, loudness, shared-gain, blind]
---

# SFT wide test and level pair, 2026-11-06

One listener answered askwright set ask-sft-wide blind; the keys were opened only afterwards.

| Question | Answer (pack = acestep-xl-sft-pack) | Listener's note |
|---|---|---|
| Calm 5201 | pack, slightly | other route had a light background tone; both stopped early |
| Calm 5202 | pack, clearly | other route had an annoying background note; both stop early |
| Combat 5201 | pack, clearly | other route too repetitive |
| Combat 5202 | pack, clearly | other route a little harsh and repetitive |
| Town 5201 | no real difference | both pretty good; one stopped a couple of seconds early |
| Town 5202 | acestep-xl-sft, slightly | both a little tinny |
| Level across three cues | kept differences, slightly | none |

## Rulings

1. **The default stays `acestep-xl-sft`.** The owner's condition was a win across captions with acceptable endings. The pack won two captions of three and early stops remain. It also adds a dependency and has no cover or repaint.
2. **The pack is the recommendation for calm and combat instrumentals where it is installed.** Recorded in the recipe and the generate model table.
3. **`mw.py master a b c --shared-gain` is added,** as agreed before the test if the kept differences won. One gain, no limiter, the loudest lands on the target, peaks can hold it lower. One level stays allowed: one slight preference is not a rule, and nobody has played it in a game.

## Caveat

The pack was side B in all six pairs, and the kept-differences side was also B. Fresh os.urandom seeds, a fair shuffle (49% swaps in 2,000 draws) and correlation against the sources show the keys are right and the order was chance (about 1 in 128), but an order effect cannot be ruled out. The ask page said sides were random, which was true. To harden ruling 2, re-run with the sides forced to balance; not owed unless someone wants the pack as the default.

Details: musicwright-generate R-20261106-7, musicwright-produce R-20261106-8. Audio in the owner's Music/sft-wide folder.
