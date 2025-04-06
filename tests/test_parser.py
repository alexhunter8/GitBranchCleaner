import shlex
from subprocess import Popen, PIPE

def test_version():
    p = Popen(shlex.split('python3 src/gbclean.py --version'), stdout=PIPE)
    out = p.communicate()[0].decode().strip()
    assert out
