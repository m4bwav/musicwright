# Theory for prompting and judging

Rules of thumb. Sources and finding numbers: ai-docs/research/03-music-fundamentals.md (R-201 to R-208).

## Modes and moods

A model responds better to mood words plus the mode name than to the mode alone; set the key
in the key field.

| Mode | Against major | Mood words | Use |
|---|---|---|---|
| Ionian (major) | 1 2 3 4 5 6 7 | bright, resolved, triumphant | menus, victory, cosy |
| Lydian | #4 | dreamy, floating, wonder, sci-fi awe | space, discovery, title screens |
| Mixolydian | b7 | heroic, bluesy, swagger | adventure, frontier, rock |
| Dorian | b3 b7 | minor but hopeful, folk, cool | exploration, Celtic, lo-fi |
| Aeolian (natural minor) | b3 b6 b7 | sad, serious, epic | drama, boss intro |
| Phrygian | b2 b3 b6 b7 | dark, menacing, Spanish | villains, desert, metal |
| Locrian | b2 b3 b5 b6 b7 | unstable, horror | brief tension only |
| Harmonic minor | b3 b6, natural 7 | exotic, villainous, gothic, "ancient" | mystery |
| Whole tone | all whole steps | dreamlike, weightless | flashbacks, zero-g, magic |

Space palette: Lydian and whole tone for wonder; sus2, sus4 and quartal chords for open space;
Phrygian or harmonic minor for hostile factions.

## Pentatonic and world scales (semitones above the root)

- Major pentatonic 0 2 4 7 9: open, folk, "no wrong notes". Chinese pentatonic modes gong (0 2 4
  7 9), shang, jue, zhi, yu (0 3 5 7 10).
- Minor pentatonic 0 3 5 7 10: blues, rock, and the primary scale of contemporary six-hole
  Native American flutes (common keys F#4, G4, A4). Prompt: "native american flute, breathy,
  solo, canyon reverb".
- Japanese in (miyako-bushi) 0 1 5 7 8: dark, plaintive (koto, shakuhachi). Yo 0 2 5 7 9: folk,
  festive.
- Maqam: Ajam ~ major, Nahawand ~ harmonic minor, Kurd ~ Phrygian, Hijaz 1 b2 3 4 (the "desert"
  augmented second). Rast and Bayati use quarter tones that current models only approximate.
- Double harmonic 0 1 4 5 7 8 11, Phrygian dominant 0 1 4 5 7 8 10: the cliché "exotic" sound.

## Progressions (Roman numerals; lower case = minor)

- Pop: I-V-vi-IV, I-V-vi-iii (Pachelbel), vi-V-IV-V, I-vi-IV-V, I-IV-vi-V.
- Epic/trailer: i-VI-III-VII; i-VI-VII; an ostinato over a pedal tone.
- Heroic: I-bVII-IV-I; victory cadence bVI-bVII-I.
- Wonder: I-II (Lydian); chromatic mediants I-bVI, I-III, I-bIII.
- Sad: vi-IV-I-V; i-iv; I-iii-vi-IV.
- Menace: i-bII; i-bVI-iv-V in harmonic minor; tritone moves.
- Flamenco: i-bVII-bVI-V. Jazz/lo-fi: ii7-V7-Imaj7, turnaround I-vi-ii-V. Blues: 12-bar.
- Ambient: one or two chords changing every 4-8 bars over a drone.

## Tempo (bpm)

ACE-Step guidance: 60-80 slow, 90-120 mid, 130-180 fast; extremes unstable. Ambient 60-80 or
no pulse; ballad 60-80; lo-fi 70-90; hip-hop 85-100; synthwave 80-118; pop 95-130; rock 100-140;
house 118-128; techno 125-140; trance 130-145; drum and bass 160-178; orchestral exploration
80-110, combat 130-170; card and strategy beds 80-110 (low fatigue). Trackers and models may
report double or half the felt tempo.

## Meter

4/4 default and most reliable. 3/4 waltz, lullaby; 6/8 lilting, jig, shanty, gallop; 12/8 shuffle;
5/4 and 7/8 restless or alien (models drift back to 4/4: say "in 7" as well as the field).

## Form

Verse-chorus: Intro, V1, (Pre), Chorus, V2, (Pre), Chorus, Bridge, Chorus, Outro, sections of 8
or 16 bars (at 120 bpm in 4/4 one bar is 2 s). AABA: four 8-bar sections. Through-composed: no
repeats, follows the story (most film cues). Game loop: A-B-A'-C and back. EDM: intro, build,
drop, breakdown, build, drop, outro in 16/32-bar blocks.

## Motif development

A motif is 2-7 notes with a recognisable rhythm. Develop it: repeat, sequence (higher or lower),
invert, reverse, augment (slower), diminish (faster), fragment, reharmonise, change mode (hero
theme in minor for the tragic beat), change orchestration (solo flute, then full brass). One
main theme reused across menu, map, boss and victory makes a soundtrack feel authored.

## Ranges (sounding pitch, C4 = middle C) and colour

- Strings: violin G3-E7 (high = shimmer, tension); viola C3-E6 (warm, dark); cello C2-A5 (A2-A4
  the "voice"); double bass E1-G4.
- Woodwinds: flute C4-C7 (low breathy, high bright); oboe Bb3-A6 (plaintive); clarinet D3-Bb6;
  bassoon Bb1-E5 (comic or mournful).
- Brass: horn B1-F5 (heroic, noble); trumpet E3-C6 (fanfare; muted = noir); trombone E2-Bb4
  (power); tuba D1-F4 (weight).
- Other: harp (glissando magic), timpani D2-A3, glockenspiel G5-C8 (sparkle), celesta C4-C8
  (wonder), piano A0-C8, guitar E2-E6, bass guitar E1-G4.
- Voices: soprano C4-A5, alto F3-D5, tenor C3-A4, baritone A2-F4, bass E2-E4; choir "aah" =
  epic, "ooh" = soft.

## Density and register (for judging)

3-5 focal elements at once. Bass below about 200 Hz, harmony 200 Hz-2 kHz, lead 1-4 kHz, sparkle
above 5 kHz. Same register and same rhythm = masking. A good track has at least two density
levels. Under dialogue or busy game sound effects, keep the 1-4 kHz lead sparse.
