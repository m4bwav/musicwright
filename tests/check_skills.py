"""Structure checks for the musicwright skills (stdlib only, Python 3.8+).

Run from the repository root: python tests/check_skills.py
Exits 1 and prints every problem when a check fails; prints one summary line when all pass.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
HUB_REFS = os.path.join(SKILLS, "musicwright", "references")
COMPANIONS = ["SKILL.md", "RESEARCH.md", "CHANGELOG.md", "LEARNINGS.md", "TESTS.md",
              "MAINTENANCE.md", "evergreen.json", os.path.join("evals", "evals.json")]
MAX_SKILL_LINES = 200          # AGENTS.md: skills stay under 200 lines
MAX_DESCRIPTION = 700          # this repository's budget (the Agent Skills spec allows 1,024)
SKIP_DIRS = {".git", "__pycache__", "dist", "node_modules", ".claude"}
TEXT_EXT = (".md", ".json", ".py", ".yml", ".yaml", ".txt", ".ps1", ".sh")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# Public-safety guards that name nothing private: an absolute path into someone's home folder
# (placeholders such as C:\Users\<you> are allowed) and AI attribution lines.
HOME_PATH = re.compile(r"(?i)\b[a-z]:[\\/]+users[\\/]+(?!<)[a-z0-9._-]+|/home/(?!<)[a-z0-9._-]+/|/Users/(?!<|Shared)[a-z0-9._-]+/")
# The owner's own machine paths, private project folders and the handle anywhere but as the GitHub owner
# in an owner/repo slug or URL (m4bwav/...): not a folder, an email or a machine name.
PRIVATE = re.compile(r"(?i)\b[a-z]:[\\/]+m4bwa\b|[\\/]Claude[\\/]Projects[\\/]|\bm4bwa(?!v/)")
# Machines on a private network (RFC 1918); 127.0.0.1 and localhost are fine.
LAN_IP = re.compile(r"\b(?:192\.168|10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")
ATTRIBUTION = re.compile(r"(?i)co-authored-by:|generated with (claude|chatgpt|copilot)|written by (claude|an ai)")

problems = []


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def walk_files():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for f in fns:
            yield os.path.join(dp, f)


def frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    fields = {}
    for line in text[3:end].strip().splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            v = m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            fields[m.group(1)] = v
    return fields


def check_skills():
    names = sorted(d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d)))
    if not names:
        problems.append("skills/: no skill folders")
    if "musicwright" not in names:
        problems.append("skills/: no hub skill musicwright")
    for name in names:
        d = os.path.join(SKILLS, name)
        if name != "musicwright" and not name.startswith("musicwright-"):
            problems.append(f"skills/{name}: skill folders are musicwright or musicwright-<part>")
        for c in COMPANIONS:
            if not os.path.isfile(os.path.join(d, c)):
                problems.append(f"skills/{name}: missing {c.replace(os.sep, '/')}")
        sk = os.path.join(d, "SKILL.md")
        if os.path.isfile(sk):
            text = open(sk, encoding="utf-8").read()
            fm = frontmatter(text)
            if fm is None:
                problems.append(f"skills/{name}/SKILL.md: no YAML frontmatter")
            else:
                if fm.get("name") != name:
                    problems.append(f"skills/{name}/SKILL.md: frontmatter name {fm.get('name')!r} differs from the folder")
                desc = fm.get("description", "")
                if not desc:
                    problems.append(f"skills/{name}/SKILL.md: empty description")
                elif len(desc) > MAX_DESCRIPTION:
                    problems.append(f"skills/{name}/SKILL.md: description is {len(desc)} characters (budget {MAX_DESCRIPTION})")
            n = text.count("\n") + 1
            if n > MAX_SKILL_LINES:
                problems.append(f"skills/{name}/SKILL.md: {n} lines (budget {MAX_SKILL_LINES})")
        eg = os.path.join(d, "evergreen.json")
        if os.path.isfile(eg):
            try:
                st = json.load(open(eg, encoding="utf-8"))
                if st.get("name") != name:
                    problems.append(f"skills/{name}/evergreen.json: name {st.get('name')!r} differs from the folder")
                for k in ("tier", "last_checked", "next_due", "protocol"):
                    if k not in st:
                        problems.append(f"skills/{name}/evergreen.json: missing {k}")
                if st.get("source"):
                    problems.append(f"skills/{name}/evergreen.json: source must be null in the repository (it is a local path)")
            except ValueError:
                pass  # reported by check_json
    return names


def check_json():
    for f in walk_files():
        if f.endswith(".json"):
            try:
                json.load(open(f, encoding="utf-8"))
            except ValueError as e:
                problems.append(f"{rel(f)}: invalid JSON ({e})")
    manifest = os.path.join(ROOT, ".claude-plugin", "plugin.json")
    try:
        m = json.load(open(manifest, encoding="utf-8"))
        if m.get("name") != "musicwright":
            problems.append(".claude-plugin/plugin.json: name is not musicwright")
        if not re.match(r"^\d+\.\d+\.\d+$", str(m.get("version", ""))):
            problems.append(".claude-plugin/plugin.json: version is not X.Y.Z")
        mw = open(os.path.join(SKILLS, "musicwright", "scripts", "mw.py"), encoding="utf-8").read()
        v = re.search(r'^VERSION = "([^"]+)"', mw, re.M)
        if not v or v.group(1) != m.get("version"):
            problems.append("skills/musicwright/scripts/mw.py: VERSION %s differs from plugin.json %s" % (v and v.group(1), m.get("version")))
    except (OSError, ValueError):
        problems.append(".claude-plugin/plugin.json: missing or unreadable")
    try:
        mk = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
        if not any(p.get("name") == "musicwright" for p in mk.get("plugins", [])):
            problems.append(".claude-plugin/marketplace.json: lists no musicwright plugin")
    except (OSError, ValueError):
        problems.append(".claude-plugin/marketplace.json: missing or unreadable")


def check_data():
    """recipes.json and loudness.json: every recipe says where it came from, every preset has numbers and a note."""
    try:
        rs = json.load(open(os.path.join(HUB_REFS, "recipes.json"), encoding="utf-8"))["recipes"]
        for k, r in rs.items():
            for f in ("route", "model", "params", "source"):
                if not r.get(f):
                    problems.append(f"recipes.json: recipe {k} has no {f}")
            if r.get("route") not in ("comfy", "rest"):
                problems.append(f"recipes.json: recipe {k} route {r.get('route')!r} is not comfy or rest")
            if r.get("route") == "comfy" and r.get("graph") not in ("acestep15", "minimax3"):
                problems.append(f"recipes.json: comfy recipe {k} graph {r.get('graph')!r} is not one mw.py builds")
            if r.get("route") == "comfy" and not (r.get("params") or {}).get("unet"):
                problems.append(f"recipes.json: comfy recipe {k} names no unet (doctor and gen look for it)")
    except (OSError, ValueError, KeyError, AttributeError) as e:
        problems.append(f"skills/musicwright/references/recipes.json: unreadable ({e})")
    try:
        ps = json.load(open(os.path.join(HUB_REFS, "loudness.json"), encoding="utf-8"))["presets"]
        for k, p in ps.items():
            if not isinstance(p.get("lufs"), (int, float)) or not isinstance(p.get("true_peak"), (int, float)):
                problems.append(f"loudness.json: preset {k} needs numeric lufs and true_peak")
            elif not (-40 <= p["lufs"] <= -5 and -10 <= p["true_peak"] <= 0):
                problems.append(f"loudness.json: preset {k} numbers look wrong ({p['lufs']} LUFS, {p['true_peak']} dBTP)")
            if not p.get("note"):
                problems.append(f"loudness.json: preset {k} has no note saying where its numbers came from")
        for k in ("streaming", "game-music", "web-video"):
            if k not in ps:
                problems.append(f"loudness.json: preset {k} is missing (mw.py new defaults to it)")
    except (OSError, ValueError, KeyError, AttributeError) as e:
        problems.append(f"skills/musicwright/references/loudness.json: unreadable ({e})")


def check_links_and_text():
    for f in walk_files():
        if not f.endswith(TEXT_EXT):
            continue
        text = open(f, encoding="utf-8", errors="replace").read()
        if f.endswith(".md"):
            for target in LINK.findall(text):
                if re.match(r"^(https?:|mailto:|#)", target):
                    continue
                path = target.split("#", 1)[0]
                if path and not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), path))):
                    problems.append(f"{rel(f)}: broken relative link {target}")
        if os.path.abspath(f) == os.path.abspath(__file__):
            continue
        m = HOME_PATH.search(text)
        if m:
            problems.append(f"{rel(f)}: absolute home-folder path {m.group(0)!r}; use a placeholder")
        pv = PRIVATE.search(text)
        if pv:
            problems.append(f"{rel(f)}: private name or machine path {pv.group(0)!r}; generalise it")
        ip = LAN_IP.search(text)
        if ip:
            problems.append(f"{rel(f)}: private network address {ip.group(0)!r}; use a placeholder such as <host>")
        a = ATTRIBUTION.search(text)
        if a:
            problems.append(f"{rel(f)}: AI attribution {a.group(0)!r}")


if __name__ == "__main__":
    names = check_skills()
    check_json()
    check_data()
    check_links_and_text()
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print(" - " + p)
        sys.exit(1)
    print(f"ok: {len(names)} skills, companions, manifests, recipes and presets, links and text guards")
