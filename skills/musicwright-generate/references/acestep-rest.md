# ACE-Step REST server

The ACE-Step 1.5 repository ships an API server (`acestep-api`, default `http://127.0.0.1:8001`).
It runs the 2B turbo model with the 5Hz LM planner and offers the tasks ComfyUI core lacks.
API reference: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/API.md

## Start and check

```bash
cd <ACE-Step-1.5 checkout> && uv run acestep-api --host 127.0.0.1 --port 8001
curl http://127.0.0.1:8001/health        # models_initialized false until the first job loads them
```

- Choose the model at start: `ACESTEP_CONFIG_PATH=acestep-v15-base ACESTEP_INIT_LLM=false acestep-api --host
  127.0.0.1 --port 8001` for lego, complete and extract (the planner is off for source tasks, so skip
  loading it); add `ACESTEP_OFFLOAD_TO_CPU=true` for `acestep-v15-xl-base` on 16 GB.
- Source tasks on base checkpoints need a server at or after commit ca1e85f (PRs #1273 and #1282):
  older servers force DCW on and base models then return noise (issue #1259). mw.py sends
  `dcw_enabled: false` for these tasks; an older server ignores the field, so update the checkout.
- The Gradio UI (port 7860) is a separate process and does not serve this API.
- The first `/release_task` loads the models inside the request (about 2.5 min on a 16 GB card):
  use a 900 s submit timeout (mw.py does).
- It peaks about 10.4 GB with the 2B turbo and planner, 7.5 GB with the 2B base (16-25 s per 60 s
  take) and 13.5 GB with XL base on CPU offload (about 530 s for three 60 s takes, load included).
  Do not run it beside ComfyUI's ACE-Step XL or a video model on 16 GB: free ComfyUI's models first
  (`POST /free` with `{"unload_models": true, "free_memory": true}` cancels nothing) once its queue
  has been idle a few minutes, and stop the server by its process id afterwards.
- If the venv breaks after a Python update: `uv python install 3.12`, move `.venv` aside, `uv sync`,
  check `torch.cuda.is_available()`. Ask before rebuilding someone's environment.
- On Windows with Smart App Control on, the venv launcher can be blocked ("An Application Control
  policy has blocked this file"); start it through uv's base Python with the venv's site-packages
  added instead of rebuilding.

## Flow

`POST /release_task` (JSON) → `{"data": {"task_id"}}`; poll `POST /query_result`
`{"task_id_list": [id]}` until `status` 1 (done) or 2 (failed); download each result's `file`
through `GET /v1/audio?path=...`. `mw.py gen --recipe acestep-rest` does all of this.

Text-to-music payload: `prompt` (caption), `lyrics` (`[instrumental]` when none), `audio_duration`,
`audio_format` (`wav` default, keep it for loops), `batch_size`, `thinking` (LM planner on),
`bpm`, `key_scale`, `use_random_seed` false + `seed`, or `sample_query` for a plain-language
description the LM turns into caption and lyrics.

## Working from existing audio (`--task`)

| `task_type` | Does | Checkpoint | mw.py |
|---|---|---|---|
| `cover` | new performance following the source's structure | any | `--task cover --src F --strength 0.2-1` |
| `repaint` | regenerate a time window, keep the rest | any | `--task repaint --src F --start S --end E` |
| extend | repaint past the end to lengthen | any | as repaint, `--end` beyond the source |
| `lego` | add one part that plays along with the source | base only | `--task lego --src F --track woodwinds` |
| `complete` | add a backing band to a single part | base only | `--task complete --src F --track drums,bass` |
| `extract` | pull one part out of a mix | base only | `--task extract --src F --track vocals` |

- Parts (`--track`): woodwinds, brass, fx, synth, strings, percussion, keyboard, guitar, bass, drums,
  backing_vocals, vocals. There is no "flute": use `woodwinds` and say flute in the caption.
- The server loads one DiT at start, named by `ACESTEP_CONFIG_PATH` (default `acestep-v15-turbo`).
  For lego, complete and extract start it with `acestep-v15-base` (2B, 4.8 GB download) or
  `acestep-v15-xl-base` (4B, 20 GB as fp32 shards; needs `ACESTEP_OFFLOAD_TO_CPU=true` on 16 GB).
  Download with the checkout's `acestep-download --model <name> --skip-main`.
- mw.py uploads `--src` (the server refuses absolute paths outside its temp folder), sends the other
  fields as one `param_obj` JSON field, uses the source length as `--duration`, sends 50 steps for
  base-only tasks unless `--steps` says otherwise, and turns the planner off for every source task:
  with it on, servers before PR #1287 (2026-08-16) ignore the source (R-20261017-4).
- `--cfg`, `--steps`, `--shift` and `--set '{json}'` go into the payload; `--sampler`, `--scheduler`
  and `--planner` do not exist on this route and are listed under `ignored`.
- Sheet the result beside the source: check whether it is the new part alone or a mix, and whether
  its notes start in the source's rests (an answer) or on top of its notes (a double).
  `mw.py answer PART --lead SRC` measures it. Lego plays along (about the same level in the rests as
  under the lead) and carries on into the lead's silent tail; `mw.py duck PART --under SRC --stem`
  shapes it into an answer (R-20261017-6).
- Percussion lego over a free-time source invents its own tempo. Run `mw.py pulse SRC` first; with no
  steady pulse, re-render the source at a fixed bpm or place accents on its phrases.

Use only source audio the user owns or has licensed.
