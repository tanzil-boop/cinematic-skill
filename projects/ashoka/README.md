# Ashoka: The King and His Empire / राजा और उसका राज्य

Two narrated documentaries made with the cinematic-film skill: the same story of Emperor Ashoka and the
Kalinga war, once in English (`king-en`, about 75 s) and once in Hindi (`raja-hi`, about 91 s).
Both share one scene (`shared/ashoka_scene.py`); each film times itself to its own voice.

Narration is made offline with [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) (voices `bm_george` for
English, `hm_omega` for Hindi), so no script text is sent to any outside service. The score was composed
offline with MusicGen (`tools/musicgen.py`, cues in `music/`), and a code-synthesised wind bed
(`tools/ambience.py`) sits under the battle scenes. Photos are free-licence images from Wikimedia Commons; see each `credits.md`.

## Rebuild

Setup (Linux): `pip install -r requirements.txt piper-tts`, ffmpeg, and `apt install libegl1 libgl1`
(skia-python needs them). Download the Piper voices into a folder `$V`:
`en_US-ryan-high` and `hi_IN-rohan-medium` (`.onnx` and `.onnx.json`) from huggingface.co/rhasspy/piper-voices.

From `skills/cinematic-film/scripts`, with `P=../../../projects/ashoka/king-en` (or `raja-hi`):

```bash
# images: photos.json has direct Commons thumbnail URLs; download each "url" to assets/photos/<file>
python3 prep_assets.py --project $P
python3 tts_say.py --project $P --cmd "python3 ../../../projects/ashoka/tools/kokoro_take.py --voice bm_george --lang en-gb --txt {txt} --out {out}"
python3 split_takes.py --project $P && python3 build_narration.py --project $P
python3 render.py --project $P --cues && python3 build_sfx.py --project $P && python3 ../../../projects/ashoka/tools/ambience.py $P
python3 ../../../projects/ashoka/tools/score.py $P ../../../projects/ashoka/music
python3 mix_soundtrack.py --project $P --music audio/score.wav --music-db -4 --sfx-db -3 --duck-ratio 3 --duck-threshold 0.03 --music-level 0.09 --music-eq-dip 4
python3 render.py --project $P --size 1920x1080 --out out/final.mp4 --audio audio/mix.m4a
python3 burn_captions.py --project $P --video out/final.mp4 --audio audio/mix.m4a --style highlighter --out out/final_captions.mp4
```

For Hindi use `--voice hm_omega --lang hi`. Kokoro model files (`kokoro-v1.0.onnx`, `voices-v1.0.bin`)
come from the kokoro-onnx GitHub releases; set `KOKORO_DIR` to their folder. Commons rate-limits uncached sizes:
if a download returns HTTP 429, wait or try another standard width (1920, 1280, 960).

Generated folders (`assets/`, `audio/`, `out/`) are not committed; they rebuild from the files here.
