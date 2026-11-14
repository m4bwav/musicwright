"""Per-frame audio envelopes for visuals: band energies, 200 ms loudness, onsets, beats and chroma.

Standard-library Python 3.9+. The caller (mw.py envelopes) decodes the audio with ffmpeg and hands over mono
float samples at two rates: the main rate for every band above 200 Hz, and a quarter rate for the sub-bass
bands, so the same 1024-point FFT covers a four-times longer window there (bass needs the longer frame to
resolve 20-100 Hz). Pure-Python FFT; slow on long songs but needs nothing installed.
"""
import cmath
import math

# Zwicker critical-band (Bark) edges in Hz.
BARK_EDGES = [20, 100, 200, 300, 400, 510, 630, 770, 920, 1080, 1270, 1480, 1720, 2000, 2320, 2700, 3150,
              3700, 4400, 5300, 6400, 7700, 9500, 12000, 15500]
LONG_FRAME_TOP_HZ = 200  # bands whose upper edge is at or below this use the long frame
NFFT = 1024


def band_edges(spec, nyquist):
    """'critical' -> Bark edges under Nyquist; an integer N -> N log-spaced bands from 30 Hz to 0.95 Nyquist."""
    top = nyquist * 0.95
    if str(spec).strip().lower() == "critical":
        edges = [e for e in BARK_EDGES if e <= top]
        if edges[-1] < top and len(edges) < len(BARK_EDGES):
            edges.append(int(top))
        return [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
    n = int(spec)
    if not 1 <= n <= 64:
        raise ValueError("--bands takes 'critical' or a number from 1 to 64")
    lo, hi = 30.0, top
    e = [lo * (hi / lo) ** (i / n) for i in range(n + 1)]
    return [(round(e[i], 1), round(e[i + 1], 1)) for i in range(n)]


_TW = {}


def fft(x):
    """Iterative radix-2 FFT of a real list whose length is a power of two; returns complex list."""
    n = len(x)
    a = [complex(v) for v in x]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        tw = _TW.get(size)
        if tw is None:
            tw = _TW[size] = [cmath.exp(-2j * math.pi * k / size) for k in range(size // 2)]
        half = size // 2
        for start in range(0, n, size):
            for k in range(half):
                u = a[start + k]
                v = a[start + k + half] * tw[k]
                a[start + k] = u + v
                a[start + k + half] = u - v
        size <<= 1
    return a


_HANN = [0.5 - 0.5 * math.cos(2 * math.pi * i / NFFT) for i in range(NFFT)]


def power_spectrum(samples, centre):
    """Hann-windowed power spectrum (first NFFT/2+1 bins) of the frame centred on sample index `centre`."""
    start = centre - NFFT // 2
    frame = [0.0] * NFFT
    n = len(samples)
    for i in range(NFFT):
        k = start + i
        if 0 <= k < n:
            frame[i] = samples[k] * _HANN[i]
    try:
        import numpy as np  # optional speed-up only; the stdlib path gives the same numbers
        s = np.fft.rfft(np.asarray(frame))
        return (s.real ** 2 + s.imag ** 2).tolist()
    except ImportError:
        s = fft(frame)
        return [(c.real * c.real + c.imag * c.imag) for c in s[:NFFT // 2 + 1]]


def _median(v):
    s = sorted(v)
    m = len(s) // 2
    return s[m] if len(s) % 2 else 0.5 * (s[m - 1] + s[m])


def compute(main, rate, low, low_rate, fps, bands_spec="critical"):
    """main/low: mono float samples in -1..1 at rate and low_rate. Returns the envelope dict."""
    duration = len(main) / float(rate)
    frames = max(1, int(math.floor(duration * fps + 1e-9)))
    bands = band_edges(bands_spec, rate / 2.0)
    long_ok = low is not None and low_rate
    meta = []
    for lo, hi in bands:
        use_long = bool(long_ok and hi <= LONG_FRAME_TOP_HZ and hi < low_rate / 2.0)
        r = low_rate if use_long else rate
        b0 = max(1, int(math.floor(lo * NFFT / r)))
        b1 = max(b0 + 1, int(math.ceil(hi * NFFT / r)))
        meta.append({"lo_hz": lo, "hi_hz": hi, "frame_ms": round(1000.0 * NFFT / r, 1), "bins": (b0, b1), "long": use_long})
    # chroma bins from the main spectrum, 65-2000 Hz
    chroma_map = []
    for k in range(1, NFFT // 2 + 1):
        f = k * rate / float(NFFT)
        if 65 <= f <= 2000:
            midi = 69 + 12 * math.log2(f / 440.0)
            chroma_map.append((k, int(round(midi)) % 12))
    energy_db, loud_db, flux, chroma = [], [], [], []
    prev_logmag = None
    win = int(0.2 * rate)
    sq = [0.0] * (len(main) + 1)  # prefix sums of squares for the 200 ms RMS
    acc = 0.0
    for i, v in enumerate(main):
        acc += v * v
        sq[i + 1] = acc
    for f in range(frames):
        t = f / float(fps)  # frame f is the picture shown at f/fps; its windows are centred there
        c = int(t * rate)
        ps = power_spectrum(main, c)
        pl = power_spectrum(low, int(t * low_rate)) if long_ok and any(m["long"] for m in meta) else None
        row = []
        for m in meta:
            spec = pl if m["long"] else ps
            b0, b1 = m["bins"]
            e = sum(spec[b0:min(b1, len(spec))]) / (NFFT * NFFT / 4.0)
            row.append(10 * math.log10(e + 1e-12))
        energy_db.append(row)
        a0, a1 = max(0, c - win // 2), min(len(main), c + win // 2)
        ms = (sq[a1] - sq[a0]) / max(1, a1 - a0)
        loud_db.append(10 * math.log10(ms + 1e-12))
        logmag = [math.log1p(1000.0 * v) for v in ps[1:]]
        flux.append(0.0 if prev_logmag is None else sum(max(0.0, x - y) for x, y in zip(logmag, prev_logmag)))
        prev_logmag = logmag
        ch = [0.0] * 12
        for k, pc in chroma_map:
            ch[pc] += ps[k]
        mx = max(ch)
        chroma.append([round(x / mx, 3) if mx > 1e-9 else 0.0 for x in ch])
    # per-band 0..1 with a 60 dB floor under the band's own peak, and an absolute floor so silence stays 0
    norm = []
    peaks = [max(r[i] for r in energy_db) for i in range(len(meta))]
    for r in energy_db:
        norm.append([round(min(1.0, max(0.0, (v - max(peaks[i] - 60.0, -100.0)) / 60.0)), 3) if peaks[i] > -100 else 0.0
                     for i, v in enumerate(r)])
    onsets, beats, tempo = _onsets_and_beats(flux, fps)
    loud_norm = [round(min(1.0, max(0.0, (v + 60.0) / 60.0)), 3) for v in loud_db]
    return {
        "fps": fps, "frames": frames, "duration_s": round(duration, 4), "rate": rate,
        "bands": [{"lo_hz": m["lo_hz"], "hi_hz": m["hi_hz"], "frame_ms": m["frame_ms"]} for m in meta],
        "energy": norm, "energy_db": [[round(v, 2) for v in r] for r in energy_db],
        "loudness_db": [round(v, 2) for v in loud_db], "loudness": loud_norm, "loudness_window_ms": 200,
        "onset_strength": [round(v, 3) for v in flux], "onsets": onsets, "beats": beats, "beat_frames": [int(round(b * fps)) for b in beats], "tempo_bpm": tempo,
        "chroma": chroma,
        "notes": "energy: per band 0..1 over a 60 dB range under the band's own peak; loudness: 200 ms RMS dBFS "
                 "(not K-weighted LUFS); bands at or under 200 Hz use a 4x longer frame",
    }


def _onsets_and_beats(flux, fps):
    n = len(flux)
    if n < 3 or max(flux) <= 1e-6:
        return [], [], None
    peak = max(flux)
    half = max(1, int(0.5 * fps))
    onsets = []
    last = -10 ** 9
    for i in range(1, n - 1):
        v = flux[i]
        if v < 0.1 * peak or v < flux[i - 1] or v < flux[i + 1]:
            continue
        local = flux[max(0, i - half):i + half + 1]
        if v < _median(local) + 0.05 * peak:
            continue
        if i - last < max(1, int(0.05 * fps)):
            continue
        onsets.append(i)
        last = i
    # tempo by autocorrelation of the flux, 60-200 bpm
    mean = sum(flux) / n
    d = [v - mean for v in flux]
    best, period = None, None
    for p in range(max(1, int(fps * 60 / 200)), min(n - 1, int(fps * 60 / 60)) + 1):
        s = sum(d[i] * d[i + p] for i in range(n - p)) / (n - p)
        if best is None or s > best:
            best, period = s, p
    beats, tempo = [], None
    if period and len(onsets) >= 4:
        # refine the period from the onset spacing near it
        gaps = [b - a for a, b in zip(onsets, onsets[1:]) if abs((b - a) - period) <= max(1, period * 0.2)]
        per = (sum(gaps) / len(gaps)) if gaps else float(period)
        tempo = round(60.0 * fps / per, 1)
        # phase: the onset sequence best explained by a grid; snap each predicted beat to the nearest onset
        tol = max(1, int(round(per * 0.15)))
        t = float(onsets[0])
        while t < n:
            i = int(round(t))
            near = [o for o in onsets if abs(o - i) <= tol]
            if near:
                i = min(near, key=lambda o: abs(o - i))
                t = float(i)
            beats.append(i)
            t += per
    return [round(i / float(fps), 4) for i in onsets], [round(i / float(fps), 4) for i in beats], tempo
