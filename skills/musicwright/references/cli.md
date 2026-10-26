# mw.py commands

`python mw.py <command> [options]`. Every command prints one JSON object; failures print
`{"ok": false, "error": ...}` and exit 1; argument errors (a missing or unknown option) print argparse's usage to stderr and exit 2. Needs ffmpeg and ffprobe on PATH (or `MUSICWRIGHT_FFMPEG`
pointing at ffmpeg). Hosts: `MUSICWRIGHT_COMFYUI` (comma list, default `http://127.0.0.1:8188,http://127.0.0.1:8000`),
`MUSICWRIGHT_ACESTEP` (default `http://127.0.0.1:8001`), or `comfyui` / `acestep_rest` in
`<studio>/config.json`. Studio: `MUSICWRIGHT_HOME`, default `~/.musicwright`.

| Command | Does | Key options |
|---|---|---|
| `doctor` | ffmpeg and filters, librosa, studio, each ComfyUI host (GPU, VRAM, music models, queue), ACE-Step REST, runnable recipes | `--host` |
| `new <dir>` | scaffold `brief.md`, `music.json`, `takes/ out/ sheets/`, `ledger.jsonl` | `--name --use --duration --preset` |
| `gen` | render takes, download them, measure each, append to the ledger | `--recipe --caption[-file] --lyrics[-file] --sections "A\|B" --duration --bpm --key --seeds 1,2 --takes 3 --name --out --host --cfg --steps --sampler --scheduler --shift --planner --set '{json}' --timeout --no-wait --dry-run`; from a source (REST): `--task cover\|repaint\|lego\|complete\|extract --src F --track woodwinds --start --end --strength --model` |
| `measure <files>` | duration, rate, LUFS, LRA, true peak, head/tail silence, interior gaps, clipping signs, warnings | `--silence-db --silence-min` |
| `sheet <files>` | one PNG: per take a log-frequency spectrogram row and a waveform row | `--out --width --spec-height --max-hz --measure` |
| `master <file>` | two-pass loudnorm (linear when possible) to a preset, 48 kHz; before and after numbers and the preset's `lra_hint`; `--peak -6` instead does gain only (peaks at -6 dBFS, no limiter, source rate) for a mastering engineer | `--preset --lufs --tp --lra --rate --peak --out` |
| `edit <file>` | trim, fade (qsin), resample, convert by extension | `--start --end --fade-in --fade-out --rate --out` |
| `join <files>` | chain equal-power crossfades; with `--lengths` each part holds that long before its crossfade | `--xfade --lengths --fade-out --out` |
| `loop <file>` | seamless loop: the tail crossfades into the head; `--bars N --bpm B` makes it exactly N bars; seam check; `--ogg` adds LOOPSTART/LOOPLENGTH | `--start --end --bars --bpm --beats-per-bar --xfade --ogg --out` |
| `seam <files>` | seam jump against the file's own 99th-percentile step (2 or less is clean, over 5 clicks) plus the level jump (a robust line through 50 ms window levels over half a second each side, read at the seam, so a first-beat hit or a swell through the seam reads clean) | |
| `duck <music>` | sidechain-duck music under dialogue or a video's sound; keeps the music's length; remuxes when the output is a video; `--stem` writes the ducked music alone | `--under --music-gain --threshold --ratio --attack --release --stem --out` |
| `mix <files>` | layer stems into one file: per-file gain (dB), offset (s; negative trims the head) and pan (-1..1, equal power); `--shelves` darkens or brightens a file with a high shelf; `--automate N:T=DB,...` gives file N a gain envelope on the mix timeline (linear in dB, 10 ms steps); sums in Python; scales the sum to peak at -1 dBFS unless `--no-limit`; `--stems DIR` writes each processed layer aligned to the mix | `--gains --offsets --pans --shelves --shelf-hz --automate --length longest\|first\|S --stems --rate --no-limit --out` |
| `pulse <files>` | is there a beat: onset count, inter-onset spread (`ioi_cv`), onset autocorrelation peak against its median, best tempo, distance from the best grid (beat, halves or thirds) against random onsets, median level rise over an onset (`onset_rise_db`; under 1 dB is a swell or ripple, so `pulse` none); `pulse` steady, weak or none; with none, `tempo_bpm` and the grid numbers are null | stdlib; no options |
| `answer <part>` | does a layered part answer the lead: its level under the lead's notes, in the lead's rests and in the lead's tail; `rests_minus_under_db` ≥ 3 answers, ≤ -3 doubles | `--lead --below` (dB under the lead's loud frames that still count as playing, default 30) |
| `render <score>` | notation to audio: ABC, ASCII tab, MusicXML or MIDI to MIDI plus audio, through FluidSynth and a SoundFont when found, otherwise a built-in sketch synth; `--check` only reads, lists bars that do not add up and gives `melody` hints per line (leap share, motif share, flags when a line leaps too often or has no rhythm that returns) | `--out --midi --synth auto\|fluidsynth\|builtin --sf2 --gain --tail --check --bpm --program --transpose --chords --tuning --tab-step --tune` |
| `notate <score>` | convert between ABC, MusicXML, MIDI and ASCII tab (notes snapped to a sixteenth grid); on MIDI `--bpm` keeps the timing | `--out --to abc\|musicxml\|midi\|tab --grid 2\|4 --max-fret` plus render's score options |
| `transcribe <audio>` | audio to MIDI, and `--to` ABC, MusicXML or tab beside it: librosa pyin for one line (prints the `uv run` line when librosa is missing) or the user's basic-pitch; drops notes under a level gate or outside the range | `--out --to --engine pyin\|basic-pitch --bpm --meter --lowest --highest --gate --program --tuning --grid` |
| `mixcheck <files>` | one ffmpeg pass: band levels against the whole (sub to air), PLR and PSR, short-term loudness contour (spread, loudest 10 s, tenths), stereo correlation, mono-fold loss, low-end correlation; flags OVER-LIMITED, FLAT, MUDDY, BRIGHT, MONO-LOSS, LOW-WIDE, BELOW-RANGE | `--lowest NOTE` |
| `compare <take> <ref>` | mixcheck both and report take minus reference | `--lowest` |
| `preview <files>` | copies at one loudness (lowered so none needs a limiter); `--blind` names them take_A.. in a shuffled order with the key in `<folder>_blind_key.json` beside the folder; `--as phone` (mono, 300 Hz-6 kHz) or `quiet` (20 dB down) | `--out --lufs --as normal\|phone\|quiet --blind --seed` |
| `monobass <file>` | Linkwitz-Riley crossover: high part keeps its stereo, the low part of the mid goes to both channels; mixcheck stereo before and after | `--hz` (default 160) `--out` |
| `analyze <files>` | tempo, beats, key estimate, tuning against A440 (cents, spread, trend), repetition share; files after the first report `cents_from_first`; flags OFF-A440, DRIFT, TUNING-GAP (librosa; prints the `uv run` line when it is missing) | `--sections` alone, a count, or tags `"Intro\|Verse\|Outro"`: section start and end in seconds and bars |
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
