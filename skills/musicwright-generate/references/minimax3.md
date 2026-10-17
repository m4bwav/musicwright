# MiniMax Music 3 (open weights, ComfyUI native)

Recipe `minimax-music3` in the hub's recipes.json. Licence: MiniMax-Music3 Community Licence
(https://huggingface.co/MiniMaxAI/MiniMax-Music3/blob/main/LICENSE): free use; companies over
USD 20M yearly revenue need permission; a product using it must show "MiniMax-Music3"
prominently; machine-made content must be published with clear disclosure; no impersonation.

## Caption: three headings

```
### Global Metadata
<genre>. Around <bpm> BPM, <key>. A complete instrumental piece approximately <n> minutes long
(<m:ss>). Emotional progression: <arc>. Listening scenario: <where it plays>. Production: <stereo,
reverb, tone, what to avoid>.

### Vocal Details
This piece is purely instrumental - no singing, no choir, no vocal chops, no spoken word.
The lead melodic role is carried by <lead>.

### Arrangement
A continuous timeline with no hard stops until the very end:
0:00-0:18: <what enters, what it does>
0:18-0:50: ...
```

Lyrics: one block about every 15 s, `[intro]`, `[instrumental]`, `[interlude]`, `[bridge]`,
`[outro]`, each with a short parenthesised performance note, e.g. `[instrumental]` newline
`(the main theme appears: a soft lead synth)`.

## Quirks seen

- Takes came back shorter than asked (98-170 s for 180-195 s requests). The graph asks for 1.2x
  the target; still render longer and join two takes when needed.
- One 240 s beatless request ran over an hour twice and then the ComfyUI server stopped
  answering. Use `mw.py gen --timeout`, and check `mw.py doctor` before queueing more.
- Runs took about 3-7 min per take, up to 13 min, with settings not recorded at the time.
- Quality has not been judged against ACE-Step by a listener yet. Treat it as a second opinion.
- Output is 32 kHz; resample to 48 kHz on delivery (`mw.py master` does).
