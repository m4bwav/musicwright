---
kind: research
status: active
date: 2026-11-02
title: Audiobox Aesthetics against the owner's verdicts (read before adding a learned quality score to the sheet or to take ranking)
tags: research,quality,scoring,audiobox
---

# A learned quality score on judged takes

Open question from the hub's RESEARCH.md: does a learned audio-quality scorer add useful signal for ranking takes? Tested on 2026-11-02 with Audiobox Aesthetics (Meta, `audiobox_aesthetics` on PyPI, CC-BY 4.0 weights) on the PC (RTX 5060 Ti), over the nine flute-solo files the owner has judged plus seven unjudged references.

## How it ran

```
uv tool run --python 3.11 --from audiobox_aesthetics --with requests --with soundfile \
  --with "torch<2.9" --with "torchaudio<2.9" audio-aes input.jsonl --batch-size 1 > out.jsonl
```

`input.jsonl` holds one `{"path": ...}` per line. The three extra pins are needed: the package does not declare `requests`, torchaudio 2.9 needs TorchCodec to load audio, and without `soundfile` torchaudio has no backend for FLAC on Windows. 16 files (40 s to 4 min) took 50 s including model load. Output has four axes from 1 to 10: CE content enjoyment, CU content usefulness, PC production complexity, PQ production quality.

## Results against the verdicts

| Comparison (owner's verdict) | CE | PQ | Agrees? |
|---|---|---|---|
| flute s52203 keep vs s41017 reject (bass a flute can't make) | 5.59 vs 3.94 | 7.01 vs 7.20 | CE yes, PQ no |
| stage 2 s8101 mixes (keep) vs s8303 mixes (maybe) | 7.10, 7.07 vs 6.40, 6.41 | 7.16, 7.24 vs 6.98, 7.03 | yes, both |
| s8303 answer slightly over s8303 straight | 6.397 vs 6.407 | 6.98 vs 7.03 | no (tiny gap) |
| stage 3 best (answer, -12 dB) over the two others | 7.143 vs 7.142, 7.115 | 7.28 vs 7.29, 7.32 | noise |

Unjudged: SA3 Medium 7.18 CE, YuE2 7.78, MiniMax Music 3 6.72 and 7.35, the spacey album 7.2 to 7.7. PC (complexity) rose by about 1 when percussion was added in stage 3, so it reads density, not quality.

## Reading

- CE agreed on both large gaps (0.7 and 1.6 points) and said nothing useful about gaps the owner called slight (under 0.05). PQ got the reject wrong: the rejected take was cleaner audio with the wrong content.
- n is small (one reject, two coarse pairs). Treat CE as a coarse pre-sort over many seeds (drop the clear losers before a listener hears them), never as a verdict and never to choose between close mixes.
- Not added to mw.py: it pulls torch (several GB) into a stdlib tool and only two comparisons back it. Revisit when ten or more judged takes exist; the ledger already holds verdicts to score against. SongEval (the other candidate) was not tried.
