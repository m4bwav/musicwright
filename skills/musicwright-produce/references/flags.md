# mixcheck and analyze flags: calibration

Where each flag's threshold came from and how often it fires on real renders. Read when a flag fires and you need to judge it; the scripted checks themselves are in [mixing.md](mixing.md).

## mixcheck flags and how often they fire

Fire rates on 78 real AI renders (ACE-Step 1.5 and MiniMax Music 3 takes, film scores and layered
mixes, 14 s to 10 min); 43 raised no flag. No listener labels exist for most of them, so each
threshold sits where a minority fires; they are heuristics, not verdicts.

| Flag | Fires when | Rate | Note |
|---|---|---|---|
| OVER-LIMITED | true peak minus integrated loudness (PLR) under 8 dB | 1/78 | after Oltheten 5.5, 14.5 |
| FLAT | longer than 90 s and short-term loudness spread (10th to 90th percentile) under 2 LU | 4/78 | fine for a steady game bed |
| MUDDY | 250-500 Hz more than 3 dB over the bass and mid bands' average, with a bass part present | 5/78 | without the bass condition it fired on both kept flute solos |
| BRIGHT | 2-5 kHz against 200 Hz-2 kHz above -10 dB for half the playing time | 5/78 | a fatigue pointer, not a harshness test: in a blind matched pair (one caption and seed at cfg 9 and 4.5) the take at -7.6 was heard as slightly harder to listen to and neither as harsh; the one render a listener once called harsh read -19.8 and did not fire; flute leads fire it |
| MONO-LOSS | more side than mid energy (correlation under 0), so mono loses over 3 dB | 13/78 | real: one render loses 10 LU folded, confirmed with `aphasemeter` |
| LOW-WIDE | correlation under 0.7 below 120 Hz | 14/78 | fixed by `monobass` |
| BELOW-RANGE | with `--lowest NOTE`: energy a whole tone under the note above -15 dB against the whole | 1/3 flute solos | the take a listener rejected for "bass a flute can't make" read -4.0; the two kept takes -25.1 and -33.3 |

Not built: sibilance spikes (no vocal material) and a codec-ceiling check (the
sheet shows it).

## analyze flags and how often they fire

Rates on 111 AI renders and layered parts and on 11 human recordings (public domain and CC BY:
orchestra, string quartet, solo cello, a piano roll, a 1920 dance band, loop-built electronic
pieces). 100 of the AI files raise none. Listener checks (2026-10-23, blind, matched level) moved
TUNING-GAP and REPEATS; see the notes.

| Flag | Fires when | AI | Human | Note |
|---|---|---|---|---|
| OFF-A440 | tuning 15 cents or more from A440 | 6/111 | 4/11 | a layering warning: strings and old recordings sit sharp on purpose |
| TUNING-GAP | a later file more than 30 cents from the first | 0/14 layers | | lego layers sat 0.4 to 14 cents from their lead; a separate jazz flute 27.6 cents off was heard as in tune (and the better mix) against one 2.5 off, so the line moved from 15 to 30 |
| DRIFT | the last third 15 cents from the first, on 90 s or more | 0/111 | 0/11 | no real file drifts; proved on a synthetic step |

Window spread (`spread_cents`) is not flagged: bends, vibrato and pitch effects raise it (L-004).
`repetition.share` is reported, not flagged (it was REPEATS at 0.9, on 5/111, all 10-minute beds):
in a blind pair a bed at 0.98 sounded slightly less repetitive than one at 0.13, and both only
middling. The share finds a steady texture, not a bed that feels stuck (L-005).
`harmony` is reported, not flagged, and uncalibrated: changes per minute, the longest one-chord span and the share of the two commonest chords. A low rate can name a take stuck on one chord (generate's acestep.md) but suits an ambient bed; 0.3 changes a minute appeared on a 10-minute bed. It prints no chord names: the best recognizer in Müller's book reaches F about 0.74 on one rock catalogue, and one fixed triad can score 0.55 (R-20261106-1).
Sections (`--sections`) found 85% of known boundaries in spliced real renders (compose L-003): recall on splices; published real-structure scores are about 50-70% pairwise F (Lerch).
