# mw.py commands

`python mw.py <command> [options]`. Every command prints one JSON object; failures print
`{"ok": false, "error": ...}` and exit 1. Needs ffmpeg and ffprobe on PATH (or `MUSICWRIGHT_FFMPEG`
pointing at ffmpeg). Hosts: `MUSICWRIGHT_COMFYUI` (comma list, default `http://127.0.0.1:8188,http://127.0.0.1:8000`),
`MUSICWRIGHT_ACESTEP` (default `http://127.0.0.1:8001`), or `comfyui` / `acestep_rest` in
`<studio>/config.json`. Studio: `MUSICWRIGHT_HOME`, default `~/.musicwright`.

| Command | Does | Key options |
|---|---|---|
| `doctor` | ffmpeg and filters, librosa, studio, each ComfyUI host (GPU, VRAM, music models, queue), ACE-Step REST, runnable recipes | `--host` |
| `new <dir>` | scaffold `brief.md`, `music.json`, `takes/ out/ sheets/`, `ledger.jsonl` | `--name --use --duration --preset` |
| `gen` | render takes, download them, measure each, append to the ledger | `--recipe --caption[-file] --lyrics[-file] --sections "A\|B" --duration --bpm --key --seeds 1,2 --takes 3 --name --out --host --cfg --steps --sampler --scheduler --shift --planner --set '{json}' --timeout --no-wait --dry-run` |
| `measure <files>` | duration, rate, LUFS, LRA, true peak, head/tail silence, interior gaps, clipping signs, warnings | `--silence-db --silence-min` |
| `sheet <files>` | one PNG: per take a log-frequency spectrogram row and a waveform row | `--out --width --spec-height --max-hz --measure` |
| `master <file>` | two-pass loudnorm (linear when possible) to a preset, 48 kHz; before and after numbers | `--preset --lufs --tp --lra --rate --out` |
| `edit <file>` | trim, fade (qsin), resample, convert by extension | `--start --end --fade-in --fade-out --rate --out` |
| `join <files>` | chain equal-power crossfades; with `--lengths` each part holds that long before its crossfade | `--xfade --lengths --fade-out --out` |
| `loop <file>` | seamless loop: the tail crossfades into the head; `--bars N --bpm B` makes it exactly N bars; seam check; `--ogg` adds LOOPSTART/LOOPLENGTH | `--start --end --bars --bpm --beats-per-bar --xfade --ogg --out` |
| `seam <files>` | seam jump against the file's own 99th-percentile step (about 1 or less is clean, over 5 clicks) plus the level jump | |
| `duck <music>` | sidechain-duck music under dialogue or a video's sound; remuxes when the output is a video | `--under --music-gain --threshold --ratio --attack --release --out` |
| `analyze <files>` | tempo, beats, key estimate (librosa); prints the `uv run` line when librosa is missing | |
| `verdict <take> keep\|reject\|maybe` | append the listener's verdict to the ledger and `<studio>/verdicts.jsonl` with the take's recipe | `--note --by` |
| `ledger [dir]` | takes with recipes and verdicts; lists unjudged takes | |
| `note taste\|lesson\|recipe\|idea "<text>"` | append a dated line to the studio notes | `--source` |

Recipes live in [recipes.json](recipes.json); loudness presets in [loudness.json](loudness.json).
Add a recipe only after a listener kept a take made with it, and cite that run in its `source`.

Typical session:

```bash
python mw.py doctor
python mw.py new music/flute-solo --name "Flute solo" --use listening --duration 60
python mw.py gen --caption "solo flute, unaccompanied ..." --sections "Intro - breathy flute|Verse - melody|Outro - fading flute" \
  --duration 66 --bpm 66 --key "A minor" --takes 3 --name flute --out music/flute-solo/takes
python mw.py sheet music/flute-solo/takes/*.flac --out music/flute-solo/sheets/flute.png --measure
python mw.py verdict music/flute-solo/takes/flute_s63389.flac keep --note "clean, breathy, good ending"
python mw.py edit music/flute-solo/takes/flute_s63389.flac --end 60 --fade-out 3 --out music/flute-solo/out/flute.wav
python mw.py master music/flute-solo/out/flute.wav --preset streaming --out music/flute-solo/out/flute_master.wav
```
