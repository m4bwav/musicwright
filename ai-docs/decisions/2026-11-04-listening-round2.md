---
kind: decision
date: 2026-11-04
title: "Listening round two: Stable Audio 3 can miss a calm brief, extract leaked once"
tags: [listening, recipes, extract, yue2, stable-audio, minimax]
---

# Listening round two, 2026-11-04

One listener, one take or pair per question, answered on the ask-round2 page in Ai/Music/hw-checks. The agent's low-confidence guesses matched one answer of four.

| Question | Answer | Ruling |
| --- | --- | --- |
| Stable Audio 3, seed 4101, calm ambient space theme | "Not bad, maybe slightly too intense, I wouldn't call it calm or even ambient" | Recipe stays, settings unchanged. Its source note says it can miss a calm brief. Ledger verdict: maybe. |
| YuE2, seed 4102, folk ballad | Keep | Source note records the second kept take. |
| MiniMax Music 3, blind | Take B, which the key shows is seed 3101 | Seed 3101 is the named reference in the source note. Ledger keeps seed 3102 as it was. |
| Extract drums, sound near the end | Leak: "mostly cymbals but sounds a little too much like a synth note" | The extract docs mention the leak and say to listen to the end of a take. Ledger verdict: maybe. |

Not concluded: that Stable Audio 3 is poor at calm music (the earlier seed 3301 was kept on the same brief), or that extract leaks in general. The mw.py routes showed no bug, so no bug hunt followed.
