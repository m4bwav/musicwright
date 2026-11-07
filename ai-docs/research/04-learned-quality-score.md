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

## SongEval: before the run (2026-11-03)

The verdict count passed the bar: 23 in the studio's verdicts.jsonl (15 keep, 6 maybe, 2 reject), of which 20 are audio files that can be scored; the other three are MIDI transcriptions or a superseded line. Keeps far outnumber rejects, so the useful test is the pairs the listener ranked, not keep against reject.

Read from github.com/ASLP-lab/SongEval at 848fb2f. A first attempt to install its requirements was refused by the session's permission check, and no workaround was tried; the owner then allowed it.

- Size and needs: `librosa==0.11.0`, `torch==2.7.0`, `muq==0.1.0`, `hydra-core==1.3.2`; a 97 MB checkpoint in the repository, plus MuQ weights (`OpenMuQ/MuQ-large-msd-iter`) downloaded from Hugging Face at first run. `--use_cpu True` avoids the shared GPU.
- Licence conflict: the README says CC BY-NC-SA 4.0, the LICENSE file says Apache 2.0. Treat it as non-commercial until settled; a private test is fine either way, shipping anything built on it is not.
- Input: reads only `.wav` and `.mp3` (FLAC takes need converting), and `ckpt_path` is relative, so run it from the clone. Writes `result.json` with Coherence, Musicality, Memorability, Clarity and Naturalness.
- Fit: it was built for full songs with vocals and accompaniment, and Naturalness scores vocal breathing and phrasing. Many judged takes are instrumental solos, stems or short mixes, so expect weak signal on those.

Steps once the install is allowed: an isolated venv on Python 3.11 outside the repository, the requirements, every scorable verdict file converted to WAV, `python eval.py -i <folder> -o <out> --use_cpu True` from the clone, then compare with the ranked pairs (s52203 over s41017, s8101 mixes over s8303 mixes, hintcover over plaincover, ComfyUI repaint over REST). As with Audiobox, it stays out of mw.py, and no score may stand in for a listener.

## SongEval: run, not adopted (2026-11-03)

The owner allowed the install. Run at 848fb2f on the CPU over the 20 judged audio files, converted to 44.1 kHz stereo WAV, in 63 s after model load. Verdict: no use for ranking takes. It stays out of mw.py and out of the take loop.

| Ranked pair (owner's verdict) | Musicality | Clarity | Agrees? |
|---|---|---|---|
| flute s52203 keep vs s41017 reject | 1.48 vs 1.93 | 1.41 vs 1.84 | no, every axis |
| hintcover vs plaincover (blind pair) | 1.76 vs 2.00 | 1.50 vs 1.75 | no, every axis |
| ComfyUI repaint vs REST repaint | 2.70 vs 2.55 | 2.49 vs 2.37 | yes, every axis |
| stage 2 s8101 mixes vs s8303 mixes | 1.96, 1.94 vs 1.68, 1.66 | 1.82, 1.83 vs 1.58, 1.59 | yes, every axis |
| s8101 answer vs straight (slight) | 1.961 vs 1.943 | 1.822 vs 1.826 | noise |
| s8303 answer vs straight (slight) | 1.679 vs 1.659 | 1.576 vs 1.590 | noise |
| stage 3 best vs the two others | 1.88 vs 1.90, 1.90 | 1.65 vs 1.67, 1.68 | no, lowest on every axis (tiny gaps) |

Reading:

- Two of the four clear pairs came out backwards, and those two are the only takes the listener marked down outright or beat blind. Audiobox CE got the flute reject right, and SongEval does not.
- The score mostly follows the kind of audio: the YuE2 song with vocals tops every axis (Musicality 4.35), multi-instrument takes sit near 2.5 to 2.9, and flute solos and mixes near 1.5 to 2. This matches the warning above that it was built for full songs, so it cannot compare across kinds of material.
- All 20 files sit in a narrow low band (1.4 to 4.5 of 5) although 14 of them were kept, so a low score says little.
- Limits: few pairs, and one verdict per pair. This rules out using it here; it does not test SongEval on full songs with vocals, which is its own target.

Install notes, if anyone reruns it: the published requirements do not run as written on Windows. Pin `torchaudio==2.7.0` (an unpinned 2.11 fails to load against torch 2.7.0 with WinError 127) and `transformers==4.50.3` (5.x fails in MuQ with `'EasyDict' object has no attribute '_attn_implementation'`). The test folder was deleted afterwards.

## Recheck on all blind picks: not adopted (2026-11-07)

Owner's request: once more, adopt only if it predicts their picks. Audiobox (four axes) and SongEval (five) scored the files as heard, on the CPU. Agreements with the 11 two-way picks ranged from 6 to 7 (best p=0.549, exact sign test); on the 4 clear picks, Audiobox CU and PQ got 4 of 4 (p=0.125, the lowest four pairs can give), and those two fell to 7 and 6 of 11 overall and 3 of 5 on the same-seed route pairs. Nine axes, no multiple-comparison correction, and the pack was side B in all clear pairs, so a side or route effect cannot be separated. No score beats chance. Closed: it stays out of mw.py and the take loop.
