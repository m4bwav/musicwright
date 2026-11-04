---
kind: decision
date: 2026-11-03
title: "Listening verdicts: ComfyUI first for source tasks, three recipes confirmed or added"
tags: [listening, recipes, cover, repaint, extract, yue2, stable-audio]
---

# Listening verdicts, 2026-11-03

One listener, one source per question, answered on the hw-checks-listening page. The agent guessed differently on all seven; the guesses were low confidence and carried no weight.

| Question | Answer | Ruling |
| --- | --- | --- |
| Extract drums, vocals (punk mix) | Mostly that part alone, both | ComfyUI extract documented as working. Near the end of the drums, a cymbal or synth sound the listener could not place. |
| Cover, blind | Take A, which the key shows is the semantic-hint cover | `--task cover` in ComfyUI uses hints unless `--strength` is given. A behaviour change, from denoise 0.6. |
| Repaint | ComfyUI good enough, and better than REST | ComfyUI leads for repaint. Different seeds, so this compares two takes as much as two routes. |
| MiniMax Music 3 | Keep | The existing recipe's source now cites the verdict. The question asked about either take, so no seed was singled out. |
| Stable Audio 3 Medium | Keep | New recipe `stable-audio3-medium`. |
| YuE2 | Keep | New recipe `yue2-3b-int8`; needs lyrics, saves the ABC plan beside the take. |

The kept takes were rendered by a standalone script; the recipes use the same settings through new graphs in `mw.py gen`, and one take of each ran on the real ComfyUI (recipecheck_* in the owner's hw-checks folder, unheard).

Not concluded: that these routes beat the alternatives in general. REST remains for extend, lego and complete, and Demucs remains an option for separation.
