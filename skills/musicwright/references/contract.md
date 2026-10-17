# The music project contract

Other plugins (a film plugin laying a score, a game plugin importing music) read these files.
Keep the field names stable; add fields, never rename them.

## Folder

```
<project>/
  brief.md        the brief in words, plus a Decisions list
  music.json      manifest (below)
  ledger.jsonl    one JSON object per line: takes and verdicts, append-only
  takes/          raw renders, named <slug>_s<seed>.<ext>
  sheets/         spectrogram contact sheets
  out/            deliverables only
```

## music.json

| Field | Meaning |
|---|---|
| `musicwright` | version that made the folder |
| `name`, `use`, `duration_s` | from the brief; `use` is game-loop, game-cue, film-cue, listening or song |
| `loudness_preset` | name from loudness.json |
| `ai_generated` | true when any deliverable came from a generator |
| `deliverables` | list of `{file, take, model, licence, seed, lufs_i, true_peak_dbtp, loop: {bars, bpm, length_s} or null}` |
| `disclosure` | the line to paste into a store page, video description or credits |

## ledger.jsonl

Take lines: `{"type": "take", "date", "take", "file", "route", "recipe", "model", "seed",
"caption", "lyrics", "duration_s", "bpm", "key", "params", "host", "measure"}`.

Verdict lines: `{"type": "verdict", "date", "take", "file", "verdict": "keep|reject|maybe",
"note", "by"}`. A take can have several verdicts; the latest wins.

## Studio (`MUSICWRIGHT_HOME`, default `~/.musicwright`)

`verdicts.jsonl` (every verdict with the take's recipe, across projects), `taste.md`,
`lessons.md`, `recipes.md`, `ideas.md`, `config.json` (`comfyui`, `acestep_rest`).
musicwright-curate owns its layout.
