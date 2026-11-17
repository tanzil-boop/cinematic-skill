#!/usr/bin/env python3
"""Battlefield ambience bed (code-synthesised, nothing to license): gusting wind over an open plain, plus a
low rumble, laid under the cold open and the Kalinga war, then a quieter breeze for the close.
Adds it into audio/sfx.wav so mix_soundtrack.py picks it up.  usage: ambience.py PROJECT"""
import json, sys, pathlib
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

proj = pathlib.Path(sys.argv[1]); seg = {s["id"]: s for s in json.loads((proj / "audio/timing.json").read_text())["segments"]}
sfx, sr = sf.read(proj / "audio/sfx.wav", always_2d=True)
n = len(sfx); t = np.arange(n) / sr; rng = np.random.default_rng(7)

def band(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], btype="band", fs=sr, output="sos"), x)

def gusts(seed, rate):
    r = np.random.default_rng(seed); k = int(n / sr * rate) + 4
    env = np.interp(t, np.linspace(0, t[-1], k), r.uniform(0.25, 1.0, k))
    return sosfilt(butter(1, 0.6, fs=sr, output="sos"), env)

out = np.zeros((n, 2))
for ch in range(2):
    white = rng.standard_normal(n)
    wind = band(white, 180, 900) * gusts(11 + ch, 0.35) + 0.5 * band(white, 900, 2600) * gusts(21 + ch, 0.6) ** 2
    rumble = band(rng.standard_normal(n), 30, 110) * 2.5
    out[:, ch] = wind + rumble * (t < seg[5]["start"])

def win(a, b, fade=1.5):
    return np.clip(np.minimum((t - a) / fade, (b - t) / fade), 0, 1)

level = (0.9 * win(0, seg[5]["start"] + 1.0) + 0.75 * win(seg[9]["start"] - 0.5, seg[11]["end"] + 1.0)
         + 0.35 * win(seg[17]["start"] - 1.0, t[-1] + 2))
out *= level[:, None]
out *= 10 ** (-27 / 20) / (np.sqrt(np.mean(out[level > 0.5] ** 2)) + 1e-9)     # about -27 dBFS RMS: felt, not noticed
sf.write(proj / "audio/sfx.wav", np.clip(sfx + out, -1, 1), sr)
print(f"ambience added to {proj}/audio/sfx.wav")
