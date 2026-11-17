#!/usr/bin/env python3
"""Offline narration for one take: each paragraph of the text file is one line, read with Piper,
joined with a clear pause so split_takes.py can cut between lines. Nothing leaves this machine.

  python3 piper_take.py --model VOICE.onnx --txt take.txt --out take.wav [--pause 0.8] [--length 1.05]
"""
import argparse, subprocess, sys, tempfile, wave, pathlib

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True); ap.add_argument("--txt", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--pause", type=float, default=0.8); ap.add_argument("--length", type=float, default=1.05)
ap.add_argument("--sentence", type=float, default=0.35, help="silence between sentences inside one line")
a = ap.parse_args()
lines = [p.strip().replace("\n", " ") for p in pathlib.Path(a.txt).read_text().split("\n\n") if p.strip()]
frames, params = [], None
with tempfile.TemporaryDirectory() as tmp:
    for i, line in enumerate(lines):
        w = pathlib.Path(tmp) / f"{i}.wav"
        r = subprocess.run([sys.executable, "-m", "piper", "-m", a.model, "-f", str(w), "--length-scale", str(a.length),
                            "--sentence-silence", str(a.sentence)], input=line, text=True, capture_output=True)
        if r.returncode:
            sys.exit(r.stderr[-1500:])
        with wave.open(str(w)) as f:
            params = params or f.getparams()
            frames.append(f.readframes(f.getnframes()))
gap = b"\x00" * int(params.framerate * a.pause) * params.sampwidth * params.nchannels
lead = b"\x00" * int(params.framerate * 0.3) * params.sampwidth * params.nchannels
with wave.open(a.out, "wb") as o:
    o.setparams(params); o.writeframes(lead + gap.join(frames) + lead)
