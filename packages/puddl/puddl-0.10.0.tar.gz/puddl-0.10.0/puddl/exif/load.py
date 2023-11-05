#!/usr/bin/env python
import base64
import sys
from pathlib import Path

import exifread
import pandas as pd
import structlog

from puddl.pg import DB

log = structlog.get_logger()


def img2dict(path: Path):
    # basics
    result = {'_path': str(path), '_name': path.name}
    # exif
    with path.open('rb') as f:
        exif_data = exifread.process_file(f)
        for k, v in exif_data.items():
            if isinstance(v, exifread.classes.IfdTag):
                exif_data[k] = v.printable
        result.update(exif_data)
    # thumb
    if 'JPEGThumbnail' in result:
        # noinspection PyTypeChecker
        payload = base64.b64encode(result['JPEGThumbnail']).decode('utf-8')
        img = 'data:image/jpeg;base64,' + payload
    else:
        img = (
            'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQ'
            'AAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
        )
    result['thumb'] = img
    return result


def main():
    directory = Path(sys.argv[1]).expanduser()

    imgs = list(directory.glob('*.jpg'))
    if not imgs:
        raise Exception('No images')
    log.info(f'processing {len(imgs)} images')

    db = DB('exif')
    log.info('connected to database', name=db.name)

    df = pd.DataFrame(img2dict(img) for img in imgs)
    db.df_dump(df, 's7', drop_cascade=True)


if __name__ == '__main__':
    main()
