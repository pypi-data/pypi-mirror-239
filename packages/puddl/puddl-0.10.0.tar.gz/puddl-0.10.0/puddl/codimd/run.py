#!/usr/bin/env python
import os
from pathlib import Path

import structlog

from puddl.codimd import Remote, Driver
from puddl.codimd.index import Pickler

dir = Path('~/puddl/md').expanduser()
persistence = Pickler(dir / '_index.pickle')

log = structlog.get_logger()
remote = Remote(
    url=os.environ['CODIMD_URL'],
    email=os.environ['CODIMD_EMAIL'],
    password=os.environ['CODIMD_PASSWORD'],
)

driver = Driver(remote)

remote_docs = driver.history()
local_docs = persistence.read(fallback={})

new_ids = remote_docs.keys() - local_docs.keys()
outdated_ids = local_docs.keys() - remote_docs.keys()
if outdated_ids:
    log.info('found outdated. doing nothing. :>', count=len(outdated_ids))
maybe_update = remote_docs.keys() & local_docs.keys()


def iter_changed_docs():
    for x in new_ids:
        yield remote_docs[x]
    for key in maybe_update:
        rdoc = remote_docs[key]
        local = local_docs[key]
        if rdoc.time > local.time:
            log.info('new', doc=rdoc)
            yield rdoc


changed = iter_changed_docs()

for doc in changed:
    content = driver.download(doc.id)
    path = dir / f'{doc.id}.md'
    path.write_text(content)
    log.info('download', len=len(content), path=path, doc=doc)

persistence.write(remote_docs)
