# Caption vocabulary

Shape: **genre + era/production + 3-5 instruments + 2-3 moods + vocal or "instrumental" +
structure hint**. Tempo and key go in their own fields when the model has them.

- **Genres**: orchestral, cinematic, epic trailer, ambient, dark ambient, drone, synthwave,
  retrowave, darksynth, chiptune, 8-bit, lo-fi hip-hop, downtempo, trip-hop, house, deep house,
  techno, trance, drum and bass, dubstep, IDM, glitch, industrial, rock, post-rock, math rock,
  shoegaze, metal, folk, celtic, bluegrass, jazz, bossa nova, funk, soul, R&B, gospel, blues,
  country, reggae, afrobeat, flamenco, J-pop, city pop, K-pop, hip-hop, trap, boom bap, musical
  theatre, sea shanty, medieval, baroque, minimalism, melodic electronica.
- **Era and production**: 70s analog, 80s gated reverb, 90s, Y2K, modern, vintage tape, live
  room, studio-polished, bedroom, lo-fi, hi-fi, wide stereo, mono, dry, cavernous, close-miked.
- **Moods**: tense, ominous, heroic, triumphant, melancholic, hopeful, playful, mysterious,
  dreamy, serene, eerie, frantic, driving, brooding, nostalgic, whimsical, majestic, sunny.
- **Timbre**: warm, bright, dark, airy, breathy, crisp, punchy, gritty, distorted, lush, sparse,
  intimate, wide, distant, glassy, metallic, wooden, plucked, bowed, legato, staccato, pizzicato,
  tremolo, swelling, pulsing, shimmering, detuned, analog, tape-saturated.
- **Structure hints**: slow build, building to a climax, steady loop, no intro, abrupt stop,
  fade-out ending, sparse then full, solo section, call and response.
- **Space and placement**: low in the mix, distant, upfront, faint, subtle, in the background.
- **Depth**: name the near part and the far part together. Near: close, dry, bright, upfront. Far:
  distant, dark, reverberant, soft. "close, dry, bright solo flute; distant, dark, reverberant
  string pad; soft low drums". Dry and close against wet and far is how a mix shows
  depth, and the words models know for it.
- **Low end, beat-driven**: tight short kick, offbeat bass, bass between the kicks.

## Describing a reference without naming the artist

Listen until you can fill five fields, then work only from the fields (after DeSantis, *Making
Music* ch. 5). The result is a description, never a copy.

| Field | Write down | Goes to |
|---|---|---|
| Sound | instruments, timbre, production, space | caption |
| Harmony | key or mode, how often the chords change | `--key`, mood words |
| Melody | lead instrument, register, contour, motif | caption |
| Rhythm | tempo, feel (straight, swung, half-time), the drum sound | `--bpm`, caption |
| Form | sections in order with their bars or seconds, what enters and leaves | `--sections`, `mw.py join --lengths` |

Translate the reference into: genre + era + instruments + vocal texture (gender, register,
breathy, raspy, belted, vibrato) + production (reverb size, saturation, drum sound) + tempo feel
+ what the arc does. Example: "an artist known for sunny instrumental electronica" becomes
"melodic mid-tempo electronica, clean bright electric guitar, warm analog synth pads, round bass,
organic electronic drums, sunny, nostalgic, hi-fi". Long-dead composers and historical styles
are fine to name.

Why: Suno strips artist names; Spotify removes tracks that imitate a voice without permission;
ACE-Step's README warns about stylistic similarity. Describing is also more precise.

## Period and acoustic music

Mood words like "gentle" or "tender" pull a modern downtempo sound even with strings in the
caption. For period or classical cues name period instruments and forms ("string quartet,
pizzicato cello, harpsichord continuo, baroque suite", "romantic-era orchestra, low strings,
solo piano") and drop modern production words.

## Failure modes

- Conflicting styles fuse badly: put contrast in time.
- Caption and sections disagree: the model follows neither well.
- Over-stacked tags get sung as lyrics in vocal tracks.
- Metadata contradicts the caption ("slow ballad" at 170 bpm).
- Extreme tempo, rare keys or very long durations go unstable or repetitive.
- Naming an instrument to exclude it ("no drums") can bring it in.

## Lyrics that sing

Mark the stressed syllables and place them on beats 1 and 3 or on the longer notes; read every
line aloud at the target tempo before rendering. A line that fights the natural stress of its
words sounds forced in a sung take (DeSantis ch. 54). ACE-Step wants 6-10 syllables a line.
