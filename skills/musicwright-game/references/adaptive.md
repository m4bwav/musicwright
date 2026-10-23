# Game music sets and adaptive music

## Cues and lengths (practice)

| Cue | Length | Notes |
|---|---|---|
| Title / main menu | 1-3 min loop | main theme; may have a one-shot intro |
| Map / deck building | 2-4 min loop, 2-3 variants | mid tempo, low fatigue, no hook every 20 s |
| Combat / encounter | 1.5-3 min loop plus intensity layers | boss gets its own |
| Ambient / exploration | 3-6 min or generative | sparse, slow harmonic rhythm |
| Shop / rest | 1-2 min | warm, light |
| Stinger | 1-8 s | in the bed's key, or neutral percussion; quantised to the beat |
| Victory / defeat | 5-20 s | victory resolves (often bVI-bVII-I); defeat falls |

## Techniques

- **Horizontal re-sequencing**: switch segments (explore → combat → victory) at musical
  boundaries (next bar, next beat, a cue point), with transition segments or stingers.
- **Vertical layering**: stems of one piece in sync; game state fades layers (drums when enemies
  appear, brass when health is low). Same length, tempo and key for every stem.
- **Stingers**: short phrases over or between music on events, quantised to the beat.
- **One parameter**: a 0-1 intensity or threat value drives layers and switches.
- **Layers by subtraction**: render or write the fullest version first and take the quieter
  intensity layers from it (stems of that one take), so every layer shares key, tempo and length
  (after DeSantis, *Making Music* ch. 63, 72). Layers rendered separately rarely agree.
- **Beds that never repeat**: two or three ambient layers whose lengths share no factor, for
  example 23, 37 and 41 s. Make each a seamless loop (`mw.py loop`, then `mw.py seam`); together
  they line up again only after hours (23 x 37 x 41 s is almost 10 h). Keep them in one key and without a
  beat, since a pulse would drift between layers (DeSantis ch. 37).

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
