# Music in Unity (manual for Unity 6.6, checked 2026-10-17)

https://docs.unity3d.com/Manual/class-AudioClip.html, https://docs.unity3d.com/Manual/AudioFiles-compatibility.html

## Import settings per music clip

| Setting | Music (long) | Short loop or stinger |
|---|---|---|
| Load Type | Streaming (decodes from disk, about 200 KB overhead per stream) | Compressed In Memory |
| Compression Format | Vorbis (quality ~70% to start; lower until audible, then raise a little) | ADPCM (3-4x smaller than PCM, cheap to decode) or PCM for stingers under about 2 s; Vorbis on a short clip wastes decode CPU (Lanham ch. 11) |
| Load In Background | on | optional |
| Preload Audio Data | off; call `LoadAudioData` before playing | on |
| Force To Mono | off | off |
| Sample Rate Setting | Preserve | Preserve |

Avoid Decompress On Load for music (decompressed Vorbis is about 10x the memory). Unity imports
WAV, AIFF, MP3, OGG, FLAC and tracker modules; give it WAV or FLAC and let it encode Vorbis.
There is no loop import setting; the Preview loop toggle is editor-only.

## Looping

- Simple loop: `AudioSource.loop = true` on a clip cut by `mw.py loop`.
- Unity ignores OGG loop tags and only partly honours a WAV `smpl` loop chunk (always starts from
  the beginning), so intro-then-loop needs two clips.
- WebGL had a loop playback bug in the past; test loops in a WebGL build if you ship one.

## Intro then loop, bar-quantised switches

```csharp
// two AudioSources: intro (loop off) and body (loop on)
double t = AudioSettings.dspTime + 0.2;               // schedule ~100-200 ms ahead
intro.PlayScheduled(t);
body.PlayScheduled(t + (double)intro.clip.samples / intro.clip.frequency);
```

The same scheduling switches between tracks on a bar line: compute the next bar from the
current track's start time and bpm, schedule the new source there and fade the old one.

## Mixer

Route music to an AudioMixer group. Snapshots handle states (explore, combat, paused); duck music
under dialogue or important SFX with a send to a ducking effect. Without middleware this is
enough for a card or strategy game. Set snapshot transition times from the fade rule in interactive.md: in over 0.5-1.5 s, out over 3-5 s.

- Snapshots switch many values at once (states, pause, zones); an exposed parameter suits one value driven every frame from script (an intensity layer's volume).
- A level with distinct areas gets a start snapshot plus one per zone, blended by the player's distance with `AudioMixer.TransitionToSnapshots(snapshots, weights, time)`, not one global mix (Lanham ch. 4).
- A snapshot selected in the editor records every change made with no save step; check which is selected before tweaking. A script holding snapshot fields disables itself when one is unassigned rather than throwing each frame.
- Duck Volume: a send from the trigger group feeds the ducked group's receive. If the duck pumps or chatters, raise Knee before touching threshold; start attack near 10 ms (Lanham ch. 3). Duck Volume and reverb are costly: put them on a return, one reverb per mix (ch. 11).

A stinger is a plain `PlayOneShot`; use `PlayScheduled` only for a quantised one.
