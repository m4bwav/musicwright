---
kind: decision
status: active
date: 2026-10-23
title: Books track 8 rulings: mixcheck, matched previews, monobass, melody hints, craft from two music books
tags: mixcheck,preview,monobass,melody,calibration,loudness,arrangement
---

# Decision: mix checks, fair comparisons and craft rules from two music books

Date: 2026-10-23. Status: adopted on branch books-8 (not released).

## Context

Two books were read for the plugin: Oltheten, *Mixing With Impact* (2018) and DeSantis, *Making
Music* (2015). The reading notes proposed a `mw.py mixcheck`, loudness-matched previews, a
`compare` command, scripted fixes, loudness hints, melody checks and prompt and arrangement
craft. Every proposal was checked against the code first, and every threshold was set on real
renders before it shipped: 78 AI renders on the owner's machine (ACE-Step 1.5, MiniMax Music 3,
film scores, layered mixes) for the mix flags, and 18 public-domain tunes against six random
walks for the melody flags.

## Rulings

- K1. Pre-master hand-off is `master --peak -6`, not a preset: `check_skills.py` requires every
  preset to carry a loudness target and a true peak, and a peak-only mode is a different job.
- K2. `preview` is its own command rather than `edit --preview`: it works on several takes at
  once, matches them to one level, and `--blind` shuffles them into take_A, take_B with the key in
  a file (the same judging hygiene as random sides in the video plugins).
- K3. The matched level drops below `--lufs` when any copy would peak over -1 dBTP with plain gain,
  so no copy needs a limiter that would change its sound.
- K4. `monobass` uses a Linkwitz-Riley crossover at 160 Hz by default; 200 Hz gives a fully mono
  low end up to about 120 Hz. Subtracting a low-passed side widened the lows (hub L-003).
- K5. Correlation and mono loss come from mid and side energy in the same ffmpeg pass as the
  bands; it agreed with `aphasemeter` and with a dual-mono fold on the worst file (10 LU), and
  saves a pass.
- K6. Flag thresholds sit where a minority of the 78 renders fire (1% to 18%), and each rate is
  published in produce's mixing.md. MUDDY needs a bass part (produce L-002). BRIGHT is labelled
  uncalibrated: the one render a listener called harsh did not stand out on presence.
- K7. BELOW-RANGE (`--lowest NOTE`) is the one flag with real labels: the flute take rejected for
  a bass reads -4.0 dB under the note, the two kept takes -25.1 and -33.3; the line is -15.
- K8. The `lra_hint` in each preset is advice in words. The book says which way the loudness
  range should lean per destination, not by how many LU.
- K9. Melody hints keep two flags (leap share over 25%, under 65% of notes in a returning
  four-note rhythm); the single-top-note and step-run rules are reported without a flag
  (compose L-002).
- K10. Section tags that carry density and the stop rule went into the prompts as craft from the
  books, marked as not yet compared by a listener.
- K11. The version stays 0.1.0; the changes are listed under Unreleased in CHANGELOG.md. Tagging
  waits for the owner.

## Not built, and why

- Tuning drift, repetition and `analyze --sections` need librosa, which is not installed here;
  they belong in `mw.py analyze` and need a calibration set of their own.
- A harshness repair with `adynamicequalizer` or `deesser`: the filter's options differ between
  ffmpeg 6.1 (CI's Ubuntu) and 9, and there is no harsh-labelled render to show a fix works.
- Sibilance spikes: no vocal material to calibrate on.
- Kick and bass onset coincidence (`pulse --against`): no drum and bass stems on disk.
- A codec-ceiling check: the spectrogram sheet already shows a hard top.
- "Too dynamic for a game bed" and "loudest point too early" need the piece's intent; `mixcheck`
  reports PLR and `loudest_10s_at_s`, and the reading guide says how to use them.

## Cost

Installed skills grew from 391 KB to 446 KB, over the 400 KB green line (yellow ends at
800). The tracked repository is about 2.2 MB, yellow since before this track.
