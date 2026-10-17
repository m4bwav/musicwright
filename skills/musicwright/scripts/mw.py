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
  analyze  tempo and key estimate (needs librosa; prints the uv one-liner when missing)
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
    except (MwError, OSError, ValueError, KeyError, urllib.error.URLError) as e:
        out({"ok": False, "command": a.cmd, "error": f"{type(e).__name__}: {e}" if not isinstance(e, MwError) else str(e)})
        return 1


if __name__ == "__main__":
    sys.exit(main())
