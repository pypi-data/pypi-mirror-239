from pathlib import Path

from tinytag import TinyTag


def duration(p: Path):
    tag = TinyTag.get(p)
    return tag.duration
