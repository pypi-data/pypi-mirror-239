#!/usr/bin/env python

# normalize rotations
import base64
import re
from io import BytesIO

from PIL import Image
from sqlalchemy import text

from puddl.pg import DB

pdl = DB('exif')
conn = pdl.engine.connect()


def img_from_b64(s):
    data = re.sub('^data:image/.+;base64,', '', s)
    return Image.open(BytesIO(base64.b64decode(data)))


def b64_to_data_jpg(img):
    buf = BytesIO()
    img.save(buf, format='JPEG')
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


if __name__ == '__main__':
    rows = conn.execute(text('SELECT id, thumb, rotation FROM markers WHERE rotation != 0'))
    for row in rows:
        img = img_from_b64(row.thumb).convert('RGB')
        # PIL.Image.rotate direction of rotation is counterclockwise
        # We have clockwise rotation in DB.
        pil_rotation = row.rotation * -1
        img = img.rotate(pil_rotation, expand=True)
        b64 = b64_to_data_jpg(img)
        conn.execute(
            text('UPDATE markers SET thumb=:thumb, rotation=0 WHERE id=:id'), parameters=dict(id=row.id, thumb=b64)
        )
    conn.commit()
