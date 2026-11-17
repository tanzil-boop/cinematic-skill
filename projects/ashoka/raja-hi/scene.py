import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "shared"))
from ashoka_scene import build  # noqa: E402


def build_film(doc):
    return build(doc, "hi")
