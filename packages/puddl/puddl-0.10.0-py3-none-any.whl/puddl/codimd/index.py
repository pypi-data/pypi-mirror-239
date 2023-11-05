import pickle
from pathlib import Path

import structlog

from .models import Index

log = structlog.get_logger()


class Pickler:
    def __init__(self, path: Path):
        self.path = path

    def write(self, x: Index):
        with self.path.open('wb') as f:
            pickle.dump(x, f)

    def read(self, fallback=None) -> Index:
        try:
            with self.path.open('rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            log.info('no index')
            return fallback
