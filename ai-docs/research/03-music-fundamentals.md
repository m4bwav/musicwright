# 03 - Music fundamentals for an agent that makes, judges and finishes music

Research for the musicwright plugin. Checked 2026-10-17 unless a finding says otherwise.
Audience: an agent prompting text-to-music models (ACE-Step 1.5 locally, Suno/Udio if used),
judging the output, and finishing it for three destinations: a Unity card game
(deckbuilder), AI short films, and personal listening. The intended user has strong taste
and no formal training, so every finding is a rule of thumb, a number or a checklist.

Labels: **[verified 2026-10-17]** = run on the test PC (Windows 11; ffmpeg 9.0.1 gyan.dev, Python 3.12
via uv, librosa 1.0.0, pyloudnorm) on generated test signals; **[source]** = from the
cited page; **[practice]** = practitioner rule of thumb; **unverified** = not run here.

## 1. Theory for prompting and judging

### R-201 Modes and the moods they carry [practice]
Mode = which scale degrees are raised or lowered against major. A text-to-music model
responds to the mode name less reliably than to mood words plus the mode, so put both
in the caption ("lydian, dreamy, wonder") and set the key in the `keyscale` field.

| Mode | Formula vs major | Mood words | Use |
|---|---|---|---|
| Ionian (major) | 1 2 3 4 5 6 7 | bright, resolved, triumphant | menus, victory, cozy |
| Lydian | #4 | dreamy, floating, wonder, sci-fi awe | space, discovery, title screens |
| Mixolydian | b7 | heroic, bluesy, rock swagger | adventure, frontier, rock |
| Dorian | b3 b7 (natural 6) | minor but hopeful, folk, funky, cool | exploration, Celtic, lo-fi |
| Aeolian (natural minor) | b3 b6 b7 | sad, serious, epic | drama, boss intro, epic |
| Phrygian | b2 b3 b6 b7 | dark, exotic, menacing, Spanish | villains, desert, metal |
| Locrian | b2 b3 b5 b6 b7 | unstable, horror | brief tension only |
| Harmonic minor | b3 b6, natural 7 | exotic, villainous, gothic | villains, mystery, "ancient" |
| Whole tone | all whole steps | dreamlike, weightless, unresolved | flashbacks, zero-g, magic |
| Chromatic / atonal | all 12 | horror, alien, chaos | horror, alien encounters |

Space-game palette: Lydian and whole-tone for wonder; sus2/sus4 and quartal (stacked
fourths) chords for "open space"; Phrygian or harmonic minor for hostile factions.
Source for the interval formulas: any theory text, e.g. Open Music Theory
(https://viva.pressbooks.pub/openmusictheory/, page refused automated fetch 2026-10-17).

### R-202 Pentatonic and world scales (semitones above the root)
- **Major pentatonic** 0 2 4 7 9: open, folk, "no wrong notes". Chinese pentatonic is
  this set; its five modes are named gong (0 2 4 7 9), shang, jue, zhi and yu
  (yu = 0 3 5 7 10, i.e. minor pentatonic). [practice]
- **Minor pentatonic** 0 3 5 7 10: blues, rock, Native American flute. Flutopedia
  names "Pentatonic Minor" as the primary scale of contemporary six-hole Native American
  flutes (flutes made since about 1980), with six notes in the primary scale
  (root to octave). https://www.flutopedia.com/scales.htm [source]. Common flute keys
  are F#4, G4 and A4 [practice]. Prompt words: "native american flute, breathy, solo,
  canyon reverb"; do not name a tribe or a sacred ceremony.
- **Japanese in (miyako-bushi)** 0 1 5 7 8 on D = D Eb G A Bb (auxiliary F and C).
  Hemitonic (has semitones), dark and plaintive: koto, shakuhachi.
  https://en.wikipedia.org/wiki/In_scale [source]
- **Japanese yo** 0 2 5 7 9 (anhemitonic, no semitones): folk, festive, min'yo.
  https://en.wikipedia.org/wiki/Anhemitonic_scale [source]. Ritsu and ryo are
  anhemitonic chant scales (ritsu M2 m3 M2 M2 m3).
  https://en.wikipedia.org/wiki/Ritsu_and_ryo_scales [source]
- **Maqam (Arabic)**: a maqam is built from two or three ajnas (tetrachord-like cells);
  the lower jins sets the character. Families on MaqamWorld: Ajam, Bayati, Hijaz, Kurd,
  Nahawand, Nikriz, Rast, Sikah; Saba stands alone.
  https://www.maqamworld.com/en/maqam.php (Johnny Farraj) [source]. Quick map
  [practice]: Ajam ~ major; Nahawand ~ harmonic minor; Kurd ~ Phrygian; Hijaz = 1 b2 3 4
  (augmented second, the "desert" sound); Rast and Bayati use quarter tones (E half-flat,
  B half-flat over C/D) that equal-tempered models only approximate. Ask for
  "oud, ney, qanun, darbuka, maqam hijaz" and expect Hijaz-flavoured 12-TET; real quarter
  tones are unlikely from current models.
- **Double harmonic / Byzantine** 0 1 4 5 7 8 11 and **Phrygian dominant** 0 1 4 5 7 8 10:
  the cliché "exotic" sound. Use sparingly; it reads as stereotype. [practice]

### R-203 Chord progressions by mood (Roman numerals, major key unless lower case)
Hooktheory's most common pop progressions: I-V-vi-IV (most popular), I-V-vi-iii
(Pachelbel), vi-V-IV-V, I-vi-IV-V ("magic changes"), I-IV-vi-V, I-V-IV-V.
https://www.hooktheory.com/theorytab/common-chord-progressions [source]
By mood [practice]:
- **Epic / trailer**: i-VI-III-VII (Am F C G); i-VI-VII; ostinato over a pedal tone.
- **Heroic**: I-bVII-IV-I (Mixolydian); bVI-bVII-I ("victory" cadence, used in games).
- **Wonder / sci-fi**: I-II (Lydian, C to D major); chromatic mediants I-bVI, I-III, I-bIII.
- **Sad / reflective**: vi-IV-I-V; i-iv; I-iii-vi-IV.
- **Menace**: i-bII (Phrygian); i-bVI-iv-V with harmonic minor; tritone moves.
- **Spanish / flamenco**: Andalusian cadence i-bVII-bVI-V.
- **Jazz / lo-fi**: ii7-V7-Imaj7; extended chords (7ths, 9ths); turnaround I-vi-ii-V.
- **Blues**: 12-bar I-I-I-I-IV-IV-I-I-V-IV-I-V.
- **Ambient**: one or two chords, slow changes (every 4-8 bars), pedal drones.

### R-204 Tempo ranges by genre and use [practice, ACE-Step guidance where cited]
ACE-Step's own guidance: 60-80 BPM slow songs, 90-120 mid-tempo, 130-180 fast; `bpm`
accepts 30-300 and extremes are unstable.
https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md [source]
Ambient/drone 60-80 or no pulse; ballad 60-80; lo-fi hip-hop 70-90; hip-hop 85-100
(trap 130-150 counted double time); synthwave 80-118; pop 95-130; rock 100-140;
house 118-128; techno 125-140; trance 130-145; drum and bass 160-178; metal 100-200;
orchestral exploration 80-110; orchestral combat 130-170; card/strategy background
80-110 (low fatigue). Doubling: a model or beat tracker may report half or double the felt tempo. Check by ear.

### R-205 Time signatures [practice]
4/4 default (ACE-Step: most reliable; 3/4 and 6/8 usually fine; complex meters vary
[source: Tutorial above]). 3/4 waltz, lullaby, old-world. 6/8 lilting, Celtic jig,
sea shanty, galloping cavalry. 12/8 blues shuffle, slow gospel. 5/4 and 7/8 restless,
off-kilter, alien or puzzle; good for sci-fi tension but models may drift back to 4/4.
Prompt both the meter field and words ("waltz", "in 7").

### R-206 Song form [practice]
- **Verse-chorus**: Intro, V1, (Pre), Chorus, V2, (Pre), Chorus, Bridge, Chorus, Outro;
  sections 8 or 16 bars (120 BPM 4/4: 1 bar = 2 s). **AABA**: four 8-bar sections, B =
  contrast. **12-bar blues**. **Through-composed**: no repeats, follows a story (most
  film cues). **Game loop**: A-B-A'-C then back; never one 8-bar loop. **EDM**: intro,
  build, drop, breakdown, build, drop, outro in 16/32-bar blocks.
ACE-Step reads section tags in lyrics: [Intro] [Verse] [Pre-Chorus] [Chorus] [Bridge]
[Outro] [Build] [Drop] [Breakdown] [Instrumental] [Guitar Solo] [Piano Interlude]
[Fade Out] [Silence]; modifiers with a hyphen ([Chorus - anthemic]); 6-10 syllables per
line; instrumental tracks can be a sequence of section tags.
https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md [source]

### R-207 Motif and development [practice]
A motif is 2-7 notes with a recognisable rhythm. Develop it rather than repeat it:
repetition, sequence (same shape higher or lower), inversion (upside down), retrograde,
augmentation (slower) and diminution (faster), fragmentation (just the head), reharmonise
(same tune, new chords), change of mode (major hero theme in minor for the tragic beat),
change of orchestration (solo flute, then full brass). For a game, one main theme
reused across menu, map, boss and victory makes the soundtrack feel authored. With
current text-to-music models, motif continuity across separate generations is weak:
use one seed plus audio-to-audio/repaint or reference audio, or a cover/remix mode,
rather than hoping a caption reproduces the tune.

### R-208 Orchestration: ranges and timbre vocabulary [practice; ranges from standard orchestration texts, C4 = middle C, sounding pitch]
- Strings: violin G3-E7 (singing E4-A6, high = shimmer/tension); viola C3-E6 (warm,
  dark); cello C2-A5 (A2-A4 the "voice"); double bass E1-G4 (pizzicato pulse).
- Woodwinds: flute C4-C7 (low breathy, high bright); oboe Bb3-A6 (plaintive,
  pastoral); clarinet D3-Bb6 (low dark, high bright); bassoon Bb1-E5 (comic or mournful).
- Brass: horn B1-F5 (heroic, noble, distant); trumpet E3-C6 (fanfare; muted = noir);
  trombone E2-Bb4 (power, menace in clusters); tuba D1-F4 (weight, villain).
- Other: harp Cb1-G#7 (glissando magic); timpani D2-A3 (rolls, hits); glockenspiel
  G5-C8 (sparkle); celesta C4-C8 (fairy, wonder); piano A0-C8; guitar E2-~E6;
  bass guitar E1-~G4.
- Voices: soprano C4-A5, alto F3-D5, tenor C3-A4, baritone A2-F4, bass E2-E4; choir
  "aah" = epic, "ooh" = soft.
Timbre words models respond to: warm, bright, dark, airy, breathy, crisp, punchy,
gritty, distorted, lush, sparse, intimate, wide, distant, glassy, metallic, wooden,
plucked, bowed, legato, staccato, pizzicato, tremolo, swelling, pulsing, shimmering,
detuned, analog, tape-saturated, lo-fi, 8-bit, chiptune.
ACE-Step's tutorial lists the caption dimensions: style/genre, emotion, instruments,
timbre texture, era and production style, vocal character, speed/rhythm and structure
hints (e.g. "fade-out ending"). [source: Tutorial above]

## 2. Genre and style vocabulary

### R-209 Compact tag vocabulary for text-to-music captions [practice + ACE-Step Tutorial]
Build captions as: **genre + era/production + 3-5 instruments + 2-3 mood words + vocal
or "instrumental" + structure hint**. Keep BPM and key out of the caption when the model
has fields for them (ACE-Step says so explicitly [source: Tutorial]).
- Genres: orchestral, cinematic, epic trailer, ambient, dark ambient, drone, synthwave,
  retrowave, darksynth, chiptune, 8-bit, lo-fi hip-hop, downtempo, trip-hop, house,
  deep house, techno, trance, drum and bass, dubstep, IDM, glitch, industrial, rock,
  post-rock, shoegaze, metal, folk, celtic, bluegrass, jazz, bossa nova, funk, soul,
  R&B, gospel, blues, country, reggae, afrobeat, flamenco, J-pop, city pop, K-pop,
  hip-hop, trap, boom bap, musical theatre, sea shanty, medieval, baroque, minimalism.
- Era/production: 70s analog, 80s gated reverb, 90s, Y2K, modern, vintage tape,
  live room, studio-polished, bedroom, lo-fi, hi-fi, wide stereo, mono, dry, cavernous.
- Moods: tense, ominous, heroic, triumphant, melancholic, hopeful, playful, mysterious,
  dreamy, serene, eerie, frantic, driving, brooding, nostalgic, whimsical, majestic.
- Structure hints: slow build, building to a climax, steady loop, no intro, abrupt
  stop, fade-out ending, sparse then full.
Failure modes from the ACE-Step tutorial: conflicting style words get fused badly;
caption-lyrics contradictions; over-stacked tags get sung as lyrics; metadata that
contradicts the caption ("slow ballad" at 170 BPM); extreme BPM, rare keys or very
long durations go unstable or repetitive. [source: Tutorial]

### R-210 Describing a style without naming living artists
- **Suno** says it has never allowed prompts for specific artists or copyrighted songs
  and strips a named artist, steering to descriptive traits
  (https://about.suno.com/blog/building-the-future-of-music-responsibly, search snippet
  only; host did not resolve 2026-10-17). Secondary reports: bracketed names warn
  (Mar 2026); an Aug 2026 lawsuit alleges workarounds.
- **Udio**: no official clause found (terms page did not render); a third-party help
  site says names are blocked (https://prismix.dev/guides/udio-not-working). Re-check.
- **ACE-Step 1.5**: no filter; its tutorial even shows "reminiscent of <artist>". The
  README warns of "unintentional copyright infringement due to stylistic similarity"
  and asks users to verify originality and disclose AI use
  (https://github.com/ace-step/ACE-Step-1.5). Licence per GitHub API 2026-10-17: **MIT**
  (older ace-step/ACE-Step is Apache-2.0); notes saying "Apache 2.0" for
  1.5 are wrong.
- **Distribution**: Spotify removes tracks imitating another artist's voice without
  permission, AI or not, credited or not
  (https://support.spotify.com/us/artists/article/music-that-impersonates-another-artists-voice/,
  https://newsroom.spotify.com/2025-09-25/spotify-strengthens-ai-protections/).
- **Rule for musicwright**: never put a living artist's name in a prompt, even where
  allowed. Translate the reference into genre + era + instruments + vocal texture
  (gender, register, breathy/raspy/belted, vibrato) + production (reverb size,
  saturation, drum sound) + tempo feel. Long-dead composers (Bach, Mozart, Debussy) and
  historical styles ("baroque", "impressionist") are fine.

## 3. Production

### R-211 Arrangement density [practice]
- 3-5 focal elements at once (lead, harmony bed, bass, rhythm, texture); more turns to
  mush, especially from AI. Each owns a register: bass < ~200 Hz, harmony 200 Hz-2 kHz,
  lead 1-4 kHz, sparkle > 5 kHz; same register + same rhythm = masking.
- Contrast drives interest (thin verses, full choruses, breakdowns); a good AI track
  shows at least two density levels. Under dialogue or UI SFX: no busy 1-4 kHz lead.

### R-212 Mixing basics [practice, e.g. Mike Senior "Mixing Secrets for the Small Studio"]
- Frequency map: sub 20-60 Hz, bass 60-250, mud 200-500, body/honk 500-1k,
  presence 1-4k (ear most sensitive; harshness 2-5k), sibilance 5-8k, air 10-16k.
- EQ: cut before boost, narrow cuts, wide gentle boosts; high-pass non-bass parts
  (pads ~100-200 Hz, reverb returns ~200-300 Hz). Masking: carve the rival (dip the
  pad at the vocal's 2-3 kHz), pan apart, or sidechain bass to kick.
- Compression: bus 1.5:1-2:1, 1-3 dB reduction; vocals 3:1-4:1, 3-6 dB; slow attack
  (10-30 ms) keeps transients. Reverb: pre-delay 10-30 ms; rooms intimate, 2-4 s halls
  epic; little on bass and kick. Stereo: kick, bass, lead centred; < ~100-150 Hz mono.
- Mastering AI output: gentle EQ, limiter, loudness normalisation only; AI tracks are
  often already crushed, so add no compression.

### R-213 Loudness targets (integrated LUFS, true peak)
| Destination | Integrated | True peak | Source |
|---|---|---|---|
| Spotify | normalises to -14 LUFS (Loud -11, Quiet -19) | < -1 dBTP; < -2 dBTP if master is louder than -14 | https://support.spotify.com/us/artists/article/loudness-normalization/ |
| Apple Music | normalises (Sound Check) at about -16 LUFS (secondary sources only) | leave at least 1 dB headroom; send 24-bit | Apple Digital Masters brief https://www.apple.com/apple-music/apple-digital-masters/docs/apple-digital-masters.pdf |
| YouTube | turns down to about -14 LUFS, never turns up (not officially documented); "content loudness" in Stats for Nerds | -1 dBTP [practice] | https://en.wikipedia.org/wiki/Audio_normalization |
| AES TD1008 (streaming guidance) | music -16 LUFS | | https://docs.telosalliance.com/docs/understanding-loudness-for-streaming-audio |
| Broadcast EBU R128 v5.0 (Nov 2023) | -23.0 LUFS ±0.5 LU (±1.0 LU live) | ≤ -1 dBTP | https://tech.ebu.ch/publications/r128 (PDF r128v5_0) |
| US broadcast ATSC A/85 | -24 LKFS ±2 | -2 dBTP | [practice, not re-fetched] |
| Netflix | -27 LKFS ±2 LU dialogue-gated (BS.1770-1) | -2 dBTP | https://backlothelp.netflix.com/hc/en-us/articles/360001794307 |
| Games, console (Sony ASWG-R001, IESD) | -24 LUFS ±2 LU over a long capture (30 min reported) | ≤ -1 dBTP | IESD sheet https://www.audiogang.org/wp-content/uploads/2015/04/IESD-Mix-Ref-Levels-v03.02.pdf ; Wwise blog (403 to fetch) |
| Games, handheld/mobile | -18 LUFS ±2 (PlayStation portable, per Wwise Feb 2024) or -16 (IESD) | ≤ -1 dBTP | same; conflicting |
| Xbox | no Microsoft-published target found; industry follows -24 console | | https://devdocs.xbox.com/reference/audio/xaudio2xbox/structs/fxloudness_parameters |
| Steam / PC | no platform spec found | | |
| Film theatrical | calibrated playback (85 dB SPL reference), not a LUFS target; trailers face their own loudness limits (TASA) | | [practice] |
Game note: these targets apply to the **whole game mix** (music + SFX + dialogue). A
music asset in Unity should be mastered consistently (pick one level, e.g. -16 to -18
LUFS for all music stems, -1 dBTP) and balanced against SFX in an AudioMixer, not
mastered to -14 like a Spotify single [practice]. For personal listening and upload,
-14 LUFS / -1 dBTP is the safe single target.

### R-214 Sample rate, bit depth, formats
- 48 kHz for games, film and video (the video world's rate; Xbox loudness metering
  only supports 48 kHz FLOAT32 [source: Xbox FXLoudness page]). 44.1 kHz is fine for
  music-only distribution. Do not upsample AI output (ACE-Step renders 48 kHz) [practice].
- Bit depth: work in 32-bit float, master to 24-bit; 16-bit only for CD-like delivery,
  with dither. Apple asks for 24-bit sources and notes dither for 24 to 16.
  [source: Apple Digital Masters brief]
- Formats: WAV (PCM, master and Unity source), FLAC (lossless, half size; Unity
  imports it), OGG Vorbis (Unity's own compressed format, loops cleanly), MP3
  (distribution only). Measured here: a 13.5 s 48 kHz stereo file was 3.9 MB WAV
  (24-bit), 2.4 MB FLAC, 224 kB OGG q6, 274 kB MP3 V2. [verified 2026-10-17]
- Unity imports .wav .aif/.aiff .mp3 .ogg .flac and tracker modules (.mod .xm .it .s3m).
  https://docs.unity3d.com/Manual/AudioFiles-compatibility.html (Unity 6.6) [source]

### R-215 Why MP3 breaks loops
MP3 frames hold 1152 samples and encoders add a delay at the start (LAME 576 samples;
iTunes 528; FhG 671) plus padding at the end; decoders add ~529 samples more. Gapless
playback works only if the decoder reads the LAME/Xing tag (or iTunes `iTunSMPB`) and
trims. https://web.dev/articles/mse-seamless-playback and
https://hydrogenaudio.org/index.php/topic,61917.0.html [source]
Measured here: a 648,000-sample WAV encoded with LAME decoded back to exactly 648,000
samples by ffmpeg (tag present), but to 649,728 samples (+1,728, 36 ms of silence)
when written with `-write_xing 0`. [verified 2026-10-17] Any engine or tool that
ignores the tag puts a gap in the loop. Use WAV source in Unity (Unity re-encodes to
Vorbis itself) or OGG.

## 4. Game music

### R-216 Seamless loops: checklist
1. Generate or cut so the loop is a whole number of bars: samples = bars x beats per
   bar x 60 / BPM x sample rate. At 120 BPM 4/4 48 kHz, 8 bars = 768,000 samples.
2. The loop end must flow into the loop start musically (same chord or a dominant
   leading back), not just technically.
3. Cut at a zero crossing on both ends, or (better for AI audio with reverb tails)
   crossfade the tail past the loop end into the head (recipe R-229).
4. No fade-in, fade-out or silence inside a loop file; fold the reverb tail past the
   loop end into the start (the crossfade does this) or it cuts off audibly.
5. Concatenate the file three times, listen at the seams, run the R-229 seam check.
Unity: loop with `AudioSource.loop = true`. Unity reads the first loop of a WAV `smpl`
chunk only while playback is already inside the region and always starts from the
beginning, so it cannot do intro-then-loop from metadata
(https://github.com/SkaillZ/tidalwav; WebGL needed a fix:
https://issuetracker.unity.com/issues/1279/a-looping-audio-sounds-different-on-webgl-than-in-the-editornative-desktop-player)
[source, community]. For an intro that plays once then a looping body, ship two clips
and stitch them with `AudioSource.PlayScheduled(dspTime)` on two AudioSources,
scheduling ~100-200 ms ahead; Unity's docs call it the preferred way to stitch music.
https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html [source]

### R-217 OGG loop tags
`LOOPSTART` and `LOOPLENGTH` (some tools `LOOP_START`/`LOOP_END`) are Vorbis comments
in **samples**, used by RPG Maker and others; Unity does not read them, Godot honours
only a custom start in OGG (community reports).
https://github.com/Splendide-Imaginarius/crosslooper (auto-finds loop points, ~76%
right by its own claim); https://rpgmaker.net/forums/topics/11574 [source]
ffmpeg writes them with `-metadata LOOPSTART=... -metadata LOOPLENGTH=...` and ffprobe
reads them back [verified 2026-10-17]. Worth writing anyway: they document the loop
for any engine and a small Unity script can read them from a sidecar JSON.

### R-218 Unity AudioClip import settings for music (Unity 6.6 manual)
https://docs.unity3d.com/Manual/class-AudioClip.html [source]
- Load Type: **Streaming** for long music (decodes from disk, minimal memory, ~200 KB
  overhead per stream); Compressed In Memory for short loops and stingers; avoid
  Decompress On Load for music (decompressed Vorbis is about 10x the memory).
- Compression Format: **Vorbis** ("best for medium length sound effects and music");
  Quality: start high, lower until you hear it, then raise slightly (~70% is a common
  start [practice]). PCM for very short stingers if CPU matters.
- Load In Background: on for large clips; check `AudioClip.loadState`.
- Preload Audio Data: off for streamed music; call `LoadAudioData` before play.
- Force To Mono: off for music.
- Sample Rate Setting: Preserve.
- The manual describes no loop import setting; the Preview "Loop" toggle is Editor-only.

### R-219 Adaptive music techniques [practice; engine docs below]
- **Horizontal re-sequencing**: switch between segments (explore -> combat -> victory)
  at musical boundaries (next bar, next beat, a custom cue), with transition segments
  or stingers between them.
- **Vertical layering (remixing)**: stems of one piece play in sync; game state fades
  layers in and out (drums when enemies appear, brass when health is low). All stems
  must share length, tempo and key; render them from one master session or split with
  Demucs (R-232).
- **Stingers**: 1-8 s phrases played over or between music on events (card played,
  rare drop, level up), quantised to the beat.
- **Parameters**: one 0-1 "intensity" or "threat" value drives layers and switches.
- **Wwise**: Music Switch Container (chooses by State/Switch), Music Playlist Container
  (sequence/random of segments), Music Segment with Entry/Exit Cues, Stingers, transition
  rules with "Sync to" Immediate / Entry Cue / Next Bar / Next Beat / custom cue; default
  state-change transition time 1 s. Audiokinetic blog and courses
  https://www.audiokinetic.com/en/courses/wwise201/ [source, search snippets; pages 403
  to fetch]. Wwise and FMOD both have free indie tiers (check current terms).
- **FMOD Studio**: timeline with loop regions, destination markers, transition markers
  and transition regions (a region points at a marker or loop region and fires when a
  parameter condition holds), quantisation of transitions to bar/beat, tempo markers,
  magnet regions, transition timelines for crossfades. (Feature names from FMOD course
  listings and community tutorials; fmod.com docs render client-side and could not be
  fetched 2026-10-17.)
- **Unity without middleware**: AudioMixer snapshots for layer volumes, `PlayScheduled`
  for bar-quantised switches, two sources per layer for crossfades. Enough for a
  deckbuilder.

### R-220 Conventions and length targets [practice]
- Title/main menu: 1-3 min loop, the main theme, may have a one-shot intro.
- Map/deck building: 2-4 min loop, 2-3 variants, mid tempo, no hook every 20 s.
- Combat/encounter: 1.5-3 min loop plus intensity layers; the boss gets its own.
- Ambient/exploration: 3-6 min or generative; sparse, slow harmonic rhythm.
- Stingers 1-8 s, in the bed's key or neutral percussion. Victory/defeat 5-20 s:
  victory resolves (often bVI-bVII-I), defeat falls. Shop/rest: 1-2 min, warm, light.
A turn-based deckbuilder session runs for hours: fatigue is the enemy. Prefer longer
loops with A/B variation, rotate several tracks per biome, leave room for SFX (no
busy 1-4 kHz lead) and let silence happen between fights.

## 5. Film and video scoring

### R-221 Spotting and cue design [practice]
Spotting session: watch the cut with the director, list each cue with start and end
timecode (SMPTE HH:MM:SS:FF), purpose (emotion, tension, transition, source music),
hits (moments that must land), and what the music must not do (fight dialogue, telegraph
a twist). Name cues 1M1, 1M2 (reel 1, music 1). Music starts and stops are as
important as content: enter under a sound or a cut, exit on a hit or let it tail out.

### R-222 Hitting cues and tempo mapping [practice]
- To land a hit on a downbeat, choose a tempo so the gap between two hits is a whole
  number of beats: BPM = 60 x beats / seconds. Example: hits 7.5 s apart, 16 beats ->
  128 BPM. Allow hits to land within about one frame (42 ms at 24 fps).
- Frame rates: 24, 25, 29.97, 30, 60 fps; one frame at 24 fps = 41.7 ms.
- AI-generated music cannot be told where hits are. Workflow: generate at the chosen
  BPM and length, then edit at bar boundaries (cut, repeat, time-stretch up to about
  ±5% before artefacts [practice]), or generate sections separately and crossfade.

### R-223 Ducking under dialogue
No authoritative dB standard was found; sources give rules of thumb:
start with a 6-12 dB duck, attack 30-80 ms, release 250-700 ms
(https://tryuncle.com/learn/davinci-resolve/how-to-duck-background-music-under-dialogue-in-davinci-resolve);
dip music to about -12 to -20 dB under dialogue
(https://online.bright-publishing.com/view/322383/49/). Practical target [practice]:
dialogue around -16 to -20 LUFS short-term for web video, music bed 10-15 LU below it
while someone speaks. Dialogue-anchored delivery: Netflix measures dialogue-gated
(-27 LKFS, R-213). ffmpeg `sidechaincompress` can duck automatically (R-230).

### R-224 Temp tracks [practice]
A temp track is existing music laid on the cut to set mood and pace. Risks: "temp
love" (the director wants the temp), and with AI it tempts style copying. For
musicwright: analyse the temp (BPM, key, instrumentation, density, form, where it
swells) and write a caption from those descriptors (R-210), never upload the temp as a
reference unless it is the user's own or licensed.

## 6. Judging quality

### R-225 Critique checklist for AI music [practice]
Listen on headphones and on small speakers; listen at the destination loudness.
1. **First 5 seconds**: is there an intro, or does it start mid-phrase? Silence or a
   click at the start?
2. **Vocals**: metallic, phasey, "underwater" or warbling timbre; lyric
   mispronunciation, skipped or invented words; tag text sung as lyrics; vowels
   smeared on long notes; sibilance hiss.
3. **Transients**: mushy or smeared drums, hi-hats turned to noise, kicks without
   punch; pre-echo before hits.
4. **Timing**: tempo drift (compare bar 1 and the last bar against a click), rushed
   fills, beat that flips to half time.
5. **Harmony**: wrong-key notes, chords that change for no reason, bass fighting the
   chords, key drift.
6. **Structure**: sections that do not contrast; chorus that never arrives; collapse
   after 2-3 minutes (repeating one bar, falling apart, sudden genre change);
   repetitive loop with no development.
7. **Ending**: abrupt cut, fade that starts too early, ending on an unresolved chord,
   trailing garbage after the music ends.
8. **Mix**: muddy low mids, harsh 2-5 kHz, dull top (codec-like roll-off above
   ~16 kHz), stereo image collapsing or swirling, artefacts like shimmering "sizzle".
9. **Brief**: does it match the caption's mood, tempo, instruments, and the scene? Would
   it fatigue after 20 loops? Does it leave room for SFX/dialogue?
10. **Originality**: does the melody sound like a known song? If yes, reject.
Score each 1-5 and keep the notes beside the file (seed, caption, verdict).

### R-226 Objective checks a script can run [verified 2026-10-17 unless marked]
| Check | Tool | Flag when |
|---|---|---|
| Integrated loudness, LRA, true peak | ffmpeg `ebur128=peak=true`, pyloudnorm | off target (R-213); TP > -1 dBTP |
| Clipping | ffmpeg `astats` Peak level, Peak count, Flat factor | peak at 0.0 dBFS with a large Peak count; flat factor jumped from 8.4 to 41.3 on a test clipped by +30 dB |
| Leading/trailing silence | ffmpeg `silencedetect=n=-60dB:d=0.2` | > 0.2 s at start, > 1 s at end (one-shots) or any (loops) |
| DC offset | `astats` DC offset | abs > 0.001 |
| Mono compatibility | fold to mono, compare loudness with `ebur128=dualmono=true` | mono > 1.5-3 LU quieter than stereo (a test with auto-pan lost 1.7 LU; mono-safe lost 0.0) |
| Phase | `aphasemeter` mean | mean < 0 (cancellation); ~0.3-0.9 is normal stereo |
| Tempo | librosa `beat.beat_track` | far from the requested BPM (beware 2x / 0.5x); 120 BPM click read as 120.19 |
| Key | chroma + Krumhansl-Schmuckler (librosa), or essentia `KeyExtractor` (default profile `bgate`; also `edma`, `temperley`, `krumhansl`) | differs from requested key; C major test read as C major (r = 0.85) |
| Tempo drift | beat intervals from librosa; std and trend | interval trend > ~1% over the track (unverified threshold) |
| Spectrum | ffmpeg `showspectrumpic` | hard cut-off (e.g. at 16 kHz), holes, constant whine |
| Loop seam | seam jump vs 99th-percentile sample step (R-229 script) | ratio > ~3 (hard-cut sine test: 80; crossfaded: 0.9) |
| Duration | ffprobe | not a whole number of bars for loops |
Essentia reference: https://essentia.upf.edu/reference/std_KeyExtractor.html [source]
librosa 1.0.0 released 2026-08-11 (GitHub API); pyloudnorm agreed with ffmpeg within
0.1 LU on the test (-14.78 vs -14.7).

## 7. Free tooling and recipes

### R-227 Loudness measure and two-pass normalise [verified 2026-10-17]
loudnorm defaults are I=-24, LRA=7, TP=-2; set them explicitly. loudnorm resamples to
192 kHz internally, so always add `-ar 48000` (or the source rate) on output. With the
measured values and `linear=true` it applies one static gain (pass 2 reported
"Normalization Type: Linear"); if the target needs more true-peak headroom than the
file has, it falls back to dynamic mode, so check the summary.
```bash
# measure (summary only; framelog=verbose hides the per-frame lines)
ffmpeg -hide_banner -nostats -i in.wav -af ebur128=peak=true:framelog=verbose -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):"

# pass 1: measure for loudnorm
ffmpeg -hide_banner -nostats -i in.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | tail -12

# pass 2: paste input_i, input_tp, input_lra, input_thresh, target_offset
ffmpeg -y -i in.wav -af loudnorm=I=-14:TP=-1:LRA=11:measured_I=-27.79:measured_TP=-18.82:measured_LRA=1.80:measured_thresh=-37.85:offset=-0.11:linear=true:print_format=summary -ar 48000 -c:a pcm_s24le out.wav
```
Python: `pyloudnorm.Meter(rate).integrated_loudness(data)` then
`pyloudnorm.normalize.loudness(data, current, target)` (normalize call unverified).

### R-228 Trim, fade, convert [verified 2026-10-17]
```bash
# strip leading and trailing silence, then a 10 ms fade-in and a 1 s fade-out at 11 s
ffmpeg -y -i in.wav -af "silenceremove=start_periods=1:start_threshold=-60dB,areverse,silenceremove=start_periods=1:start_threshold=-60dB,areverse,afade=t=in:d=0.01,afade=t=out:st=11:d=1" out.wav

# cut 8 s starting at 0.5 s, fade the last 2 s
ffmpeg -y -i in.wav -ss 0.5 -t 8 -af "afade=t=out:st=6:d=2" cut.wav

# formats
ffmpeg -y -i in.wav -c:a flac out.flac
ffmpeg -y -i in.wav -c:a libvorbis -q:a 6 -metadata LOOPSTART=24000 -metadata LOOPLENGTH=480000 out.ogg
ffmpeg -y -i in.wav -c:a libmp3lame -q:a 2 out.mp3          # distribution only, never for loops
ffprobe -v error -show_entries format_tags -of default=nw=1 out.ogg   # read the loop tags back
ffmpeg -y -i in.wav -ar 48000 -c:a pcm_s24le out48k24.wav   # resample / bit depth; add -af aresample=resampler=soxr for better SRC (gyan build has libsoxr)
```
`afade` default curve is `tri` (linear); `qsin`, `hsin`, `exp`, `log` are alternatives.

### R-229 Crossfaded loop and seam check [verified 2026-10-17]
Loop region S..E seconds; X seconds of the audio after E is faded into the first X
seconds of the loop, so the seam is continuous and the reverb tail is kept. Output
length = E - S.
```bash
S=0.5; E=8.5; X=0.5; SX=1.0   # SX = S + X
ffmpeg -y -i src.wav -filter_complex "[0]asplit=3[a][b][c];\
[a]atrim=start=$E:duration=$X,asetpts=PTS-STARTPTS,afade=t=out:d=$X:curve=qsin[tail];\
[b]atrim=start=$S:duration=$X,asetpts=PTS-STARTPTS,afade=t=in:d=$X:curve=qsin[head];\
[tail][head]amix=inputs=2:normalize=0:duration=first[xf];\
[c]atrim=start=$SX:end=$E,asetpts=PTS-STARTPTS[body];\
[xf][body]concat=n=2:v=0:a=1" -c:a pcm_s16le loop.wav
```
Seam check (stdlib Python, 16-bit WAV): compares the jump from the last to the first
sample with the 99th percentile of sample-to-sample steps. Off-period sine test: hard
cut ratio 80.0, crossfaded loop 0.9.
```python
import sys, wave, array
for fn in sys.argv[1:]:
    w = wave.open(fn); n = w.getnframes(); ch = w.getnchannels()
    L = array.array('h', w.readframes(n))[0::ch]
    d = sorted(abs(L[i+1]-L[i]) for i in range(len(L)-1)); p99 = d[int(len(d)*0.99)]
    print(fn, "seam ratio", round(abs(L[0]-L[-1]) / max(p99, 1), 2))
```
Zero-crossing alternative (unverified): find the nearest sample to each loop point where
the sign changes in the same direction (both rising), cut there. Works for sparse
material; crossfade is safer for dense AI mixes.

### R-230 More recipes (ducking, crossfade, atempo and soxr ran without error 2026-10-17; the build has libsoxr; duck depth and stretch quality were not measured)
```bash
# analysis bundle [verified 2026-10-17]
ffmpeg -hide_banner -nostats -i in.wav -af silencedetect=n=-60dB:d=0.2 -f null - 2>&1 | grep silence_
ffmpeg -hide_banner -nostats -i in.wav -af astats=measure_perchannel=none:measure_overall=Peak_level+Peak_count+Flat_factor+DC_offset -f null - 2>&1 | grep -E "Peak|Flat|DC"
ffmpeg -y -i in.wav -lavfi "showspectrumpic=s=1024x512:legend=1" spectrum.png
ffmpeg -hide_banner -nostats -i in.wav -af "pan=mono|c0=0.5*c0+0.5*c1,ebur128=framelog=verbose:dualmono=true" -f null - 2>&1 | grep -E "^\s+I:"

# duck music under dialogue (runs; tune threshold/ratio by ear)
ffmpeg -i music.wav -i voice.wav -filter_complex "[1]asplit[sc][v];[0][sc]sidechaincompress=threshold=0.05:ratio=8:attack=50:release=500[m];[m][v]amix=inputs=2:normalize=0" mix.wav

# join two segments with a 2 s crossfade (8 s + 8 s gave 14 s)
ffmpeg -i a.wav -i b.wav -filter_complex "acrossfade=d=2:c1=qsin:c2=qsin" ab.wav

# time-stretch by 3% without pitch change (runs; quality past ~5% not tested)
ffmpeg -i in.wav -af "atempo=1.03" out.wav
```
sox (not installed here; unverified): `sox in.wav out.wav silence 1 0.1 -60d reverse silence 1 0.1 -60d reverse`,
`sox in.wav -n stats`, `sox in.wav -n spectrogram -o spec.png`.

### R-231 Free and cheap tools [practice; check prices]
- **Audacity** (free): editing, spectrogram view, loop-point finding, label exports.
- **Reaper**: full DAW, 60-day evaluation, discounted personal licence (about USD 60;
  check reaper.fm). Best value for scripted batch work (ReaScript, Lua/Python).
- **LMMS** (free): pattern-based DAW for MIDI and synths.
- **MuseScore Studio** (free): notation; write a motif, export MIDI or audio.
- **ffmpeg** (installed, 9.0.1): everything in R-227..R-230.
- **librosa** (Python, 1.0.0): tempo, beats, chroma, onset, spectral features. Run
  without installing: `uv run --no-project --python 3.12 --with librosa --with pyloudnorm --with soundfile python -I script.py` [verified 2026-10-17].
- **essentia** (Python/C++, AGPL): KeyExtractor, RhythmExtractor2013, many descriptors.
- **pyloudnorm** (Python): BS.1770 loudness, matches ffmpeg.
- **Demucs** (R-232) for stems.
- **Wwise / FMOD Studio**: free under revenue limits for indies (check current terms).

### R-232 Demucs stem separation
Upstream facebookresearch/demucs was archived 2025-01-01; the author's fork
adefossez/demucs is the home, released v4.1.0 (modernised packaging, models on Hugging
Face), Python >= 3.10, "not actively working on Demucs anymore". Models: `htdemucs`
(default), `htdemucs_ft` (fine-tuned, ~4x slower, a bit better), `htdemucs_6s` (adds
guitar and piano; piano weak), `mdx_extra`.
https://github.com/adefossez/demucs and https://github.com/facebookresearch/demucs [source]
```bash
uvx demucs --two-stems=vocals song.wav      # vocals + accompaniment (unverified here)
uvx demucs -n htdemucs_ft song.wav          # drums, bass, other, vocals (unverified here)
```
Use: make vertical layers from one AI track (drums-only layer for combat intensity),
remove AI vocals, or check whether a "vocal" artefact sits in the vocal stem. Separated
stems carry bleed and artefacts; fine for game layers at moderate levels.

## 8. Learning path (free, brief)

### R-233 Best free resources [practice; spot-checked 2026-10-17]
1. **Ableton Learning Music** https://learningmusic.ableton.com/ (browser, no install;
   beats, scales, chords, basslines, melodies, song structure). Start here.
2. **musictheory.net** (lessons, ear trainers); **Open Music Theory** free textbook
   https://viva.pressbooks.pub/openmusictheory/; **Hooktheory TheoryTab** (real songs
   in Roman numerals); **MIT OCW** 21M.051 Fundamentals of Music.
3. **Cambridge-MT** free multitracks for mixing practice; **Wwise courses** (free
   certification) and **FMOD** videos for adaptive music.
4. YouTube for vocabulary: 12tone, Adam Neely, David Bennett Piano, 8-bit Music Theory
   (game music analysis).
Order for someone with taste but no training: Ableton Learning Music (one evening) -> 8-bit Music Theory and
Hooktheory to name what they already like -> Cambridge-MT mixing -> Wwise/FMOD only if
the deckbuilder outgrows Unity's mixer.

## Volatile claims to re-check (next check due 2027-01-17)
- Spotify normalisation (-14 / -11 / -19 LUFS, -1 / -2 dBTP) - support article.
- Apple Music Sound Check level (-16 LUFS is secondary-source only) and Apple Digital
  Masters guidance (24-bit, 1 dB headroom).
- YouTube -14 LUFS (never officially documented; "content loudness" behaviour).
- EBU R128 version (5.0, Nov 2023) and any new supplement; AES TD1008 figures.
- Netflix -27 LKFS dialogue-gated / -2 dBTP (QC page lists looser thresholds).
- PlayStation console/portable targets (-24 / -18 LUFS, per a Feb 2024 Wwise blog; IESD
  says -16 for mobile); any Microsoft-published Xbox target; any Steam guidance.
- Suno artist-name policy and lawsuits; Udio terms after the UMG settlement; whether
  ACE-Step adds a filter; ACE-Step 1.5 licence (MIT per GitHub, 2026-10-17).
- Spotify AI impersonation policy (Sept 2025) and any AI-labelling requirements.
- Unity manual (6.6) import settings, WAV smpl loop behaviour, WebGL loop fix.
- Wwise and FMOD indie licence terms; FMOD feature names (docs not fetchable).
- Demucs fork status (v4.1.0) and librosa 1.x API changes (`beat_track` returns an
  array tempo in 1.0.0).
- Reaper licence price.
