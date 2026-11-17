#!/usr/bin/env python3
"""Offline narration for one take with Kokoro (natural neural voice, runs locally; nothing leaves this machine).
Each paragraph of the text file is one line; lines are joined with a clear pause for split_takes.py.

  python3 kokoro_take.py --voice bm_george --lang en-gb --txt take.txt --out take.wav [--speed 0.95] [--pause 0.8]
"""
import argparse, os, pathlib
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

D = pathlib.Path(os.environ.get("KOKORO_DIR", "/home/user/voices/kokoro"))
ap = argparse.ArgumentParser()
ap.add_argument("--voice", required=True); ap.add_argument("--lang", default="en-gb")
ap.add_argument("--txt", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--speed", type=float, default=0.95); ap.add_argument("--pause", type=float, default=0.8)
a = ap.parse_args()
k = Kokoro(str(D / "kokoro-v1.0.onnx"), str(D / "voices-v1.0.bin"))
lines = [p.strip().replace("\n", " ") for p in pathlib.Path(a.txt).read_text().split("\n\n") if p.strip()]
parts, sr = [], 24000
for line in lines:
    audio, sr = k.create(line, voice=a.voice, speed=a.speed, lang=a.lang)
    parts.append(np.asarray(audio, dtype=np.float32))
gap = np.zeros(int(sr * a.pause), np.float32); lead = np.zeros(int(sr * 0.3), np.float32)
out = [lead]
for i, p in enumerate(parts):
    out += ([gap] if i else []) + [p]
sf.write(a.out, np.concatenate(out + [lead]), sr)
