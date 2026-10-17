# ACE-Step REST server

The ACE-Step 1.5 repository ships an API server (`acestep-api`, default `http://127.0.0.1:8001`).
It runs the 2B turbo model with the 5Hz LM planner and offers the tasks ComfyUI core lacks.
API reference: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/API.md

## Start and check

```bash
cd <ACE-Step-1.5 checkout> && uv run acestep-api --host 127.0.0.1 --port 8001
curl http://127.0.0.1:8001/health        # models_initialized false until the first job loads them
```

- The Gradio UI (port 7860) is a separate process and does not serve this API.
- The first `/release_task` loads the models inside the request (about 2.5 min on a 16 GB card):
  use a 900 s submit timeout (mw.py does).
- It peaks about 10.4 GB. Do not run it beside ComfyUI's ACE-Step XL or a video model on 16 GB.
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

## Tasks beyond text-to-music (not yet run here; check the API doc for current field names)

| `task_type` | Does | Key fields |
|---|---|---|
| `cover` | new performance following a source's structure | `src_audio_path`, `audio_cover_strength` |
| `repaint` | regenerate a time range, keep the rest | `src_audio_path`, `repainting_start`, `repainting_end` |
| extend | repaint past the end to lengthen | as repaint, end beyond the source |
| `extract`, `lego`, `complete` | stems and part completion | base model only |

Use only source audio the user owns or has licensed.
