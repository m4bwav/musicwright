# Music in Unity (manual for Unity 6.6, checked 2026-10-17)

https://docs.unity3d.com/Manual/class-AudioClip.html, https://docs.unity3d.com/Manual/AudioFiles-compatibility.html

## Import settings per music clip

| Setting | Music (long) | Short loop or stinger |
|---|---|---|
| Load Type | Streaming (decodes from disk, about 200 KB overhead per stream) | Compressed In Memory |
| Compression Format | Vorbis (quality ~70% to start; lower until audible, then raise a little) | Vorbis, or PCM for very short stingers |
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
enough for a card or strategy game.
