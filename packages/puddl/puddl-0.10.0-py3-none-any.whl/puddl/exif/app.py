from pathlib import Path

from flask import Flask, send_from_directory
from sqlalchemy import text

from puddl.pg import DB

app = Flask(__name__)
pdl = DB('exif')
conn = pdl.engine.connect()
root = Path('.').absolute()


@app.route('/')
def index():
    return send_from_directory(root, 'index.html')


@app.route('/<path:path>')
def _home(path):
    print(path)
    return send_from_directory(root, path)


@app.route("/space")
def space():
    data = []
    rows = conn.execute(
        text('SELECT id, lat, lng, alt, thumb, rotation, url, dt, since_start FROM markers ORDER BY dt ASC')
    )

    for row in rows:
        d = dict(zip(rows.keys(), row))
        data.append(d)
    return {'rows': data}


@app.route("/time")
def time():
    return {
        'tmin': conn.execute(text('SELECT min(dt) FROM markers')).scalar(),
        'tmax': conn.execute(text('SELECT max(dt) FROM markers')).scalar(),
    }
