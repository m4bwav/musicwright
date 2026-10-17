"""Tests for skills/musicwright/scripts/mw.py (stdlib unittest, Python 3.9+).

Run from the repository root: python tests/test_mw.py
Synthetic audio (sine tones, a click track at a known tempo, a file with trailing silence, a clipped file, a
hard-cut tone, a short video) is made with ffmpeg in a temporary folder and every command is run on it. Tests
that need ffmpeg skip when ffmpeg or ffprobe is not on PATH (set MUSICWRIGHT_REQUIRE_FFMPEG=1 to fail instead,
as CI does). `analyze` checks its soft failure when librosa is missing and runs for real when it is installed
(MUSICWRIGHT_REQUIRE_LIBROSA=1 makes a missing librosa a failure). Nothing touches the network: ComfyUI and
ACE-Step hosts point at an unused localhost port, and `gen` runs only with --dry-run.
"""
import contextlib
import io
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "musicwright", "scripts"))
import mw  # noqa: E402

HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
REQUIRE_FFMPEG = os.environ.get("MUSICWRIGHT_REQUIRE_FFMPEG") == "1"
REQUIRE_LIBROSA = os.environ.get("MUSICWRIGHT_REQUIRE_LIBROSA") == "1"
NEEDS_FFMPEG = unittest.skipUnless(HAVE_FFMPEG or REQUIRE_FFMPEG, "ffmpeg and ffprobe not on PATH (install ffmpeg to run the audio tests)")
RATE = 48000
TMP = None
FX = {}
_saved_env = {}


def unused_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def run(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = mw.main([str(a) for a in argv])
    text = buf.getvalue()
    return code, json.loads(text)


def ff(*args):
    p = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + [str(a) for a in args],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("ffmpeg failed: " + p.stderr[-800:])


def lavfi(src, dst, af=None, extra=()):
    ff("-f", "lavfi", "-i", src, *(["-af", af] if af else []), *extra, "-c:a", "pcm_s16le", dst)
    return str(dst)


def wav_seconds(path):
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def mean_volume(path, start, end, af=""):
    """Mean volume in dB of [start, end) of a file, after an optional filter chain."""
    chain = f"atrim=start={start}:end={end}" + ("," + af if af else "") + ",volumedetect"
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", chain, "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"mean_volume:\s+(-?[\d.]+|-inf) dB", p.stderr)
    return float(m.group(1)) if m and m.group(1) != "-inf" else -200.0


def tags(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format_tags:stream_tags", "-of", "json", str(path)],
                       capture_output=True, text=True)
    d = json.loads(p.stdout or "{}")
    t = dict((d.get("format") or {}).get("tags") or {})
    for st in d.get("streams") or []:
        t.update(st.get("tags") or {})
    return {k.upper(): v for k, v in t.items()}


def setUpModule():
    global TMP
    TMP = Path(tempfile.mkdtemp(prefix="mw_test_"))
    port = unused_port()
    for k, v in {"MUSICWRIGHT_COMFYUI": f"http://127.0.0.1:{port}", "MUSICWRIGHT_ACESTEP": f"http://127.0.0.1:{port}",
                 "MUSICWRIGHT_HOME": str(TMP / "studio"), "MUSICWRIGHT_FFMPEG": None}.items():
        _saved_env[k] = os.environ.get(k)
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    if not HAVE_FFMPEG:
        if REQUIRE_FFMPEG:
            raise RuntimeError("MUSICWRIGHT_REQUIRE_FFMPEG=1 but ffmpeg or ffprobe is not on PATH")
        print("ffmpeg not found: skipping the audio tests (doctor, new, gen --dry-run, verdict, ledger and note still run)", file=sys.stderr)
        return
    a = str(TMP / "audio")
    os.makedirs(a)
    # sine at the default amplitude 1/8 (-18.06 dBFS peak), stereo by duplication
    FX["tone"] = lavfi(f"sine=frequency=440:sample_rate={RATE}:duration=10", f"{a}/tone.wav", extra=("-ac", "2"))
    FX["tone220"] = lavfi(f"sine=frequency=220:sample_rate={RATE}:duration=12", f"{a}/tone220.wav", extra=("-ac", "2"))
    FX["tone330"] = lavfi(f"sine=frequency=330:sample_rate={RATE}:duration=6", f"{a}/tone330.wav", extra=("-ac", "2"))
    FX["tone550"] = lavfi(f"sine=frequency=550:sample_rate={RATE}:duration=6", f"{a}/tone550.wav", extra=("-ac", "2"))
    FX["tone660"] = lavfi(f"sine=frequency=660:sample_rate={RATE}:duration=6", f"{a}/tone660.wav", extra=("-ac", "2"))
    # 120 bpm click track: a 10 ms 1 kHz blip every 0.5 s
    FX["clicks"] = lavfi(f"aevalsrc='if(lt(mod(t,0.5),0.01),0.8*sin(2*PI*1000*t),0)':s={RATE}:d=12", f"{a}/clicks.wav")
    # 4 s of tone then 5 s of digital silence
    FX["tail"] = lavfi(f"sine=frequency=440:sample_rate={RATE}:duration=4", f"{a}/tail.wav", af="apad=pad_dur=5")
    # 12 dB too hot: clipped flat at full scale
    FX["clipped"] = lavfi(f"sine=frequency=440:sample_rate={RATE}:duration=4", f"{a}/clipped.wav", af="volume=12")
    # tone cut where the last sample is near a crest and the first is zero: an audible loop seam
    FX["hardcut"] = lavfi(f"sine=frequency=440:sample_rate={RATE}:duration=3", f"{a}/hardcut.wav", af="atrim=end_sample=96027")
    # duck fixtures: a 220 Hz bed and a 3 kHz key that is loud from 4 s to 8 s only
    FX["bed"] = lavfi(f"sine=frequency=220:sample_rate={RATE}:duration=10", f"{a}/bed.wav", af="volume=2", extra=("-ac", "2"))
    FX["key"] = lavfi(f"aevalsrc='if(between(t,4,8),0.5*sin(2*PI*3000*t),0)':s={RATE}:d=10", f"{a}/key.wav")
    FX["video"] = f"{a}/clip.mp4"
    ff("-f", "lavfi", "-i", "testsrc=size=160x120:rate=10:duration=10", "-i", FX["key"],
       "-c:v", "mpeg4", "-c:a", "aac", "-shortest", FX["video"])


def tearDownModule():
    for k, v in _saved_env.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    if TMP:
        shutil.rmtree(TMP, ignore_errors=True)


class Basics(unittest.TestCase):
    def test_version_matches_plugin_json(self):
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            self.assertEqual(mw.VERSION, json.load(f)["version"])

    def test_doctor_is_ok_with_no_hosts_up(self):
        code, d = run("doctor")
        self.assertEqual(code, 0)
        self.assertTrue(d["ok"])
        self.assertEqual(len(d["comfyui"]), 1)
        self.assertFalse(d["comfyui"][0]["up"])
        self.assertFalse(d["acestep_rest"]["up"])
        self.assertEqual(d["recipes_runnable"], [])
        self.assertEqual(d["studio"], os.environ["MUSICWRIGHT_HOME"])
        if HAVE_FFMPEG:
            self.assertTrue(d["ffmpeg"].startswith("ffmpeg version"))
            self.assertEqual(d["ffmpeg_filters_missing"], [])
        else:
            self.assertIsNone(d["ffmpeg"])
            self.assertIn("not found", d["ffmpeg_error"])

    def test_doctor_host_option_lists_each_host(self):
        p1, p2 = unused_port(), unused_port()
        code, d = run("doctor", "--host", f"http://127.0.0.1:{p1}, http://127.0.0.1:{p2}/")
        self.assertEqual([h["host"] for h in d["comfyui"]], [f"http://127.0.0.1:{p1}", f"http://127.0.0.1:{p2}"])

    def test_hosts_from_studio_config(self):
        home = TMP / "cfgstudio"
        home.mkdir(exist_ok=True)
        (home / "config.json").write_text(json.dumps({"comfyui": ["http://h1:8188/", "http://h2:8000"], "acestep_rest": "http://h3:8001/"}), encoding="utf-8")
        saved = {k: os.environ.pop(k, None) for k in ("MUSICWRIGHT_COMFYUI", "MUSICWRIGHT_ACESTEP")}
        old_home = os.environ["MUSICWRIGHT_HOME"]
        os.environ["MUSICWRIGHT_HOME"] = str(home)
        try:
            self.assertEqual(mw.comfy_hosts(), ["http://h1:8188", "http://h2:8000"])
            self.assertEqual(mw.rest_host(), "http://h3:8001")
            self.assertEqual(mw.comfy_hosts("http://a:1"), ["http://a:1"])
        finally:
            os.environ["MUSICWRIGHT_HOME"] = old_home
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v

    def test_new_scaffolds_and_refuses_twice(self):
        d = TMP / "proj_new"
        code, r = run("new", d, "--name", "Menu theme", "--use", "game-loop", "--duration", "90")
        self.assertEqual(code, 0)
        for sub in ("takes", "out", "sheets"):
            self.assertTrue((d / sub).is_dir())
        self.assertTrue((d / "brief.md").is_file())
        self.assertTrue((d / "ledger.jsonl").is_file())
        man = json.loads((d / "music.json").read_text(encoding="utf-8"))
        self.assertEqual(man["loudness_preset"], "game-music")
        self.assertEqual(man["duration_s"], 90)
        self.assertTrue(man["ai_generated"])
        self.assertIn("game-music", (d / "brief.md").read_text(encoding="utf-8"))
        code, r = run("new", d, "--name", "again", "--use", "song")
        self.assertEqual(code, 1)
        self.assertFalse(r["ok"])
        self.assertIn("already has music.json", r["error"])

    def test_new_default_presets_exist(self):
        presets = mw.presets()
        for use in ("game-loop", "game-cue", "film-cue", "listening", "song"):
            code, r = run("new", TMP / ("proj_" + use), "--name", use, "--use", use)
            self.assertIn(r["manifest"]["loudness_preset"], presets)

    def test_sections_to_lyrics(self):
        self.assertEqual(mw.sections_to_lyrics("Intro - soft flute| Verse |"), "[Intro - soft flute]\n\n[Verse]")
        self.assertIsNone(mw.sections_to_lyrics(None))


class GenDryRun(unittest.TestCase):
    ACE_NODES = {"UNETLoader", "DualCLIPLoader", "VAELoader", "ModelSamplingAuraFlow", "TextEncodeAceStepAudio1.5",
                 "ConditioningZeroOut", "EmptyAceStep1.5LatentAudio", "KSampler", "VAEDecodeAudio", "SaveAudio"}
    MINIMAX_NODES = {"CLIPLoader", "UNETLoader", "VAELoader", "MiniMaxMusic3TextEncode", "EmptyMiniMaxMusic3LatentAudio",
                     "ConditioningZeroOut", "KSampler", "VAEDecodeAudioTiled", "SaveAudio"}

    def gen(self, recipe, *extra):
        return run("gen", "--recipe", recipe, "--caption", "bright flute over soft strings, 90 bpm", "--duration", "60",
                   "--seeds", "11,22", "--name", "dry take", "--out", TMP / "gen_out", "--dry-run", *extra)

    @staticmethod
    def node(graph, cls):
        return next(n for n in graph.values() if n["class_type"] == cls)

    def check_links(self, graph):
        for nid, n in graph.items():
            for k, v in n["inputs"].items():
                if isinstance(v, list):
                    self.assertIn(v[0], graph, f"node {nid} input {k} links to missing node {v[0]}")

    def test_every_recipe_dry_runs(self):
        for name, r in mw.recipes().items():
            with self.subTest(recipe=name):
                code, d = self.gen(name)
                self.assertEqual(code, 0, d)
                self.assertTrue(d["dry_run"])
                self.assertEqual([j["seed"] for j in d["jobs"]], [11, 22])
                if r["route"] == "comfy":
                    self.assertEqual(d["host"], os.environ["MUSICWRIGHT_COMFYUI"])
                    for j in d["jobs"]:
                        g = j["graph"]
                        self.check_links(g)
                        want = self.ACE_NODES if r["graph"] == "acestep15" else self.MINIMAX_NODES
                        self.assertEqual({n["class_type"] for n in g.values()}, want)
                        ks = self.node(g, "KSampler")["inputs"]
                        self.assertEqual(ks["seed"], j["seed"])
                        for k_graph, k_recipe in (("cfg", "cfg"), ("steps", "steps"), ("sampler_name", "sampler"), ("scheduler", "scheduler")):
                            self.assertEqual(ks[k_graph], r["params"][k_recipe])
                        self.assertEqual(self.node(g, "UNETLoader")["inputs"]["unet_name"], r["params"]["unet"])
                        self.assertEqual(self.node(g, "SaveAudio")["inputs"]["filename_prefix"], f"musicwright/dry_take_s{j['seed']}")
                    self.assertEqual(d["params"]["unet"], r["params"]["unet"])
                else:
                    self.assertEqual(d["host"], os.environ["MUSICWRIGHT_ACESTEP"])
                    for j in d["jobs"]:
                        p = j["payload"]
                        self.assertEqual(p["audio_duration"], 60)
                        self.assertEqual(p["seed"], j["seed"])
                        self.assertFalse(p["use_random_seed"])
                        self.assertEqual(p["prompt"], "bright flute over soft strings, 90 bpm")
                        self.assertEqual(p["lyrics"], "[instrumental]")
                        self.assertEqual(p["audio_format"], r["params"].get("format", "wav"))
                        self.assertEqual(p["thinking"], r["params"].get("thinking", True))
                        self.assertNotIn("bpm", p)

    def test_acestep_graph_params_and_overrides(self):
        code, d = self.gen("acestep-xl-sft", "--bpm", "100", "--key", "D minor", "--cfg", "3.5", "--shift", "2.5",
                           "--planner", "planner.safetensors", "--set", '{"steps": 20, "temperature": 0.7}',
                           "--sections", "Intro - flute|Outro")
        g = d["jobs"][0]["graph"]
        te = self.node(g, "TextEncodeAceStepAudio1.5")["inputs"]
        self.assertEqual(te["tags"], "bright flute over soft strings, 90 bpm")
        self.assertEqual(te["lyrics"], "[Intro - flute]\n\n[Outro]")
        self.assertEqual((te["bpm"], te["keyscale"], te["duration"], te["temperature"]), (100, "D minor", 60.0, 0.7))
        self.assertEqual(te["seed"], 11)
        ks = self.node(g, "KSampler")["inputs"]
        self.assertEqual((ks["cfg"], ks["steps"]), (3.5, 20))
        self.assertEqual(self.node(g, "ModelSamplingAuraFlow")["inputs"]["shift"], 2.5)
        self.assertEqual(self.node(g, "DualCLIPLoader")["inputs"]["clip_name2"], "planner.safetensors")
        self.assertEqual(self.node(g, "EmptyAceStep1.5LatentAudio")["inputs"]["seconds"], 60.0)
        self.assertEqual(d["params"]["cfg"], 3.5)

    def test_instrumental_default_and_files(self):
        cap = TMP / "caption.txt"
        cap.write_text("  calm harp\n", encoding="utf-8")
        lyr = TMP / "lyrics.txt"
        lyr.write_text("[Verse]\nla la\n", encoding="utf-8")
        code, d = run("gen", "--recipe", "acestep-xl-sft", "--caption-file", cap, "--lyrics-file", lyr, "--seeds", "5",
                      "--out", TMP / "gen_out", "--dry-run")
        te = self.node(d["jobs"][0]["graph"], "TextEncodeAceStepAudio1.5")["inputs"]
        self.assertEqual((te["tags"], te["lyrics"]), ("calm harp", "[Verse]\nla la\n"))
        code, d = run("gen", "--caption", "x", "--seeds", "5", "--out", TMP / "gen_out", "--dry-run")
        self.assertEqual(self.node(d["jobs"][0]["graph"], "TextEncodeAceStepAudio1.5")["inputs"]["lyrics"], "[Instrumental]")

    def test_minimax_duration_pad_and_cap(self):
        code, d = self.gen("minimax-music3")
        te = self.node(d["jobs"][0]["graph"], "MiniMaxMusic3TextEncode")["inputs"]
        self.assertAlmostEqual(te["max_duration"], 72.0)
        self.assertEqual(te["lyrics"], "[instrumental]")
        code, d = run("gen", "--recipe", "minimax-music3", "--caption", "x", "--duration", "600", "--seeds", "1",
                      "--out", TMP / "gen_out", "--dry-run")
        self.assertEqual(self.node(d["jobs"][0]["graph"], "MiniMaxMusic3TextEncode")["inputs"]["max_duration"], 340.0)

    def test_rest_payload_options(self):
        code, d = self.gen("acestep-rest", "--bpm", "128", "--key", "A minor", "--lyrics", "[Chorus]\nhey")
        p = d["jobs"][0]["payload"]
        self.assertEqual((p["bpm"], p["key_scale"], p["lyrics"]), (128, "A minor", "[Chorus]\nhey"))

    def test_takes_count_without_seeds(self):
        code, d = run("gen", "--caption", "x", "--takes", "4", "--out", TMP / "gen_out", "--dry-run")
        seeds = [j["seed"] for j in d["jobs"]]
        self.assertEqual(len(set(seeds)), 4)

    def test_errors_fail_soft(self):
        code, d = run("gen", "--recipe", "nope", "--caption", "x", "--out", TMP / "gen_out", "--dry-run")
        self.assertEqual(code, 1)
        self.assertIn("unknown recipe", d["error"])
        code, d = run("gen", "--out", TMP / "gen_out", "--dry-run")
        self.assertIn("--caption", d["error"])

    def test_real_gen_with_no_host_fails_soft(self):
        code, d = run("gen", "--caption", "x", "--seeds", "1", "--out", TMP / "gen_out", "--timeout", "5")
        self.assertEqual(code, 1)
        self.assertIn("no ComfyUI host", d["error"])
        code, d = run("gen", "--recipe", "acestep-rest", "--caption", "x", "--seeds", "1", "--out", TMP / "gen_out")
        self.assertEqual(code, 1)
        self.assertIn("no ACE-Step REST server", d["error"])


class Studio(unittest.TestCase):
    def setUp(self):
        self.home = TMP / ("studio_" + self._testMethodName)
        self.old = os.environ["MUSICWRIGHT_HOME"]
        os.environ["MUSICWRIGHT_HOME"] = str(self.home)

    def tearDown(self):
        os.environ["MUSICWRIGHT_HOME"] = self.old

    def test_verdict_ledger_and_studio(self):
        d = TMP / "proj_ledger"
        run("new", d, "--name", "Boss", "--use", "game-cue")
        takes = d / "takes"
        a, b = takes / "boss_s11.wav", takes / "boss_s22.wav"
        for f in (a, b):
            f.write_bytes(b"RIFF")
        for f, seed in ((a, 11), (b, 22)):
            mw.append_jsonl(d / "ledger.jsonl", {"type": "take", "date": mw.now(), "take": f.stem, "file": str(f.resolve()),
                                                 "route": "comfy", "recipe": "acestep-xl-sft", "model": "m", "seed": seed,
                                                 "caption": "dark brass", "lyrics": None, "duration_s": 60, "params": {"cfg": 4.5}})
        code, v = run("verdict", a, "keep", "--note", "the horn line works", "--by", "tester")
        self.assertEqual(code, 0)
        self.assertTrue(v["matched_take"])
        self.assertEqual(Path(v["ledger"]).resolve(), (d / "ledger.jsonl").resolve())
        self.assertEqual(v["recorded"]["take"], "boss_s11")
        self.assertEqual(v["recorded"]["by"], "tester")
        st = mw.read_jsonl(self.home / "verdicts.jsonl")
        self.assertEqual(len(st), 1)
        self.assertEqual(st[0]["recipe"]["seed"], 11)
        self.assertEqual(st[0]["recipe"]["caption"], "dark brass")
        code, led = run("ledger", d)
        self.assertEqual(code, 0)
        self.assertEqual([t["take"] for t in led["takes"]], ["boss_s11", "boss_s22"])
        self.assertEqual(led["takes"][0]["verdicts"][0]["verdict"], "keep")
        self.assertEqual(led["unjudged"], ["boss_s22"])
        code, led = run("ledger", takes)  # found from a subfolder
        self.assertEqual(code, 0)
        self.assertEqual(led["unjudged"], ["boss_s22"])

    def test_verdict_on_unknown_take_still_records(self):
        d = TMP / "proj_unknown"
        run("new", d, "--name", "x", "--use", "song")
        code, v = run("verdict", d / "takes" / "loose.wav", "reject")
        self.assertEqual(code, 0)
        self.assertFalse(v["matched_take"])
        self.assertEqual(v["recorded"]["take"], "loose.wav")
        self.assertEqual(len(mw.read_jsonl(d / "ledger.jsonl")), 1)

    def test_ledger_missing(self):
        empty = TMP / "no_ledger_here"
        empty.mkdir(exist_ok=True)
        code, d = run("ledger", empty)
        if code == 1:  # a ledger above the temp folder would be found instead; only check the soft failure shape
            self.assertIn("no ledger.jsonl", d["error"])

    def test_note_appends(self):
        code, n = run("note", "taste", "likes bright flute leads", "--source", "verdict 2026-10-17")
        self.assertEqual(code, 0)
        run("note", "taste", "rejects drones")
        text = (self.home / "taste.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Taste notes"))
        self.assertIn("likes bright flute leads (source: verdict 2026-10-17)", text)
        self.assertIn("rejects drones", text)
        self.assertEqual(text.count("\n- "), 2)
        for kind, fname in mw.NOTE_FILES.items():
            run("note", kind, "x")
            self.assertTrue((self.home / fname).is_file())


@NEEDS_FFMPEG
class Measure(unittest.TestCase):
    def test_tone_levels(self):
        code, d = run("measure", FX["tone"])
        self.assertEqual(code, 0)
        m = d["files"][0]
        self.assertAlmostEqual(m["duration_s"], 10.0, delta=0.01)
        self.assertEqual((m["sample_rate"], m["channels"]), (RATE, 2))
        self.assertTrue(-30 < m["lufs_i"] < -15, m["lufs_i"])
        self.assertAlmostEqual(m["sample_peak_db"], -21.07, delta=0.3)
        self.assertAlmostEqual(m["true_peak_dbtp"], m["sample_peak_db"], delta=0.3)
        self.assertEqual((m["head_silence_s"], m["tail_silence_s"]), (0.0, 0.0))
        self.assertEqual(m["warnings"], [])

    def test_tail_silence_warns(self):
        m = run("measure", FX["tail"])[1]["files"][0]
        self.assertAlmostEqual(m["tail_silence_s"], 5.0, delta=0.1)
        self.assertTrue(any("silence at the end" in w for w in m["warnings"]), m["warnings"])

    def test_clipping_warns(self):
        m = run("measure", FX["clipped"])[1]["files"][0]
        self.assertGreater(m["sample_peak_db"], -0.1)
        self.assertTrue(any("clipping likely" in w for w in m["warnings"]), m["warnings"])
        self.assertTrue(any("true peak" in w for w in m["warnings"]), m["warnings"])

    def test_several_files_and_missing_file(self):
        code, d = run("measure", FX["tone"], FX["clicks"])
        self.assertEqual(len(d["files"]), 2)
        code, d = run("measure", TMP / "nope.wav")
        self.assertEqual(code, 1)
        self.assertIn("no such file", d["error"])

    def test_ffmpeg_env_override_finds_ffprobe_beside_it(self):
        os.environ["MUSICWRIGHT_FFMPEG"] = shutil.which("ffmpeg")
        try:
            probe = Path(mw.ffmpeg_bin("ffprobe"))
            self.assertTrue(probe.name.lower().startswith("ffprobe"))
            self.assertEqual(run("measure", FX["tone"])[0], 0)
        finally:
            os.environ.pop("MUSICWRIGHT_FFMPEG", None)


@NEEDS_FFMPEG
class Sheet(unittest.TestCase):
    def test_sheet_png(self):
        dst = TMP / "sheets" / "two.png"
        code, d = run("sheet", FX["tone"], FX["clicks"], "--out", dst, "--width", "400", "--measure")
        self.assertEqual(code, 0, d)
        self.assertTrue(dst.is_file())
        data = dst.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertGreater(len(data), 1000)
        w, h = int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
        self.assertEqual((w, h), (400, 2 * (240 + 70)))
        self.assertEqual(d["rows"], ["tone.wav", "clicks.wav"])
        self.assertEqual(len(d["measure"]), 2)


@NEEDS_FFMPEG
class Master(unittest.TestCase):
    def test_master_to_presets(self):
        for preset in ("game-music", "streaming"):
            with self.subTest(preset=preset):
                dst = TMP / f"master_{preset}.wav"
                code, d = run("master", FX["tone"], "--preset", preset, "--out", dst)
                self.assertEqual(code, 0, d)
                target = mw.presets()[preset]["lufs"]
                self.assertEqual(d["target"]["lufs"], target)
                self.assertLessEqual(abs(d["after"]["lufs_i"] - target), 1.0, d["after"])
                self.assertLessEqual(abs(run("measure", dst)[1]["files"][0]["lufs_i"] - target), 1.0)
                self.assertEqual(d["after"]["sample_rate"], 48000)

    def test_master_overrides_and_default_name(self):
        code, d = run("master", FX["tone220"], "--preset", "web-video", "--lufs", "-20", "--tp", "-2", "--rate", "44100")
        self.assertEqual(code, 0, d)
        self.assertTrue(d["out"].endswith("tone220_web-video.wav"))
        self.assertLessEqual(abs(d["after"]["lufs_i"] + 20), 1.0)
        self.assertEqual(d["after"]["sample_rate"], 44100)
        os.remove(d["out"])

    def test_unknown_preset(self):
        code, d = run("master", FX["tone"], "--preset", "loud")
        self.assertEqual(code, 1)
        self.assertIn("unknown preset", d["error"])


@NEEDS_FFMPEG
class Edit(unittest.TestCase):
    def test_trim_fade_and_formats(self):
        for ext, codec in ((".wav", "pcm_s24le"), (".flac", "flac"), (".ogg", "vorbis"), (".mp3", "mp3")):
            with self.subTest(ext=ext):
                dst = TMP / f"edit{ext}"
                code, d = run("edit", FX["tone"], "--out", dst, "--start", "1", "--end", "4", "--fade-in", "0.5", "--fade-out", "1")
                self.assertEqual(code, 0, d)
                self.assertEqual(d["length_s"], 3.0)
                self.assertEqual(d["codec"], codec)
                self.assertAlmostEqual(d["duration_s"], 3.0, delta=0.06)

    def test_fades_are_applied(self):
        dst = TMP / "edit_fade.wav"
        run("edit", FX["tone"], "--out", dst, "--fade-in", "2", "--fade-out", "2")
        self.assertLess(mean_volume(dst, 0, 0.3), mean_volume(dst, 4, 6) - 10)
        self.assertLess(mean_volume(dst, 9.7, 10), mean_volume(dst, 4, 6) - 10)

    def test_rate_and_bad_range(self):
        dst = TMP / "edit_rate.wav"
        code, d = run("edit", FX["tone"], "--out", dst, "--rate", "22050")
        self.assertEqual(d["sample_rate"], 22050)
        code, d = run("edit", FX["tone"], "--out", dst, "--start", "5", "--end", "2")
        self.assertEqual(code, 1)
        self.assertIn("end must be after start", d["error"])


@NEEDS_FFMPEG
class Join(unittest.TestCase):
    def test_join_with_lengths(self):
        # each part keeps length + xfade (the last only its length); each crossfade overlaps xfade,
        # so the cue lasts sum(lengths) and crossfade i starts at the sum of the first i lengths
        dst = TMP / "join_lengths.wav"
        code, d = run("join", FX["tone330"], FX["tone550"], FX["tone660"], "--out", dst, "--xfade", "1", "--lengths", "3,2.5,2")
        self.assertEqual(code, 0, d)
        self.assertAlmostEqual(d["duration_s"], 7.5, delta=0.01)
        self.assertEqual(d["crossfade_centres_s"], [3.0, 5.5])

    def test_join_whole_files_and_fade_out(self):
        dst = TMP / "join_whole.flac"
        code, d = run("join", FX["tone330"], FX["tone550"], "--out", dst, "--xfade", "2", "--fade-out", "1.5")
        self.assertEqual(code, 0, d)
        self.assertAlmostEqual(d["duration_s"], 6 + 6 - 2, delta=0.01)
        self.assertEqual(d["crossfade_centres_s"], [])
        self.assertLess(mean_volume(dst, 9.8, 10), mean_volume(dst, 7, 8) - 10)

    def test_join_errors(self):
        code, d = run("join", FX["tone330"], "--out", TMP / "j.wav")
        self.assertIn("two or more", d["error"])
        code, d = run("join", FX["tone330"], FX["tone550"], "--out", TMP / "j.wav", "--lengths", "3")
        self.assertIn("one value per file", d["error"])


@NEEDS_FFMPEG
class Loop(unittest.TestCase):
    def test_bar_exact_loop_with_clean_seam_and_ogg_tags(self):
        dst = TMP / "loop_bars.wav"
        code, d = run("loop", FX["tone220"], "--out", dst, "--bars", "4", "--bpm", "120", "--ogg")
        self.assertEqual(code, 0, d)
        want = 4 * 4 * 60 / 120
        self.assertEqual(d["loop_length_s"], want)
        self.assertLess(abs(wav_seconds(dst) - want), 0.001)
        self.assertEqual(d["seam"]["verdict"], "clean")
        self.assertEqual((d["bars"], d["bpm"]), (4, 120.0))
        t = tags(d["ogg"])
        self.assertEqual(t.get("LOOPSTART"), "0")
        self.assertEqual(t.get("LOOPLENGTH"), str(int(want * 48000)))

    def test_three_four_and_offset_start(self):
        dst = TMP / "loop_34.wav"
        code, d = run("loop", FX["clicks"], "--out", dst, "--bars", "2", "--bpm", "90", "--beats-per-bar", "3",
                      "--start", "0.5", "--xfade", "0.5", "--rate", "44100")
        self.assertEqual(code, 0, d)
        want = 2 * 3 * 60 / 90
        self.assertLess(abs(wav_seconds(dst) - want), 0.001)
        self.assertEqual(d["source_window_s"], [0.5, round(0.5 + want + 0.5, 3)])

    def test_ogg_output_with_ogg_flag_tags_the_same_file(self):
        dst = TMP / "loop_direct.ogg"
        code, d = run("loop", FX["tone220"], "--out", dst, "--bars", "2", "--bpm", "120", "--ogg")
        self.assertEqual(code, 0, d)
        self.assertEqual(Path(d["ogg"]).resolve(), dst.resolve())
        t = tags(dst)
        self.assertEqual(t.get("LOOPLENGTH"), str(4 * 48000))
        self.assertAlmostEqual(run("measure", dst)[1]["files"][0]["duration_s"], 4.0, delta=0.01)

    def test_window_loop_and_errors(self):
        dst = TMP / "loop_window.wav"
        code, d = run("loop", FX["tone220"], "--out", dst, "--start", "1", "--end", "7", "--xfade", "1")
        self.assertEqual(code, 0, d)
        self.assertLess(abs(wav_seconds(dst) - 5.0), 0.001)
        code, d = run("loop", FX["tone220"], "--out", dst, "--bars", "4")
        self.assertIn("--bars needs --bpm", d["error"])
        code, d = run("loop", FX["tone220"], "--out", dst, "--bars", "16", "--bpm", "60")
        self.assertIn("of source but the file is", d["error"])
        code, d = run("loop", FX["tone220"], "--out", dst, "--end", "2", "--xfade", "1.5")
        self.assertIn("longer than the crossfade", d["error"])


@NEEDS_FFMPEG
class Seam(unittest.TestCase):
    def test_hard_cut_scores_high_and_crossfaded_loop_low(self):
        lp = TMP / "seam_loop.wav"
        run("loop", FX["tone220"], "--out", lp, "--bars", "2", "--bpm", "100")
        code, d = run("seam", FX["hardcut"], lp)
        self.assertEqual(code, 0, d)
        hard, soft = d["files"]
        self.assertGreater(hard["ratio"], 5)
        self.assertEqual(hard["verdict"], "audible seam likely")
        self.assertLessEqual(soft["ratio"], 2)
        self.assertEqual(soft["verdict"], "clean")
        self.assertGreater(hard["ratio"], 4 * max(soft["ratio"], 0.5))

    def test_seam_converts_other_formats(self):
        fl = TMP / "seam_hard.flac"
        ff("-i", FX["hardcut"], "-c:a", "flac", fl)
        code, d = run("seam", fl)
        self.assertEqual(code, 0, d)
        self.assertEqual(d["files"][0]["verdict"], "audible seam likely")


@NEEDS_FFMPEG
class Duck(unittest.TestCase):
    def test_music_drops_under_the_key(self):
        dst = TMP / "ducked.wav"
        code, d = run("duck", FX["bed"], "--under", FX["key"], "--out", dst)
        self.assertEqual(code, 0, d)
        self.assertTrue(dst.is_file())
        self.assertFalse(d["remuxed_video"])
        low = "lowpass=f=500,lowpass=f=500,lowpass=f=500"  # keep the 220 Hz music, drop the 3 kHz key
        free = mean_volume(dst, 1, 3, low)
        ducked = mean_volume(dst, 5, 7, low)
        self.assertLess(ducked, free - 3, (free, ducked))
        self.assertGreater(mean_volume(dst, 5, 7, "highpass=f=2000,highpass=f=2000"), -40)  # the key is still there

    def test_video_is_remuxed(self):
        dst = TMP / "ducked.mp4"
        code, d = run("duck", FX["bed"], "--under", FX["video"], "--out", dst, "--music-gain", "-6")
        self.assertEqual(code, 0, d)
        self.assertTrue(d["remuxed_video"])
        self.assertEqual(d["settings"]["music_gain_db"], -6)
        p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "json", str(dst)],
                           capture_output=True, text=True)
        kinds = sorted(s["codec_type"] for s in json.loads(p.stdout)["streams"])
        self.assertEqual(kinds, ["audio", "video"])


class FakeHost:
    """A localhost stand-in for ComfyUI and the ACE-Step REST server, serving one WAV for every take."""

    def __init__(self, wav_bytes):
        import http.server
        import threading
        host = self
        self.wav = wav_bytes
        self.prompts, self.tasks, self.fail = [], [], False
        unets = sorted({r["params"]["unet"] for r in mw.recipes().values() if r["route"] == "comfy"})

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def send(self, obj=None, raw=None, ctype="application/json"):
                body = raw if raw is not None else json.dumps(obj).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                p = self.path
                if p == "/system_stats":
                    self.send({"system": {"comfyui_version": "test"}, "devices": [{"name": "fake gpu", "vram_total": 16 * 2 ** 30}]})
                elif p == "/models/diffusion_models":
                    self.send(unets + ["some_image_model.safetensors"])
                elif p == "/queue":
                    self.send({"queue_running": [], "queue_pending": [["x"]]})
                elif p.startswith("/history/"):
                    pid = p.rsplit("/", 1)[1]
                    st = {"status_str": "error", "completed": False, "messages": [["execution_error", {"node_id": "8"}]]} if host.fail \
                        else {"status_str": "success", "completed": True}
                    self.send({pid: {"status": st, "outputs": {"10": {"audio": [{"filename": f"{pid}_00001_.wav", "subfolder": "musicwright", "type": "output"}]}}}})
                elif p.startswith("/view") or p.startswith("/v1/audio"):
                    self.send(raw=host.wav, ctype="audio/wav")
                elif p == "/health":
                    self.send({"data": {"status": "ok"}})
                else:
                    self.send_error(404)

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                if self.path == "/prompt":
                    host.prompts.append(body)
                    self.send({"prompt_id": f"p{len(host.prompts)}", "number": len(host.prompts), "node_errors": {}})
                elif self.path == "/release_task":
                    host.tasks.append(body)
                    self.send({"data": {"task_id": f"t{len(host.tasks)}"}})
                elif self.path == "/query_result":
                    res = json.dumps([{"file": "/v1/audio?path=take.wav", "metas": {"bpm": 90}}])
                    self.send({"data": [{"task_id": body["task_id_list"][0], "status": 1, "result": res}]})
                else:
                    self.send_error(404)

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = "http://127.0.0.1:%d" % self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()


@NEEDS_FFMPEG
class GenAgainstFakeHost(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake = FakeHost(Path(FX["tone"]).read_bytes())

    @classmethod
    def tearDownClass(cls):
        cls.fake.close()

    def test_doctor_sees_the_host_and_its_models(self):
        old = os.environ["MUSICWRIGHT_ACESTEP"]
        os.environ["MUSICWRIGHT_ACESTEP"] = self.fake.url
        try:
            code, d = run("doctor", "--host", self.fake.url)
        finally:
            os.environ["MUSICWRIGHT_ACESTEP"] = old
        h = d["comfyui"][0]
        self.assertTrue(h["up"])
        self.assertEqual((h["device"], h["vram_gb"], h["queue"]), ("fake gpu", 16.0, {"running": 0, "pending": 1}))
        self.assertNotIn("some_image_model.safetensors", h["music_models"])
        self.assertTrue(d["acestep_rest"]["up"])
        self.assertEqual(sorted(d["recipes_runnable"]), sorted(mw.recipes()))

    def test_comfy_gen_downloads_measures_and_logs(self):
        d = TMP / "proj_gen"
        run("new", d, "--name", "gen", "--use", "game-loop")
        n0 = len(self.fake.prompts)
        code, r = run("gen", "--caption", "bright flute", "--seeds", "7,8", "--duration", "30", "--name", "flute",
                      "--host", "http://127.0.0.1:%d,%s" % (unused_port(), self.fake.url), "--out", d / "takes")
        self.assertEqual(code, 0, r)
        self.assertEqual(r["host"], self.fake.url)  # the unreachable host is skipped
        self.assertEqual(len(self.fake.prompts) - n0, 2)
        self.assertEqual([Path(t["file"]).name for t in r["takes"]], ["flute_s7.wav", "flute_s8.wav"])
        self.assertAlmostEqual(r["takes"][0]["measure"]["duration_s"], 10.0, delta=0.01)
        self.assertEqual(Path(r["ledger"]).resolve(), (d / "ledger.jsonl").resolve())
        rows = mw.read_jsonl(d / "ledger.jsonl")
        self.assertEqual([(x["take"], x["seed"], x["recipe"]) for x in rows], [("flute_s7", 7, "acestep-xl-sft"), ("flute_s8", 8, "acestep-xl-sft")])
        self.assertEqual(rows[0]["params"]["cfg"], mw.recipes()["acestep-xl-sft"]["params"]["cfg"])
        code, r2 = run("gen", "--caption", "bright flute", "--seeds", "7", "--name", "flute", "--host", self.fake.url, "--out", d / "takes")
        self.assertEqual(Path(r2["takes"][0]["file"]).name, "flute_s7_2.wav")  # never overwrites a take
        code, v = run("verdict", d / "takes" / "flute_s8.wav", "keep")
        self.assertTrue(v["matched_take"])

    def test_no_wait_queues(self):
        code, r = run("gen", "--caption", "x", "--seeds", "3", "--host", self.fake.url, "--out", TMP / "gen_nowait", "--no-wait")
        self.assertEqual(code, 0, r)
        self.assertTrue(r["queued"])
        self.assertTrue(r["jobs"][0]["prompt_id"].startswith("p"))
        self.assertNotIn("--collect", r["next"])

    def test_failed_job_fails_soft(self):
        self.fake.fail = True
        try:
            code, r = run("gen", "--caption", "x", "--seeds", "3", "--host", self.fake.url, "--out", TMP / "gen_fail")
        finally:
            self.fake.fail = False
        self.assertEqual(code, 1)
        self.assertIn("failed", r["error"])

    def test_model_missing_on_host(self):
        from unittest import mock
        rs = json.loads(json.dumps(mw.recipes()))
        rs["acestep-xl-sft"]["params"]["unet"] = "absent_model.safetensors"
        with mock.patch.object(mw, "recipes", return_value=rs):
            code, r = run("gen", "--caption", "x", "--seeds", "3", "--host", self.fake.url, "--out", TMP / "gen_fail")
        self.assertEqual(code, 1)
        self.assertIn("no absent_model.safetensors", r["error"])

    def test_rest_gen(self):
        old = os.environ["MUSICWRIGHT_ACESTEP"]
        os.environ["MUSICWRIGHT_ACESTEP"] = self.fake.url
        try:
            code, r = run("gen", "--recipe", "acestep-rest", "--caption", "quick draft", "--seeds", "9", "--bpm", "100",
                          "--name", "draft", "--out", TMP / "gen_rest")
        finally:
            os.environ["MUSICWRIGHT_ACESTEP"] = old
        self.assertEqual(code, 0, r)
        self.assertEqual(Path(r["takes"][0]["file"]).name, "draft_s9.wav")
        self.assertEqual(r["takes"][0]["metas"], {"bpm": 90})
        sent = self.fake.tasks[-1]
        self.assertEqual((sent["prompt"], sent["seed"], sent["bpm"]), ("quick draft", 9, 100))
        rows = mw.read_jsonl(TMP / "gen_rest" / "ledger.jsonl")
        self.assertEqual(rows[-1]["route"], "rest")


@NEEDS_FFMPEG
class Analyze(unittest.TestCase):
    def test_analyze(self):
        try:
            import librosa  # noqa: F401
            have = True
        except ImportError:
            have = False
        code, d = run("analyze", FX["clicks"])
        if not have:
            if REQUIRE_LIBROSA:
                self.fail("MUSICWRIGHT_REQUIRE_LIBROSA=1 but librosa is not installed")
            self.assertEqual(code, 1)  # a soft failure the agent acts on: one JSON object, exit 1 (references/cli.md)
            self.assertFalse(d["ok"])
            self.assertIn("librosa", d["error"])
            self.assertIn("uv run", d["fix"])
            self.assertIn("--with librosa", d["fix"])
            self.assertIn("clicks.wav", d["fix"])
            self.assertIn("analyze", d["fix"])
            return
        self.assertEqual(code, 0, d)
        self.assertTrue(d["ok"])
        bpm = d["files"][0]["tempo_bpm"]
        self.assertTrue(any(abs(bpm - t) / t < 0.05 for t in (60, 120, 240)), bpm)
        self.assertIn(d["files"][0]["key"].split()[1], ("major", "minor"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
