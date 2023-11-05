from pathlib import Path

import pytest

from puddl.bash_history.parser import iter_bash_history


@pytest.fixture
def content():
    return """\
cat /tmp/something
#1585254366
cat <<EOF > /tmp/hello
world
EOF
#1585254441
tail ~/.bash_history
#1585254727
# this is a comment
echo and it's valid.
"""


@pytest.fixture
def bash_history_path(tmp_path, content) -> Path:
    path = tmp_path / 'example.bash_history'
    path.write_text(content)
    return path


def test_hist2dict(bash_history_path):
    with bash_history_path.open() as f:
        actual = list(iter_bash_history(f))
    multiline = """\
cat <<EOF > /tmp/hello
world
EOF\
"""
    expected = [
        (1585254366, multiline),
        (1585254441, 'tail ~/.bash_history'),
        (1585254727, "# this is a comment\necho and it's valid."),
    ]
    assert actual == expected
