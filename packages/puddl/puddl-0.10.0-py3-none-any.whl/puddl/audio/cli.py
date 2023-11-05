from pathlib import Path

import click

import puddl.audio
from puddl.cli.base import root


@root.command(name='duration')
@click.argument('paths', type=Path, nargs=-1)
def duration(paths: [Path]):
    """
    Sum of audio duration of PATHS.
    """
    x = sum(puddl.audio.duration(path) for path in paths)
    print(x)
