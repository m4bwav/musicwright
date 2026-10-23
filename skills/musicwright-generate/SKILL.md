---
name: musicwright-generate
description: "Use when music should come from an AI model and the question is which model or how to prompt it: pick the model for the job and licence (ACE-Step 1.5 XL or MiniMax Music 3 locally through ComfyUI, the ACE-Step REST server for drafts, cover, repaint and stems, YuE2, Stable Audio 3, hosted Lyria 3.5 or ElevenLabs), write captions and section tags, fish with seeds, fix harsh or off-brief takes, build long pieces from movements. Use on 'which music model', 'ACE-Step settings', 'it sounds harsh', 'can I use Suno output commercially'. A whole track from a brief ('make me a song') starts at musicwright; theory is -compose; finishing is -produce. Also 'refresh musicwright-generate'."
---

# musicwright-generate

Text (and sometimes audio) in, music audio out. This skill chooses the model, writes the prompt,
runs the takes through `mw.py gen` (in the musicwright hub's `scripts/`) and steers the re-rolls.
The hub's take loop (sheet, report, verdict) applies to every render.

## Step 1: choose the model

Check what can run here first: `mw.py doctor` lists `recipes_runnable`. Then:

| Job | First choice | Why |
|---|---|---|
| Instrumental 30 s to 4 min (beds, themes, solos, cues) | `acestep-xl-sft` (ComfyUI) | MIT, commercial outputs, best local quality, about 1.5 min per 3 min |
| Fast drafts, many seeds | `acestep-rest` (2B turbo) | a 60 s take in about 22 s once warm |
| Cover, repaint a time range, extend, stems | ACE-Step REST tasks | not in ComfyUI core ([references/acestep-rest.md](references/acestep-rest.md)) |
| Song with sung lyrics | `acestep-xl-sft` with lyrics, then `minimax-music3` as a second opinion | MiniMax needs product attribution and disclosure |
| Lyrics-led song with an editable score | YuE2 (ComfyUI native) | not yet measured on 16 GB; companies need a licence |
| Loops and SFX, licensed training data | Stable Audio 3 Small or Medium (ComfyUI native) | free under USD 1M revenue; no vocals |
| Hosted, paid | Lyria 3.5 (USD 0.08 a song, SynthID), ElevenLabs Music (USD 0.15 a minute) | check plan terms for film and games |
| Suno, Udio | manual only, never automated | no public API; Udio downloads are off |

Model details, VRAM and licences: [references/models.md](references/models.md) and
[references/licences.md](references/licences.md). Say which licence applies before rendering.

## Step 2: write the prompt (ACE-Step; MiniMax differs, see references/minimax3.md)

- **Caption = what it sounds like.** Genre + era/production + 3-5 instruments + 2-3 mood words +
  "instrumental" or a vocal description + a structure hint. Four or more dimensions, specific
  words, no contradictions. If two styles must meet, make the contrast happen over time in the
  sections instead of in the caption.
- **Keep tempo and key out of the caption**: they go in `--bpm` and `--key`. A ballad caption at
  170 bpm fights itself.
- **Sections = what happens over time.** `--sections "Intro - breathy flute|Verse - melody|Bridge -
  ornamented|Outro - fading flute"`: one modifier per bracket, 4-6 sections for 3 min, 7-9 for 10
  min, and they must agree with the caption. Without sections use `[Instrumental]`.
- **Sections carry density**: say who plays, not only the mood: `Intro - pad and kick only|Build -
  bass and arpeggios enter|Breakdown - drums drop out|Outro - parts leave in reverse order`. Name
  the near and the far parts in the caption (close, dry lead; distant, dark pad).
- **Read the listener's taste first**: the studio's `taste.md`, including its "Tired of" list
  (musicwright-curate), so a new caption does not repeat what they have worn out.
- **Say what to leave out by saying what is there**: "solo flute, unaccompanied" works better than
  "no drums", because naming an instrument can summon it.
- **Noise textures** (static, hiss, beeps, sonar) come out loud and harsh. Qualify them ("faint,
  distant, low in the mix") or add them afterwards.
- **No living artists.** Describe era, instruments, production and feel instead.
- Full rules, examples and the vocabulary: [references/acestep.md](references/acestep.md) and
  musicwright-compose's references/vocabulary.md.

## Step 3: fish, then lock

1. Fish: 3-6 seeds at the target length (or 120-180 s for long pieces), same caption.
2. Look and report (hub Step 3), get a verdict, lock the best seed.
3. Change **one** knob, re-render the locked seed, compare on matched copies (`mw.py preview`).
   Then scale up.
4. Stop: three or four one-knob changes after the lock is usually the end of real gains. When the
   last two did not help, say so and finish with the best take; further changes are a coin toss
   (after DeSantis, *Making Music* ch. 76, 78).

Cheat-sheet (ACE-Step XL):

| Problem | Change |
|---|---|
| harsh, brittle | cfg down (7 to 4-5); the default recipe is already 4.5 |
| boring, static | better sections; LM temperature 0.85 to 1.0 (`--set '{"temperature":1.0}'`) |
| ignores the caption | LM cfg 2 to 3 (`--set '{"lm_cfg":3}'`), or recipe `acestep-xl-sft-classic` |
| mushy, smeared | shift 3 to 4 |
| sterile, stiff | shift 1.5-2 |
| wrong tempo or key | set `--bpm` and `--key` explicitly |
| an unwanted instrument | reword the caption (solo, unaccompanied, only X); re-roll seeds |
| goes quiet at the end | render 5-10 s longer than needed and trim |

## Step 4: long pieces and changes of mood

One caption holds one colour: a single 60 s render will not travel from dread to dawn even with
section tags. Render each movement with its own caption, key and length (a few seconds longer
than its slot), then join them on the hit points: `mw.py join a.flac b.flac c.flac --lengths
24,10,12 --xfade 2` (musicwright-score has the full method). Ten-minute one-shots drift and
repeat; three movements of about 3 min crossfaded hold up better.

## Step 5: add a part to a kept take

1. `mw.py pulse lead.flac`: a steady pulse can carry percussion; with none, offer a re-render at
   a fixed bpm or phrase-placed accents instead of a beat.
2. Start the REST server on `acestep-v15-base` (references/acestep-rest.md), then
   `mw.py gen --recipe acestep-rest-lego --task lego --src lead.flac --track woodwinds --caption "..."
   --seeds 8101,8202,8303`. Sheet each take: noise means DCW was on (an old server).
3. Lego plays along rather than answering. For call and response,
   `mw.py duck part.wav --under lead.flac --stem --out answer.wav`, then `mw.py answer answer.wav --lead lead.flac`.
4. `mw.py mix lead.flac answer.wav --stems stems/ --out mix.wav`; let the listener judge the plain
   and the ducked mix side by side.


- Record every take in the ledger (mw.py does it). A take with no seed and caption is lost work.
- A recipe goes into `recipes.json` only after a listener kept a take made with it.
- A shared GPU runs one heavy job at a time: queue behind video or image jobs, never cancel them.
  The REST server and ComfyUI's ACE-Step each hold 10-13 GB on a 16 GB card, so do not run both.
- Hosted APIs cost money: say the price and ask before the first paid call.

## References

- [references/models.md](references/models.md): every model by task, VRAM, ComfyUI support, length, status.
- [references/acestep.md](references/acestep.md): ACE-Step captions, sections, parameters, failure modes.
- [references/minimax3.md](references/minimax3.md): MiniMax Music 3's three-heading caption and its quirks.
- [references/acestep-rest.md](references/acestep-rest.md): the REST server, launch, payloads, cover, repaint, extract.
- [references/hosted.md](references/hosted.md): Lyria, ElevenLabs, Suno, Udio, Mureka: routes, prices, terms.
- [references/licences.md](references/licences.md): output rights, disclosure lines, platform rules.

## Maintenance

Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md), [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md),
[LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), `evergreen.json`. Models and terms change
monthly: read `evergreen.json` first and refresh when due.
