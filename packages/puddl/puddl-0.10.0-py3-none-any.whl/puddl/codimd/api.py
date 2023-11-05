import requests
import structlog

from puddl.codimd.models import Remote, Doc, Index

log = structlog.get_logger()


class CodiMDError(Exception):
    pass


def raise_on_alert_in_dom(response: requests.Response):
    """
    CodiMD seems not to know how to return non-200 HTTP status codes.
    So we look for "alert" in the DOM. *sigh*
    Could use beautiful soup or lxml for that, but meh.
    """
    o = response.text.find('alert')
    if o >= 0:
        raise CodiMDError(response.text[o : o + 200])  # noqa E203


class Driver:
    def __init__(self, remote: Remote):
        self.remote = remote
        self.s = requests.session()
        login = self.s.post(f'{remote.url}/login', data={'email': remote.email, 'password': remote.password})
        login.raise_for_status()

    def iter_history_raw(self):
        history = self.s.get(f'{self.remote.url}/history')
        history.raise_for_status()
        raise_on_alert_in_dom(history)
        records = history.json()['history']
        # [{'id': 'pycharm', 'text': 'pycharm', 'time': 1582037284079, 'tags': []}, ...]
        log.debug('history', records=records)
        for r in records:
            yield r

    def history(self) -> Index:
        docs = [Doc.model_validate(r) for r in self.iter_history_raw()]
        return {d.id: d for d in docs}

    def download(self, note_id: str) -> str:
        log.debug('download', note_id=note_id)
        r = self.s.get(f'{self.remote.url}/{note_id}/download')
        return r.text
