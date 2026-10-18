#!/usr/bin/env python3
"""musicwright CLI: generate, measure, look at, finish and log music.

Standard-library Python 3.9+. Needs ffmpeg and ffprobe on PATH (or MUSICWRIGHT_FFMPEG
pointing at ffmpeg) for audio work; ComfyUI or the ACE-Step REST server only for `gen`.
Every command prints exactly one JSON object on stdout and fails soft with
{"ok": false, "error": ...}. Run `mw.py <command> -h` for options.

Commands
  doctor   what is installed and reachable (ffmpeg, ComfyUI hosts, music models, ACE-Step REST)
  new      scaffold a music project folder (brief.md, music.json, takes/, out/, sheets/)
  gen      render takes through ComfyUI (ACE-Step 1.5 XL, MiniMax Music 3) or the ACE-Step REST API,
           including parts added to an existing track (--task lego --src --track)
  measure  loudness (LUFS, LRA, true peak), duration, head and tail silence, clipping signs
  sheet    one PNG of spectrogram + waveform rows for several takes (the agent's way to look)
  master   two-pass loudness normalisation to a named preset
  edit     trim, fade and convert one file
  join     crossfade movements into one cue
  loop     make a seamless loop (tail crossfaded into head), optionally bar-aligned, and check the seam
  seam     score how audible a file's loop seam is
  duck     duck music under dialogue or a video's own sound, optionally remux the video
  mix      layer stems (gain, offset, pan) into one file and write the aligned stems
  pulse    is there a beat: onsets, inter-onset spread, autocorrelation and grid fit (stdlib)
  answer   does a layered part answer the lead: its level in the lead's rests against under its notes
  analyze  tempo and key estimate (needs librosa; prints the uv one-liner when missing)
  render   notation to audio: ABC, ASCII tab, MusicXML or MIDI -> MIDI and audio (FluidSynth or a built-in synth)
  notate   convert between ABC, MusicXML, MIDI and ASCII tab
  transcribe audio to MIDI and notation (librosa pyin for one instrument, basic-pitch for several)
  verdict  record a listener's keep/reject/maybe with notes, copied to the studio
  ledger   list a project's takes with recipes and verdicts
  note     append a taste note, lesson or recipe to the studio
"""
import argparse
import datetime as _dt
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import wave
from array import array
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notation  # noqa: E402  (same folder; stdlib only)

VERSION = "0.1.0"
HERE = Path(__file__).resolve().parent
REFS = HERE.parent / "references"
DEFAULT_COMFY = "http://127.0.0.1:8188,http://127.0.0.1:8000"
DEFAULT_REST = "http://127.0.0.1:8001"
AUDIO_EXT = {".wav", ".flac", ".mp3", ".ogg", ".opus", ".m4a", ".aac", ".aif", ".aiff"}


class MwError(Exception):
    pass


# ---------------------------------------------------------------- helpers

def out(obj):
    sys.stdout.write(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def now():
    return _dt.datetime.now().isoformat(timespec="seconds")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def studio_dir():
    return Path(os.environ.get("MUSICWRIGHT_HOME") or Path.home() / ".musicwright")


def studio_config():
    p = studio_dir() / "config.json"
    if p.exists():
        try:
            return load_json(p)
        except (OSError, ValueError):
            return {}
    return {}


def comfy_hosts(arg=None):
    raw = arg or os.environ.get("MUSICWRIGHT_COMFYUI") or studio_config().get("comfyui") or DEFAULT_COMFY
    if isinstance(raw, list):
        raw = ",".join(raw)
    return [h.strip().rstrip("/") for h in raw.split(",") if h.strip()]


def rest_host(arg=None):
    return (arg or os.environ.get("MUSICWRIGHT_ACESTEP") or studio_config().get("acestep_rest") or DEFAULT_REST).rstrip("/")


def ffmpeg_bin(name="ffmpeg"):
    env = os.environ.get("MUSICWRIGHT_FFMPEG")
    if env:
        p = Path(env)
        cand = p.with_name(name + p.suffix) if name != "ffmpeg" else p
        if cand.exists():
            return str(cand)
    found = shutil.which(name)
    if not found:
        raise MwError(f"{name} not found on PATH; install ffmpeg (winget install ffmpeg, brew install ffmpeg, apt install ffmpeg) or set MUSICWRIGHT_FFMPEG")
    return found


def run(cmd, check=True):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and p.returncode != 0:
        tail = "\n".join(p.stderr.strip().splitlines()[-6:])
        raise MwError(f"{Path(cmd[0]).name} failed ({p.returncode}): {tail}")
    return p


def ffmpeg(args, check=True):
    return run([ffmpeg_bin(), "-hide_banner", "-nostats"] + args, check=check)


def probe(path):
    p = run([ffmpeg_bin("ffprobe"), "-v", "error", "-show_entries",
             "format=duration:stream=sample_rate,channels,codec_name", "-of", "json", str(path)])
    d = json.loads(p.stdout or "{}")
    st = (d.get("streams") or [{}])[0]
    return {"duration_s": round(float((d.get("format") or {}).get("duration") or 0), 3),
            "sample_rate": int(st.get("sample_rate") or 0), "channels": int(st.get("channels") or 0),
            "codec": st.get("codec_name")}


def need_file(path):
    p = Path(path)
    if not p.is_file():
        raise MwError(f"no such file: {path}")
    return p


_ENCODERS = None


def has_encoder(name):
    """True when this ffmpeg build has the encoder (Homebrew's ffmpeg, for one, ships without libvorbis)."""
    global _ENCODERS
    if _ENCODERS is None:
        listing = run([ffmpeg_bin(), "-hide_banner", "-encoders"], check=False).stdout
        _ENCODERS = {ln.split()[1] for ln in listing.splitlines() if len(ln.split()) > 1 and len(ln.split()[0]) == 6}
    return name in _ENCODERS


def vorbis_codec():
    if has_encoder("libvorbis"):
        return ["-c:a", "libvorbis", "-q:a", "6"]
    # ffmpeg's built-in Vorbis encoder: experimental and plainer, but always present
    return ["-c:a", "vorbis", "-strict", "experimental", "-ac", "2"]


def out_codec(path):
    ext = Path(path).suffix.lower()
    if ext == ".ogg":
        return vorbis_codec()
    return {".wav": ["-c:a", "pcm_s24le"], ".flac": ["-c:a", "flac"],
            ".mp3": ["-c:a", "libmp3lame", "-q:a", "0"], ".opus": ["-c:a", "libopus", "-b:a", "160k"],
            ".m4a": ["-c:a", "aac", "-b:a", "256k"]}.get(ext, [])


def http(url, payload=None, timeout=30):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"} if data else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
    return json.loads(body.decode("utf-8")) if body else {}


def http_multipart(url, fields, files, timeout=30):
    """POST form fields and files as multipart/form-data; returns the JSON reply."""
    boundary = "mw" + uuid.uuid4().hex
    body = bytearray()
    for k, v in fields.items():
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode("utf-8")
    for k, path in files.items():
        p = Path(path)
        body += (f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; filename="{p.name}"\r\n'
                 f'Content-Type: application/octet-stream\r\n\r\n').encode("utf-8")
        body += p.read_bytes() + b"\r\n"
    body += f"--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(url, data=bytes(body), headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return json.loads(data.decode("utf-8")) if data else {}


def http_get_bytes(url, timeout=300):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def out_file(path):
    """--out as a Path with its folder created (ffmpeg does not create folders)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def write_lf(path, text):
    """Write UTF-8 text with LF line ends (Path.write_text takes newline= only from Python 3.10)."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def append_jsonl(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def read_jsonl(path):
    rows = []
    p = Path(path)
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    pass
    return rows


def slug(s):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", s).strip("_")[:60] or "take"


# ---------------------------------------------------------------- measuring

def measure_file(path, silence_db=-50.0, silence_min=0.3):
    p = need_file(path)
    info = probe(p)
    r = ffmpeg(["-i", str(p), "-af",
                f"ebur128=peak=true,silencedetect=n={silence_db}dB:d={silence_min},astats=metadata=0",
                "-f", "null", "-"])
    err = r.stderr
    res = dict(file=str(p), **info)
    summ = err[err.rfind("Summary:"):] if "Summary:" in err else ""
    m = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summ)
    res["lufs_i"] = float(m.group(1)) if m and m.group(1) != "-inf" else None
    m = re.search(r"LRA:\s+(-?[\d.]+) LU", summ)
    res["lra"] = float(m.group(1)) if m else None
    m = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS", summ, re.S)
    res["true_peak_dbtp"] = float(m.group(1)) if m and m.group(1) != "-inf" else None
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: (-?[\d.]+)", err)]
    dur = info["duration_s"]
    head = ends[0] if starts and starts[0] <= 0.05 and ends else 0.0
    tail = 0.0
    if starts:
        last = starts[-1]
        if len(ends) < len(starts) or (ends and ends[-1] >= dur - 0.05 and ends[-1] > last):
            tail = max(0.0, dur - last)
    res["head_silence_s"] = round(head, 2)
    res["tail_silence_s"] = round(tail, 2)
    interior = []
    for i, s in enumerate(starts):
        e = ends[i] if i < len(ends) else dur
        if s > 0.05 and e < dur - 0.05:
            interior.append([round(s, 2), round(e, 2)])
    res["gaps"] = interior[:20]
    ov = err[err.rfind("Overall"):] if "Overall" in err else ""
    m = re.search(r"Peak level dB:\s+(-?[\d.]+|-inf)", ov)
    res["sample_peak_db"] = float(m.group(1)) if m and m.group(1) != "-inf" else None
    m = re.search(r"Flat factor:\s+(-?[\d.]+)", ov)
    res["flat_factor"] = float(m.group(1)) if m else None
    warn = []
    if res["sample_peak_db"] is not None and res["sample_peak_db"] > -0.1 and (res["flat_factor"] or 0) > 20:
        warn.append("clipping likely: peak at 0 dBFS with a high flat factor")
    if res["true_peak_dbtp"] is not None and res["true_peak_dbtp"] > -1.0:
        warn.append("true peak above -1 dBTP")
    if res["tail_silence_s"] > 3:
        warn.append(f"{res['tail_silence_s']} s of silence at the end (render went quiet early: trim or re-roll)")
    if res["head_silence_s"] > 1:
        warn.append(f"{res['head_silence_s']} s of silence at the start")
    if res["lufs_i"] is None:
        warn.append("no measurable loudness (silent file?)")
    res["warnings"] = warn
    return res


def cmd_measure(a):
    rows = [measure_file(f, a.silence_db, a.silence_min) for f in a.files]
    return {"ok": True, "files": rows}


def cmd_sheet(a):
    files = [need_file(f) for f in a.files]
    if not files:
        raise MwError("give at least one audio file")
    w, sh, wh = a.width, a.spec_height, a.wave_height
    inputs, parts, labels = [], [], []
    for i, f in enumerate(files):
        inputs += ["-i", str(f)]
        parts.append(f"[{i}:a]asplit=2[a{i}][b{i}]")
        parts.append(f"[a{i}]showspectrumpic=s={w}x{sh}:legend=0:fscale=log:stop={a.max_hz}[s{i}]")
        parts.append(f"[b{i}]showwavespic=s={w}x{wh}:split_channels=0:colors=0x9fd3ff[w{i}]")
        labels.append(f.name)
    rows = "".join(f"[s{i}][w{i}]" for i in range(len(files)))
    fc = ";".join(parts) + f";{rows}vstack=inputs={2 * len(files)}[v]"
    dst = out_file(a.out)
    ffmpeg(["-y"] + inputs + ["-filter_complex", fc, "-map", "[v]", "-frames:v", "1", str(dst)])
    meas = [measure_file(f) for f in files] if a.measure else []
    return {"ok": True, "sheet": str(dst.resolve()), "rows": labels,
            "layout": f"per take, top to bottom: spectrogram {w}x{sh} (log frequency, 0-{a.max_hz} Hz, time left to right) then waveform {w}x{wh}",
            "read_it": "open the PNG and look: one bright line with harmonics = one melodic voice; broad vertical stripes = drums; a wide low band = pad, drone or bass; dark columns = silence; a dark block at the end = the render went quiet",
            "measure": meas}


# ---------------------------------------------------------------- finishing

def presets():
    return load_json(REFS / "loudness.json")["presets"]


def loudnorm_two_pass(src, dst, target_i, target_tp, target_lra, rate):
    r1 = ffmpeg(["-i", str(src), "-af", f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}:print_format=json",
                 "-f", "null", "-"])
    blob = r1.stderr[r1.stderr.rfind("{"):r1.stderr.rfind("}") + 1]
    try:
        m = json.loads(blob)
    except ValueError:
        raise MwError("could not read loudnorm's first-pass measurement")
    af = (f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}:measured_I={m['input_i']}:"
          f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true:print_format=json")
    r2 = ffmpeg(["-y", "-i", str(src), "-af", af, "-ar", str(rate)] + out_codec(dst) + [str(dst)])
    blob2 = r2.stderr[r2.stderr.rfind("{"):r2.stderr.rfind("}") + 1]
    try:
        n = json.loads(blob2)
        mode = n.get("normalization_type")
    except ValueError:
        mode = None
    return m, mode


def cmd_master(a):
    src = need_file(a.input)
    pr = presets()
    if a.preset not in pr:
        raise MwError(f"unknown preset {a.preset}; choose from {', '.join(sorted(pr))}")
    p = pr[a.preset]
    ti = a.lufs if a.lufs is not None else p["lufs"]
    tp = a.tp if a.tp is not None else p["true_peak"]
    dst = out_file(a.out) if a.out else src.with_name(f"{src.stem}_{a.preset}.wav")
    before = measure_file(src)
    first, mode = loudnorm_two_pass(src, dst, ti, tp, a.lra, a.rate)
    after = measure_file(dst)
    warn = []
    if mode and mode != "linear":
        warn.append("loudnorm fell back to dynamic mode (the target needs more gain than the peaks allow); dynamics were changed. Lower the target or accept it.")
    if after["lufs_i"] is not None and abs(after["lufs_i"] - ti) > 1.0:
        warn.append(f"result {after['lufs_i']} LUFS is more than 1 LU from the target {ti}")
    return {"ok": True, "out": str(dst.resolve()), "preset": a.preset, "target": {"lufs": ti, "true_peak": tp},
            "preset_note": p.get("note"), "normalization": mode,
            "before": {k: before[k] for k in ("lufs_i", "true_peak_dbtp", "lra")},
            "after": {k: after[k] for k in ("lufs_i", "true_peak_dbtp", "lra", "duration_s", "sample_rate")},
            "warnings": warn}


def cmd_edit(a):
    src = need_file(a.input)
    info = probe(src)
    start = a.start or 0.0
    end = a.end if a.end is not None else info["duration_s"]
    if end <= start:
        raise MwError("end must be after start")
    length = end - start
    f = [f"atrim=start={start}:end={end}", "asetpts=PTS-STARTPTS"]
    if a.fade_in:
        f.append(f"afade=t=in:st=0:d={a.fade_in}:curve=qsin")
    if a.fade_out:
        f.append(f"afade=t=out:st={max(0.0, length - a.fade_out)}:d={a.fade_out}:curve=qsin")
    dst = out_file(a.out)
    extra = ["-ar", str(a.rate)] if a.rate else []
    ffmpeg(["-y", "-i", str(src), "-af", ",".join(f)] + extra + out_codec(dst) + [str(dst)])
    return {"ok": True, "out": str(dst.resolve()), "length_s": round(length, 3), **{k: v for k, v in probe(dst).items()}}


def cmd_join(a):
    files = [need_file(f) for f in a.files]
    if len(files) < 2:
        raise MwError("join needs two or more files")
    x = a.xfade
    lengths = [float(v) for v in a.lengths.split(",")] if a.lengths else None
    if lengths and len(lengths) != len(files):
        raise MwError("--lengths needs one value per file")
    inputs, parts = [], []
    for i, f in enumerate(files):
        inputs += ["-i", str(f)]
        if lengths:
            keep = lengths[i] + (x if i < len(files) - 1 else 0)
            parts.append(f"[{i}:a]atrim=start=0:end={keep},asetpts=PTS-STARTPTS,aresample=48000[p{i}]")
        else:
            parts.append(f"[{i}:a]aresample=48000[p{i}]")
    prev = "p0"
    for i in range(1, len(files)):
        lab = f"x{i}"
        parts.append(f"[{prev}][p{i}]acrossfade=d={x}:c1=qsin:c2=qsin[{lab}]")
        prev = lab
    tail = f"[{prev}]"
    if a.fade_out:
        parts.append(f"{tail}areverse,afade=t=in:d={a.fade_out}:curve=qsin,areverse[fo]")
        tail = "[fo]"
    fc = ";".join(parts)
    dst = out_file(a.out)
    ffmpeg(["-y"] + inputs + ["-filter_complex", fc, "-map", tail] + out_codec(dst) + [str(dst)])
    hits, t = [], 0.0
    if lengths:
        for L in lengths[:-1]:
            t += L
            hits.append(round(t, 3))
    return {"ok": True, "out": str(dst.resolve()), "duration_s": probe(dst)["duration_s"],
            "crossfade_centres_s": hits, "note": "each crossfade starts at the hit point and lasts --xfade seconds"}


def read_pcm16(path):
    """Return (left channel samples as array('h'), rate, channels) from a 16-bit WAV."""
    with wave.open(str(path), "rb") as w:
        ch, rate, width, n = w.getnchannels(), w.getframerate(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    if width != 2:
        raise MwError("seam check needs 16-bit PCM")
    a = array("h")
    a.frombytes(raw)
    if sys.byteorder == "big":
        a.byteswap()
    return a[0::ch], rate, ch


def seam_score(path):
    """Loop seam jump compared with the file's own sample-to-sample motion. ~1 is inaudible, >5 clicks."""
    p = need_file(path)
    tmp = None
    try:
        if p.suffix.lower() != ".wav" or probe(p)["codec"] != "pcm_s16le":
            tmp = Path(tempfile.mkdtemp(prefix="mw_")) / "seam.wav"
            ffmpeg(["-y", "-i", str(p), "-c:a", "pcm_s16le", str(tmp)])
            src = tmp
        else:
            src = p
        L, rate, ch = read_pcm16(src)
    finally:
        pass
    if len(L) < 1000:
        raise MwError("file too short for a seam check")
    steps = sorted(abs(L[i + 1] - L[i]) for i in range(0, len(L) - 1, max(1, len(L) // 200000)))
    p99 = steps[int(len(steps) * 0.99)] or 1
    jump = abs(L[0] - L[-1])
    win = min(len(L) // 4, rate // 20)
    rms_end = math.sqrt(sum(v * v for v in L[-win:]) / win) or 1.0
    rms_start = math.sqrt(sum(v * v for v in L[:win]) / win) or 1.0
    level_jump_db = round(20 * math.log10(max(rms_start, 1.0) / max(rms_end, 1.0)), 2)
    ratio = round(jump / p99, 2)
    if tmp:
        shutil.rmtree(tmp.parent, ignore_errors=True)
    verdict = "clean" if ratio <= 2 and abs(level_jump_db) < 3 else ("check by ear" if ratio <= 5 and abs(level_jump_db) < 6 else "audible seam likely")
    return {"file": str(p), "seam_jump": jump, "p99_step": p99, "ratio": ratio,
            "level_jump_db": level_jump_db, "verdict": verdict}


def cmd_seam(a):
    return {"ok": True, "files": [seam_score(f) for f in a.files]}


def cmd_loop(a):
    src = need_file(a.input)
    info = probe(src)
    x = a.xfade
    start = a.start or 0.0
    if a.bars:
        if not a.bpm:
            raise MwError("--bars needs --bpm")
        body = a.bars * a.beats_per_bar * 60.0 / a.bpm
        end = start + body + x
    else:
        end = a.end if a.end is not None else info["duration_s"]
        body = end - start - x
    if end > info["duration_s"] + 1e-3:
        raise MwError(f"loop needs {end:.2f} s of source but the file is {info['duration_s']} s; lower --bars or --start")
    if body <= x:
        raise MwError("loop body must be longer than the crossfade")
    # out = (tail fading out + head fading in) followed by seg[x : L-x]; length L - x.
    # The crossfade is done here on raw float samples, not in an ffmpeg filter graph:
    # amix/concat graphs behave differently across ffmpeg versions (6.1 refused them).
    ch = max(1, min(info["channels"] or 2, 2))
    rate = a.rate
    tmpd = Path(tempfile.mkdtemp(prefix="mw_loop_"))
    try:
        raw_in, raw_out = tmpd / "in.f32", tmpd / "out.f32"
        ffmpeg(["-y", "-ss", f"{start:.6f}", "-i", str(src), "-t", f"{end - start:.6f}", "-ac", str(ch),
                "-ar", str(rate), "-f", "f32le", "-c:a", "pcm_f32le", str(raw_in)])
        buf = array("f")
        buf.frombytes(raw_in.read_bytes())
        if sys.byteorder == "big":
            buf.byteswap()
        nx = int(round(x * rate))
        nbody = int(round(body * rate))
        have = len(buf) // ch
        if have < nbody + nx:
            raise MwError(f"decoded only {have} frames, need {nbody + nx}; lower --bars or --start")
        out_buf = array("f", buf[: nbody * ch])
        for i in range(nx):
            gin = math.sin(0.5 * math.pi * (i + 0.5) / nx)
            gout = math.cos(0.5 * math.pi * (i + 0.5) / nx)
            for c in range(ch):
                out_buf[i * ch + c] = buf[i * ch + c] * gin + buf[(nbody + i) * ch + c] * gout
        if sys.byteorder == "big":
            out_buf.byteswap()
        raw_out.write_bytes(out_buf.tobytes())
        dst = out_file(a.out)
        codec = ["-c:a", "pcm_s16le"] if dst.suffix.lower() == ".wav" else out_codec(dst)
        samples = nbody
        loop_tags = ["-metadata", "LOOPSTART=0", "-metadata", f"LOOPLENGTH={samples}"]
        # an .ogg --out with --ogg is tagged in this pass; re-encoding it onto itself would fail
        meta = loop_tags if a.ogg and dst.suffix.lower() == ".ogg" else []
        ffmpeg(["-y", "-f", "f32le", "-ar", str(rate), "-ac", str(ch), "-i", str(raw_out)] + codec + meta + [str(dst)])
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    res = {"ok": True, "out": str(dst.resolve()), "loop_length_s": round(body, 4),
           "source_window_s": [round(start, 3), round(end, 3)], "xfade_s": x, "seam": seam_score(dst)}
    if a.ogg:
        og = dst.with_suffix(".ogg")
        if not meta:
            ffmpeg(["-y", "-i", str(dst)] + vorbis_codec() + loop_tags + [str(og)])
        res["ogg"] = str(og.resolve())
        res["ogg_note"] = "LOOPSTART/LOOPLENGTH (in samples) are read by RPG Maker and some players; Unity ignores them, so set Loop on the AudioSource and import the WAV or this OGG"
    if a.bars:
        res["bars"] = a.bars
        res["bpm"] = a.bpm
    return res


def cmd_duck(a):
    music = need_file(a.music)
    under = need_file(a.under)
    has_video = any(s.get("codec_type") == "video" for s in json.loads(run(
        [ffmpeg_bin("ffprobe"), "-v", "error", "-show_entries", "stream=codec_type", "-of", "json", str(under)]).stdout or "{}").get("streams", []))
    g = a.music_gain
    # the key is padded with silence so the ducked music keeps its own length when the key is shorter
    key = "[1:a]aresample=48000,apad[sc]" if a.stem else "[1:a]aresample=48000,asplit=2[sc0][keep];[sc0]apad[sc]"
    fc = (f"[0:a]volume={g}dB,aresample=48000[mu];{key};"
          f"[mu][sc]sidechaincompress=threshold={a.threshold}:ratio={a.ratio}:attack={a.attack}:release={a.release}[d]")
    if not a.stem:
        fc += ";[d][keep]amix=inputs=2:normalize=0:duration=longest[o]"
    dst = out_file(a.out)
    args = ["-y", "-i", str(music), "-i", str(under), "-filter_complex", fc]
    if a.stem:
        args += ["-map", "[d]"] + out_codec(dst) + [str(dst)]
    elif has_video and dst.suffix.lower() in (".mp4", ".mov", ".mkv"):
        args += ["-map", "1:v", "-map", "[o]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", str(dst)]
    else:
        args += ["-map", "[o]"] + out_codec(dst) + [str(dst)]
    ffmpeg(args)
    remuxed = not a.stem and has_video and dst.suffix.lower() in (".mp4", ".mov", ".mkv")
    return {"ok": True, "out": str(dst.resolve()),
            "returns": "the ducked music alone, at the music's length" if a.stem else ("the video with the ducked mix" if remuxed else "the ducked music mixed with the key"),
            "duration_s": probe(dst)["duration_s"], "remuxed_video": remuxed,
            "settings": {"music_gain_db": g, "threshold": a.threshold, "ratio": a.ratio, "attack_ms": a.attack, "release_ms": a.release},
            "next": "run measure on the result and master it to the destination preset"}


def per_file(spec, n, name, default=0.0):
    if not spec:
        return [default] * n
    vals = [float(v) for v in spec.split(",")]
    if len(vals) != n:
        raise MwError(f"--{name} needs one value per file ({n}), got {len(vals)}")
    return vals


def decode_f32(path, rate, tmpd):
    """Decode to interleaved stereo float32 at rate (ffmpeg decodes; the arithmetic stays in Python, L-001)."""
    raw = Path(tmpd) / (uuid.uuid4().hex + ".f32")
    ffmpeg(["-y", "-i", str(path), "-ac", "2", "-ar", str(rate), "-f", "f32le", "-c:a", "pcm_f32le", str(raw)])
    buf = array("f")
    buf.frombytes(raw.read_bytes())
    if sys.byteorder == "big":
        buf.byteswap()
    raw.unlink()
    return buf


def encode_f32(buf, rate, dst, tmpd):
    raw = Path(tmpd) / (uuid.uuid4().hex + ".f32")
    b = array("f", buf)
    if sys.byteorder == "big":
        b.byteswap()
    raw.write_bytes(b.tobytes())
    ffmpeg(["-y", "-f", "f32le", "-ar", str(rate), "-ac", "2", "-i", str(raw)] + out_codec(dst) + [str(dst)])
    raw.unlink()


def cmd_mix(a):
    files = [need_file(f) for f in a.files]
    n = len(files)
    gains = per_file(a.gains, n, "gains")
    offsets = per_file(a.offsets, n, "offsets")
    pans = per_file(a.pans, n, "pans")
    if any(abs(p) > 1 for p in pans):
        raise MwError("--pans values run from -1 (left) to 1 (right)")
    rate = a.rate
    tmpd = Path(tempfile.mkdtemp(prefix="mw_mix_"))
    try:
        stems = []
        for f, g, off, pan in zip(files, gains, offsets, pans):
            buf = decode_f32(f, rate, tmpd)
            lin = 10 ** (g / 20.0)
            ang = (pan + 1) * math.pi / 4  # equal-power balance; centre leaves both channels at unity
            gl, gr = lin * math.cos(ang) * math.sqrt(2), lin * math.sin(ang) * math.sqrt(2)
            shift = int(round(off * rate))
            if shift < 0:
                buf = buf[-shift * 2:]
            stems.append((buf, max(shift, 0), gl, gr))
        ends = [s[1] + len(s[0]) // 2 for s in stems]
        if a.length == "longest":
            total = max(ends)
        elif a.length == "first":
            total = ends[0]
        else:
            total = int(round(float(a.length) * rate))
        if total <= 0:
            raise MwError("the mix would be empty; check --offsets and --length")
        mix = array("f", bytes(4 * 2 * total))
        aligned = []
        for buf, start, gl, gr in stems:
            one = array("f", bytes(4 * 2 * total)) if a.stems else None
            frames = min(len(buf) // 2, total - start)
            for i in range(max(frames, 0)):
                j, k = 2 * (start + i), 2 * i
                left, right = buf[k] * gl, buf[k + 1] * gr
                mix[j] += left
                mix[j + 1] += right
                if one is not None:
                    one[j], one[j + 1] = left, right
            aligned.append(one)
        peak = max(max(mix), -min(mix))
        warn, scale = [], 1.0
        ceiling = 10 ** (-1 / 20.0)
        if peak > ceiling and not a.no_limit:
            scale = ceiling / peak
            mix = array("f", (v * scale for v in mix))
            warn.append(f"the sum peaked at {20 * math.log10(peak):+.1f} dBFS; mix and stems scaled by {20 * math.log10(scale):.1f} dB to peak at -1 dBFS (master it afterwards)")
        dst = out_file(a.out)
        encode_f32(mix, rate, dst, tmpd)
        stem_files = []
        if a.stems:
            sd = Path(a.stems)
            sd.mkdir(parents=True, exist_ok=True)
            for i, (f, one) in enumerate(zip(files, aligned), 1):
                if scale != 1.0:
                    one = array("f", (v * scale for v in one))
                sf = sd / f"{i:02d}_{slug(f.stem)}.wav"
                encode_f32(one, rate, sf, tmpd)
                stem_files.append(str(sf.resolve()))
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    m = measure_file(dst)
    return {"ok": True, "out": str(dst.resolve()), "duration_s": round(total / rate, 3),
            "layers": [{"file": str(f), "gain_db": g, "offset_s": o, "pan": p} for f, g, o, p in zip(files, gains, offsets, pans)],
            "scaled_db": round(20 * math.log10(scale), 2), "stems": stem_files,
            "measure": {k: m[k] for k in ("lufs_i", "true_peak_dbtp", "lra")}, "warnings": warn,
            "next": "sheet the mix beside its stems, then master it to the destination preset"}


def cmd_analyze(a):
    try:
        import librosa  # noqa: F401
        import numpy as np
    except ImportError:
        script = Path(__file__).resolve()
        return {"ok": False, "error": "librosa is not installed in this Python",
                "fix": f'uv run --no-project --python 3.12 --with librosa --with soundfile python "{script}" analyze ' + " ".join(f'"{f}"' for f in a.files)}
    import librosa
    import numpy as np
    maj = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    mnr = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    rows = []
    for f in a.files:
        y, sr = librosa.load(str(need_file(f)), sr=None, mono=True)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr).mean(axis=1)
        cands = sorted(((float(np.corrcoef(np.roll(p, k), chroma)[0, 1]), names[k] + (" major" if mj else " minor"))
                        for mj, p in ((1, maj), (0, mnr)) for k in range(12)), reverse=True)
        onset = librosa.onset.onset_strength(y=y, sr=sr)
        rows.append({"file": str(f), "tempo_bpm": round(float(np.atleast_1d(tempo)[0]), 2), "beats": int(len(beats)),
                     "key": cands[0][1], "key_confidence": round(cands[0][0], 2), "runner_up": cands[1][1],
                     "onset_strength_mean": round(float(onset.mean()), 3),
                     "note": "tempo can come back doubled or halved; key estimates on modal or pentatonic music often name the relative major/minor"})
    return {"ok": True, "librosa": librosa.__version__, "files": rows}


# ---------------------------------------------------------------- pulse and answer (stdlib measures)

ENV_RATE, ENV_HOP = 8000, 0.01  # 8 kHz mono, 10 ms frames


def envelope_db(path, tmpd):
    """Frame levels in dB (20 ms windows every 10 ms) of a file decoded to 8 kHz mono."""
    raw = Path(tmpd) / (uuid.uuid4().hex + ".f32")
    ffmpeg(["-y", "-i", str(path), "-ac", "1", "-ar", str(ENV_RATE), "-f", "f32le", "-c:a", "pcm_f32le", str(raw)])
    buf = array("f")
    buf.frombytes(raw.read_bytes())
    if sys.byteorder == "big":
        buf.byteswap()
    raw.unlink()
    hop, win = int(ENV_RATE * ENV_HOP), int(ENV_RATE * 0.02)
    env = []
    for i in range(0, max(len(buf) - win, 0) + 1, hop):
        s = sum(v * v for v in buf[i:i + win]) / win
        env.append(10 * math.log10(s) if s > 1e-12 else -120.0)
    return env


def onsets_from_env(env, floor_db=-50.0):
    """Onset frames: peaks of the rising level (dB per 10 ms) above an adaptive threshold."""
    flux = [0.0] + [max(0.0, env[i] - env[i - 1]) if env[i] > floor_db else 0.0 for i in range(1, len(env))]
    sm = [sum(flux[max(0, i - 1):i + 2]) / 3 for i in range(len(flux))]
    mean = sum(sm) / max(len(sm), 1)
    sd = math.sqrt(sum((v - mean) ** 2 for v in sm) / max(len(sm), 1))
    thr, gap, last, hits = mean + 1.5 * sd, int(0.08 / ENV_HOP), -10 ** 9, []
    for i in range(1, len(sm) - 1):
        if sm[i] > thr and sm[i] >= sm[i - 1] and sm[i] >= sm[i + 1] and i - last >= gap:
            hits.append(i)
            last = i
    return sm, hits


def grid_deviation(times, period):
    """Mean distance of onsets from the best-phased grid (the beat, or its halves or thirds), in grid steps.

    0 is on the grid; random onsets score grid_chance, computed the same way."""
    best = 1.0
    for div in (1, 2, 3):
        step = period / div
        for k in range(40):
            ph = period * k / 40
            d = sum(abs(((t - ph) / step + 0.5) % 1 - 0.5) for t in times) / len(times)
            best = min(best, d)
    return best


def pulse_of(path, tmpd):
    import random
    env = envelope_db(path, tmpd)
    strength, hits = onsets_from_env(env)
    times = [h * ENV_HOP for h in hits]
    dur = len(env) * ENV_HOP
    row = {"file": str(path), "duration_s": round(dur, 2), "onsets": len(times),
           "onsets_per_min": round(60 * len(times) / dur, 1) if dur else 0}
    if len(times) < 6:
        row.update({"pulse": "none", "why": "fewer than 6 onsets"})
        return row
    iois = [b - a for a, b in zip(times, times[1:])]
    m = sum(iois) / len(iois)
    row["ioi_cv"] = round(math.sqrt(sum((v - m) ** 2 for v in iois) / len(iois)) / m, 2)
    mu = sum(strength) / len(strength)
    x = [v - mu for v in strength]
    e0 = sum(v * v for v in x) or 1.0
    lags = range(int(0.25 / ENV_HOP), min(int(2.0 / ENV_HOP), len(x) // 2) + 1)  # 240 to 30 bpm
    ac = [(L, sum(x[i] * x[i + L] for i in range(len(x) - L)) / e0) for L in lags]
    vals = sorted(v for _, v in ac)
    med = vals[len(vals) // 2]
    lag, peak = max(ac, key=lambda t: t[1])
    period = lag * ENV_HOP
    bpm = 60 / period
    while bpm < 60:
        bpm *= 2
    while bpm > 180:
        bpm /= 2
    dev = grid_deviation(times, period)
    rng = random.Random(1)
    chance = sum(grid_deviation(sorted(rng.uniform(0, dur) for _ in times), period) for _ in range(20)) / 20
    contrast = peak - med
    votes = (contrast >= 0.2) * 2 + (contrast >= 0.15) + (dev <= 0.75 * chance) + (row["ioi_cv"] <= 0.5)
    row.update({"autocorr_peak": round(peak, 2), "autocorr_median": round(med, 2), "autocorr_contrast": round(contrast, 2),
                "tempo_bpm": round(bpm, 1), "grid_deviation": round(dev, 3), "grid_chance": round(chance, 3),
                "pulse": "steady" if votes >= 3 else ("weak" if votes >= 1 else "none")})
    return row


def cmd_pulse(a):
    tmpd = Path(tempfile.mkdtemp(prefix="mw_pulse_"))
    try:
        rows = [pulse_of(need_file(f), tmpd) for f in a.files]
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    return {"ok": True, "files": rows,
            "reading": "steady: a beat a percussion part can lock to (tempo_bpm may be doubled or halved); "
                       "weak or none: free time, so place accents on phrases or re-render on a fixed tempo rather than adding a beat. "
                       "grid_deviation near grid_chance means the onsets ignore the grid; ioi_cv above about 0.8 is rubato or phrase-led"}


def power_mean_db(env, idx):
    if not idx:
        return None
    p = sum(10 ** (env[i] / 10) for i in idx) / len(idx)
    return round(10 * math.log10(p), 1) if p > 1e-12 else -120.0


def cmd_answer(a):
    tmpd = Path(tempfile.mkdtemp(prefix="mw_answer_"))
    try:
        part = envelope_db(need_file(a.part), tmpd)
        lead = envelope_db(need_file(a.lead), tmpd)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    n = min(len(part), len(lead))
    part, lead = part[:n], lead[:n]
    ref = sorted(lead)[int(0.95 * (n - 1))] if n else -120.0
    thr = max(ref - a.below, -60.0)
    on = [lead[i] > thr for i in range(n)]
    if not any(on):
        raise MwError("the lead is silent throughout; check --lead")
    first, last = on.index(True), n - 1 - on[::-1].index(True)
    under = [i for i in range(n) if on[i]]
    rests = [i for i in range(first, last + 1) if not on[i]]
    tail = list(range(last + 1, n))
    du, dr, dt = power_mean_db(part, under), power_mean_db(part, rests), power_mean_db(part, tail)
    gap = round(dr - du, 1) if du is not None and dr is not None else None
    pthr = max(sorted(part)[int(0.95 * (n - 1))] - a.below, -60.0)
    fill = round(sum(part[i] > pthr for i in rests) / len(rests), 2) if rests else None
    shape = None if gap is None else ("answers (louder in the lead's rests)" if gap >= 3 else
                                      "doubles (quieter in the rests)" if gap <= -3 else "plays along (same level under and between)")
    return {"ok": True, "part": str(a.part), "lead": str(a.lead), "lead_threshold_db": round(thr, 1),
            "lead_active_share": round(len(under) / n, 2), "part_under_lead_db": du, "part_in_rests_db": dr,
            "part_in_tail_db": dt, "rests_minus_under_db": gap, "part_active_in_rests": fill, "shape": shape,
            "next": "to make a part answer, duck it under the lead: mw.py duck PART --under LEAD --stem --out answer.wav, then measure again"}


# ---------------------------------------------------------------- notation: render, notate, transcribe

SCORE_EXT = {".abc": "abc", ".mid": "midi", ".midi": "midi", ".musicxml": "musicxml", ".xml": "musicxml",
             ".txt": "tab", ".tab": "tab"}


def fluidsynth_bin():
    env = os.environ.get("MUSICWRIGHT_FLUIDSYNTH")
    if env:
        return env if Path(env).exists() else None
    return shutil.which("fluidsynth")


def soundfont(arg=None):
    for cand in (arg, os.environ.get("MUSICWRIGHT_SOUNDFONT"), studio_config().get("soundfont")):
        if cand:
            if not Path(cand).exists():
                raise MwError(f"SoundFont not found: {cand}")
            return Path(cand)
    return None


def load_score(a, path):
    prog = notation.program_of(getattr(a, "program", None))
    score, kind = notation.load(need_file(path), tuning=getattr(a, "tuning", None), tab_step=getattr(a, "tab_step", None),
                                bpm=getattr(a, "bpm", None), program=prog, chords=getattr(a, "chords", False),
                                tune=getattr(a, "tune", None))
    if getattr(a, "transpose", 0):
        notation.transpose(score, a.transpose)
    return score, kind


def cmd_render(a):
    score, kind = load_score(a, a.score)
    res = {"ok": True, "score": str(Path(a.score).resolve()), "read_as": kind, **score.summary(), "warnings": score.warnings}
    if a.check:
        res["next"] = "fix the warnings (a bar that is too long or short usually means a wrong note length), then render with --out"
        return res
    if not a.out:
        raise MwError("give --out (an audio file), or --check to only read the score")
    dst = out_file(a.out)
    mid = Path(a.midi) if a.midi else dst.with_suffix(".mid")
    if mid.resolve() == dst.resolve():
        raise MwError("--out is the MIDI file; give an audio file (.wav, .flac, .mp3, .ogg) and --midi for the MIDI")
    mid.parent.mkdir(parents=True, exist_ok=True)
    notation.write_midi(score, mid)
    fs, sf = fluidsynth_bin(), soundfont(a.sf2)
    synth = a.synth
    if synth == "auto":
        synth = "fluidsynth" if fs and sf else "builtin"
        if synth == "builtin":
            res["warnings"].append("rendered with the built-in synth (a sketch: plucked strings, simple winds and organ). "
                                   "For General MIDI instruments install FluidSynth and a SoundFont (references/notation.md)")
    tmpd = Path(tempfile.mkdtemp(prefix="mw_render_"))
    try:
        raw = tmpd / "render.wav"
        if synth == "fluidsynth":
            if not fs:
                raise MwError("FluidSynth not found: put fluidsynth on PATH or set MUSICWRIGHT_FLUIDSYNTH")
            if not sf:
                raise MwError("no SoundFont: pass --sf2, set MUSICWRIGHT_SOUNDFONT, or add \"soundfont\" to the studio config.json")
            run([fs, "-ni", "-q", "-g", str(a.gain), "-r", "48000", "-F", str(raw), str(sf), str(mid)])
            res["soundfont"] = str(sf)
        else:
            notation.synth_wav(score, raw)
        chain = ["-af", f"apad=pad_dur={a.tail}"] if synth == "fluidsynth" and a.tail else []
        ffmpeg(["-y", "-i", str(raw)] + chain + ["-ar", "48000", "-ac", "2"] + out_codec(dst) + [str(dst)])
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    m = measure_file(dst)
    res.update({"out": str(dst.resolve()), "midi": str(mid.resolve()), "synth": synth,
                "measure": {k: m[k] for k in ("duration_s", "lufs_i", "true_peak_dbtp")},
                "next": "listen, or make it sound performed with an AI cover of this render: mw.py gen --recipe acestep-rest "
                        "--task cover --src OUT --strength 0.6 --caption \"<instruments, style>\" --seeds 1,2,3 (try 0.5-0.9)"})
    return res


def cmd_notate(a):
    score, kind = load_score(a, a.score)
    dst = out_file(a.out)
    to = a.to or {".abc": "abc", ".mid": "midi", ".midi": "midi", ".musicxml": "musicxml", ".xml": "musicxml",
                  ".txt": "tab", ".tab": "tab"}.get(dst.suffix.lower())
    if not to:
        raise MwError("say the format with --to abc|musicxml|midi|tab, or end --out in .abc, .musicxml, .mid or .txt")
    warn = list(score.warnings)
    if to == "midi":
        notation.write_midi(score, dst)
    elif to == "abc":
        write_lf(dst, notation.write_abc(score, a.grid))
    elif to == "musicxml":
        write_lf(dst, notation.write_musicxml(score, a.grid))
    else:
        text, w = notation.write_tab(score, notation.tuning_from_spec(a.tuning), a.grid, max_fret=a.max_fret)
        write_lf(dst, text + "\n")
        warn += w
    if to in ("abc", "musicxml", "tab") and kind in ("midi", "tab"):
        warn.append(f"notes were snapped to a grid of {a.grid} steps a beat; triplets and free rhythm come out approximate")
    return {"ok": True, "from": kind, "to": to, "out": str(dst.resolve()), **score.summary(), "warnings": warn,
            "next": "open .musicxml in MuseScore (free) for a printable score; mw.py render plays any of these back"}


def split_at_onsets(notes, onsets, min_note=0.06):
    out = []
    for n in notes:
        cuts = [t for t in onsets if n.start + min_note < t < n.end() - min_note]
        s = n.start
        for c in cuts + [n.end()]:
            out.append(notation.Note(s, c - s, n.pitch, n.vel))
            s = c
    return out


def gate_notes(score, src, below_db, lowest, highest):
    """Drop notes the recording barely sounds (hiss and hum in rests read as notes) or that fall outside the range."""
    tmpd = Path(tempfile.mkdtemp(prefix="mw_gate_"))
    try:
        env = envelope_db(src, tmpd)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    ref = sorted(env)[int(0.95 * (len(env) - 1))] if env else 0.0
    thr = ref - below_db
    lo, hi = notation.parse_pitch_name(lowest), notation.parse_pitch_name(highest)
    dropped = {"quiet": 0, "range": 0}
    for tr in score.tracks:
        keep = []
        for n in tr.notes:
            if not lo <= n.pitch <= hi:
                dropped["range"] += 1
                continue
            i0 = int(score.seconds(n.start) / ENV_HOP)
            i1 = max(int(score.seconds(n.end()) / ENV_HOP), i0 + 1)
            seg = env[i0:i1] or [-120.0]
            level = 10 * math.log10(sum(10 ** (v / 10) for v in seg) / len(seg))
            if level < thr:
                dropped["quiet"] += 1
                continue
            keep.append(n)
        tr.notes = keep
    return {"threshold_db": round(thr, 1), "dropped_quiet": dropped["quiet"], "dropped_out_of_range": dropped["range"]}


def cmd_transcribe(a):
    src = need_file(a.audio)
    dst = out_file(a.out)
    if dst.suffix.lower() not in (".mid", ".midi"):
        raise MwError("--out is the MIDI file (.mid); add --to abc,musicxml,tab for notation beside it")
    prog = notation.program_of(a.program) if a.program is not None else None
    res = {"ok": True, "audio": str(src.resolve()), "engine": a.engine}
    if a.engine == "basic-pitch":
        exe = os.environ.get("MUSICWRIGHT_BASIC_PITCH") or shutil.which("basic-pitch")
        if not exe:
            return {"ok": False, "error": "basic-pitch is not installed",
                    "fix": 'uv tool install --python 3.11 basic-pitch --with "numpy<2" --with "setuptools<81"   '
                           "(Apache-2.0, a few hundred MB with TensorFlow; it does not install on Python 3.12+)"}
        tmpd = Path(tempfile.mkdtemp(prefix="mw_bp_"))
        try:
            os.environ.setdefault("PYTHONIOENCODING", "utf-8")  # basic-pitch prints emoji; a Windows console codec would crash it
            run([exe, str(tmpd), str(src)])
            mids = list(tmpd.glob("*.mid"))
            if not mids:
                raise MwError("basic-pitch wrote no MIDI file")
            score = notation.parse_midi(mids[0].read_bytes())
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)
        bp_bpm = score.tempos[0][1]
        bpm = a.bpm or bp_bpm
        if a.bpm and abs(a.bpm - bp_bpm) > 1e-6:  # basic-pitch writes its own tempo; rescale beats to the asked one
            k = a.bpm / bp_bpm
            for n in score.notes():
                n.start *= k
                n.dur *= k
            score.tempos = [(0.0, float(a.bpm))]
        for t in score.tracks:
            if prog is not None:
                t.program = prog
    else:
        try:
            import librosa
            import numpy as np  # noqa: F401
        except ImportError:
            script = Path(__file__).resolve()
            args = " ".join(f'"{x}"' for x in [a.audio, "--out", a.out] + (["--to", a.to] if a.to else []) + (["--bpm", str(a.bpm)] if a.bpm else []))
            return {"ok": False, "error": "librosa is not installed in this Python (transcribe uses its pyin pitch tracker)",
                    "fix": f'uv run --no-project --python 3.12 --with librosa --with soundfile python "{script}" transcribe {args}'}
        y, sr = librosa.load(str(src), sr=22050, mono=True)
        hop = 256
        fmin = librosa.note_to_hz(a.lowest)
        fmax = librosa.note_to_hz(a.highest)
        f0, voiced, _ = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=sr, frame_length=2048, hop_length=hop)
        rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
        times = librosa.times_like(f0, sr=sr, hop_length=hop)
        f0l = [None if (v != v) else float(v) for v in f0]
        notes = notation.notes_from_f0([float(t) for t in times], f0l, [bool(v) for v in voiced],
                                       [float(r) for r in rms], hop=hop / sr)
        onsets = [float(t) for t in librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop, units="time", backtrack=False)]
        notes = split_at_onsets(notes, onsets)
        bpm = a.bpm
        if not bpm:
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            bpm = round(float(np.atleast_1d(tempo)[0]), 1) or 120.0
            res["bpm_estimated"] = True
        score = notation.score_from_seconds(notes, bpm, 73 if prog is None else prog, src.stem)
        if not score.notes():
            raise MwError("no pitched notes found; is the audio silent, or outside --lowest/--highest?")
        score.title = src.stem
    res["gate"] = gate_notes(score, src, a.gate, a.lowest, a.highest)
    if not score.notes():
        raise MwError("every note fell under the level gate or outside --lowest/--highest; lower --gate or widen the range")
    score.meter = tuple(int(x) for x in a.meter.split("/")) if a.meter else score.meter
    score.key = score.key or notation.estimate_key(score.notes())
    notation.write_midi(score, dst)
    files = {"midi": str(dst.resolve())}
    warn = []
    for fmt in [f.strip() for f in (a.to or "").split(",") if f.strip()]:
        ext = {"abc": ".abc", "musicxml": ".musicxml", "tab": ".tab.txt"}.get(fmt)
        if not ext:
            raise MwError(f"--to {fmt}: choose from abc, musicxml, tab")
        f = dst.with_name(dst.stem + ext)
        if fmt == "abc":
            write_lf(f, notation.write_abc(score, a.grid))
        elif fmt == "musicxml":
            write_lf(f, notation.write_musicxml(score, a.grid))
        else:
            text, w = notation.write_tab(score, notation.tuning_from_spec(a.tuning), a.grid)
            write_lf(f, text + "\n")
            warn += w
        files[fmt] = str(f.resolve())
    if a.engine == "pyin":
        warn.append("pyin follows one line: chords come back as one note, and a free-time take is notated against "
                    f"{bpm:g} bpm, so the rhythm is approximate (check mw.py pulse; pass --bpm when you know it)")
    res.update({"files": files, **score.summary(), "warnings": warn,
                "next": "mw.py render the MIDI and compare it with the recording by ear; open the .musicxml in MuseScore to read or fix it"})
    return res


# ---------------------------------------------------------------- projects, ledger, studio

BRIEF = """# {name}

- Use: {use} (game-loop, game-cue, film-cue, listening, song)
- Length: {duration} s
- Destination loudness preset: {preset}
- Mood and story arc:
- Instruments (and ones to keep out):
- Tempo feel and key (or leave to the model):
- References described in words (never upload or name a living artist):
- Must hit (times in seconds, for film cues):

## Decisions
"""


def cmd_new(a):
    d = Path(a.dir)
    if (d / "music.json").exists():
        raise MwError(f"{d} already has music.json")
    for sub in ("takes", "out", "sheets"):
        (d / sub).mkdir(parents=True, exist_ok=True)
    pr = a.preset or {"game-loop": "game-music", "game-cue": "game-music", "film-cue": "web-video",
                      "listening": "streaming", "song": "streaming"}[a.use]
    man = {"musicwright": VERSION, "name": a.name, "use": a.use, "duration_s": a.duration, "loudness_preset": pr,
           "created": now(), "ai_generated": True, "deliverables": [], "disclosure": None}
    write_lf(d / "music.json", json.dumps(man, indent=1) + "\n")
    if not (d / "brief.md").exists():
        write_lf(d / "brief.md", BRIEF.format(name=a.name, use=a.use, duration=a.duration, preset=pr))
    (d / "ledger.jsonl").touch()
    return {"ok": True, "dir": str(d.resolve()), "manifest": man, "next": "fill brief.md, then mw.py gen ... --out " + str(d / "takes")}


def find_ledger(path):
    p = Path(path).resolve()
    for cand in [p] + list(p.parents):
        if (cand / "ledger.jsonl").exists():
            return cand / "ledger.jsonl"
        if cand.is_dir() and (cand / "music.json").exists():
            return cand / "ledger.jsonl"
    return None


def cmd_verdict(a):
    target = Path(a.take)
    led = find_ledger(target.parent if target.suffix else target) or (target.parent / "ledger.jsonl")
    rows = read_jsonl(led)
    match = next((r for r in reversed(rows) if r.get("type") == "take" and (r.get("file") == str(target.resolve()) or Path(r.get("file", "")).name == target.name or r.get("take") == a.take)), None)
    v = {"type": "verdict", "date": now(), "take": match.get("take") if match else target.name,
         "file": match.get("file") if match else str(target), "verdict": a.verdict, "note": a.note or "",
         "by": a.by}
    append_jsonl(led, v)
    st = dict(v)
    if match:
        st["recipe"] = {k: match.get(k) for k in ("route", "model", "seed", "caption", "lyrics", "params", "duration_s")}
    append_jsonl(studio_dir() / "verdicts.jsonl", st)
    return {"ok": True, "ledger": str(led), "studio": str(studio_dir() / "verdicts.jsonl"), "recorded": v,
            "matched_take": bool(match)}


def cmd_ledger(a):
    led = find_ledger(a.dir)
    if not led:
        raise MwError(f"no ledger.jsonl at or above {a.dir}")
    rows = read_jsonl(led)
    takes = [r for r in rows if r.get("type") == "take"]
    verdicts = {}
    for r in rows:
        if r.get("type") == "verdict":
            verdicts.setdefault(r.get("take"), []).append({"verdict": r["verdict"], "note": r.get("note"), "date": r.get("date")})
    for t in takes:
        t["verdicts"] = verdicts.get(t.get("take"), [])
    return {"ok": True, "ledger": str(led), "takes": takes, "unjudged": [t["take"] for t in takes if not t["verdicts"]]}


NOTE_FILES = {"taste": "taste.md", "lesson": "lessons.md", "recipe": "recipes.md", "idea": "ideas.md"}


def cmd_note(a):
    sd = studio_dir()
    sd.mkdir(parents=True, exist_ok=True)
    f = sd / NOTE_FILES[a.kind]
    if not f.exists():
        write_lf(f, f"# {a.kind.capitalize()} notes\n\nAppended by mw.py note; curate with musicwright-curate.\n\n")
    with open(f, "a", encoding="utf-8", newline="\n") as fh:
        src = f" (source: {a.source})" if a.source else ""
        fh.write(f"- {_dt.date.today().isoformat()}: {a.text}{src}\n")
    return {"ok": True, "file": str(f), "kind": a.kind}


# ---------------------------------------------------------------- generation

def recipes():
    return load_json(REFS / "recipes.json")["recipes"]


def sections_to_lyrics(sections):
    if not sections:
        return None
    return "\n\n".join(f"[{s.strip()}]" for s in sections.split("|") if s.strip())


def graph_acestep(r, caption, lyrics, seed, duration, bpm, key, prefix, overrides):
    p = dict(r["params"])
    p.update(overrides)
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": p["unet"], "weight_dtype": "default"}},
        "2": {"class_type": "DualCLIPLoader", "inputs": {"clip_name1": p["clip1"], "clip_name2": p["clip2"], "type": "ace", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": p["vae"]}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"shift": p["shift"], "model": ["1", 0]}},
        "5": {"class_type": "TextEncodeAceStepAudio1.5", "inputs": {
            "clip": ["2", 0], "tags": caption, "lyrics": lyrics or "[Instrumental]", "seed": seed,
            "bpm": bpm or p.get("bpm", 90), "duration": float(duration), "timesignature": str(p.get("timesignature", "4")),
            "language": p.get("language", "en"), "keyscale": key or p.get("keyscale", "C major"),
            "generate_audio_codes": True, "cfg_scale": p["lm_cfg"], "temperature": p["temperature"],
            "top_p": p["top_p"], "top_k": 0, "min_p": 0.0}},
        "6": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["5", 0]}},
        "7": {"class_type": "EmptyAceStep1.5LatentAudio", "inputs": {"seconds": float(duration), "batch_size": 1}},
        "8": {"class_type": "KSampler", "inputs": {
            "model": ["4", 0], "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["7", 0], "seed": seed,
            "steps": p["steps"], "cfg": p["cfg"], "sampler_name": p["sampler"], "scheduler": p["scheduler"], "denoise": 1.0}},
        "9": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveAudio", "inputs": {"audio": ["9", 0], "filename_prefix": prefix}},
    }, p


def graph_minimax3(r, caption, lyrics, seed, duration, bpm, key, prefix, overrides):
    p = dict(r["params"])
    p.update(overrides)
    return {
        "3": {"class_type": "CLIPLoader", "inputs": {"clip_name": p["text_encoder"], "type": "minimax", "device": "default"}},
        "6": {"class_type": "UNETLoader", "inputs": {"unet_name": p["unet"], "weight_dtype": "default"}},
        "7": {"class_type": "VAELoader", "inputs": {"vae_name": p["vae"]}},
        "13": {"class_type": "MiniMaxMusic3TextEncode", "inputs": {
            "clip": ["3", 0], "caption": caption, "lyrics": lyrics or "[instrumental]", "seed": seed,
            "max_duration": min(float(duration) * p.get("duration_pad", 1.2), p.get("max_seconds", 340.0)),
            "cfg_scale": p["lm_cfg"], "top_k": p["top_k"]}},
        "15": {"class_type": "EmptyMiniMaxMusic3LatentAudio", "inputs": {"seconds": ["13", 1], "batch_size": 1}},
        "10": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["13", 0]}},
        "9": {"class_type": "KSampler", "inputs": {
            "model": ["6", 0], "seed": seed, "steps": p["steps"], "cfg": p["cfg"], "sampler_name": p["sampler"],
            "scheduler": p["scheduler"], "positive": ["13", 0], "negative": ["10", 0], "latent_image": ["15", 0], "denoise": 1.0}},
        "42": {"class_type": "VAEDecodeAudioTiled", "inputs": {"samples": ["9", 0], "vae": ["7", 0], "tile_size": 1536, "overlap": 64}},
        "35": {"class_type": "SaveAudio", "inputs": {"audio": ["42", 0], "filename_prefix": prefix}},
    }, p


GRAPHS = {"acestep15": graph_acestep, "minimax3": graph_minimax3}


def pick_comfy(hosts, needed_model):
    """First reachable host that has the model; returns (host, info) or raises."""
    tried = []
    for h in hosts:
        try:
            models = http(h + "/models/diffusion_models", timeout=5)
        except (urllib.error.URLError, OSError, ValueError) as e:
            tried.append(f"{h}: unreachable ({type(e).__name__})")
            continue
        if needed_model in models:
            q = http(h + "/queue", timeout=5)
            return h, {"running": len(q.get("queue_running", [])), "pending": len(q.get("queue_pending", []))}
        tried.append(f"{h}: no {needed_model}")
    raise MwError("no ComfyUI host can run this recipe: " + "; ".join(tried))


def wait_comfy(host, ids, timeout, poll=5.0):
    done, t0 = {}, time.time()
    while len(done) < len(ids):
        if time.time() - t0 > timeout:
            raise MwError(f"timed out after {timeout} s; still waiting on {[i for i in ids if i not in done]}; check {host}/queue")
        for pid in ids:
            if pid in done:
                continue
            try:
                h = http(f"{host}/history/{pid}", timeout=15)
            except (urllib.error.URLError, OSError, ValueError):
                continue
            if pid in h:
                st = h[pid].get("status", {})
                if st.get("status_str") == "error":
                    msgs = [m for m in st.get("messages", []) if m and m[0] == "execution_error"]
                    raise MwError(f"ComfyUI job {pid} failed: {json.dumps(msgs)[:600]}")
                if st.get("completed"):
                    done[pid] = h[pid]
        if len(done) < len(ids):
            time.sleep(poll)
    return done


def comfy_outputs(entry):
    files = []
    for node in (entry.get("outputs") or {}).values():
        for f in node.get("audio", []) or []:
            files.append(f)
    return files


def gen_comfy(a, r, seeds, caption, lyrics, outdir):
    hosts = comfy_hosts(a.host)
    if a.dry_run:
        host, q = hosts[0], None
    else:
        host, q = pick_comfy(hosts, r["params"]["unet"])
    ov = json.loads(a.set) if a.set else {}
    for k in ("cfg", "steps", "sampler", "scheduler", "shift"):
        v = getattr(a, k, None)
        if v is not None:
            ov[k] = v
    if a.planner:
        ov["clip2"] = a.planner
    jobs, recipe_used = [], None
    for s in seeds:
        prefix = f"musicwright/{slug(a.name)}_s{s}"
        g, recipe_used = GRAPHS[r["graph"]](r, caption, lyrics, s, a.duration, a.bpm, a.key, prefix, ov)
        if a.dry_run:
            jobs.append({"seed": s, "graph": g})
            continue
        resp = http(host + "/prompt", {"prompt": g, "client_id": "musicwright-" + uuid.uuid4().hex[:8]}, timeout=30)
        if resp.get("node_errors"):
            raise MwError(f"ComfyUI rejected the graph: {json.dumps(resp['node_errors'])[:600]}")
        jobs.append({"seed": s, "prompt_id": resp["prompt_id"]})
    if a.dry_run:
        return {"ok": True, "dry_run": True, "host": host, "jobs": jobs, "params": recipe_used}
    base = {"host": host, "queue_before": q, "jobs": jobs, "params": recipe_used}
    if a.no_wait:
        return {"ok": True, "queued": True, **base,
                "next": f"watch {host}/queue; finished audio is listed at {host}/history/<prompt_id> and saved in ComfyUI's output/musicwright folder. Queued takes are not downloaded, measured or logged; run gen without --no-wait for that."}
    t0 = time.time()
    done = wait_comfy(host, [j["prompt_id"] for j in jobs], a.timeout)
    takes = []
    for j in jobs:
        for f in comfy_outputs(done[j["prompt_id"]]):
            qs = urllib.parse.urlencode({"filename": f["filename"], "subfolder": f.get("subfolder", ""), "type": f.get("type", "output")})
            data = http_get_bytes(f"{host}/view?{qs}")
            dst = outdir / f"{slug(a.name)}_s{j['seed']}{Path(f['filename']).suffix}"
            n = 2
            while dst.exists():
                dst = outdir / f"{slug(a.name)}_s{j['seed']}_{n}{Path(f['filename']).suffix}"
                n += 1
            dst.write_bytes(data)
            takes.append({"seed": j["seed"], "file": dst, "prompt_id": j["prompt_id"]})
    return {"ok": True, **base, "elapsed_s": round(time.time() - t0), "takes": takes}


def gen_rest(a, r, seeds, caption, lyrics, outdir):
    host = rest_host(a.host)
    try:
        if not a.dry_run:
            http(host + "/health", timeout=10)
    except (urllib.error.URLError, OSError) as e:
        raise MwError(f"no ACE-Step REST server at {host} ({type(e).__name__}); start it (see musicwright-generate references/acestep-rest.md) or use a comfy recipe")
    p = dict(r["params"])
    task = a.task or "text2music"
    takes, t0 = [], time.time()
    for s in seeds:
        payload = {"audio_duration": a.duration, "audio_format": p.get("format", "wav"), "batch_size": 1,
                   "thinking": p.get("thinking", True), "prompt": caption or "", "lyrics": lyrics or "[instrumental]",
                   "use_random_seed": False, "seed": s}
        if a.bpm:
            payload["bpm"] = a.bpm
        if a.key:
            payload["key_scale"] = a.key
        if task != "text2music":
            payload["task_type"] = task
            # With the planner on, servers before ACE-Step PR #1287 (2026-08-16) wrote audio codes from the
            # text alone and ignored the source; source tasks run without it (R-005 in musicwright-generate).
            payload.update({"thinking": False, "use_cot_caption": False, "use_cot_language": False})
        if task in BASE_TASKS:
            # DCW forced on turns base-model output into noise (ACE-Step issue #1259; R-20261017-6)
            payload["dcw_enabled"] = False
        if task in ("lego", "extract"):
            payload["track_name"] = a.track
        if task == "complete":
            payload["track_classes"] = [t.strip() for t in a.track.split(",")]
        if a.start is not None:
            payload["repainting_start"] = a.start
        if a.end is not None:
            payload["repainting_end"] = a.end
        if a.strength is not None:
            payload["audio_cover_strength"] = a.strength
        if a.model:
            payload["model"] = a.model
        if a.steps:
            payload["inference_steps"] = a.steps
        elif task in BASE_TASKS:
            payload["inference_steps"] = 50  # base checkpoints are 50-step models; the server default is turbo's 8
        if a.cfg is not None:
            payload["guidance_scale"] = a.cfg
        if a.shift is not None:
            payload["shift"] = a.shift
        if a.set:
            payload.update(json.loads(a.set))
        if a.dry_run:
            takes.append({"seed": s, "payload": payload, **({"upload": {"src_audio": str(a.src)}} if a.src else {})})
            continue
        if a.src:
            resp = http_multipart(host + "/release_task", {"param_obj": json.dumps(payload)}, {"src_audio": a.src}, timeout=900)
        else:
            resp = http(host + "/release_task", payload, timeout=900)
        tid = (resp.get("data") or {}).get("task_id")
        if not tid:
            raise MwError(f"no task_id from ACE-Step: {json.dumps(resp)[:400]}")
        ts = time.time()
        while True:
            if time.time() - ts > a.timeout:
                raise MwError(f"ACE-Step task {tid} timed out after {a.timeout} s")
            time.sleep(4)
            try:
                q = http(host + "/query_result", {"task_id_list": [tid]}, timeout=30)
            except (urllib.error.URLError, OSError):
                continue
            e = (q.get("data") or [{}])[0]
            if e.get("status") == 2:
                raise MwError(f"ACE-Step task failed: {json.dumps(e)[:500]}")
            if e.get("status") == 1:
                res = e.get("result") or "[]"
                res = json.loads(res) if isinstance(res, str) else res
                break
        for item in res:
            fu = item.get("file")
            if not fu:
                continue
            url = fu if fu.startswith("http") else host + fu
            dst = outdir / f"{slug(a.name)}_s{s}.{payload['audio_format']}"
            dst.write_bytes(http_get_bytes(url))
            takes.append({"seed": s, "file": dst, "task_id": tid, "metas": item.get("metas")})
    ignored = [o for o in ("sampler", "scheduler", "planner") if getattr(a, o, None)]
    extra = {"ignored": ignored, "ignored_note": "the REST route has no sampler, scheduler or planner file choice"} if ignored else {}
    if a.dry_run:
        return {"ok": True, "dry_run": True, "host": host, "task": task, "jobs": takes, **extra}
    return {"ok": True, "host": host, "task": task, "params": {**p, **{k: v for k, v in payload.items() if k not in ("prompt", "lyrics", "seed")}},
            "elapsed_s": round(time.time() - t0), "takes": takes, **extra}


REST_TASKS = ("text2music", "cover", "repaint", "lego", "complete", "extract")
BASE_TASKS = ("lego", "complete", "extract")
TRACKS = ("woodwinds", "brass", "fx", "synth", "strings", "percussion",
          "keyboard", "guitar", "bass", "drums", "backing_vocals", "vocals")


def check_task(a, r):
    """Validate --task and its options before anything is created or sent."""
    task = a.task or "text2music"
    if task == "text2music":
        if a.src or a.track:
            raise MwError("--src and --track need --task (cover, repaint, lego, complete or extract)")
        return
    if r["route"] != "rest":
        raise MwError(f"--task {task} runs on the ACE-Step REST server; use --recipe acestep-rest (ComfyUI's native ACE-Step nodes have no source-audio tasks)")
    if not a.src:
        raise MwError(f"--task {task} needs --src, the audio to work from")
    a.src = need_file(a.src)
    if task in ("lego", "extract", "complete"):
        if not a.track:
            raise MwError(f"--task {task} needs --track, one of: {', '.join(TRACKS)}" + (" (comma separated for complete)" if task == "complete" else ""))
        names = [t.strip() for t in a.track.split(",")] if task == "complete" else [a.track]
        bad = [t for t in names if t not in TRACKS]
        if bad:
            raise MwError(f"unknown track {', '.join(bad)}; ACE-Step knows {', '.join(TRACKS)} (a flute is woodwinds)")
    elif a.track:
        raise MwError(f"--track is for lego, extract and complete, not {task}")
    if a.duration is None:
        a.duration = probe(a.src)["duration_s"]


def cmd_gen(a):
    rs = recipes()
    if a.recipe not in rs:
        raise MwError(f"unknown recipe {a.recipe}; choose from {', '.join(sorted(rs))}")
    r = rs[a.recipe]
    check_task(a, r)
    if a.duration is None:
        a.duration = 120.0
    caption = a.caption
    if a.caption_file:
        caption = Path(a.caption_file).read_text(encoding="utf-8").strip()
    if not caption and a.task != "extract":
        raise MwError("give --caption or --caption-file")
    lyrics = a.lyrics
    if a.lyrics_file:
        lyrics = Path(a.lyrics_file).read_text(encoding="utf-8")
    lyrics = lyrics or sections_to_lyrics(a.sections)
    if a.seeds:
        seeds = [int(s) for s in a.seeds.split(",")]
    else:
        base = int(time.time()) % 90000 + 1000
        seeds = [base + i * 111 for i in range(a.takes)]
    outdir = Path(a.out)
    if not a.dry_run:
        outdir.mkdir(parents=True, exist_ok=True)
    fn = gen_comfy if r["route"] == "comfy" else gen_rest
    res = fn(a, r, seeds, caption, lyrics, outdir)
    if res.get("dry_run") or res.get("queued"):
        return res
    led = find_ledger(outdir) or (outdir / "ledger.jsonl")
    for t in res["takes"]:
        f = Path(t["file"])
        m = measure_file(f)
        t["file"] = str(f.resolve())
        t["measure"] = {k: m[k] for k in ("duration_s", "lufs_i", "true_peak_dbtp", "tail_silence_s", "warnings")}
        append_jsonl(led, {"type": "take", "date": now(), "take": f.stem, "file": t["file"], "route": r["route"],
                           "recipe": a.recipe, "model": r.get("model"), "seed": t["seed"], "caption": caption,
                           "lyrics": lyrics, "duration_s": a.duration, "bpm": a.bpm, "key": a.key,
                           "params": res.get("params"), "host": res.get("host"), "measure": t["measure"],
                           **({"task": a.task, "src": str(Path(a.src).resolve()), "track": a.track} if a.task else {})})
    res["ledger"] = str(led.resolve())
    res["next"] = "mw.py sheet <takes> --out sheets/<name>.png, look at it, then ask the listener and record mw.py verdict"
    return res


# ---------------------------------------------------------------- doctor

def cmd_doctor(a):
    rep = {"ok": True, "musicwright": VERSION, "python": sys.version.split()[0], "platform": sys.platform}
    try:
        v = run([ffmpeg_bin(), "-version"]).stdout.splitlines()[0]
        rep["ffmpeg"] = v
        filters = run([ffmpeg_bin(), "-hide_banner", "-filters"]).stdout
        rep["ffmpeg_filters_missing"] = [f for f in ("ebur128", "loudnorm", "showspectrumpic", "sidechaincompress", "acrossfade") if f not in filters]
    except MwError as e:
        rep["ffmpeg"] = None
        rep["ffmpeg_error"] = str(e)
    try:
        import librosa  # noqa: F401
        rep["librosa"] = librosa.__version__
    except ImportError:
        rep["librosa"] = None
        rep["librosa_hint"] = "optional, for analyze; uv run --no-project --python 3.12 --with librosa --with soundfile python mw.py analyze ..."
    rep["fluidsynth"] = fluidsynth_bin()
    try:
        rep["soundfont"] = str(soundfont()) if soundfont() else None
    except MwError as e:
        rep["soundfont"] = None
        rep["soundfont_error"] = str(e)
    if not (rep["fluidsynth"] and rep["soundfont"]):
        rep["render_hint"] = "optional, for render: FluidSynth (LGPL) and a General MIDI SoundFont; without them render uses its built-in sketch synth"
    rep["basic_pitch"] = shutil.which("basic-pitch")
    rep["studio"] = str(studio_dir())
    rep["studio_exists"] = studio_dir().exists()
    hosts = []
    music_like = re.compile(r"ace|music|audio|yue|song|diffrhythm", re.I)
    for h in comfy_hosts(a.host):
        e = {"host": h}
        try:
            st = http(h + "/system_stats", timeout=4)
            dev = (st.get("devices") or [{}])[0]
            e.update(up=True, comfyui=(st.get("system") or {}).get("comfyui_version"), device=dev.get("name"),
                     vram_gb=round((dev.get("vram_total") or 0) / 2 ** 30, 1))
            dm = http(h + "/models/diffusion_models", timeout=5)
            e["music_models"] = [m for m in dm if music_like.search(m)]
            q = http(h + "/queue", timeout=5)
            e["queue"] = {"running": len(q.get("queue_running", [])), "pending": len(q.get("queue_pending", []))}
        except (urllib.error.URLError, OSError, ValueError) as ex:
            e.update(up=False, error=type(ex).__name__)
        hosts.append(e)
    rep["comfyui"] = hosts
    rh = rest_host(None)
    try:
        hz = http(rh + "/health", timeout=4)
        rep["acestep_rest"] = {"host": rh, "up": True, "health": hz}
    except (urllib.error.URLError, OSError, ValueError) as ex:
        rep["acestep_rest"] = {"host": rh, "up": False, "error": type(ex).__name__}
    have = {m for h in hosts for m in h.get("music_models", [])}
    rep["recipes_runnable"] = [k for k, r in recipes().items()
                               if (r["route"] == "comfy" and r["params"]["unet"] in have) or (r["route"] == "rest" and rep["acestep_rest"]["up"])]
    return rep


# ---------------------------------------------------------------- argparse

def build_parser():
    ap = argparse.ArgumentParser(prog="mw.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("doctor", help="what is installed and reachable")
    s.add_argument("--host", help="ComfyUI hosts, comma separated (default MUSICWRIGHT_COMFYUI or studio config)")
    s.set_defaults(fn=cmd_doctor)

    s = sub.add_parser("new", help="scaffold a music project folder")
    s.add_argument("dir")
    s.add_argument("--name", required=True)
    s.add_argument("--use", required=True, choices=["game-loop", "game-cue", "film-cue", "listening", "song"])
    s.add_argument("--duration", type=float, default=120)
    s.add_argument("--preset", help="loudness preset (default by use)")
    s.set_defaults(fn=cmd_new)

    s = sub.add_parser("gen", help="render takes")
    s.add_argument("--recipe", default="acestep-xl-sft", help="see references/recipes.json")
    s.add_argument("--caption", help="what it sounds like: genre, instruments, mood, production")
    s.add_argument("--caption-file")
    s.add_argument("--lyrics", help="lyrics or section tags; default [Instrumental]")
    s.add_argument("--lyrics-file")
    s.add_argument("--sections", help="section tags joined by |, e.g. 'Intro - soft flute|Verse - melody|Outro - fade'")
    s.add_argument("--duration", type=float, help="seconds; default 120, or the --src length for source tasks")
    s.add_argument("--bpm", type=int)
    s.add_argument("--key", help="e.g. 'A minor', 'D major'")
    s.add_argument("--seeds", help="comma separated; default random")
    s.add_argument("--takes", type=int, default=3, help="number of seeds when --seeds is not given")
    s.add_argument("--name", default="take")
    s.add_argument("--out", default="takes")
    s.add_argument("--host", help="ComfyUI hosts (comma list) or the REST host")
    s.add_argument("--cfg", type=float)
    s.add_argument("--steps", type=int)
    s.add_argument("--sampler")
    s.add_argument("--scheduler")
    s.add_argument("--shift", type=float)
    s.add_argument("--planner", help="ACE-Step planner LM file (clip_name2)")
    s.add_argument("--set", help="JSON object of recipe param overrides")
    s.add_argument("--task", choices=REST_TASKS, help="REST route: work from --src (cover, repaint; lego, complete, extract need a base model)")
    s.add_argument("--src", help="source audio for --task (uploaded to the server)")
    s.add_argument("--track", help="lego/extract: the part, e.g. woodwinds or percussion; complete: comma list")
    s.add_argument("--start", type=float, help="repaint/lego window start, seconds")
    s.add_argument("--end", type=float, help="repaint/lego window end, seconds (-1 = end)")
    s.add_argument("--strength", type=float, help="cover: how closely to follow the source, 0-1")
    s.add_argument("--model", help="REST route: DiT the server should use, e.g. acestep-v15-base")
    s.add_argument("--timeout", type=int, default=3600)
    s.add_argument("--no-wait", action="store_true")
    s.add_argument("--dry-run", action="store_true", help="print the graph or payload, submit nothing")
    s.set_defaults(fn=cmd_gen)

    s = sub.add_parser("measure", help="loudness, peaks, silences")
    s.add_argument("files", nargs="+")
    s.add_argument("--silence-db", type=float, default=-50.0)
    s.add_argument("--silence-min", type=float, default=0.3)
    s.set_defaults(fn=cmd_measure)

    s = sub.add_parser("sheet", help="spectrogram + waveform contact sheet")
    s.add_argument("files", nargs="+")
    s.add_argument("--out", required=True)
    s.add_argument("--width", type=int, default=1200)
    s.add_argument("--spec-height", type=int, default=240)
    s.add_argument("--wave-height", type=int, default=70)
    s.add_argument("--max-hz", type=int, default=8000)
    s.add_argument("--measure", action="store_true", help="also measure each take")
    s.set_defaults(fn=cmd_sheet)

    s = sub.add_parser("master", help="two-pass loudness normalisation to a preset")
    s.add_argument("input")
    s.add_argument("--preset", default="streaming")
    s.add_argument("--lufs", type=float)
    s.add_argument("--tp", type=float)
    s.add_argument("--lra", type=float, default=11.0)
    s.add_argument("--rate", type=int, default=48000)
    s.add_argument("--out")
    s.set_defaults(fn=cmd_master)

    s = sub.add_parser("edit", help="trim, fade, convert")
    s.add_argument("input")
    s.add_argument("--out", required=True)
    s.add_argument("--start", type=float)
    s.add_argument("--end", type=float)
    s.add_argument("--fade-in", type=float)
    s.add_argument("--fade-out", type=float)
    s.add_argument("--rate", type=int)
    s.set_defaults(fn=cmd_edit)

    s = sub.add_parser("join", help="crossfade movements into one cue")
    s.add_argument("files", nargs="+")
    s.add_argument("--out", required=True)
    s.add_argument("--xfade", type=float, default=2.0)
    s.add_argument("--lengths", help="seconds each part holds before its crossfade, comma separated")
    s.add_argument("--fade-out", type=float)
    s.set_defaults(fn=cmd_join)

    s = sub.add_parser("loop", help="make a seamless loop")
    s.add_argument("input")
    s.add_argument("--out", required=True)
    s.add_argument("--start", type=float)
    s.add_argument("--end", type=float)
    s.add_argument("--bars", type=int, help="loop exactly this many bars (needs --bpm)")
    s.add_argument("--bpm", type=float)
    s.add_argument("--beats-per-bar", type=int, default=4)
    s.add_argument("--xfade", type=float, default=1.5)
    s.add_argument("--rate", type=int, default=48000)
    s.add_argument("--ogg", action="store_true", help="also write an OGG with LOOPSTART/LOOPLENGTH tags")
    s.set_defaults(fn=cmd_loop)

    s = sub.add_parser("seam", help="score a loop seam")
    s.add_argument("files", nargs="+")
    s.set_defaults(fn=cmd_seam)

    s = sub.add_parser("duck", help="duck music under dialogue or a video's sound")
    s.add_argument("music")
    s.add_argument("--under", required=True, help="dialogue audio or a video whose sound keys the duck")
    s.add_argument("--out", required=True)
    s.add_argument("--music-gain", type=float, default=0.0, help="dB applied to the music before ducking")
    s.add_argument("--threshold", type=float, default=0.03)
    s.add_argument("--ratio", type=float, default=4)
    s.add_argument("--attack", type=float, default=40)
    s.add_argument("--release", type=float, default=500)
    s.add_argument("--stem", action="store_true", help="write the ducked music alone (its own length), not the mix")
    s.set_defaults(fn=cmd_duck)

    s = sub.add_parser("mix", help="layer stems with gain, offset and pan into one file")
    s.add_argument("files", nargs="+")
    s.add_argument("--out", required=True)
    s.add_argument("--gains", help="dB per file, comma separated (default 0)")
    s.add_argument("--offsets", help="seconds per file; positive starts it later, negative trims its head")
    s.add_argument("--pans", help="-1 left .. 0 centre .. 1 right, per file")
    s.add_argument("--length", default="longest", help="longest, first, or seconds")
    s.add_argument("--stems", help="also write each aligned, processed layer to this folder")
    s.add_argument("--rate", type=int, default=48000)
    s.add_argument("--no-limit", action="store_true", help="keep the sum even if it peaks above -1 dBFS")
    s.set_defaults(fn=cmd_mix)

    s = sub.add_parser("analyze", help="tempo and key (librosa)")
    s.add_argument("files", nargs="+")
    s.set_defaults(fn=cmd_analyze)

    s = sub.add_parser("pulse", help="is there a beat? onsets, IOI spread, autocorrelation, grid fit (stdlib)")
    s.add_argument("files", nargs="+")
    s.set_defaults(fn=cmd_pulse)

    s = sub.add_parser("answer", help="does a part answer the lead? its level in the lead's rests vs under its notes")
    s.add_argument("part")
    s.add_argument("--lead", required=True)
    s.add_argument("--below", type=float, default=30.0, help="the lead counts as playing within this many dB of its loud frames")
    s.set_defaults(fn=cmd_answer)

    def score_opts(s):
        s.add_argument("--bpm", type=float, help="tempo in quarter notes a minute (overrides the score's)")
        s.add_argument("--program", help="General MIDI instrument for every part: a number 0-127 or a name (flute, guitar, piano)")
        s.add_argument("--transpose", type=int, default=0, help="semitones up (negative for down)")
        s.add_argument("--chords", action="store_true", help="play ABC chord symbols (\"Am\" \"G7\") as a block-chord part")
        s.add_argument("--tuning", help="tab tuning: guitar, dropd, dadgad, openg, bass, bass5, guitar7, ukulele, or pitches low to high (E2,A2,D3,G3,B3,E4)")
        s.add_argument("--tab-step", type=float, help="beats per tab column (default: the usual gap between notes is an eighth note)")
        s.add_argument("--tune", help="which X: tune of a multi-tune ABC file (default the first)")

    s = sub.add_parser("render", help="notation to audio: ABC, ASCII tab, MusicXML or MIDI -> MIDI + WAV/FLAC")
    s.add_argument("score")
    s.add_argument("--out", help="audio file to write (.wav, .flac, .mp3, .ogg)")
    s.add_argument("--midi", help="where to write the MIDI (default beside --out)")
    s.add_argument("--synth", choices=["auto", "fluidsynth", "builtin"], default="auto")
    s.add_argument("--sf2", help="SoundFont for FluidSynth (or MUSICWRIGHT_SOUNDFONT, or soundfont in the studio config.json)")
    s.add_argument("--gain", type=float, default=1.0, help="FluidSynth gain (its default 0.2 renders quietly)")
    s.add_argument("--tail", type=float, default=1.0, help="seconds of silence added after a FluidSynth render for reverb to ring")
    s.add_argument("--check", action="store_true", help="only read the score and report bars, notes and problems")
    score_opts(s)
    s.set_defaults(fn=cmd_render)

    s = sub.add_parser("notate", help="convert between notations: ABC, MusicXML, MIDI, ASCII tab")
    s.add_argument("score")
    s.add_argument("--out", required=True, help=".abc, .musicxml, .mid or .txt (tab)")
    s.add_argument("--to", choices=["abc", "musicxml", "midi", "tab"])
    s.add_argument("--grid", type=int, choices=[2, 4], default=4, help="steps a beat when snapping MIDI or tab to notation (4 = sixteenths)")
    s.add_argument("--max-fret", type=int, default=15)
    score_opts(s)
    s.set_defaults(fn=cmd_notate)

    s = sub.add_parser("transcribe", help="audio to notation: one instrument (librosa pyin) or polyphonic (basic-pitch) -> MIDI, ABC, MusicXML, tab")
    s.add_argument("audio")
    s.add_argument("--out", required=True, help="the MIDI file to write")
    s.add_argument("--to", help="also write these beside it, comma separated: abc,musicxml,tab")
    s.add_argument("--engine", choices=["pyin", "basic-pitch"], default="pyin")
    s.add_argument("--bpm", type=float, help="tempo to notate against (default: estimated)")
    s.add_argument("--meter", help="time signature for the notation, such as 4/4 or 3/4")
    s.add_argument("--lowest", default="C2", help="lowest note to keep, such as E2 for guitar or C4 for flute (narrower is better)")
    s.add_argument("--highest", default="C7", help="highest note to keep, such as A5 for a wooden flute")
    s.add_argument("--gate", type=float, default=35.0, help="drop notes more than this many dB under the recording's loud passages")
    s.add_argument("--program", help="General MIDI instrument for the MIDI (default flute for pyin)")
    s.add_argument("--tuning", help="tuning for --to tab (default guitar)")
    s.add_argument("--grid", type=int, choices=[2, 4], default=4)
    s.set_defaults(fn=cmd_transcribe)

    s = sub.add_parser("verdict", help="record a listener's verdict on a take")
    s.add_argument("take", help="take file or take name")
    s.add_argument("verdict", choices=["keep", "reject", "maybe"])
    s.add_argument("--note")
    s.add_argument("--by", default="listener")
    s.set_defaults(fn=cmd_verdict)

    s = sub.add_parser("ledger", help="list takes, recipes and verdicts")
    s.add_argument("dir", nargs="?", default=".")
    s.set_defaults(fn=cmd_ledger)

    s = sub.add_parser("note", help="append to the studio notes")
    s.add_argument("kind", choices=sorted(NOTE_FILES))
    s.add_argument("text")
    s.add_argument("--source")
    s.set_defaults(fn=cmd_note)
    return ap


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass
    a = build_parser().parse_args(argv)
    try:
        res = a.fn(a)
        out(res)
        return 0 if res.get("ok", True) else 1
    except (MwError, notation.NotationError, OSError, ValueError, KeyError, urllib.error.URLError) as e:
        out({"ok": False, "command": a.cmd, "error": f"{type(e).__name__}: {e}" if not isinstance(e, (MwError, notation.NotationError)) else str(e)})
        return 1


if __name__ == "__main__":
    sys.exit(main())
