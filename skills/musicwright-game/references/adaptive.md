# Game music sets and adaptive music

## Cues and lengths (practice)

| Cue | Length | Notes |
|---|---|---|
| Title / main menu | 1-3 min loop | main theme; may have a one-shot intro |
| Map / deck building | 2-4 min loop, 2-3 variants | mid tempo, low fatigue, no hook every 20 s |
| Combat / encounter | 1.5-3 min loop plus intensity layers | boss gets its own |
| Chase | loop, like combat | driving; ends on a stinger when the chase is won or lost |
| Ambient / exploration | 3-6 min or generative | sparse, slow harmonic rhythm |
| Mystery | loop or one-shot | the first time the player enters a new place; unresolved, sparse |
| Shop / rest | 1-2 min | warm, light |
| Stinger | 1-8 s | neutral (pentatonic or unpitched) and played at once by default; in the bed's key and quantised by choice. Kinds: interactive.md |
| Warning | a stinger or a layer | a hazard ahead or enemies about to arrive; marks a new enemy's first appearance |
| Victory / defeat | 5-20 s | victory resolves (often bVI-bVII-I); defeat falls |
| Villain motif | a phrase, not a track | the antagonist's own few notes, woven into any cue where they appear |
| In-game one-shot | a phrase | ends at an unpredictable moment, so its end thins out into the atmosphere |
| Tutorial / puzzle | loop | tutorial may be interrupted repeatedly and adds no stress; puzzle sets a mood for thinking, rarely action music |
| Pause menu | loop | subdued, sits over a pause; not the title track |
| Minigame / diegetic | any | breaks style on purpose; a radio or jukebox can play anything |
| Scripted event / cutscene | fitted | builds and stops allowed in scripted events, whose timing is not fixed; cutscenes score like film and develop themes |
| Attract mode | short | a fast medley of themes |

Build order: global tracks and the main theme first, since they define the style and get tested for fatigue longest; boss tracks and cutscenes last, so they can reuse the themes.

Ask of each cue what its job is: state of mind, world builder, pace setter, audience, branding or demarcation.

## By game genre

Conventions as of 2014 (Phillips ch. 5), a starting point. Check a current game in the genre before writing a brief.

| Genre | Usual music |
|---|---|
| Shooter | rock drive plus orchestra, sometimes choir |
| Platformer, puzzle | anything goes |
| Action-adventure, Western RPG | orchestra, some rock |
| Northeast Asian RPG | orchestra and rock mixed with techno, retro-pop, ballads |
| Survival horror | atmospheric orchestra, some metal |
| Racing | hard electronica, a strong tradition to keep; players expect full song-form tracks |
| Simulation, strategy | rock, orchestra or both |
| Life sim | friendly: light orchestra, pop, almost no rock |
| Fighting | all kinds of rock, occasional orchestra |
| Stealth | dark suspense: orchestra with synth or rock beats |

Brief notes:

- Sim, strategy and puzzle: overlapping ostinati with slow change. A melodic cinematic score can sit on top of the game.
- Horror: edgy rather than constantly frightening, or the real scares lose force.
- Racing and fast action: speed comes from contrast. Fast rhythm over slow harmony reads faster than a fast tempo alone.
- Competitive shooter: music on events only, since players hunt by sound; avoid snares that read as gunfire.

## Building a loop

A landmark tells the player they are walking in circles: a returning chorus, a surprise, a sudden burst. Song form is the worst case. The opposite failure is blandness, so do not strip all melody to be safe. Caption words are untested.

| Length | Type | Caption words |
|---|---|---|
| under 60 s | repeating figure | single ostinato over a pedal, static harmony, no melody |
| any | slow texture (suits dark moods, blends with effects) | slow swelling chords, no pulse, melody fragments only |
| 1.5-4 min | small equal events, no peak | constant small flourishes, no climax, even energy |
| 1.5-4 min | perpetual development | melody evolving continuously, no repeated chorus |
| 5 min and up | succession of variations | linked movements in `mw.py join`, each in a related key |

## Cues from the level plan

After Rogers, *Level Up!* (Levels 4, 10, 13 and 17).

- **Take the cues from the plan.** A beat chart has one column per level and a music row; a
  room table has big and small moments. Map each area to its track and each big moment to an
  intensity step or a boss cue. A new enemy's first appearance gets a warning; a rest room gets
  silence or a rest cue.
- **Rotate.** Give an area or world at least two tracks and alternate them, so one never plays
  twice running, and do not put the same track in two neighbouring columns of the plan. Classic
  games do reuse one level theme on purpose; when a repeat is meant, the plan says so.
- **Energy a notch above the screen** for action and traversal cues: slow music makes players
  move slowly. Not for long map, deck-building or ambient beds, where the low-fatigue rules in
  the skill's Step 1 win.
- **The title screen gets the most distinctive piece.** It tells the player what kind of game this is. Distinctive need not mean loud: it sits under menus, is heard at every launch, and an anthem over first options and tutorials can add to a new player's anxiety.
- **Silence and ducking are events.** Drop the music for a big reveal, a power-up or a
  slow-motion moment; muffle or slow it during bullet time. Silence used everywhere stops
  meaning anything. Withdrawing music also says nothing more is here, so check a rest room's
  silence is not misread that way. In action games a simpler version of the track (drop the top
  stems) carries a lull between waves better than silence: it is not over yet.
- **Stingers point the right way.** Success rises in pitch, failure falls, and every fight ends
  on a victory stinger.
- **A visual twin for every cue that carries information.** A warning, a timer or an enemy
  about to arrive must also show on screen, for players who cannot hear it.

## Techniques

Which to use, transitions, stinger kinds, layer fades and a flip-flop guard: [interactive.md](interactive.md).

- **Horizontal re-sequencing**: switch segments (explore → combat → victory) at musical
  boundaries (next bar, next beat, a cue point), with transition segments or stingers.
- **Vertical layering**: stems of one piece in sync; game state fades layers (drums when enemies
  appear, brass when health is low). Same length, tempo and key for every stem.
- **Stingers**: short phrases over or between music on events. Play at once when the event must be felt
  now, which is the usual case, with neutral content because the chord underneath is unknown. Quantise
  in music-driven games, or when the engine knows the beat and a short delay is acceptable.
- **One parameter**: a 0-1 intensity or threat value drives layers and switches.
- **Layers by subtraction**: render or write the fullest version first and take the quieter
  intensity layers from it (stems of that one take), so every layer shares key, tempo and length
  (after DeSantis, *Making Music* ch. 63, 72). Layers rendered separately rarely agree.
- **Beds that never repeat**: two or three ambient layers whose lengths share no factor, for
  example 23, 37 and 41 s. Make each a seamless loop (`mw.py loop`, then `mw.py seam`); together
  they line up again only after hours (23 x 37 x 41 s is almost 10 h). Keep them in one key and without a
  beat, since a pulse would drift between layers (DeSantis ch. 37). One exception: a rhythm-only
  layer with no pitch may drift on purpose over a loosely timed ambient layer (Sweet ch. 9, the Halo scores).

- Wait 1-3 s in a new game state before switching music, so brief changes do not flip it (one author's advice, untested). Also hold after a change: interactive.md "Implementation check".

## Middleware terms

- **Wwise**: Music Switch Container (chooses by State or Switch), Music Playlist Container,
  Music Segment with Entry and Exit Cues, Stingers, transition rules synced to Immediate, Entry
  Cue, Next Bar, Next Beat or a custom cue. Free indie tier (check current terms).
- **FMOD Studio**: timeline with loop regions, destination and transition markers, transition
  regions that fire on a parameter condition, quantised transitions, tempo markers, transition
  timelines for crossfades. Free indie tier (check current terms). Feature names come from
  course listings; the docs did not render for the research fetch.
- **Unity alone**: AudioMixer snapshots for layer volumes, `PlayScheduled` for bar-quantised
  switches, two sources per layer for crossfades (unity.md).

## Disclosure

Steam's Content Survey asks about AI content that ships with the game, sound included:
pre-generated music is described like any content. Keep the model and licence per file in
`music.json` so the answer is a copy-paste.
