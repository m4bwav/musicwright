"""Notation for mw.py: read ABC, ASCII tab, MusicXML and MIDI; write MIDI, ABC, MusicXML and tab; a small synth.

Standard-library Python 3.9+. Times are in quarter-note beats; a tempo map turns them into seconds.
The readers cover what people paste and what models write (see musicwright-notation's
references/formats.md for the supported subset); anything outside it is reported as a warning,
never guessed silently.
"""
import math
import re
import struct
import wave
import xml.etree.ElementTree as ET
import zipfile
from fractions import Fraction
from pathlib import Path


class NotationError(Exception):
    pass


# ---------------------------------------------------------------- model

class Note:
    __slots__ = ("start", "dur", "pitch", "vel", "tie")

    def __init__(self, start, dur, pitch, vel=90, tie=False):
        self.start, self.dur, self.pitch, self.vel, self.tie = float(start), float(dur), int(pitch), int(vel), tie

    def end(self):
        return self.start + self.dur


class Track:
    def __init__(self, name="", program=0, drums=False):
        self.name, self.program, self.drums, self.notes = name, program, drums, []


class Score:
    def __init__(self):
        self.title = ""
        self.tracks = []
        self.tempos = [(0.0, 120.0)]  # (beat, bpm)
        self.meter = (4, 4)
        self.key = None  # (fifths, "major"|"minor") when the source says
        self.warnings = []

    def notes(self):
        return [n for t in self.tracks for n in t.notes]

    def length_beats(self):
        return max((n.end() for n in self.notes()), default=0.0)

    def seconds(self, beat):
        """Beat -> seconds through the tempo map."""
        t, prev_b, prev_bpm = 0.0, 0.0, self.tempos[0][1]
        for b, bpm in self.tempos[1:]:
            if b >= beat:
                break
            t += (b - prev_b) * 60.0 / prev_bpm
            prev_b, prev_bpm = b, bpm
        return t + (beat - prev_b) * 60.0 / prev_bpm

    def summary(self):
        ns = self.notes()
        return {"title": self.title, "tracks": [{"name": t.name, "program": t.program, "drums": t.drums, "notes": len(t.notes),
                                                 "range": [midi_name(min(n.pitch for n in t.notes)), midi_name(max(n.pitch for n in t.notes))] if t.notes else None}
                                                for t in self.tracks],
                "notes": len(ns), "beats": round(self.length_beats(), 3), "duration_s": round(self.seconds(self.length_beats()), 3),
                "bpm": self.tempos[0][1], "tempo_changes": len(self.tempos) - 1, "meter": f"{self.meter[0]}/{self.meter[1]}",
                "key": key_name(*self.key) if self.key else None}


NAMES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
LETTER_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
MAJOR_FIFTHS = {"C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6, "C#": 7, "F": -1, "Bb": -2, "Eb": -3,
                "Ab": -4, "Db": -5, "Gb": -6, "Cb": -7}
MODE_SHIFT = {"": 0, "maj": 0, "major": 0, "ion": 0, "m": -3, "min": -3, "minor": -3, "aeo": -3, "dor": -2,
              "phr": -4, "lyd": 1, "mix": -1, "loc": -5}
SHARP_ORDER, FLAT_ORDER = "FCGDAEB", "BEADGCF"


def midi_name(p):
    return f"{NAMES_SHARP[p % 12]}{p // 12 - 1}"


def parse_pitch_name(s):
    """'E2', 'F#3', 'Bb1' -> MIDI number."""
    m = re.fullmatch(r"([A-Ga-g])([#b]?)(-?\d)", s.strip())
    if not m:
        raise NotationError(f"cannot read pitch {s!r} (write it like E2, F#3 or Bb1)")
    pc = LETTER_PC[m.group(1).upper()] + {"#": 1, "b": -1, "": 0}[m.group(2)]
    return 12 * (int(m.group(3)) + 1) + pc


def key_name(fifths, mode):
    order = ["Cb", "Gb", "Db", "Ab", "Eb", "Bb", "F", "C", "G", "D", "A", "E", "B", "F#", "C#"]
    if mode == "minor":
        minors = ["Ab", "Eb", "Bb", "F", "C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
        return minors[fifths + 7] + " minor"
    return order[fifths + 7] + " major"


def key_signature(fifths):
    """letter -> alteration for a key signature."""
    sig = {c: 0 for c in "ABCDEFG"}
    for c in (SHARP_ORDER[:fifths] if fifths > 0 else FLAT_ORDER[:-fifths]):
        sig[c] = 1 if fifths > 0 else -1
    return sig


KS_MAJ = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KS_MIN = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]


def estimate_key(notes):
    """Krumhansl-Schmuckler on duration-weighted pitch classes -> (fifths, mode)."""
    hist = [0.0] * 12
    for n in notes:
        hist[n.pitch % 12] += n.dur
    if not any(hist):
        return (0, "major")

    def corr(a, b):
        ma, mb = sum(a) / 12, sum(b) / 12
        num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
        den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) or 1
        return num / den
    best = max(((corr([prof[(i - k) % 12] for i in range(12)], hist), k, mode)
                for mode, prof in (("major", KS_MAJ), ("minor", KS_MIN)) for k in range(12)))
    _, tonic, mode = best
    rel = tonic if mode == "major" else (tonic + 3) % 12
    fifths = (rel * 7) % 12
    if fifths > 6:
        fifths -= 12
    return (fifths, mode)


GM = {"piano": 0, "bright piano": 1, "electric piano": 4, "harpsichord": 6, "celesta": 8, "glockenspiel": 9,
      "music box": 10, "vibraphone": 11, "marimba": 12, "xylophone": 13, "organ": 19, "church organ": 19,
      "accordion": 21, "harmonica": 22, "nylon guitar": 24, "guitar": 25, "steel guitar": 25, "jazz guitar": 26,
      "clean guitar": 27, "muted guitar": 28, "overdrive guitar": 29, "distortion guitar": 30, "bass": 33,
      "acoustic bass": 32, "fingered bass": 33, "picked bass": 34, "fretless bass": 35, "slap bass": 36,
      "violin": 40, "viola": 41, "cello": 42, "contrabass": 43, "harp": 46, "timpani": 47, "strings": 48,
      "choir": 52, "trumpet": 56, "trombone": 57, "tuba": 58, "french horn": 60, "horn": 60, "brass": 61,
      "soprano sax": 64, "alto sax": 65, "sax": 65, "tenor sax": 66, "baritone sax": 67, "oboe": 68,
      "english horn": 69, "bassoon": 70, "clarinet": 71, "piccolo": 72, "flute": 73, "recorder": 74,
      "pan flute": 75, "shakuhachi": 77, "whistle": 78, "ocarina": 79, "synth lead": 80, "synth pad": 88,
      "sitar": 104, "banjo": 105, "shamisen": 106, "koto": 107, "kalimba": 108, "bagpipe": 109, "fiddle": 110,
      "steel drums": 114}


def program_of(spec):
    if spec is None:
        return None
    s = str(spec).strip().lower()
    if s.isdigit():
        v = int(s)
        if not 0 <= v <= 127:
            raise NotationError("--program numbers run 0-127 (General MIDI, zero-based: 73 is flute)")
        return v
    if s not in GM:
        raise NotationError(f"unknown instrument {spec!r}; use a General MIDI number 0-127 or one of: {', '.join(sorted(GM))}")
    return GM[s]


# ---------------------------------------------------------------- bars and repeats (shared by ABC and MusicXML)

class Bar:
    def __init__(self):
        self.events = []  # (offset_beats, Note) with Note.start relative to the bar
        self.length = 0.0
        self.start_repeat = self.end_repeat = False
        self.ending = None  # set of pass numbers
        self.chords = []  # (offset, symbol)
        self.ending_closed = False


def expand_bars(bars):
    """Play repeats and first/second endings; returns bars in performance order."""
    out, i, start, pas, done, last_end = [], 0, 0, 1, set(), -1
    guard = 0
    while i < len(bars):
        guard += 1
        if guard > 100000:
            break
        b = bars[i]
        if b.start_repeat and pas == 1:
            start = i
        if pas == 2 and not b.ending and i > last_end:
            pas = 1
        if b.ending and pas not in b.ending:
            i += 1
            continue
        out.append(b)
        if b.end_repeat and i not in done:
            done.add(i)
            last_end = i
            i, pas = start, 2
            continue
        if b.end_repeat:
            pas, start = 1, i + 1
        i += 1
    return out


def bars_to_notes(bars, track):
    t = 0.0
    chords = []
    for b in bars:
        for off, n in b.events:
            track.notes.append(Note(t + off, n.dur, n.pitch, n.vel, n.tie))
        for off, sym in b.chords:
            chords.append((t + off, sym))
        t += b.length
    merge_ties(track)
    return t, chords


def merge_ties(track):
    notes = sorted(track.notes, key=lambda n: (n.start, n.pitch))
    out, open_ties = [], {}
    for n in notes:
        key = n.pitch
        prev = open_ties.get(key)
        if prev is not None and abs(prev.end() - n.start) < 1e-6:
            prev.dur += n.dur
            prev.tie = n.tie
            if not n.tie:
                del open_ties[key]
            continue
        out.append(n)
        if n.tie:
            open_ties[key] = n
        else:
            open_ties.pop(key, None)
    for n in out:
        n.tie = False
    track.notes = out


# ---------------------------------------------------------------- chord symbols

CHORD_INTERVALS = [("maj7", [0, 4, 7, 11]), ("m7b5", [0, 3, 6, 10]), ("dim7", [0, 3, 6, 9]), ("m7", [0, 3, 7, 10]),
                   ("mmaj7", [0, 3, 7, 11]), ("7sus4", [0, 5, 7, 10]), ("sus4", [0, 5, 7]), ("sus2", [0, 2, 7]),
                   ("dim", [0, 3, 6]), ("aug", [0, 4, 8]), ("+", [0, 4, 8]), ("m6", [0, 3, 7, 9]), ("6", [0, 4, 7, 9]),
                   ("9", [0, 4, 7, 10, 14]), ("add9", [0, 4, 7, 14]), ("m9", [0, 3, 7, 10, 14]), ("7", [0, 4, 7, 10]),
                   ("min", [0, 3, 7]), ("maj", [0, 4, 7]), ("m", [0, 3, 7]), ("5", [0, 7]), ("", [0, 4, 7])]


def chord_pitches(sym):
    m = re.fullmatch(r"([A-G])([#b]?)([^/]*)(?:/([A-G][#b]?))?", sym.strip())
    if not m:
        return None
    root = LETTER_PC[m.group(1)] + {"#": 1, "b": -1, "": 0}[m.group(2)]
    qual = m.group(3)
    for name, iv in CHORD_INTERVALS:
        if qual == name:
            break
    else:
        return None
    base = 48 + root if root <= 6 else 36 + root  # root between F#2 and F#3
    ps = [base + i for i in iv]
    if m.group(4):
        b = LETTER_PC[m.group(4)[0]] + {"#": 1, "b": -1, "": 0}[m.group(4)[1:] or ""]
        ps = [36 + b] + ps
    return ps


def add_chord_track(score, chords, end_beat, program=0):
    if not chords:
        return 0
    t = Track("chords", program)
    bad = []
    for i, (beat, sym) in enumerate(chords):
        nxt = chords[i + 1][0] if i + 1 < len(chords) else end_beat
        ps = chord_pitches(sym)
        if ps is None:
            bad.append(sym)
            continue
        for p in ps:
            t.notes.append(Note(beat, max(nxt - beat, 0.25), p, 64))
    if bad:
        score.warnings.append(f"chord symbols not understood (skipped): {', '.join(sorted(set(bad)))}")
    if t.notes:
        score.tracks.append(t)
    return len(chords) - len(bad)


# ---------------------------------------------------------------- ABC

ABC_TUPLET_Q = {2: 3, 3: 2, 4: 3, 5: 2, 6: 2, 7: 2, 8: 3, 9: 2}
ABC_NOTE = re.compile(r"(\^\^|\^|__|_|=)?([A-Ga-g])([,']*)(\d*)(/*)(\d*)")
ABC_REST = re.compile(r"([zx])(\d*)(/*)(\d*)")


def abc_length(num, slashes, den, unit):
    n = Fraction(int(num)) if num else Fraction(1)
    if slashes:
        d = int(den) if den else 2 ** len(slashes)
        n /= d
    return n * unit


def abc_key(text):
    t = text.strip()
    if not t or t.lower().startswith("none"):
        return 0, "major"
    if t.upper().startswith("HP") or t.lower().startswith("hp"):
        return 2, "major"
    m = re.match(r"([A-G])([#b]?)\s*([A-Za-z]*)", t)
    if not m:
        return 0, "major"
    tonic = m.group(1) + m.group(2)
    mode = m.group(3).lower()[:3] if m.group(3).lower() not in ("m", "min", "minor", "major", "maj") else m.group(3).lower()
    if mode in ("exp", "cle", "tra", "oct", "mid", "sta", "met"):
        mode = ""
    shift = MODE_SHIFT.get(mode, MODE_SHIFT.get(mode[:3], 0))
    base = MAJOR_FIFTHS.get(tonic)
    if base is None:  # enharmonic tonics such as A# or D#
        base = MAJOR_FIFTHS.get(NAMES_FLAT[(LETTER_PC[tonic[0]] + (1 if tonic[1:] == "#" else -1)) % 12], 0)
    f = base + shift
    while f > 7:
        f -= 12
    while f < -7:
        f += 12
    return f, ("minor" if shift == -3 else "major")


def parse_abc(text, select=None):
    """ABC 2.1 subset -> Score. select picks one tune by X: number (default the first)."""
    tunes = re.split(r"(?m)^(?=X:)", text)
    tunes = [t for t in tunes if t.strip().startswith("X:")] or [text]
    if select is not None:
        tunes = [t for t in tunes if re.match(rf"X:\s*{select}\b", t.strip())] or tunes
    tune = tunes[0]
    score = Score()
    unit = None
    meter = (4, 4)
    fifths, mode = 0, "major"
    bpm = None
    voices = {}  # id -> state
    order = []
    programs = {}
    cur_id = "1"
    in_body = False

    def voice(vid):
        if vid not in voices:
            voices[vid] = {"bars": [Bar()], "t": 0.0, "acc": {}, "tie_next": False, "tuplet": None, "broken": None,
                           "last": None, "name": vid, "fifths": fifths}
            order.append(vid)
        return voices[vid]

    def apply_field(k, v, header):
        nonlocal unit, meter, fifths, mode, bpm, cur_id
        v = v.split("%")[0].strip()
        if k == "T" and not score.title:
            score.title = v
        elif k == "L":
            m = re.match(r"(\d+)/(\d+)", v)
            if m:
                unit = Fraction(int(m.group(1)), int(m.group(2))) * 4
        elif k == "M":
            if v in ("C", ""):
                meter = (4, 4)
            elif v == "C|":
                meter = (2, 2)
            else:
                m = re.match(r"(\d+)/(\d+)", v)
                if m:
                    meter = (int(m.group(1)), int(m.group(2)))
            if header:
                score.meter = meter
        elif k == "K":
            fifths, mode = abc_key(v)
            if score.key is None:
                score.key = (fifths, mode)
            for st in voices.values():
                st["fifths"] = fifths
            return True
        elif k == "Q":
            m = re.search(r"(\d+)/(\d+)\s*=\s*(\d+(?:\.\d+)?)", v)
            if m:
                beat = Fraction(int(m.group(1)), int(m.group(2))) * 4
                bpm = float(m.group(3)) * float(beat)
            else:
                m = re.search(r"(\d+(?:\.\d+)?)", v)
                if m:
                    bpm = float(m.group(1)) * float(unit or Fraction(1, 2))
        elif k == "V":
            vid = v.split()[0] if v else "1"
            st = voice(vid)
            nm = re.search(r'(?:name|nm)\s*=\s*"([^"]*)"', v)
            if nm:
                st["name"] = nm.group(1)
            cur_id = vid
        return False

    lines = tune.splitlines()
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("%%MIDI"):
            m = re.match(r"%%MIDI\s+program\s+(?:(\d+)\s+)?(\d+)", line)
            if m:
                programs[cur_id] = int(m.group(2))
            continue
        if line.startswith("%") or not line.strip():
            continue
        fm = re.match(r"^([A-Za-z]):(.*)$", line)
        if fm and not (in_body and fm.group(1) in "|"):
            k, v = fm.group(1), fm.group(2)
            if apply_field(k, v, not in_body) and not in_body:
                in_body = True
                if unit is None:
                    unit = Fraction(1, 16) * 4 if meter[0] / meter[1] < 0.75 else Fraction(1, 8) * 4
            continue
        if not in_body:
            continue
        if unit is None:
            unit = Fraction(1, 2)
        parse_abc_line(line, voice(cur_id), unit, lambda: meter, score, apply_field)

    if bpm is None:
        bpm = 120.0
        score.warnings.append("no Q: tempo; rendered at 120 quarter notes a minute (set Q:1/4=N or --bpm)")
    score.tempos = [(0.0, bpm)]
    all_chords = []
    for vid in order:
        st = voices[vid]
        bars = [b for b in st["bars"] if b.events or b.length or b.chords or b.end_repeat or b.start_repeat]
        expected = 4.0 * score.meter[0] / score.meter[1]
        for i, b in enumerate(bars[1:-1], 2):  # first and last bars may be pickups
            if abs(b.length - expected) > 1e-6:
                score.warnings.append(f"voice {st['name']} bar {i} lasts {b.length:g} beats, not {expected:g}")
        tr = Track(st["name"], programs.get(vid, 0))
        end, chords = bars_to_notes(expand_bars(bars), tr)
        all_chords.extend(chords)
        score.tracks.append(tr)
    score._chords = all_chords
    if not score.notes():
        raise NotationError("no notes found; is this ABC (an X: line, a K: line, then the tune)?")
    return score


def parse_abc_line(line, st, unit, meter_fn, score, apply_field):
    i, n = 0, len(line)
    chord = None  # list of Notes being collected inside [ ]
    pending_ending = None

    def bar():
        return st["bars"][-1]

    def new_bar(end_repeat=False, start_repeat=False):
        b = bar()
        b.length = st["t"]
        if end_repeat:
            b.end_repeat = True
        nb = Bar()
        nb.start_repeat = start_repeat
        if b.ending and not end_repeat and not b.ending_closed:
            nb.ending = b.ending
        st["bars"].append(nb)
        st["t"] = 0.0
        st["acc"] = {}

    def add_note(pitch, length, tie):
        f = 1.0
        if st["tuplet"]:
            p, q, left = st["tuplet"]
            f = q / p
            st["tuplet"] = (p, q, left - 1) if left > 1 else None
        if st["broken"] is not None:
            f *= st["broken"]
            st["broken"] = None
        dur = float(length) * f
        note = Note(st["t"], dur, pitch, 90, tie)
        return note

    while i < n:
        c = line[i]
        if c == "%":
            break
        if c == "\\" or c in " \t`y":
            i += 1
            continue
        if c == '"':
            j = line.find('"', i + 1)
            j = n if j < 0 else j
            sym = line[i + 1:j]
            if sym and sym[0] not in "^_<>@":
                bar().chords.append((st["t"], sym))
            i = j + 1
            continue
        if c in "!+":
            j = line.find(c, i + 1)
            i = n if j < 0 else j + 1
            continue
        if c == "[" and i + 2 < n and line[i + 1].isalpha() and line[i + 2] == ":":
            j = line.find("]", i)
            j = n if j < 0 else j
            apply_field(line[i + 1], line[i + 3:j], False)
            if line[i + 1] == "K":
                st["acc"] = {}
            i = j + 1
            continue
        if c == "[" and i + 1 < n and line[i + 1].isdigit():
            m = re.match(r"\[([\d,\-]+)", line[i:])
            bar().ending = parse_ending(m.group(1))
            i += len(m.group(0))
            continue
        if c in "|:":
            m = re.match(r"(:*)(\|\]|\|\||\[\||\|)?(:*)(\d[\d,\-]*)?", line[i:])
            tok = m.group(0)
            if not tok:
                i += 1
                continue
            ends, bl, starts, ending = m.group(1), m.group(2), m.group(3), m.group(4)
            if not bl and ends and starts:  # "::"
                ends, starts = ":", ":"
            if chord is not None:
                chord = None
            closing = bool(ends) or bl in ("||", "|]", "[|") or bool(starts)
            if bar().ending is not None and closing:
                bar().ending_closed = True
            if st["t"] > 0 or bar().events or ends:
                new_bar(end_repeat=bool(ends), start_repeat=bool(starts))
            elif starts:
                bar().start_repeat = True
            if ending:
                bar().ending = parse_ending(ending)
            i += len(tok)
            continue
        if c == "[":
            chord = []
            i += 1
            continue
        if c == "]" and chord is not None:
            m = re.match(r"\](\d*)(/*)(\d*)", line[i:])
            mult = abc_length(m.group(1), m.group(2), m.group(3), Fraction(1)) if (m.group(1) or m.group(2)) else Fraction(1)
            tie = False
            j = i + len(m.group(0))
            if j < n and line[j] == "-":
                tie = True
                j += 1
            if chord:
                first = chord[0].dur * float(mult)
                for note in chord:
                    note.dur *= float(mult)
                    note.tie = note.tie or tie
                    bar().events.append((note.start, note))
                st["last"] = chord
                st["t"] += first
            chord = None
            i = j
            continue
        if c == "(" and i + 1 < n and line[i + 1].isdigit():
            m = re.match(r"\((\d)(?::(\d*))?(?::(\d*))?", line[i:])
            p = int(m.group(1))
            q = int(m.group(2)) if m.group(2) else ABC_TUPLET_Q.get(p, 2)
            if p in (5, 7, 9) and not m.group(2) and meter_fn()[1] == 8 and meter_fn()[0] % 3 == 0:
                q = 3
            r = int(m.group(3)) if m.group(3) else p
            st["tuplet"] = (p, q, r)
            i += len(m.group(0))
            continue
        if c in "()":
            i += 1
            continue
        if c in "><":
            m = re.match(r"(>+|<+)", line[i:])
            k = len(m.group(1))
            long_f, short_f = 2 - 0.5 ** k, 0.5 ** k
            prev = st["last"]
            if prev:
                fa, fb = (long_f, short_f) if c == ">" else (short_f, long_f)
                add = None
                for note in prev:
                    old = note.dur
                    note.dur *= fa
                    add = note.dur - old
                st["t"] += add or 0
                st["broken"] = fb
            i += k
            continue
        if c == "-":
            if st["last"]:
                for note in st["last"]:
                    note.tie = True
            i += 1
            continue
        if c in ".~HLMOPSTuvJR":
            i += 1
            continue
        if c == "Z":
            m = re.match(r"Z(\d*)", line[i:])
            k = int(m.group(1) or 1)
            full = 4.0 * meter_fn()[0] / meter_fn()[1]
            for b in range(k):
                st["t"] += full
                if b < k - 1:
                    new_bar()
            i += len(m.group(0))
            continue
        m = ABC_REST.match(line, i)
        if m:
            length = abc_length(m.group(2), m.group(3), m.group(4), unit)
            note = add_note(0, length, False)
            st["t"] += note.dur
            st["last"] = None
            i = m.end()
            continue
        m = ABC_NOTE.match(line, i)
        if m:
            acc, letter, octs, num, slashes, den = m.groups()
            up = letter.upper()
            octave = 5 if letter.islower() else 4
            octave += octs.count("'") - octs.count(",")
            keyacc = key_signature(st["fifths"])[up]
            akey = (up, octave)
            if acc:
                alter = {"^": 1, "^^": 2, "_": -1, "__": -2, "=": 0}[acc]
                st["acc"][akey] = alter
            else:
                alter = st["acc"].get(akey, keyacc)
            pitch = 12 * (octave + 1) + LETTER_PC[up] + alter  # C is middle C, MIDI 60
            length = abc_length(num, slashes, den, unit)
            j = m.end()
            tie = j < n and line[j] == "-"
            if tie:
                j += 1
            if chord is not None:
                note = Note(st["t"], float(length), pitch, 90, tie)
                chord.append(note)
            else:
                note = add_note(pitch, length, tie)
                bar().events.append((note.start, note))
                st["last"] = [note]
                st["t"] += note.dur
            i = j
            continue
        score.warnings.append(f"skipped unknown ABC character {c!r}")
        i += 1
    bar().length = st["t"]


def parse_ending(s):
    out = set()
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-", 1)
            out.update(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return out or {1}


# ---------------------------------------------------------------- ASCII tab

TUNINGS = {"guitar": [64, 59, 55, 50, 45, 40], "standard": [64, 59, 55, 50, 45, 40], "dropd": [64, 59, 55, 50, 45, 38],
           "dadgad": [62, 57, 55, 50, 45, 38], "openg": [62, 59, 55, 50, 43, 38], "bass": [43, 38, 33, 28],
           "bass5": [43, 38, 33, 28, 23], "guitar7": [64, 59, 55, 50, 45, 40, 35], "ukulele": [69, 64, 60, 67]}
TAB_LINE = re.compile(r"^\s*([A-Ga-g][#b]?)?\s*(\|\||\||:)?([-0-9|hpbrxsHPBX/\\~()<>.^*= ]+)\|?\s*$")


def parse_tuning(spec, count):
    if spec is None:
        return None
    s = spec.strip().lower().replace(" ", "")
    if s in TUNINGS:
        t = TUNINGS[s]
    else:
        parts = [p for p in re.split(r"[,]", spec) if p.strip()]
        if len(parts) < 2:
            raise NotationError(f"--tuning {spec!r}: name one ({', '.join(sorted(TUNINGS))}) or list pitches low to high like E2,A2,D3,G3,B3,E4")
        t = list(reversed([parse_pitch_name(p) for p in parts]))
    if len(t) != count:
        raise NotationError(f"--tuning has {len(t)} strings but the tab has {count}")
    return t


def tuning_from_spec(spec):
    """A tuning name or a low-to-high pitch list -> MIDI pitches, highest string first (None passes through)."""
    if not spec:
        return None
    key = spec.strip().lower().replace(" ", "")
    if key in TUNINGS:
        return list(TUNINGS[key])
    return parse_tuning(spec, len([p for p in spec.split(",") if p.strip()]))


def tab_systems(text):
    """Groups of consecutive tab lines (4-8 strings)."""
    systems, cur = [], []
    for line in text.splitlines():
        m = TAB_LINE.match(line)
        if m and line.count("-") >= 3:
            cur.append((m.group(1), m.group(3)))
        else:
            if len(cur) >= 4:
                systems.append(cur)
            cur = []
    if len(cur) >= 4:
        systems.append(cur)
    return systems


def parse_tab(text, tuning=None, step=None, bpm=None, program=None):
    systems = tab_systems(text)
    if not systems:
        raise NotationError("no tab found: expected 4-8 lines like e|---0---3---| with one line per string")
    count = len(systems[0])
    labels = [l for l, _ in systems[0]]
    tun = parse_tuning(tuning, count) if tuning else None
    score = Score()
    if tun is None:
        base = {4: TUNINGS["bass"], 5: TUNINGS["bass5"], 6: TUNINGS["guitar"], 7: TUNINGS["guitar7"]}.get(count)
        if base is None:
            raise NotationError(f"tab with {count} strings: give --tuning")
        tun = []
        for i, lab in enumerate(labels):
            if lab:
                pc = LETTER_PC[lab[0].upper()] + {"#": 1, "b": -1, "": 0}[lab[1:] or ""]
                cands = [12 * o + pc for o in range(1, 8)]
                tun.append(min(cands, key=lambda p: abs(p - base[i])))
            else:
                tun.append(base[i])
        if count == 4 and labels and all(labels) and [l.upper() for l in labels] == ["A", "E", "C", "G"]:
            tun = TUNINGS["ukulele"]
    onsets = []  # (column, string, pitch)
    col0 = 0
    for sysi, lines in enumerate(systems):
        if len(lines) != count:
            score.warnings.append(f"tab system {sysi + 1} has {len(lines)} strings, not {count}; skipped")
            continue
        width = max(len(b) for _, b in lines)
        rows = [b.ljust(width, "-") for _, b in lines]
        keep = [c for c in range(width) if not all(r[c] == "|" for r in rows)]  # bar lines take no time
        colmap = {c: k for k, c in enumerate(keep)}
        for s, r in enumerate(rows):
            c = 0
            while c < width:
                ch = r[c]
                if ch.isdigit():
                    j = c
                    while j < width and r[j].isdigit() and j - c < 2:
                        j += 1
                    fret = int(r[c:j])
                    if fret > 24 and j - c == 2:  # two single-digit frets side by side
                        fret, j = int(r[c]), c + 1
                    if c in colmap:
                        onsets.append((col0 + colmap[c], s, tun[s] + fret))
                    c = j
                    continue
                c += 1
        col0 += len(keep)
    if not onsets:
        raise NotationError("the tab has no fret numbers")
    cols = sorted({o[0] for o in onsets})
    gaps = sorted(b - a for a, b in zip(cols, cols[1:]) if b > a)
    med = gaps[len(gaps) // 2] if gaps else 2
    col_beats = float(step) if step else 0.5 / med  # the usual spacing between notes counts as an eighth
    if not step:
        score.warnings.append(f"tab has no rhythm: each column taken as {col_beats:g} beats (the usual gap between notes = an eighth note); set --tab-step to change")
    tr = Track("tab", program if program is not None else (33 if count in (4, 5) and tun[0] < 50 else 25))
    last_on_string = {}
    for col, s, p in sorted(onsets):
        if s in last_on_string:
            prev = last_on_string[s]
            prev.dur = min(prev.dur, col * col_beats - prev.start)
        n = Note(col * col_beats, 4.0, p, 90)
        tr.notes.append(n)
        last_on_string[s] = n
    end = (cols[-1] + med) * col_beats
    for n in tr.notes:
        n.dur = max(min(n.dur, end - n.start, 2.0), col_beats)
    score.tracks.append(tr)
    score.tempos = [(0.0, float(bpm or 100))]
    score.tuning = tun
    score.title = "tab"
    return score


# ---------------------------------------------------------------- MusicXML

STEP_PC = LETTER_PC


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def read_musicxml_bytes(path):
    p = Path(path)
    if p.suffix.lower() == ".mxl":
        with zipfile.ZipFile(p) as z:
            root = None
            if "META-INF/container.xml" in z.namelist():
                c = ET.fromstring(z.read("META-INF/container.xml"))
                for el in c.iter():
                    if _local(el.tag) == "rootfile" and el.get("full-path"):
                        root = el.get("full-path")
                        break
            if root is None:
                root = next(n for n in z.namelist() if n.endswith((".xml", ".musicxml")) and not n.startswith("META-INF"))
            return z.read(root)
    return p.read_bytes()


def parse_musicxml(data):
    root = ET.fromstring(data)
    for el in root.iter():
        el.tag = _local(el.tag)
    if root.tag == "score-timewise":
        raise NotationError("timewise MusicXML is not supported; export partwise from the notation program")
    score = Score()
    t = root.find("work/work-title")
    if t is None:
        t = root.find("movement-title")
    if t is not None and t.text:
        score.title = t.text.strip()
    names, programs = {}, {}
    for sp in root.iter("score-part"):
        pid = sp.get("id")
        pn = sp.find("part-name")
        names[pid] = (pn.text or pid).strip() if pn is not None else pid
        mp = sp.find("midi-instrument/midi-program")
        if mp is not None and mp.text:
            programs[pid] = max(0, int(mp.text) - 1)
        if sp.find("midi-instrument/midi-channel") is not None and (sp.findtext("midi-instrument/midi-channel") or "").strip() == "10":
            programs[pid] = -1
    tempos = []
    for part in root.iter("part"):
        pid = part.get("id")
        bars, div = [], 1.0
        first = not score.tracks
        for meas in part.iter("measure"):
            b = Bar()
            cur, maxt, last_start = 0.0, 0.0, 0.0
            for el in meas:
                tag = el.tag
                if tag == "attributes":
                    d = el.findtext("divisions")
                    if d:
                        div = float(d)
                    if first:
                        tb, tt = el.findtext("time/beats"), el.findtext("time/beat-type")
                        if tb and tt and tb.isdigit():
                            if not bars:
                                score.meter = (int(tb), int(tt))
                        f = el.findtext("key/fifths")
                        if f is not None and score.key is None:
                            score.key = (int(f), "minor" if (el.findtext("key/mode") or "").lower() == "minor" else "major")
                elif tag == "note":
                    if el.find("grace") is not None or el.find("cue") is not None:
                        continue
                    dur = float(el.findtext("duration") or 0) / div
                    is_chord = el.find("chord") is not None
                    start = last_start if is_chord else cur
                    if el.find("rest") is None:
                        pe = el.find("pitch") if el.find("pitch") is not None else el.find("unpitched")
                        if pe is not None and el.find("pitch") is not None:
                            step = pe.findtext("step")
                            alter = float(pe.findtext("alter") or 0)
                            octv = int(pe.findtext("octave"))
                            pitch = 12 * (octv + 1) + STEP_PC[step] + int(round(alter))
                        else:
                            pitch = 38  # unpitched: a snare on the drum channel
                        ties = [x.get("type") for x in el.findall("tie")]
                        n = Note(start, dur, pitch, 90, "start" in ties)
                        b.events.append((start, n))
                    if not is_chord:
                        last_start = cur
                        cur += dur
                    maxt = max(maxt, cur)
                elif tag == "backup":
                    cur -= float(el.findtext("duration") or 0) / div
                elif tag == "forward":
                    cur += float(el.findtext("duration") or 0) / div
                    maxt = max(maxt, cur)
                elif tag in ("direction", "sound"):
                    snd = el if tag == "sound" else el.find(".//sound")
                    if snd is not None and snd.get("tempo") and first:
                        tempos.append((len(bars), cur, float(snd.get("tempo"))))
                elif tag == "barline":
                    rep = el.find("repeat")
                    if rep is not None:
                        if rep.get("direction") == "forward":
                            b.start_repeat = True
                        else:
                            b.end_repeat = True
                    en = el.find("ending")
                    if en is not None and en.get("type") == "start":
                        b.ending = parse_ending(en.get("number", "1").replace(" ", ""))
            b.length = maxt
            bars.append(b)
        if first:
            first_bars = bars
        prog = programs.get(pid, 0)
        tr = Track(names.get(pid, pid), max(prog, 0), prog == -1)
        bars_to_notes(expand_bars(bars), tr)
        score.tracks.append(tr)
    if tempos:
        starts, acc = [], 0.0
        for b in first_bars:
            starts.append(acc)
            acc += b.length
        tm = [(starts[i] + off if i < len(starts) else 0.0, bpm) for i, off, bpm in tempos]
        score.tempos = [(0.0, tm[0][1])] + [x for x in tm[1:] if x[0] > 0]
    else:
        score.warnings.append("no tempo marking; rendered at 120 quarter notes a minute (set --bpm)")
    if any(any(b.end_repeat for b in first_bars) for _ in [0]):
        score.warnings.append("repeats were played out; tempo changes after a repeat are placed by the written bars")
    if not score.notes():
        raise NotationError("no notes found in the MusicXML")
    return score


def fmt_dur_type(units):
    """16th-note units -> (type, dots) when one notehead can show it."""
    table = {16: ("whole", 0), 12: ("half", 1), 8: ("half", 0), 6: ("quarter", 1), 4: ("quarter", 0),
             3: ("eighth", 1), 2: ("eighth", 0), 1: ("16th", 0), 24: ("whole", 1)}
    return table.get(units)


def split_units(units):
    out = []
    for size in (16, 12, 8, 6, 4, 3, 2, 1):
        while units >= size:
            out.append(size)
            units -= size
    return out


# ---------------------------------------------------------------- quantised stream (shared by ABC, MusicXML and tab writers)

def quantised_stream(track, grid, bar_units, total_units=None):
    """A track -> bars of (units, [pitches] or [] for a rest, tie_out) events on a grid of `grid` steps a beat."""
    ons = {}
    for n in track.notes:
        s = int(round(n.start * grid))
        e = max(int(round(n.end() * grid)), s + 1)
        ons.setdefault(s, []).append((e, n.pitch))
    starts = sorted(ons)
    events = []  # (start, end, pitches)
    for i, s in enumerate(starts):
        nxt = starts[i + 1] if i + 1 < len(starts) else None
        e = max(x[0] for x in ons[s])
        if nxt is not None:
            e = min(e, nxt)
        if getattr(track, "mono", False):  # one line: two notes snapped to one slot keep the longer
            events.append((s, e, [max(ons[s])[1]]))
            continue
        events.append((s, e, sorted({x[1] for x in ons[s]})))
    end = total_units or (events[-1][1] if events else 0)
    nbars = max(1, -(-end // bar_units))
    bars = [[] for _ in range(nbars)]
    t = 0
    seq = []
    for s, e, ps in events:
        if s > t:
            seq.append((t, s, []))
        seq.append((s, e, ps))
        t = e
    if t < nbars * bar_units:
        seq.append((t, nbars * bar_units, []))
    for s, e, ps in seq:
        while s < e:
            bi = s // bar_units
            bend = (bi + 1) * bar_units
            seg_end = min(e, bend)
            pieces = split_units(seg_end - s)
            for k, u in enumerate(pieces):
                last = (k == len(pieces) - 1) and seg_end == e
                bars[bi].append((u, ps, bool(ps) and not last))
            s = seg_end
    return bars


def spell(pitch, fifths):
    names = NAMES_SHARP if fifths >= 0 else NAMES_FLAT
    nm = names[pitch % 12]
    return nm[0], {"#": 1, "b": -1}.get(nm[1:], 0), pitch // 12 - 1


def write_abc(score, grid=4):
    fifths, mode = score.key or estimate_key(score.notes())
    num, den = score.meter
    bar_units = int(round(4 * grid * num / den))
    L = 4 * grid  # L:1/(4*grid) -> one unit
    bpm = score.tempos[0][1]
    lines = ["X:1", f"T:{score.title or 'Untitled'}", f"M:{num}/{den}", f"L:1/{L}", f"Q:1/4={int(round(bpm))}"]
    kn = key_name(fifths, mode)
    lines.append("K:" + kn.split()[0] + ("m" if mode == "minor" else ""))
    total = int(round(score.length_beats() * grid))
    sig = key_signature(fifths)
    for vi, tr in enumerate(score.tracks, 1):
        if len(score.tracks) > 1:
            lines.append(f'V:{vi} name="{tr.name or vi}"')
            lines.append(f"%%MIDI program {tr.program}")
        bars = quantised_stream(tr, grid, bar_units, total)
        out_bars = []
        for bar in bars:
            acc = {}
            toks = []
            for units, ps, tie in bar:
                ln = "" if units == 1 else str(units)
                if not ps:
                    toks.append("z" + ln)
                    continue
                heads = []
                for p in ps:
                    letter, alter, octv = spell(p, fifths)
                    k = (letter, octv)
                    cur = acc.get(k, sig[letter])
                    a = ""
                    if alter != cur:
                        a = {1: "^", -1: "_", 0: "=", 2: "^^", -2: "__"}[alter]
                        acc[k] = alter
                    if octv >= 5:
                        head = letter.lower() + "'" * (octv - 5)
                    else:
                        head = letter + "," * (4 - octv)
                    heads.append(a + head)
                body = heads[0] if len(heads) == 1 else "[" + "".join(heads) + "]"
                toks.append(body + ln + ("-" if tie else ""))
            out_bars.append(" ".join(toks))
        for i in range(0, len(out_bars), 4):
            chunk = out_bars[i:i + 4]
            lines.append(" | ".join(chunk) + (" |]" if i + 4 >= len(out_bars) else " |"))
    return "\n".join(lines) + "\n"


def write_musicxml(score, grid=4):
    fifths, mode = score.key or estimate_key(score.notes())
    num, den = score.meter
    bar_units = int(round(4 * grid * num / den))
    total = int(round(score.length_beats() * grid))
    root = ET.Element("score-partwise", version="4.0")
    w = ET.SubElement(root, "work")
    ET.SubElement(w, "work-title").text = score.title or "Untitled"
    pl = ET.SubElement(root, "part-list")
    for i, tr in enumerate(score.tracks, 1):
        sp = ET.SubElement(pl, "score-part", id=f"P{i}")
        ET.SubElement(sp, "part-name").text = tr.name or f"Part {i}"
        mi = ET.SubElement(sp, "midi-instrument", id=f"P{i}-I1")
        ET.SubElement(mi, "midi-channel").text = "10" if tr.drums else str(min(i, 9) if i < 10 else i + 1)
        ET.SubElement(mi, "midi-program").text = str(tr.program + 1)
    for i, tr in enumerate(score.tracks, 1):
        part = ET.SubElement(root, "part", id=f"P{i}")
        low = min((n.pitch for n in tr.notes), default=60)
        for bi, bar in enumerate(quantised_stream(tr, grid, bar_units, total), 1):
            m = ET.SubElement(part, "measure", number=str(bi))
            if bi == 1:
                at = ET.SubElement(m, "attributes")
                ET.SubElement(at, "divisions").text = str(grid)
                k = ET.SubElement(at, "key")
                ET.SubElement(k, "fifths").text = str(fifths)
                ET.SubElement(k, "mode").text = mode
                tm = ET.SubElement(at, "time")
                ET.SubElement(tm, "beats").text = str(num)
                ET.SubElement(tm, "beat-type").text = str(den)
                cl = ET.SubElement(at, "clef")
                ET.SubElement(cl, "sign").text = "F" if low < 55 else "G"
                ET.SubElement(cl, "line").text = "4" if low < 55 else "2"
                d = ET.SubElement(m, "direction", placement="above")
                dt = ET.SubElement(d, "direction-type")
                mt = ET.SubElement(dt, "metronome")
                ET.SubElement(mt, "beat-unit").text = "quarter"
                ET.SubElement(mt, "per-minute").text = str(int(round(score.tempos[0][1])))
                ET.SubElement(d, "sound", tempo=str(round(score.tempos[0][1], 2)))
            tie_in = getattr(tr, "_tie_in", set())
            for units, ps, tie in bar:
                heads = ps or [None]
                for hi, p in enumerate(heads):
                    ne = ET.SubElement(m, "note")
                    if hi:
                        ET.SubElement(ne, "chord")
                    if p is None:
                        ET.SubElement(ne, "rest")
                    else:
                        letter, alter, octv = spell(p, fifths)
                        pe = ET.SubElement(ne, "pitch")
                        ET.SubElement(pe, "step").text = letter
                        if alter:
                            ET.SubElement(pe, "alter").text = str(alter)
                        ET.SubElement(pe, "octave").text = str(octv)
                    ET.SubElement(ne, "duration").text = str(units)
                    if p is not None and p in tie_in:
                        ET.SubElement(ne, "tie", type="stop")
                    if tie:
                        ET.SubElement(ne, "tie", type="start")
                    ty = fmt_dur_type(units * 4 // grid) if grid != 4 else fmt_dur_type(units)
                    if ty:
                        ET.SubElement(ne, "type").text = ty[0]
                        for _ in range(ty[1]):
                            ET.SubElement(ne, "dot")
                    if p is not None and (tie or p in tie_in):
                        nt = ET.SubElement(ne, "notations")
                        if p in tie_in:
                            ET.SubElement(nt, "tied", type="stop")
                        if tie:
                            ET.SubElement(nt, "tied", type="start")
                tie_in = set(ps) if tie else set()
            tr._tie_in = tie_in
    _indent(root)
    body = ET.tostring(root, encoding="unicode")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
            '"http://www.musicxml.org/dtds/partwise.dtd">\n' + body + "\n")


def _indent(el, level=0):
    pad = "\n" + "  " * level
    if len(el):
        if not el.text or not el.text.strip():
            el.text = pad + "  "
        for ch in el:
            _indent(ch, level + 1)
        if not ch.tail or not ch.tail.strip():
            ch.tail = pad
    if level and (not el.tail or not el.tail.strip()):
        el.tail = pad


def write_tab(score, tuning=None, grid=4, bars_per_line=4, max_fret=15):
    tun = tuning or getattr(score, "tuning", None) or TUNINGS["guitar"]
    nstr = len(tun)
    num, den = score.meter
    bar_units = int(round(4 * grid * num / den))
    total = int(round(score.length_beats() * grid))
    notes = [n for t in score.tracks for n in t.notes]
    tr = Track("all")
    tr.notes = notes
    tr.mono = len(score.tracks) == 1 and getattr(score.tracks[0], "mono", False)
    bars = quantised_stream(tr, grid, bar_units, total)
    low = min(tun)
    warnings = []
    hand = 0
    cols_per_unit = 2 if grid <= 4 else 1
    out_bars = []
    for bar in bars:
        cols = [["-"] * (bar_units * cols_per_unit) for _ in range(nstr)]
        pos = 0
        for units, ps, tie in bar:
            used = set()
            for p in sorted(ps, reverse=True):
                opts = [(s, p - tun[s]) for s in range(nstr) if s not in used and 0 <= p - tun[s] <= max_fret]
                if not opts:
                    warnings.append(f"{midi_name(p)} is outside the tuning (lowest {midi_name(low)}); left out")
                    continue
                s, f = min(opts, key=lambda o: (abs(o[1] - hand) if o[1] else 0) + 0.3 * o[1])
                used.add(s)
                if f:
                    hand = f
                txt = str(f)
                c = pos * cols_per_unit
                for k, ch in enumerate(txt):
                    if c + k < len(cols[s]):
                        cols[s][c + k] = ch
            pos += units
        out_bars.append(["".join(r) for r in cols])
    labels = [NAMES_SHARP[p % 12] for p in tun]
    if nstr == 6 and tun == TUNINGS["guitar"]:
        labels[0] = "e"
    wl = max(len(x) for x in labels)
    lines = [f"{score.title or 'tab'}  (tuning {' '.join(midi_name(p) for p in reversed(tun))}; {cols_per_unit} columns = one 1/{4 * grid} note)"]
    for i in range(0, len(out_bars), bars_per_line):
        chunk = out_bars[i:i + bars_per_line]
        for s in range(nstr):
            lines.append(labels[s].ljust(wl) + "|" + "|".join(b[s] for b in chunk) + "|")
        lines.append("")
    return "\n".join(lines), sorted(set(warnings))


# ---------------------------------------------------------------- MIDI

def _vlq(v):
    out = [v & 0x7F]
    v >>= 7
    while v:
        out.insert(0, (v & 0x7F) | 0x80)
        v >>= 7
    return bytes(out)


def write_midi(score, path, tpq=480):
    tracks = []
    meta = bytearray()
    evs = [(int(round(b * tpq)), 0, b"\xff\x51\x03" + int(round(60000000 / bpm)).to_bytes(3, "big")) for b, bpm in score.tempos]
    num, den = score.meter
    evs.append((0, 0, b"\xff\x58\x04" + bytes([num, int(math.log2(den)), 24, 8])))
    if score.key:
        evs.append((0, 0, b"\xff\x59\x02" + struct.pack("bB", score.key[0], 1 if score.key[1] == "minor" else 0)))
    if score.title:
        t = score.title.encode("utf-8")[:120]
        evs.append((0, 0, b"\xff\x03" + _vlq(len(t)) + t))
    tracks.append(_track_bytes(evs))
    ch_next = 0
    for tr in score.tracks:
        if tr.drums:
            ch = 9
        else:
            ch = ch_next
            ch_next += 1
            if ch_next == 9:
                ch_next = 10
            ch = min(ch, 15)
        evs = []
        nm = (tr.name or "").encode("utf-8")[:60]
        if nm:
            evs.append((0, 0, b"\xff\x03" + _vlq(len(nm)) + nm))
        evs.append((0, 1, bytes([0xC0 | ch, tr.program & 0x7F])))
        for n in tr.notes:
            if n.pitch < 0 or n.pitch > 127:
                continue
            s = int(round(n.start * tpq))
            e = max(int(round(n.end() * tpq)), s + 1)
            evs.append((s, 2, bytes([0x90 | ch, n.pitch, max(1, min(127, n.vel))])))
            evs.append((e, 0, bytes([0x80 | ch, n.pitch, 0])))
        tracks.append(_track_bytes(evs))
    data = b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks), tpq) + b"".join(tracks)
    Path(path).write_bytes(data)
    return path


def _track_bytes(evs):
    evs.sort(key=lambda e: (e[0], e[1]))
    body, last = bytearray(), 0
    for t, _, msg in evs:
        body += _vlq(t - last) + msg
        last = t
    body += b"\x00\xff\x2f\x00"
    return b"MTrk" + struct.pack(">I", len(body)) + bytes(body)


def parse_midi(data):
    if data[:4] != b"MThd":
        raise NotationError("not a MIDI file (no MThd header)")
    _, fmt, ntr, div = struct.unpack(">IHHH", data[4:14])
    if div & 0x8000:
        raise NotationError("SMPTE-timed MIDI is not supported")
    tpq = div
    pos = 8 + struct.unpack(">I", data[4:8])[0]
    score = Score()
    tempos = []
    groups = {}  # (track, channel) -> Track
    for ti in range(ntr):
        if data[pos:pos + 4] != b"MTrk":
            break
        ln = struct.unpack(">I", data[pos + 4:pos + 8])[0]
        p, end = pos + 8, pos + 8 + ln
        pos = end
        t, status, name, active, progs = 0, 0, "", {}, {}
        while p < end:
            v = 0
            while True:
                b = data[p]
                p += 1
                v = (v << 7) | (b & 0x7F)
                if not b & 0x80:
                    break
            t += v
            b = data[p]
            if b == 0xFF:
                typ = data[p + 1]
                p += 2
                ml = 0
                while True:
                    c = data[p]
                    p += 1
                    ml = (ml << 7) | (c & 0x7F)
                    if not c & 0x80:
                        break
                body = data[p:p + ml]
                p += ml
                if typ == 0x51 and ml == 3:
                    tempos.append((t / tpq, 60000000 / int.from_bytes(body, "big")))
                elif typ == 0x58 and ml >= 2 and not score.notes():
                    score.meter = (body[0], 2 ** body[1])
                elif typ == 0x59 and ml == 2 and score.key is None:
                    score.key = (struct.unpack("b", body[:1])[0], "minor" if body[1] else "major")
                elif typ == 0x03:
                    name = body.decode("utf-8", "replace")
                    if ti == 0 and not score.title:
                        score.title = name
                continue
            if b in (0xF0, 0xF7):
                p += 1
                ml = 0
                while True:
                    c = data[p]
                    p += 1
                    ml = (ml << 7) | (c & 0x7F)
                    if not c & 0x80:
                        break
                p += ml
                continue
            if b & 0x80:
                status = b
                p += 1
            kind, ch = status & 0xF0, status & 0x0F
            if kind in (0xC0, 0xD0):
                d1 = data[p]
                p += 1
                if kind == 0xC0:
                    progs[ch] = d1
                continue
            d1, d2 = data[p], data[p + 1]
            p += 2
            if kind == 0x90 and d2 > 0:
                active.setdefault((ch, d1), []).append((t, d2))
            elif kind == 0x80 or (kind == 0x90 and d2 == 0):
                st = active.get((ch, d1))
                if st:
                    t0, vel = st.pop(0)
                    key = (ti, ch)
                    if key not in groups:
                        groups[key] = Track(name or f"track {ti} ch {ch + 1}", progs.get(ch, 0), ch == 9)
                    groups[key].program = progs.get(ch, groups[key].program)
                    groups[key].notes.append(Note(t0 / tpq, max(t - t0, 1) / tpq, d1, vel))
    score.tracks = [groups[k] for k in sorted(groups)]
    for tr in score.tracks:
        tr.notes.sort(key=lambda n: (n.start, n.pitch))
    tempos.sort()
    if tempos:
        score.tempos = [(0.0, tempos[0][1])] + [x for x in tempos[1:] if x[0] > 0]
    if not score.notes():
        raise NotationError("the MIDI file has no notes")
    return score


# ---------------------------------------------------------------- load any

def load(path, tuning=None, tab_step=None, bpm=None, program=None, chords=False, tune=None):
    p = Path(path)
    ext = p.suffix.lower()
    if ext in (".mid", ".midi"):
        score = parse_midi(p.read_bytes())
        kind = "midi"
    elif ext in (".xml", ".musicxml", ".mxl"):
        score = parse_musicxml(read_musicxml_bytes(p))
        kind = "musicxml"
    else:
        text = p.read_text(encoding="utf-8", errors="replace")
        if ext == ".abc" or re.search(r"(?m)^K:", text) and re.search(r"(?m)^X:", text):
            score = parse_abc(text, tune)
            kind = "abc"
        elif tab_systems(text):
            score = parse_tab(text, tuning, tab_step, bpm, program)
            kind = "tab"
        else:
            raise NotationError(f"cannot tell what {p.name} holds: use .abc, .mid, .musicxml/.mxl, or a text file of ASCII tab")
    if bpm and kind == "midi":
        # MIDI is timed: keep every note where it sounds and count it in the new tempo (notation of a performance)
        if len(score.tempos) > 1:
            score.warnings.append("the MIDI has tempo changes; --bpm re-counted it from the first tempo only")
        k = float(bpm) / score.tempos[0][1]
        for n in score.notes():
            n.start *= k
            n.dur *= k
        score.tempos = [(0.0, float(bpm))]
    elif bpm:
        score.tempos = [(0.0, float(bpm))]
        score.warnings = [w for w in score.warnings if "rendered at 120" not in w]
    if program is not None and kind != "tab":
        for t in score.tracks:
            if not t.drums and t.name != "chords":
                t.program = program
    if chords and getattr(score, "_chords", None):
        add_chord_track(score, score._chords, score.length_beats())
    elif getattr(score, "_chords", None):
        score.warnings.append(f"{len(score._chords)} chord symbols were not played (add --chords to play them)")
    return score, kind


def transpose(score, semitones):
    for n in score.notes():
        n.pitch += semitones


# ---------------------------------------------------------------- built-in synth (no SoundFont needed)

def synth_wav(score, path, rate=22050, tail=1.5):
    """Small additive and plucked-string synth: a preview and a source for an AI cover, not a final sound."""
    import random
    total = score.seconds(score.length_beats()) + tail
    n_samples = int(total * rate) + 1
    buf = [0.0] * n_samples
    rng = random.Random(7)
    for tr in score.tracks:
        prog = tr.program
        kind = "drum" if tr.drums else ("pluck" if 24 <= prog <= 39 or 104 <= prog <= 108 or prog in (6, 46) else
                                        "bell" if 8 <= prog <= 15 else "wind" if 64 <= prog <= 79 else "organ")
        for n in tr.notes:
            t0 = score.seconds(n.start)
            t1 = score.seconds(n.end())
            amp = 0.25 * (n.vel / 127.0)
            i0 = int(t0 * rate)
            if kind == "drum":
                ln = int(0.12 * rate)
                for k in range(ln):
                    if i0 + k < n_samples:
                        buf[i0 + k] += amp * (rng.random() * 2 - 1) * math.exp(-k / (0.03 * rate))
                continue
            f = 440.0 * 2 ** ((n.pitch - 69) / 12.0)
            if kind == "pluck":
                period = max(2, int(rate / f))
                ring = [rng.random() * 2 - 1 for _ in range(period)]
                ln = int(min(max(t1 - t0, 0.2) + 0.3, 4.0) * rate)
                decay = 0.996 if f < 200 else 0.994
                idx = 0
                for k in range(ln):
                    j = i0 + k
                    if j >= n_samples:
                        break
                    a = ring[idx]
                    b2 = ring[(idx + 1) % period]
                    ring[idx] = decay * 0.5 * (a + b2)
                    rel = 1.0 if t0 + k / rate < t1 else math.exp(-(t0 + k / rate - t1) / 0.08)
                    buf[j] += amp * 1.6 * a * rel
                    idx = (idx + 1) % period
                continue
            harm = {"wind": [(1, 1.0), (2, 0.25), (3, 0.08)], "bell": [(1, 1.0), (2.76, 0.4), (5.4, 0.2)],
                    "organ": [(1, 1.0), (2, 0.5), (3, 0.3), (4, 0.15)]}[kind]
            att, rel_t = (0.06, 0.12) if kind == "wind" else (0.005, 0.6 if kind == "bell" else 0.05)
            ln = int(((t1 - t0) + rel_t * 3) * rate)
            w = [2 * math.pi * f * h / rate for h, _ in harm]
            g = [a for _, a in harm]
            norm = sum(g)
            for k in range(ln):
                j = i0 + k
                if j >= n_samples:
                    break
                tt = k / rate
                env = min(1.0, tt / att) if tt < t1 - t0 else math.exp(-(tt - (t1 - t0)) / rel_t)
                if kind == "bell":
                    env *= math.exp(-tt / 1.2)
                if kind == "wind":
                    env *= 1 + 0.03 * math.sin(2 * math.pi * 5 * tt)
                s = 0.0
                for wi, gi in zip(w, g):
                    s += gi * math.sin(wi * k)
                buf[j] += amp * env * s / norm
    peak = max((abs(v) for v in buf), default=0.0) or 1.0
    scale = (10 ** (-3 / 20.0)) / peak
    with wave.open(str(path), "wb") as wv:
        wv.setnchannels(1)
        wv.setsampwidth(2)
        wv.setframerate(rate)
        frames = bytearray()
        for v in buf:
            frames += struct.pack("<h", int(max(-1.0, min(1.0, v * scale)) * 32767))
        wv.writeframes(bytes(frames))
    return path


# ---------------------------------------------------------------- audio -> notes (monophonic, librosa pyin)

def notes_from_f0(times, f0, voiced, rms=None, min_note=0.06, hop=None):
    """Frames of f0 (Hz or None) -> Notes in seconds (start, dur) with MIDI pitch, merged and cleaned."""
    hop = hop or (times[1] - times[0] if len(times) > 1 else 0.01)
    pitches = []
    for f, v in zip(f0, voiced):
        pitches.append(69 + 12 * math.log2(f / 440.0) if v and f and f > 0 else None)
    k = 2  # median-smooth the pitch track over 5 frames
    sm = []
    for i in range(len(pitches)):
        win = [p for p in pitches[max(0, i - k):i + k + 1] if p is not None]
        sm.append(sorted(win)[len(win) // 2] if pitches[i] is not None and win else None)
    notes, cur, start = [], None, 0
    vals = []
    for i, p in enumerate(sm + [None]):
        r = None if p is None else int(round(p))
        if cur is not None and (r is None or abs(p - cur) > 0.7):
            # the note's own median is the anchor, so a step reached by a smooth slide still splits;
            # the new pitch must hold 3 frames (vibrato and passing frames stay in the note)
            hold = r is not None and all(sm[j] is not None and abs(sm[j] - cur) > 0.7 and abs(sm[j] - p) < 0.6
                                         for j in range(i, min(i + 3, len(sm))))
            if r is None or hold:
                dur = (i - start) * hop
                if dur >= min_note:
                    vel = 90
                    if rms is not None:
                        seg = rms[start:i]
                        if seg:
                            db = 20 * math.log10(max(sum(seg) / len(seg), 1e-6))
                            vel = int(max(30, min(120, 110 + 2 * db)))
                    pitch = int(round(sorted(vals)[len(vals) // 2]))
                    notes.append(Note(times[start], dur, pitch, vel))
                cur = None
        if cur is None and r is not None:
            cur, start, vals = p, i, [p]
        elif cur is not None and p is not None:
            vals.append(p)
            cur = sorted(vals)[len(vals) // 2]
    return notes


def score_from_seconds(notes, bpm, program=73, name="transcription"):
    sc = Score()
    sc.tempos = [(0.0, float(bpm))]
    tr = Track(name, program)
    tr.mono = True
    k = bpm / 60.0
    for n in notes:
        tr.notes.append(Note(n.start * k, n.dur * k, n.pitch, n.vel))
    sc.tracks.append(tr)
    return sc
