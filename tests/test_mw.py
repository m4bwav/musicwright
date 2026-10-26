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
    # a 2 s loop that starts on a kick (one a second over a steady bed): a smooth seam with a loud first 50 ms
    FX["kickloop"] = lavfi(f"aevalsrc='0.1*sin(2*PI*220*t)+0.8*exp(-mod(t,1)*30)*sin(2*PI*150*mod(t,1))':s={RATE}:d=2",
                           f"{a}/kickloop.wav")
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
            self.assertEqual(mw.comfy_hosts("127.0.0.1:8199, h4:8188/"), ["http://127.0.0.1:8199", "http://h4:8188"])
            self.assertEqual(mw.rest_host("h5:8001"), "http://h5:8001")
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

    def test_new_unknown_preset(self):
        d = TMP / "proj_badpreset"
        code, r = run("new", d, "--name", "x", "--use", "song", "--preset", "loud")
        self.assertEqual(code, 1)
        self.assertIn("unknown preset", r["error"])
        self.assertFalse(d.exists())

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

    def test_comfy_says_what_it_filled_or_ignored(self):
        code, d = run("gen", "--caption", "x", "--seeds", "1", "--out", TMP / "gen_out", "--dry-run")
        self.assertEqual([v.split()[0] for v in d["filled_in"]], ["bpm", "key"])
        code, d = run("gen", "--caption", "x", "--bpm", "120", "--key", "D major", "--seeds", "1", "--out", TMP / "gen_out", "--dry-run")
        self.assertNotIn("filled_in", d)
        code, d = run("gen", "--recipe", "minimax-music3", "--caption", "x", "--bpm", "100", "--seeds", "1",
                      "--out", TMP / "gen_out", "--dry-run")
        self.assertEqual(d["ignored"], ["bpm"])

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

    def test_rest_sends_cfg_steps_and_set_and_names_ignored_options(self):
        code, d = self.gen("acestep-rest", "--cfg", "5", "--steps", "32", "--shift", "2", "--set", '{"use_adg": true}', "--sampler", "euler")
        p = d["jobs"][0]["payload"]
        self.assertEqual((p["guidance_scale"], p["inference_steps"], p["shift"], p["use_adg"]), (5.0, 32, 2.0, True))
        self.assertEqual(d["ignored"], ["sampler"])
        self.assertNotIn("task_type", p)

    def test_source_tasks_dry_run(self):
        src = FX.get("tone220") or __file__  # existence is all the dry run checks without ffmpeg
        if not HAVE_FFMPEG:
            self.skipTest("the source length comes from ffprobe")
        code, d = run("gen", "--recipe", "acestep-rest", "--task", "lego", "--src", src, "--track", "percussion",
                      "--caption", "light tambourine", "--start", "2", "--end", "8", "--seeds", "1", "--out", TMP / "gen_out", "--dry-run")
        self.assertEqual(code, 0, d)
        p = d["jobs"][0]["payload"]
        self.assertEqual((p["task_type"], p["track_name"], p["repainting_start"], p["repainting_end"]), ("lego", "percussion", 2.0, 8.0))
        self.assertEqual((p["thinking"], p["use_cot_caption"], p["inference_steps"], p["audio_duration"]), (False, False, 50, 12.0))
        self.assertIs(p["dcw_enabled"], False)
        self.assertEqual(d["jobs"][0]["upload"]["src_audio"], str(Path(src)))
        code, d = run("gen", "--recipe", "acestep-rest", "--task", "complete", "--src", src, "--track", "drums, bass",
                      "--caption", "x", "--duration", "20", "--seeds", "1", "--out", TMP / "gen_out", "--dry-run")
        p = d["jobs"][0]["payload"]
        self.assertEqual((p["track_classes"], p["audio_duration"]), (["drums", "bass"], 20.0))
        code, d = run("gen", "--recipe", "acestep-rest", "--task", "cover", "--src", src, "--strength", "0.4",
                      "--caption", "x", "--seeds", "1", "--out", TMP / "gen_out", "--dry-run")
        p = d["jobs"][0]["payload"]
        self.assertEqual((p["task_type"], p["audio_cover_strength"], p["inference_steps"] if "inference_steps" in p else None), ("cover", 0.4, None))
        code, d = run("gen", "--recipe", "acestep-rest", "--task", "extract", "--src", src, "--track", "vocals",
                      "--seeds", "1", "--out", TMP / "gen_out", "--dry-run")
        self.assertEqual(code, 0, d)  # extract needs no caption

    def test_source_task_errors(self):
        src = __file__
        cases = [
            (("--task", "lego", "--track", "woodwinds"), "needs --src"),
            (("--task", "lego", "--src", src), "needs --track"),
            (("--task", "lego", "--src", src, "--track", "flute"), "a flute is woodwinds"),
            (("--task", "complete", "--src", src, "--track", "drums,kazoo"), "unknown track kazoo"),
            (("--task", "cover", "--src", src, "--track", "drums"), "--track is for"),
            (("--src", src), "need --task"),
            (("--task", "lego", "--src", TMP / "missing.wav", "--track", "drums"), "missing.wav"),
        ]
        for extra, msg in cases:
            with self.subTest(extra=extra):
                code, d = run("gen", "--recipe", "acestep-rest", "--caption", "x", "--seeds", "1", "--out", TMP / "gen_err", "--dry-run", *extra)
                self.assertEqual(code, 1, d)
                self.assertIn(msg, d["error"])
        code, d = run("gen", "--task", "lego", "--src", src, "--track", "drums", "--caption", "x", "--out", TMP / "gen_err", "--dry-run")
        self.assertIn("REST server", d["error"])  # the default comfy recipe cannot do source tasks
        self.assertFalse((TMP / "gen_err").exists())

    def test_dry_run_creates_no_folder(self):
        code, d = run("gen", "--caption", "x", "--seeds", "1", "--out", TMP / "gen_dry_only", "--dry-run")
        self.assertEqual(code, 0, d)
        self.assertFalse((TMP / "gen_dry_only").exists())

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
        code, v = run("verdict", d / "takes" / "missing.wav", "reject")
        self.assertEqual(code, 1)
        self.assertIn("no such file", v["error"])
        loose = d / "takes" / "loose.wav"
        loose.write_bytes(b"RIFF")
        code, v = run("verdict", loose, "reject")
        self.assertEqual(code, 0)
        self.assertFalse(v["matched_take"])
        self.assertEqual(v["recorded"]["take"], "loose")
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

    def test_master_custom_target_is_named_custom(self):
        code, d = run("master", FX["tone220"], "--lufs", "-20")
        self.assertEqual(code, 0, d)
        self.assertEqual(d["preset"], "custom")
        self.assertTrue(d["out"].endswith("tone220_custom.wav"))
        self.assertIsNone(d["preset_note"])
        os.remove(d["out"])

    def test_dynamic_mode_on_a_steady_tone_does_not_blame_peaks(self):
        dst = TMP / "master_steady.wav"
        code, d = run("master", FX["tone"], "--preset", "streaming", "--out", dst)
        self.assertEqual(code, 0, d)
        self.assertLess(d["before"]["lra"], 1)
        for w in d["warnings"]:
            self.assertNotIn("peaks allow", w)

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

    def test_loop_starting_on_a_hit_is_clean(self):
        code, d = run("seam", FX["kickloop"])
        self.assertEqual(code, 0, d)
        self.assertLess(abs(d["files"][0]["level_jump_db"]), 3, d)
        self.assertEqual(d["files"][0]["verdict"], "clean")

    def test_loop_cut_on_a_kick_over_a_swelling_bed_is_clean(self):
        # 0.1.1 still read this one as "check by ear" at 3.5 dB: the bed swells through the seam
        src = lavfi("aevalsrc='0.25*sin(2*PI*220*t)*(0.7+0.3*sin(2*PI*0.2*t))+0.15*sin(2*PI*329.63*t)"
                    "+0.5*exp(-25*mod(t,0.625))*sin(2*PI*70*t)':s=44100:d=40", TMP / "audio" / "kick_swell.wav", extra=("-ac", "2"))
        code, d = run("loop", src, "--start", "5", "--bars", "12", "--bpm", "96", "--xfade", "1.5", "--out", TMP / "kick_swell_loop.wav")
        self.assertEqual(code, 0, d)
        self.assertLess(abs(d["seam"]["level_jump_db"]), 2, d["seam"])
        self.assertEqual(d["seam"]["verdict"], "clean")

    def test_a_real_level_step_is_still_caught(self):
        step = lavfi(f"aevalsrc='if(lt(t,2),0.1,0.4)*sin(2*PI*220*t)':s={RATE}:d=4", TMP / "audio" / "step.wav")
        code, d = run("seam", step)
        self.assertEqual(code, 0, d)
        self.assertLess(d["files"][0]["level_jump_db"], -10, d)  # quiet head after a loud tail
        self.assertEqual(d["files"][0]["verdict"], "audible seam likely")

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

    def test_short_key_keeps_the_music_length_and_stem_returns_music_alone(self):
        short_key = TMP / "short_key.wav"
        ff("-i", FX["key"], "-af", "atrim=end=6", short_key)  # loud from 4 s, ends at 6 s; the bed lasts 10 s
        code, d = run("duck", FX["bed"], "--under", short_key, "--out", TMP / "duck_long.wav")
        self.assertEqual(code, 0, d)
        self.assertAlmostEqual(d["duration_s"], 10.0, delta=0.05)
        stem = TMP / "duck_stem.wav"
        code, d = run("duck", FX["bed"], "--under", FX["key"], "--out", stem, "--stem")
        self.assertEqual(code, 0, d)
        self.assertIn("alone", d["returns"])
        self.assertLess(mean_volume(stem, 5, 7, "highpass=f=2000,highpass=f=2000"), -60)  # no key in the stem
        self.assertLess(mean_volume(stem, 5, 7), mean_volume(stem, 1, 3) - 3)  # but the music still ducks

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


@NEEDS_FFMPEG
class Mix(unittest.TestCase):
    def test_layers_offsets_gains_and_stems(self):
        dst, sd = TMP / "mix" / "a" / "mix.wav", TMP / "mix" / "stems"
        code, d = run("mix", FX["tone330"], FX["tone550"], "--offsets", "0,4", "--gains", "0,-6", "--out", dst, "--stems", sd)
        self.assertEqual(code, 0, d)
        self.assertAlmostEqual(d["duration_s"], 10.0, delta=0.01)  # 550 Hz starts at 4 s and lasts 6 s
        self.assertAlmostEqual(mw.probe(dst)["duration_s"], 10.0, delta=0.01)
        self.assertEqual([Path(s).name for s in d["stems"]], ["01_tone330.wav", "02_tone550.wav"])
        bp = "bandpass=f=550:width_type=q:w=8,bandpass=f=550:width_type=q:w=8"
        self.assertLess(mean_volume(dst, 1, 3, bp), -45)  # the second layer is silent before its offset
        self.assertGreater(mean_volume(dst, 5, 6, bp), -40)
        a330 = mean_volume(d["stems"][0], 1, 3)
        a550 = mean_volume(d["stems"][1], 5, 6)
        self.assertAlmostEqual(a330 - a550, 6.0, delta=0.3)  # -6 dB gain
        for s in d["stems"]:
            self.assertAlmostEqual(mw.probe(s)["duration_s"], 10.0, delta=0.01)  # stems are aligned to the mix

    def test_pan_length_and_negative_offset(self):
        dst = TMP / "mix_pan.wav"
        code, d = run("mix", FX["tone330"], "--pans", "-1", "--offsets", "-2", "--length", "3", "--out", dst)
        self.assertEqual(code, 0, d)
        self.assertAlmostEqual(d["duration_s"], 3.0, delta=0.01)
        left = mean_volume(dst, 0.5, 2.5, "pan=mono|c0=c0")
        right = mean_volume(dst, 0.5, 2.5, "pan=mono|c0=c1")
        self.assertLess(right, left - 40)
        code, d = run("mix", FX["tone330"], FX["tone"], "--length", "first", "--out", TMP / "mix_first.wav")
        self.assertAlmostEqual(d["duration_s"], 6.0, delta=0.01)

    def test_hot_sum_is_scaled_and_errors_fail_soft(self):
        code, d = run("mix", FX["bed"], FX["bed"], FX["bed"], FX["bed"], "--gains", "6,6,6,6", "--out", TMP / "mix_hot.wav")
        self.assertEqual(code, 0, d)
        self.assertLess(d["scaled_db"], 0)
        self.assertTrue(d["warnings"])
        self.assertLessEqual(d["measure"]["true_peak_dbtp"], -0.5)
        code, d = run("mix", FX["tone"], FX["tone330"], "--gains", "1", "--out", TMP / "x.wav")
        self.assertIn("one value per file", d["error"])
        code, d = run("mix", FX["tone"], "--pans", "2", "--out", TMP / "x.wav")
        self.assertIn("-1 (left)", d["error"])


@NEEDS_FFMPEG
class PulseAndAnswer(unittest.TestCase):
    def test_click_track_is_steady_and_scattered_clicks_are_not(self):
        free = TMP / "audio" / "free_clicks.wav"
        times = [0.3, 0.9, 2.4, 2.7, 4.6, 5.1, 7.3, 7.6, 8.0, 10.2, 11.5, 13.9, 14.3, 16.8, 17.0, 19.4]
        with wave.open(str(free), "wb") as w:  # clicks at irregular times, as a free-time solo would leave them
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            frames = bytearray(2 * RATE * 20)
            for t in times:
                for i in range(int(0.01 * RATE)):
                    v = int(26000 * mw.math.sin(2 * mw.math.pi * 1000 * i / RATE))
                    j = 2 * (int(t * RATE) + i)
                    frames[j:j + 2] = v.to_bytes(2, "little", signed=True)
            w.writeframes(bytes(frames))
        code, d = run("pulse", FX["clicks"], free)
        self.assertEqual(code, 0, d)
        steady, loose = d["files"]
        self.assertEqual(steady["pulse"], "steady", steady)
        self.assertAlmostEqual(steady["tempo_bpm"], 120, delta=2)
        self.assertLess(steady["grid_deviation"], 0.05)
        self.assertLess(steady["ioi_cv"], 0.1)
        self.assertNotEqual(loose["pulse"], "steady", loose)
        self.assertGreater(loose["ioi_cv"], 0.5)
        self.assertGreater(steady["onset_rise_db"], 10)

    def test_swelling_tone_has_no_pulse(self):
        # 0.1.1 called this "steady" at 120 bpm: the envelope's ripple on the rise read as onsets
        swell = lavfi(f"aevalsrc='0.3*sin(2*PI*196*t)*(0.6+0.4*sin(2*PI*0.1*t))':s={RATE}:d=27", TMP / "audio" / "swell.wav")
        code, d = run("pulse", swell)
        self.assertEqual(code, 0, d)
        row = d["files"][0]
        self.assertLess(row["onset_rise_db"], 1, row)
        self.assertEqual(row["pulse"], "none", row)
        self.assertIsNone(row["tempo_bpm"], row)  # no beat, so no tempo beside "none"
        self.assertIsNone(row["grid_deviation"], row)

    def test_answer_tells_a_reply_from_a_double(self):
        a = TMP / "audio"
        lead = lavfi(f"aevalsrc='if(lt(mod(t,2),1),0.5*sin(2*PI*440*t),0)':s={RATE}:d=10", a / "lead.wav")
        reply = lavfi(f"aevalsrc='if(gte(mod(t,2),1),0.5*sin(2*PI*660*t),0)':s={RATE}:d=10", a / "reply.wav")
        double = lavfi(f"aevalsrc='if(lt(mod(t,2),1),0.5*sin(2*PI*660*t),0)':s={RATE}:d=10", a / "double.wav")
        code, d = run("answer", reply, "--lead", lead)
        self.assertEqual(code, 0, d)
        self.assertGreater(d["rests_minus_under_db"], 20)
        self.assertTrue(d["shape"].startswith("answers"), d)
        self.assertAlmostEqual(d["lead_active_share"], 0.5, delta=0.05)
        code, d = run("answer", double, "--lead", lead)
        self.assertLess(d["rests_minus_under_db"], -20)
        self.assertTrue(d["shape"].startswith("doubles"), d)
        code, d = run("answer", FX["tone"], "--lead", TMP / "audio" / "missing.wav")
        self.assertFalse(d["ok"])


def stereo(expr_l, expr_r, name, d=6):
    """A stereo test file from two aevalsrc expressions (left|right)."""
    return lavfi(f"aevalsrc='{expr_l}|{expr_r}':s={RATE}:d={d}", TMP / "audio" / name)


def flag_codes(row):
    return [f["code"] for f in row["flags"]]


@NEEDS_FFMPEG
class MixCheck(unittest.TestCase):
    """mixcheck flags: each has a file that must raise it and one that must not."""

    @classmethod
    def setUpClass(cls):
        s = "sin(2*PI*{}*t)"
        cls.inphase = stereo("0.3*" + s.format(440), "0.3*" + s.format(440), "inphase.wav")
        cls.antiphase = stereo("0.3*" + s.format(440), "-0.3*" + s.format(440), "antiphase.wav")
        cls.lowwide = stereo(f"0.3*{s.format(60)}+0.2*{s.format(1000)}", f"-0.3*{s.format(60)}+0.2*{s.format(1000)}", "lowwide.wav")
        both = lambda e, n: stereo(e, e, n)  # noqa: E731
        cls.flute_drone = both(f"0.3*{s.format(110)}+0.3*{s.format(880)}", "flute_drone.wav")
        cls.flute = both("0.3*" + s.format(880), "flute.wav")
        cls.muddy = both(f"0.12*{s.format(100)}+0.4*{s.format(350)}+0.12*{s.format(1000)}", "muddy.wav")
        cls.muddy_solo = both(f"0.4*{s.format(450)}+0.12*{s.format(1000)}", "muddy_solo.wav")
        cls.bright = both(f"0.1*{s.format(500)}+0.3*{s.format(3000)}", "bright.wav")
        cls.dull = both("0.3*" + s.format(500), "dull.wav")
        cls.bursts = both(f"if(lt(mod(t,1),0.05),0.9,0.03)*{s.format(1000)}", "bursts.wav")
        cls.steady100 = stereo("0.3*" + s.format(1000), "0.3*" + s.format(1000), "steady100.wav", d=100)
        cls.swell100 = stereo(f"0.01*pow(10,t/50)*{s.format(1000)}", f"0.01*pow(10,t/50)*{s.format(1000)}", "swell100.wav", d=100)

    def check(self, *files, lowest=None):
        code, d = run("mixcheck", *files, *(["--lowest", lowest] if lowest else []))
        self.assertEqual(code, 0, d)
        return d["files"]

    def test_mono_loss_and_wide_lows(self):
        inph, anti, low = self.check(self.inphase, self.antiphase, self.lowwide)
        self.assertGreater(inph["stereo"]["correlation"], 0.95)
        self.assertNotIn("MONO-LOSS", flag_codes(inph))
        self.assertLess(anti["stereo"]["correlation"], -0.95)
        self.assertIn("MONO-LOSS", flag_codes(anti))
        self.assertLess(low["stereo"]["low_correlation"], -0.9)
        self.assertIn("LOW-WIDE", flag_codes(low))
        self.assertNotIn("LOW-WIDE", flag_codes(inph))

    def test_below_range_finds_a_drone_under_a_solo(self):
        drone, solo = self.check(self.flute_drone, self.flute, lowest="C4")
        self.assertIn("BELOW-RANGE", flag_codes(drone))
        self.assertGreater(drone["below_lowest"]["level_db"], -15)
        self.assertNotIn("BELOW-RANGE", flag_codes(solo))
        self.assertLess(solo["below_lowest"]["level_db"], -30)
        self.assertNotIn("below_lowest", self.check(self.flute)[0])

    def test_muddy_needs_a_bass_part_and_bright_needs_presence(self):
        mud, solo, bright, dull = self.check(self.muddy, self.muddy_solo, self.bright, self.dull)
        self.assertIn("MUDDY", flag_codes(mud))
        self.assertGreater(solo["lowmid_excess_db"], 3)  # the excess is there, but there is no bass part to muddy
        self.assertNotIn("MUDDY", flag_codes(solo))
        self.assertIn("BRIGHT", flag_codes(bright))
        self.assertNotIn("BRIGHT", flag_codes(dull))

    def test_over_limited_and_flat(self):
        steady, bursts = self.check(self.steady100, self.bursts)
        self.assertLess(steady["plr_db"], 8)
        self.assertIn("OVER-LIMITED", flag_codes(steady))
        self.assertGreater(bursts["plr_db"], 8)
        self.assertNotIn("OVER-LIMITED", flag_codes(bursts))
        self.assertIn("FLAT", flag_codes(steady))
        self.assertLess(steady["contour"]["spread_lu"], 1)
        swell = self.check(self.swell100)[0]
        self.assertNotIn("FLAT", flag_codes(swell))
        self.assertGreater(swell["contour"]["spread_lu"], 10)
        self.assertGreater(swell["contour"]["loudest_10s_at_s"], 80)
        self.assertEqual(len(swell["contour"]["by_tenth_lufs"]), 10)
        self.assertEqual(swell["contour"]["by_tenth_lufs"], sorted(swell["contour"]["by_tenth_lufs"]))

    def test_other_rates_and_part_second_lengths(self):
        a = TMP / "audio"
        r44 = lavfi("sine=frequency=440:sample_rate=44100:duration=6.3", a / "r44.wav", extra=("-ac", "2"))
        r8 = str(a / "r8.flac")
        ff("-f", "lavfi", "-i", "sine=frequency=440:sample_rate=8000:duration=5", "-c:a", "flac", r8)
        for row in self.check(r44, r8):
            self.assertAlmostEqual(row["lufs_i"], -21.0, delta=1.5, msg=row)

    def test_retries_on_the_best_input_abort(self):
        # static ffmpeg 7.0.2 aborts on a part-second 48 kHz stream; simulate it and check the padded retry
        part = lavfi("sine=frequency=440:sample_rate=44100:duration=3.5", TMP / "audio" / "part35.wav", extra=("-ac", "2"))
        real, calls = mw.ffmpeg, []

        def flaky(args, check=True):
            calls.append(args)
            if "-filter_complex" in args and len(calls) == 1:
                return subprocess.CompletedProcess(args, -6, "", "Assertion best_input >= 0 failed at src/fftools/ffmpeg_filter.c:1923")
            return real(args, check)
        for f in (FX["tone"], part):
            want = self.check(f)[0]
            calls.clear()
            mw.ffmpeg = flaky
            try:
                got = self.check(f)[0]
            finally:
                mw.ffmpeg = real
            self.assertEqual(len(calls), 4)  # failed pass, padded copy, measured pass, loudness of the original
            self.assertTrue(any("apad" in " ".join(c) for c in calls))
            # loudness and length come from the original, not the padded copy (0.1.2 read 3.5 s as 4 and lower)
            for k in ("duration_s", "lufs_i", "true_peak_dbtp", "plr_db"):
                self.assertEqual(got[k], want[k], (f, k))
            if f == FX["tone"]:
                self.assertEqual(got, want)
        self.assertAlmostEqual(want["duration_s"], 3.5, delta=0.01)

    def test_compare_reports_both_and_the_gap(self):
        code, d = run("compare", FX["tone"], FX["bed"])
        self.assertEqual(code, 0, d)
        self.assertAlmostEqual(d["take_minus_ref"]["lufs_i"], d["take"]["lufs_i"] - d["ref"]["lufs_i"], delta=0.11)
        self.assertLess(d["take_minus_ref"]["lufs_i"], -4)  # the bed is 6 dB hotter, a little less after K-weighting
        self.assertEqual(set(d["take_minus_ref"]["bands_db"]), {b for b, _, _ in mw.MIX_BANDS})
        code, d = run("compare", FX["tone"], TMP / "audio" / "missing.wav")
        self.assertFalse(d["ok"])


@NEEDS_FFMPEG
class FixesAndPreviews(unittest.TestCase):
    def test_preview_matches_loudness_blind_and_phone(self):
        out = TMP / "previews"
        code, d = run("preview", FX["tone"], FX["bed"], "--out", out, "--lufs", "-20")
        self.assertEqual(code, 0, d)
        levels = [mw.measure_file(p["preview"])["lufs_i"] for p in d["previews"]]
        self.assertAlmostEqual(levels[0], levels[1], delta=0.3)
        self.assertAlmostEqual(levels[0], -20, delta=0.5)
        code, d = run("preview", FX["tone"], FX["bed"], "--out", out / "blind", "--blind", "--seed", "1")
        names = sorted(Path(p["preview"]).name for p in d["previews"])
        self.assertEqual(names, ["take_A.wav", "take_B.wav"])
        self.assertEqual(Path(d["key_file"]).resolve(), (out / "blind_blind_key.json").resolve())  # not in the folder the listener opens
        self.assertEqual(sorted(p.name for p in (out / "blind").iterdir()), ["take_A.wav", "take_B.wav"])
        key = json.loads(Path(d["key_file"]).read_text(encoding="utf-8"))
        self.assertEqual(sorted(Path(v).name for v in key.values()), ["bed.wav", "tone.wav"])
        self.assertNotIn("source_lufs", d["previews"][0])  # nothing in the reply gives the order away
        wide = stereo("0.3*sin(2*PI*440*t)", "0.1*sin(2*PI*660*t)", "pv_wide.wav")
        code, d = run("preview", wide, "--out", out / "phone", "--as", "phone")
        self.assertEqual(code, 0, d)
        p = d["previews"][0]["preview"]
        self.assertLess(mean_volume(p, 1, 5, "pan=mono|c0=c0-c1"), -80)  # mono
        code, d = run("preview", FX["tone"], "--out", out / "quiet", "--as", "quiet", "--lufs", "-20")
        self.assertAlmostEqual(mw.measure_file(d["previews"][0]["preview"])["lufs_i"], -40, delta=0.5)

    def test_monobass_centres_the_lows_and_leaves_the_rest(self):
        # the bass in the left channel only (correlation 0): folded, it sits in both. Pure anti-phase bass would vanish instead
        src = stereo("0.3*sin(2*PI*60*t)+0.2*sin(2*PI*1000*t)", "0.2*sin(2*PI*1000*t)", "mb_src.wav")
        dst = TMP / "mb" / "mono_low.wav"
        code, d = run("monobass", src, "--out", dst)
        self.assertEqual(code, 0, d)
        self.assertLess(d["before"]["low_correlation"], 0.1)
        self.assertGreater(d["after"]["low_correlation"], 0.9)
        bp = "bandpass=f=1000:width_type=q:w=8,bandpass=f=1000:width_type=q:w=8"
        for ch in ("c0", "c1"):  # the 1 kHz part keeps its level in each channel
            self.assertAlmostEqual(mean_volume(dst, 1, 5, f"pan=mono|c0={ch}," + bp), mean_volume(src, 1, 5, f"pan=mono|c0={ch}," + bp), delta=0.3)
        anti = stereo("0.3*sin(2*PI*60*t)+0.2*sin(2*PI*1000*t)", "-0.3*sin(2*PI*60*t)+0.2*sin(2*PI*1000*t)", "mb_anti.wav")
        code, d = run("monobass", anti, "--out", TMP / "mb" / "anti.wav")
        self.assertLess(d["before"]["low_correlation"], -0.9)
        self.assertIsNone(d["after"]["low_correlation"])  # bass in anti-phase cancels in mono; only a faint residue is left

    def test_mix_shelves_and_automation(self):
        hi = lavfi(f"sine=frequency=8000:sample_rate={RATE}:duration=6", TMP / "audio" / "hi8k.wav", extra=("-ac", "2"))
        code, d = run("mix", hi, "--shelves", "-6", "--shelf-hz", "1500", "--out", TMP / "mix_shelf.wav", "--no-limit")
        self.assertEqual(code, 0, d)
        self.assertAlmostEqual(mean_volume(hi, 1, 5) - mean_volume(TMP / "mix_shelf.wav", 1, 5), 6.0, delta=0.5)
        dst = TMP / "mix_auto.wav"
        code, d = run("mix", FX["tone"], "--automate", "1:0=0,4=0,5=-6", "--out", dst, "--no-limit")
        self.assertEqual(code, 0, d)
        self.assertEqual(d["layers"][0]["automation"], [[0.0, 0.0], [4.0, 0.0], [5.0, -6.0]])
        self.assertAlmostEqual(mean_volume(dst, 1, 3) - mean_volume(dst, 6, 9), 6.0, delta=0.3)
        self.assertAlmostEqual(mean_volume(dst, 1, 3), mean_volume(FX["tone"], 1, 3), delta=0.2)
        code, d = run("mix", FX["tone"], "--automate", "2:0=0", "--out", TMP / "x.wav")
        self.assertIn("file number", d["error"])
        code, d = run("mix", FX["tone"], "--automate", "1:zero=0", "--out", TMP / "x.wav")
        self.assertIn("FILE:SECONDS=DB", d["error"])

    def test_master_peak_mode_and_lra_hint(self):
        code, d = run("master", FX["tone"], "--peak", "-6", "--out", TMP / "pre.wav")
        self.assertEqual(code, 0, d)
        self.assertEqual(d["mode"], "peak")
        self.assertAlmostEqual(d["after"]["sample_peak_db"], -6, delta=0.15)
        self.assertAlmostEqual(d["gain_db"], -6 - d["before"]["sample_peak_db"], delta=0.02)
        code, d = run("master", FX["tone"], "--peak", "3", "--out", TMP / "pre2.wav")
        self.assertIn("at or below 0", d["error"])
        code, d = run("master", FX["tone"], "--preset", "game-music", "--out", TMP / "gm.wav")
        self.assertTrue(d["lra_hint"])


ODE = """X:1
T:Steps and a motif
M:4/4
L:1/4
K:D
F F G A | A G F E | D D E F | F3/2 E/ E2 | F F G A | A G F E | D D E F | E3/2 D/ D2 |
"""
# a random walk: leaps everywhere, and a rhythm (in sixteenths) where no four durations in a row come back
WANDER = "\n".join(["X:1", "T:Random walk", "M:4/4", "L:1/16", "K:C", " ".join(
    p + str(d) for p, d in zip("C, a D g' E, c' F b G, d' A, e' B, f C g, a' D, b' E".split(),
                               (3, 1, 5, 2, 7, 1, 4, 6, 2, 3, 8, 1, 5, 3, 2, 6, 4, 1, 7, 2))) + " |]", ""])


class MelodyHints(unittest.TestCase):
    def test_wandering_line_gets_both_hints_and_a_motif_line_none(self):
        good, bad = TMP / "ode.abc", TMP / "wander.abc"
        good.write_text(ODE, encoding="utf-8")
        bad.write_text(WANDER, encoding="utf-8")
        code, d = run("render", good, "--check")
        self.assertEqual(code, 0, d)
        self.assertEqual(d["melody"][0]["hints"], [], d["melody"])
        self.assertGreater(d["melody"][0]["motif_share"], 0.65)
        code, d = run("render", bad, "--check")
        m = d["melody"][0]
        self.assertGreater(m["leap_share"], 0.25, m)
        self.assertLess(m["motif_share"], 0.65, m)
        self.assertEqual(len(m["hints"]), 2, m)

    def test_chords_and_short_lines_are_skipped(self):
        sc = mw.notation.Score()
        t = mw.notation.Track("pad")
        for i in range(16):  # block chords: three notes on every start, enough starts to pass the length check
            t.notes += [mw.notation.Note(i, 1, 60 + k) for k in (0, 4, 7)]
        sc.tracks.append(t)
        self.assertEqual(mw.notation.melody_hints(sc), [])
        t.notes = [mw.notation.Note(i, 1, 60 + i) for i in range(6)]
        self.assertEqual(mw.notation.melody_hints(sc), [])



FIXTURES = Path(__file__).resolve().parent / "fixtures"


def pitches(track):
    return [mw.notation.midi_name(n.pitch) for n in track.notes]


class NotationReaders(unittest.TestCase):
    """notation.py readers and writers: standard library only, no ffmpeg."""

    def test_abc_keys_lengths_repeats_and_chords(self):
        s, kind = mw.notation.load(FIXTURES / "tune.abc", chords=True)
        self.assertEqual(kind, "abc")
        self.assertEqual(s.title, "Fixture tune")
        self.assertEqual(s.tempos, [(0.0, 120.0)])
        self.assertAlmostEqual(s.length_beats(), 24.0)  # A B ending-1, A B ending-2
        mel = s.tracks[0]
        self.assertEqual(pitches(mel)[:4], ["G4", "B4", "D5", "B4"])  # C is middle C; d is an octave up
        self.assertEqual(pitches(mel)[7], "C#5")
        self.assertEqual(pitches(mel)[-2:], ["F#4", "G4"])  # K:G sharpens F
        starts = [round(n.start, 3) for n in mel.notes]
        self.assertEqual(starts[8:10], [8.0, 8.75])  # B>A: dotted then short
        self.assertEqual(starts[20:23], [20.0, 20.333, 20.667])  # (3ABA in one beat
        self.assertEqual(len(s.tracks), 2)  # --chords adds the chord part
        self.assertEqual(s.key, (1, "major"))
        self.assertEqual(s.warnings, [])

    def test_abc_bar_check_accidentals_and_voices(self):
        abc = "X:1\nT:t\nM:3/4\nL:1/4\nK:F\nB ^F F | B2 | F3 |\nV:2\nC, D, E, | F,3 | G,3 |\n"
        s = mw.notation.parse_abc(abc)
        top = pitches(s.tracks[0])
        self.assertEqual(top[:3], ["A#4", "F#4", "F#4"])  # B is flat in F (Bb = A#), ^F lasts to the bar line
        self.assertEqual(top[4], "F4")  # the bar line cancels ^F
        self.assertTrue(any("bar 2 lasts 2" in w for w in s.warnings), s.warnings)  # the 2-beat bar in 3/4
        self.assertEqual(pitches(s.tracks[1])[0], "C3")
        self.assertIn("no Q: tempo", " ".join(s.warnings))
        with self.assertRaises(mw.notation.NotationError):
            mw.notation.parse_abc("just some words")

    def test_tab_tuning_frets_and_step(self):
        s, kind = mw.notation.load(FIXTURES / "riff.txt", bpm=100)
        self.assertEqual(kind, "tab")
        self.assertEqual(s.tuning[-1], 38)  # the low string is labelled D: drop D
        ps = pitches(s.tracks[0])
        self.assertIn("C4", ps)  # D3 string, fret 10 (two digits)
        self.assertEqual(sorted(set(ps)), sorted({"D2", "D3", "G3", "A3", "F3", "C4"}))
        self.assertTrue(any("no rhythm" in w for w in s.warnings))
        s2, _ = mw.notation.load(FIXTURES / "riff.txt", tab_step=0.25)
        self.assertAlmostEqual(s2.tracks[0].notes[2].start - s2.tracks[0].notes[0].start, 4 * 0.25)
        with self.assertRaises(mw.notation.NotationError):
            mw.notation.parse_tuning("E2,A2", 6)

    def test_midi_round_trip(self):
        s, _ = mw.notation.load(FIXTURES / "tune.abc")
        f = Path(tempfile.mkdtemp(prefix="mw_nt_")) / "t.mid"
        mw.notation.write_midi(s, f)
        back = mw.notation.parse_midi(f.read_bytes())
        self.assertEqual(pitches(back.tracks[0]), pitches(s.tracks[0]))
        self.assertAlmostEqual(back.tempos[0][1], 120.0, places=3)
        self.assertEqual(back.meter, (4, 4))
        self.assertEqual(back.key, (1, "major"))
        for a, b in zip(s.tracks[0].notes, back.tracks[0].notes):
            self.assertAlmostEqual(a.start, b.start, places=2)
        shutil.rmtree(f.parent, ignore_errors=True)

    def test_musicxml_and_abc_writers_read_back(self):
        abc = "X:1\nT:w\nM:4/4\nL:1/8\nQ:1/4=90\nK:Bb\nB2 d2 f4 | e2 c2 B4- | B8 |]\n"
        s = mw.notation.parse_abc(abc)
        xml = mw.notation.write_musicxml(s)
        back = mw.notation.parse_musicxml(xml.encode())
        self.assertEqual(pitches(back.tracks[0]), pitches(s.tracks[0]))
        self.assertAlmostEqual(back.tracks[0].notes[-1].dur, 6.0)  # tied across the bar line
        self.assertEqual(back.tempos[0][1], 90.0)
        again = mw.notation.parse_abc(mw.notation.write_abc(s))
        self.assertEqual(pitches(again.tracks[0]), pitches(s.tracks[0]))
        self.assertEqual([n.start for n in again.tracks[0].notes], [n.start for n in s.tracks[0].notes])
        tab, warn = mw.notation.write_tab(s)
        self.assertIn("e|", tab)
        self.assertEqual(warn, [])

    def test_mono_slot_keeps_the_longer_note_and_key_estimate(self):
        sc = mw.notation.score_from_seconds([mw.notation.Note(0.0, 0.05, 62), mw.notation.Note(0.06, 0.6, 64)], 60)
        bars = mw.notation.quantised_stream(sc.tracks[0], 4, 16)
        self.assertEqual(bars[0][0][1], [64])
        notes = [mw.notation.Note(i, 1, p) for i, p in enumerate([57, 60, 64, 57, 62, 65, 57, 64, 69])]
        self.assertEqual(mw.notation.estimate_key(notes), (0, "minor"))  # A minor
        self.assertEqual(mw.notation.program_of("flute"), 73)
        with self.assertRaises(mw.notation.NotationError):
            mw.notation.program_of("kazoo")


@NEEDS_FFMPEG
class NotationCommands(unittest.TestCase):
    def test_render_check_and_builtin_render(self):
        code, d = run("render", FIXTURES / "tune.abc", "--check")
        self.assertEqual(code, 0, d)
        self.assertEqual(d["read_as"], "abc")
        self.assertEqual(d["beats"], 24.0)
        self.assertIn("chord symbols were not played", " ".join(d["warnings"]))
        dst = TMP / "nt" / "tune.wav"
        code, d = run("render", FIXTURES / "tune.abc", "--chords", "--synth", "builtin", "--out", dst)
        self.assertEqual(code, 0, d)
        self.assertEqual(d["synth"], "builtin")
        self.assertTrue(Path(d["midi"]).exists())
        self.assertAlmostEqual(d["measure"]["duration_s"], 12.0 + 1.5, delta=0.1)  # 24 beats at 120 + the release tail
        self.assertGreater(mean_volume(dst, 0.5, 11), -40)

    def test_render_tab_transposed_flac_and_errors(self):
        dst = TMP / "nt" / "riff.flac"
        code, d = run("render", FIXTURES / "riff.txt", "--bpm", "90", "--transpose", "-2", "--synth", "builtin", "--out", dst)
        self.assertEqual(code, 0, d)
        self.assertEqual(d["tracks"][0]["range"][0], "C2")  # D2 down a tone
        self.assertEqual(mw.probe(dst)["codec"], "flac")
        code, d = run("render", FIXTURES / "tune.abc", "--synth", "fluidsynth", "--out", TMP / "nt" / "x.wav")
        if not mw.fluidsynth_bin():
            self.assertFalse(d["ok"])
            self.assertIn("FluidSynth not found", d["error"])
        code, d = run("render", FIXTURES / "tune.abc")
        self.assertIn("--out", d["error"])
        code, d = run("render", FIXTURES / "tune.abc", "--program", "kazoo", "--check")
        self.assertIn("unknown instrument", d["error"])

    def test_notate_formats(self):
        for to, ext, marker in (("abc", ".abc", "K:G"), ("musicxml", ".musicxml", "<score-partwise"), ("tab", ".txt", "e|")):
            dst = TMP / "nt" / ("tune" + ext)
            code, d = run("notate", FIXTURES / "tune.abc", "--out", dst)
            self.assertEqual(code, 0, d)
            self.assertEqual(d["to"], to)
            self.assertIn(marker, Path(dst).read_text(encoding="utf-8"))
        mid = TMP / "nt" / "tune.mid"
        code, d = run("notate", FIXTURES / "tune.abc", "--out", mid)
        self.assertEqual(d["to"], "midi")
        code, d = run("notate", mid, "--bpm", "60", "--out", TMP / "nt" / "slow.abc")
        self.assertEqual(code, 0, d)
        self.assertAlmostEqual(d["beats"], 12.0)  # MIDI keeps its timing: 12 s at 60 bpm is 12 beats
        self.assertIn("snapped to a grid", " ".join(d["warnings"]))
        code, d = run("notate", FIXTURES / "tune.abc", "--out", TMP / "nt" / "x.pdf")
        self.assertFalse(d["ok"])

    def test_transcribe(self):
        a = TMP / "audio"
        seq = lavfi(f"aevalsrc='0.4*sin(2*PI*if(lt(t,0.5),440,if(lt(t,1),493.88,if(lt(t,1.5),523.25,0)))*t)*lt(t,1.5)':s={RATE}:d=2.5",
                    a / "abc_seq.wav")
        try:
            import librosa  # noqa: F401
            have = True
        except ImportError:
            have = False
        code, d = run("transcribe", seq, "--out", TMP / "nt" / "seq.mid", "--to", "abc,musicxml,tab", "--bpm", "120",
                      "--lowest", "C4", "--highest", "C6")
        if not have:
            if REQUIRE_LIBROSA:
                self.fail("MUSICWRIGHT_REQUIRE_LIBROSA=1 but librosa is not installed")
            self.assertFalse(d["ok"])
            self.assertIn("uv run", d["fix"])
            self.assertIn("transcribe", d["fix"])
            return
        self.assertEqual(code, 0, d)
        names = d["tracks"][0]
        self.assertEqual(names["range"], ["A4", "C5"])
        self.assertTrue(all(Path(f).exists() for f in d["files"].values()))
        back = mw.notation.parse_midi(Path(d["files"]["midi"]).read_bytes())
        self.assertEqual([mw.notation.midi_name(n.pitch) for n in back.notes()], ["A4", "B4", "C5"])
        self.assertLess(d["duration_s"], 1.7)  # nothing in the silent tail
        code, d = run("transcribe", seq, "--out", TMP / "nt" / "seq.abc")
        self.assertIn(".mid", d["error"])


@NEEDS_FFMPEG
class OutFolders(unittest.TestCase):
    def test_commands_create_missing_out_folders(self):
        base = TMP / "deep"
        cases = [
            ("master", FX["tone"], "--out", base / "m" / "x.wav"),
            ("edit", FX["tone"], "--end", "2", "--out", base / "e" / "x.wav"),
            ("join", FX["tone330"], FX["tone550"], "--xfade", "1", "--out", base / "j" / "x.wav"),
            ("loop", FX["tone"], "--bars", "2", "--bpm", "120", "--out", base / "l" / "x.wav"),
            ("duck", FX["bed"], "--under", FX["key"], "--out", base / "d" / "x.wav"),
            ("sheet", FX["tone"], "--out", base / "s" / "x.png"),
        ]
        for argv in cases:
            with self.subTest(cmd=argv[0]):
                code, d = run(*argv)
                self.assertEqual(code, 0, d)
                self.assertTrue(Path(argv[-1]).is_file())


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
                raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                ctype = self.headers.get("Content-Type", "")
                if ctype.startswith("multipart/form-data"):
                    import email
                    msg = email.message_from_bytes(b"Content-Type: " + ctype.encode() + b"\r\n\r\n" + raw)
                    body, host.uploads = {}, {}
                    for part in msg.get_payload():
                        name = part.get_param("name", header="content-disposition")
                        if part.get_filename():
                            host.uploads[name] = part.get_payload(decode=True)
                        else:
                            body[name] = part.get_payload(decode=True).decode("utf-8")
                    body = json.loads(body.get("param_obj", "{}"))
                else:
                    body = json.loads(raw or b"{}")
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

    def test_rest_lego_uploads_the_source(self):
        old = os.environ["MUSICWRIGHT_ACESTEP"]
        os.environ["MUSICWRIGHT_ACESTEP"] = self.fake.url
        try:
            code, r = run("gen", "--recipe", "acestep-rest", "--task", "lego", "--src", FX["tone220"], "--track", "woodwinds",
                          "--caption", "second flute", "--seeds", "5", "--model", "acestep-v15-base", "--name", "layer",
                          "--out", TMP / "gen_lego")
        finally:
            os.environ["MUSICWRIGHT_ACESTEP"] = old
        self.assertEqual(code, 0, r)
        self.assertEqual(self.fake.uploads["src_audio"], Path(FX["tone220"]).read_bytes())
        sent = self.fake.tasks[-1]
        self.assertEqual((sent["task_type"], sent["track_name"], sent["model"], sent["thinking"], sent["audio_duration"]),
                         ("lego", "woodwinds", "acestep-v15-base", False, 12.0))
        row = mw.read_jsonl(TMP / "gen_lego" / "ledger.jsonl")[-1]
        self.assertEqual((row["task"], row["track"], Path(row["src"]).name), ("lego", "woodwinds", "tone220.wav"))


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
        self.assertIn("tuning", d["files"][0])
        self.assertIn("share", d["files"][0]["repetition"])


def have_librosa():
    try:
        import librosa  # noqa: F401
        return True
    except ImportError:
        if REQUIRE_LIBROSA:
            raise
        return False


@NEEDS_FFMPEG
@unittest.skipUnless(have_librosa(), "librosa not installed (analyze's soft failure is tested above)")
class AnalyzeMusic(unittest.TestCase):
    """Tuning, repetition and sections on synthetic tones with a known answer (books track 11)."""

    @classmethod
    def setUpClass(cls):
        a = str(TMP / "audio")
        sharp = 440 * 2 ** (30 / 1200)  # 30 cents above A440
        cls.sharp = lavfi(f"sine=frequency={sharp:.3f}:sample_rate=22050:duration=20", f"{a}/sharp.wav")
        cls.mild = lavfi(f"sine=frequency={440 * 2 ** (20 / 1200):.3f}:sample_rate=22050:duration=20", f"{a}/mild.wav")
        cls.wide = lavfi(f"sine=frequency={440 * 2 ** (42 / 1200):.3f}:sample_rate=22050:duration=20", f"{a}/wide.wav")
        cls.drift = lavfi(f"aevalsrc='0.3*sin(2*PI*if(lt(t,50),440,{sharp:.3f})*t)':s=22050:d=100", f"{a}/drift.wav")
        cls.steady = lavfi("aevalsrc='0.3*sin(2*PI*440*t)':s=22050:d=100", f"{a}/steady.wav")
        arp = "0.3*sin(2*PI*220*pow(2,{}/12)*t)"
        # a four-note figure that repeats every 4 s for four minutes, and three minutes that never repeat
        cls.loop = lavfi("aevalsrc='" + arp.format("mod(floor(t),4)*3") + "':s=22050:d=240", f"{a}/loop.wav")
        cls.through = lavfi("aevalsrc='" + arp.format("floor(12*mod(abs(sin(floor(t)*12.9898)*43758.5453),1))") + "':s=22050:d=180",
                            f"{a}/through.wav")
        # A (an arpeggio) 0-15 s, B (a held two-note chord) 15-40 s, A again 40-60 s, over a click every 0.6 s
        cls.aba = lavfi("aevalsrc='if(lt(t,15)+gte(t,40)," + arp.format("mod(floor(t*2),3)*4")
                        + ",0.2*sin(2*PI*370*t)+0.2*sin(2*PI*554*t))+if(lt(mod(t,0.6),0.01),0.6*sin(2*PI*2000*t),0)'"
                        ":s=22050:d=60", f"{a}/aba.wav")

    def codes(self, row):
        return [f["code"] for f in row["flags"]]

    def test_offset_and_gap(self):
        code, d = run("analyze", FX["tone"], self.sharp)
        self.assertEqual(code, 0, d)
        plain, sharp = d["files"]
        self.assertLess(abs(plain["tuning"]["cents"]), 5)
        self.assertAlmostEqual(sharp["tuning"]["cents"], 30, delta=5)
        self.assertNotIn("OFF-A440", self.codes(plain))
        self.assertIn("OFF-A440", self.codes(sharp))
        self.assertAlmostEqual(sharp["cents_from_first"], 30, delta=5)

    def test_gap_flag_over_30_cents(self):
        code, d = run("analyze", FX["tone"], self.mild, self.wide)
        self.assertEqual(code, 0, d)
        _, mild, wide = d["files"]
        self.assertAlmostEqual(mild["cents_from_first"], 20, delta=5)
        self.assertNotIn("TUNING-GAP", self.codes(mild))
        self.assertAlmostEqual(wide["cents_from_first"], 42, delta=5)
        self.assertIn("TUNING-GAP", self.codes(wide))

    def test_drift(self):
        code, d = run("analyze", self.drift, self.steady)
        self.assertEqual(code, 0, d)
        moving, steady = d["files"]
        self.assertAlmostEqual(moving["tuning"]["trend_cents"], 30, delta=6)
        self.assertIn("DRIFT", self.codes(moving))
        self.assertLess(abs(steady["tuning"]["trend_cents"]), 3)
        self.assertNotIn("DRIFT", self.codes(steady))

    def test_repeats(self):
        code, d = run("analyze", self.loop, self.through)
        self.assertEqual(code, 0, d)
        loop, through = d["files"]
        self.assertGreaterEqual(loop["repetition"]["share"], 0.9)
        self.assertNotIn("REPEATS", self.codes(loop))  # reported, not flagged (listening check 2026-10-23)
        self.assertLess(through["repetition"]["share"], 0.5)
        self.assertNotIn("REPEATS", self.codes(through))

    def test_sections(self):
        for arg in ("3", "A|B|A return", None):
            code, d = run("analyze", self.aba, "--sections", *([arg] if arg else []))
            self.assertEqual(code, 0, d)
            secs = d["files"][0]["sections"]
            self.assertEqual(len(secs), 3, (arg, secs))
            self.assertAlmostEqual(secs[1]["start_s"], 15, delta=3)
            self.assertAlmostEqual(secs[2]["start_s"], 40, delta=3)
            self.assertAlmostEqual(secs[-1]["end_s"], 60, delta=0.5)
            self.assertEqual(secs[0]["start_bar"], 1)
            for s in secs[1:]:  # boundaries move to the nearest beat (the clicks)
                self.assertLess(abs(s["start_s"] - round(s["start_s"] / 0.6) * 0.6), 0.07, s)
        self.assertEqual([s["name"] for s in secs], [None, None, None])
        code, d = run("analyze", self.aba, "--sections", "A|B|A return")
        self.assertEqual(d["files"][0]["sections"][2]["name"], "A return")
        code, d = run("analyze", self.aba)
        self.assertNotIn("sections", d["files"][0])


if __name__ == "__main__":
    unittest.main(verbosity=1)
