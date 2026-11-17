#!/usr/bin/env python3
"""Lay the three score cues to a film's sections: A (cold open), B (empire + war, lines 5-11), C (dhamma + close).
Each cue loops if its section is longer, and the joins crossfade over 2.5 s.  usage: score.py PROJECT MUSIC_DIR"""
import json, sys, pathlib
import numpy as np, soundfile as sf
from scipy.signal import resample_poly

proj, md = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
tm = json.loads((proj / "audio/timing.json").read_text()); seg = {s["id"]: s for s in tm["segments"]}
SR, X = 48000, 2.5
total = tm["total_duration"] + 3
bounds = [0, seg[5]["start"] - 0.6, seg[12]["start"] - 0.8, total]
out = np.zeros(int(total * SR) + SR)
for k, name in enumerate("ABC"):
    a, sr = sf.read(md / f"cue{name}.wav"); a = a if a.ndim == 1 else a.mean(1)
    a = resample_poly(a, SR, sr); a /= np.abs(a).max() + 1e-9
    t0, t1 = bounds[k], bounds[k + 1] + (X if k < 2 else 0)
    n = int((t1 - t0) * SR); piece = np.tile(a, n // len(a) + 1)[:n]
    env = np.ones(n); f = int(X * SR)
    if k: env[:f] = np.linspace(0, 1, f)
    if k < 2: env[-f:] = np.minimum(env[-f:], np.linspace(1, 0, f))
    i0 = int(t0 * SR); out[i0:i0 + n] += piece * env
sf.write(proj / "audio/score.wav", np.stack([out, out], 1) * 0.8, SR)
print("score", proj / "audio/score.wav", f"{total:.1f}s")
