# Slide guitar study (2026-11-13)

Question: how does musicwright get a convincing slide (bottleneck, lap steel, dobro) guitar, from notation, from a text-to-music model, or from samples? Sources checked on 2026-11-13. Nothing here has been judged by a listener except where it says so.

## What was wrong locally

- `mw.py render` turned tab slides into new plucks: `parse_tab` read `5/7` as two notes, wrote no pitch bend and the MIDI reader dropped controllers. The compose notation table said so ("bends and slides as pitch changes" were not read). LEARNINGS entry `no-slide-or-bend-in-render`.
- A working route existed outside the plugin, in the owner's own game-music code (so copying it in is fine): a numpy string model with one pluck, a legato glide between slide notes, a bar scrape that follows the pitch speed and late vibrato. In a blind A/B the listener preferred it to sampled and SoundFont slides. Samples still beat it for plain plucks, so the kept arrangement was a hybrid: samples for plucks, the string model for the slide line.
- Fixed in 0.1.31: see "What was built" below.

## MIDI slide rules (for a SoundFont or sampler)

- Set the bend range first: RPN 0 (CC101 0, CC100 0, CC6 12, CC38 0, then CC101/100 127 to close). The General MIDI default is +-2 semitones, the main reason MIDI slides sound wrong or stop short. FluidSynth and sfizz honour RPN 0.
- Fewer note-ons: a slide is one pluck that glides. Re-plucking each fret is the tell of a sequenced slide.
- Approach the target from 1/8 to 1/2 semitone below over 30-80 ms for slide-ins; glides between frets 90-320 ms, longer for wider moves.
- Overshoot slightly and settle (about 0.1 semitone, 200 ms).
- Late, wide vibrato: starts after the note has settled, 4-6 Hz, +-20 to 40 cents (a fretted vibrato is narrower and starts sooner).
- Mono legato: one slide line per channel, or the bend drags every sounding note along.

## Text-to-music prompt tags

Evidence is from Suno users only; untested on ACE-Step. Tags: "bottleneck slide guitar", "lap steel slides", "slide resonator guitar", "warm dobro slides"; a genre (delta blues, country, Hawaiian); a role ("long gliding notes between vocal lines"). Treat as candidates for a judged A/B, not a recipe.

## Sample instruments and recordings

- Commercial: Ample Slide Lapsteel; Orange Tree Samples SLIDE (about $79, Kontakt).
- Free: Spitfire LABS Lap Steel (a plugin, so it needs a VST host such as DawDreamer to script).
- Free recordings are scarce: Freesound "blues slide riff" by juskiddink, listed public domain (freesound.org/s/77268, verify the licence on the page before use); Pianobook Dobro Slide (use in music allowed, no redistributing resampled libraries).
- Palette idea: cut a recording into single notes, glides of +-1, 2, 3, 5 and 7 semitones and vibrato tails; write a pitch manifest with pyin; place them with Rubber Band R3 (`--pitchmap`/`--timemap`, `--formant`) keeping shifts within 3-4 semitones.
- Audacity is for auditioning and manual clean-up only. Its mod-script-pipe needs the GUI running, so it is not an automation route.

## Source material from full mixes

- Separation: Demucs `htdemucs_6s` has a guitar stem; UVR and MVSep wrap similar models. No separator targets slide guitar specifically.
- Artefacts and bleed are acceptable for training a LoRA or a timbre model, risky for palette notes that will be heard bare.
- Sparse old recordings (one guitar and a voice) separate best.
- A LoRA trains fine on full captioned mixes; separation is optional there.

## Teaching a model one instrument

- ACE-Step 1.5 LoRA: the official repo has a LoRA training tab; its benchmark is 8 songs in about 1 hour on a 3090, and it lists 12 GB VRAM; the paper says a LoRA trains from a few songs and inference runs under 4 GB. The XL (4B) variants want 12 GB with offload, 20 GB recommended. Sources: [ACE-Step-1.5 repo](https://github.com/ACE-Step/ACE-Step-1.5), [arXiv 2602.00744](https://arxiv.org/abs/2602.00744). Not verified here: VRAM for a LoRA on the XL model.
- ACE-Step reference audio and repaint: both are listed features (reference audio for style guidance; repaint for local regeneration that uses the surrounding audio as context). A slide phrase can be repainted into a take, or a slide clip given as reference. Untested for slide timbre. Source: same repo README; the community [tutorial](https://huggingface.co/aTrapDeer/ace-step15-endpoint/blob/main/docs/Tutorial.md).
- Stable Audio Open: fine-tune with stable-audio-tools (`train.py --ckpt-path` from the released checkpoint, JSON configs, PyTorch 2.5+). The weights are under Stability's community licence, which limits commercial use. Sources: [stable-audio-tools README](https://github.com/Stability-AI/stable-audio-tools), [arXiv 2407.14358](https://arxiv.org/abs/2407.14358).
- MusicGen-melody: 1.5B (and a 3.3B large) model conditioned on text plus a melody's chromagram (`generate_with_chroma`). A rendered slide line could steer the melody, but the chroma carries pitch class, not the glide, and the weights are CC BY-NC 4.0. Sources: [audiocraft MUSICGEN.md](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md), [model card](https://facebookresearch.github.io/audiocraft/model_cards/MUSICGEN_MODEL_CARD.html).
- Timbre transfer: RAVE/BRAVE and DDSP turn a rendered line (the string model or a SoundFont) into the target timbre. DDSP is monophonic and wants 30-60 minutes of clean single-instrument audio; [arXiv 2503.11562](https://arxiv.org/abs/2503.11562); a 2024 Hosei University study chained DDSP into RAVE on SoundFont renders. A physical Karplus-Strong model alone stays a plucked synth.
- Data scarcity: free slide recordings are few, so a timbre model is the hardest route; a LoRA on captioned mixes is the cheapest.

## Style LoRA on old records

- Technically yes: 30-100 captioned tracks is a usual LoRA set.
- Rights: in the US, sound recordings published before 1923 entered the public domain on 1 January 2022 under the Music Modernization Act; since then each publication year enters on 1 January 100 years later, so 1925 recordings entered on 1 January 2026 (terms change for recordings from 1947 on). Check each recording; the underlying composition has its own copyright. Sources: [UCSB DAHR, Public Domain Day 2026](https://adp.library.ucsb.edu/index.php/resources/detail/516), [Music Modernization Act](https://en.wikipedia.org/wiki/Music_Modernization_Act), [LoC on the MMA](https://blogs.loc.gov/now-see-hear/2019/02/copyright-breakdown-the-music-modernization-act/).
- Data: pre-1926 blues and Hawaiian steel guitar records (archive.org items marked public domain), plus renders of a free lap steel plugin. The Library of Congress National Jukebox streams Victor recordings 1901-1925 under a streaming licence from Sony with no downloads, so it is a listening source, not a training download ([about page](https://www.loc.gov/jukebox/about)).
- Caption with generic style words, never a performer's name. Keep a model trained on material that is not public domain out of any project that may be sold, and declare AI content where a store asks (Steam's disclosure).

## What was built (0.1.31)

- Tab `/`, a backslash and `s` between frets become one note with a glide; `/7` at the start slides in from two semitones below (a backslash from above); `~` after a fret asks for vibrato. Glides wider than 12 semitones re-pluck with a warning.
- Slide notes go on their own track and MIDI channel with RPN 0 = +-12 and a pitch-bend curve every 10 ms: glide 90-320 ms, 0.08 overshoot, 200 ms settle, late vibrato at 5 Hz +-0.3 semitones after 0.3 s on holds over 0.6 s. FluidSynth plays the MIDI file as written, so the bends reach the audio.
- The built-in synth renders slide notes with a stdlib port of the string model (12 partials, scrape noise). `--slide-engine string` also routes the slide track through that model when FluidSynth renders the rest, mixed at -6 dB.

## Ranked plan

1. Done: bend range plus glide curve in MIDI render, string model in the built-in synth.
2. Listener A/B: SoundFont glide vs `--slide-engine string` on the same tab.
3. Prompt-tag A/B on ACE-Step 1.5 with the tags above, two seeds each.
4. Palette from a public-domain recording (separated if needed), placed with Rubber Band.
5. ACE-Step LoRA on public-domain slide records, then reference/repaint tests.
6. Timbre transfer (RAVE or DDSP) only if a clean hour of data turns up.
