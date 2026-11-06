# Interactive music: choosing, transitions, repetition

From Sweet, *Writing Interactive Music for Video Games* (2014), and Phillips, *A Composer's Guide to Game Music* (2014). Numbers are one author's starting points, not measurements. Caption recipes are translations for AI takes, untested on models unless a line says otherwise.

## Choose the technique

| Need | Model | Trade |
|---|---|---|
| Cues over about 20 s, change may wait | Branching at a marker | Never cuts a phrase, but changes late. Keep phrases under about 10 s, or the boss cue outlives the boss. Suits rock and techno more than long classical lines |
| Must change at once, tempo or harmony too | Transition cue | Interrupts; medium quality. Keep them at least about 30 s apart or they turn obvious |
| Must change at once, cheap | Crossfade | Interrupts, sounds like a changed station unless both cues share a tempo map and chords and cross on a bar |
| Many quick intensity changes | Vertical layers | Immediate, no interruption; cannot change tempo or harmony on an event |

Any-order segments lock key and tempo and cap a theme at the segment's length, so prefer long segments unless reaction speed really matters. Combine models only when the game needs it. Triggers are direct (a shot) or indirect (low health). State the design in three sentences; a long explanation signals costly complexity. Simple layers or a crossfade need no middleware.

## Horizontal patterns

- **Parallel track.** A more intense companion at the same bpm, key and bar count, cut with identical `--start --bars`. Enter on a downbeat, resume the normal track in time. Make it with `mw.py gen --task cover` from the normal take (untested for this).
- **Overlapping segments.** Each short segment has a brief intro that overlaps what came before and a close that melds into what follows.
- **Segment graph.** For a branching event, write a table of segment, exit marker, next segment: intro, combat loop, tense loop, success, failure, escalated loop.
- **Fill.** A one-bar fill before a planned switch prepares it. A stinger reacts; a fill is placed.

## Transitions

Add a transitions table beside the cue list: rows and columns of states, each cell a file, "cut" or "crossfade", with fade times. Many cells reuse one file. Pairs heard often get two or three variants.

Caption recipe for a transition take, in the destination's key and bpm, cut with `mw.py edit`:

- Length 3-15 s; longer closes better, short ones grow repetitive.
- It closes the source, then introduces the destination. A cadence closes; a percussion swell alone only bridges.
- Opening by source: rubato can start on its rhythmic motif, a rhythmic source needs a swell that will not fight the pulse. Different tempos: start with no tempo, or accelerando or ritardando. Several or unknown keys: a run, cluster, cymbal swell or ambiguous chord.
- High to low intensity: rise first, swell into a cadence, then drop. Do not simply fade down.
- Put the destination's intro in the transition so it does not replay when the destination loops.
- End transitions: swell, cadence, held chord, silence.

Check structure with `mw.py sheet` and `measure`, then a listener. An AI take of this shape is untested.

## Stinger kinds

Decide first whether it is **local** or **global**. A local stinger shares the tempo, instruments and perhaps theme of the track it interrupts. A global one is heard all game, so it must carry the score's signature and survive repetition.

| Kind | Rule |
|---|---|
| Victory | Shouts with no build-up, so easy to overdo |
| Global death | Short and understated: it lands on a frustrated player and takes the blame. A non-global defeat may run longer |
| Transition | Prepares the next track's key and tempo. Next track unknown: a rising alarm or falling gesture, clustered, with no clear meter |
| Hint | Gives information (an object, a route, a hazard); part of the mechanic |
| Prize | A smaller victory, or a mysterious one in a story game |
| Random pool | For horror, many short shocks at surprising events. Never one shock reused |

1-8 s is typical; a fuller victory or transition piece can run to about 20 s (the sources give about 10 and about 20).

## Layers

- **Stems are not layers.** Mix stems are made to play together, layers to play in changing subsets. Demucs stems are usable, as inFAMOUS 2's grouped session parts were, but check every combination the game will use.
- Group stems into low, medium and high intensity rather than one layer per instrument. Two to four layers is normal, and each above the first needs its own trigger, so write the trigger beside the layer.
- **Additive** layers stack on one rising value and all fit together. **Individual** layers each have an input (flying, low health). **Interchange** is a foundation plus alternates that replace each other and clash if played together; keep alternates related with `gen --task cover` or `repaint` from one take (untested for this).
- Pick a full take that swells and changes, since stems of a static take inherit its flatness. Ask for rests in parts and melody in phrases. A layer playing throughout is the common failure: game fades end up standing in for real dynamics.
- Melody is the hard layer, since a fade can land mid-phrase. Tie it to a known moment or keep it out of the fading set.
- Separate by register so each entry is audible: tuba and piccolo stay distinct, tuba and timpani merge.
- **Fades: in over 0.5-1.5 s, out over 3-5 s.** Abrupt fade-outs sound like a fault. Layers can also go solo, sit at half volume or mark a state (a choir only while flying).

## Fighting repetition

- The real cure is more and longer music; a short loop with landmarks is the worst case.
- Weighted random playlists of phrase files, of differing lengths. `mw.py loop` cuts them from one take; they share reverb tails, so check seams in pairs.
- Per-layer variants multiply (three drums by three basses gives nine). Nested lengths need sample-accurate playback; layers that must agree harmonically keep one length.
- Several start points where players restart a hard level often.
- Random phrases with varied silence. Drop the music when a player stays too long in one area.
- Generative beds: check rhythm and large-scale form, the usual tells.

## Implementation check

- Debounce on entry (adaptive.md), and hold after a change: at least about 15 s in Sweet's example, with listed exceptions such as boss death. A player walking across a forest and cave trigger exposes the engine.
- List each cue's trigger kind: placed triggers and zones sit in a level editor; ambushes, weather and plot events need code hooks.
- Hook a marked placeholder first, then the real asset. Sketch in the engine early.
- Lowercase filenames with exact case, one rule for marking a final version.
- Log each state change and music switch in a play session, then read the log for flip-flops, missing cues and late changes. For an agent, this stands in for ears.
- Budget: minutes = allowed size / bitrate. Each layer takes a voice, so reserve voices.
- Mix against effects: music premixed alone gets buried. If temporary effects or dialogue exist, compare with `mw.py mixcheck` and keep dense music out of their band.
- Real-time filters: low-pass near death, high-pass on a long jump. Keep music out of 3D positioning unless it is in the world; a placed snare can be taken for gunfire.
- Tempo states are prerendered files: two or three per state with ramp clips, and a timeout so shifts do not stack. An AI take at another bpm is a different piece, so stretch offline or use cover mode and check.
- Rhythm-tied levels reverse the order: the music comes first, and designers get a list of accents with times and restart points on phrase boundaries.
