import re
import hashlib
import subprocess
import uuid
from typing import Callable, List


def gen_uuid_str() -> str:
    """gen uuid like this: 'df130e24-c7f9-11ea-befd-acde48001122'
    """
    return str(uuid.uuid1())


def plain2md5(s: str, encoding='utf8') -> str:
    if isinstance(s, str):
        s = s.encode(encoding)
    elif not isinstance(s, bytes):
        raise TypeError("Unsupported type %r" % type(s))
    return hashlib.md5(s).hexdigest()


def is_url(url: str) -> bool:
    return True if re.match(r'^https?:\/\/.+', url) else False


def execute_cmd(cmd: List, timeout: int, on_lines: Callable):
    """execute cmd
    """
    proc = subprocess.run(cmd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          timeout=timeout,
                          check=True,
                          universal_newlines=True)
    for line in proc.stdout.split("\n"):
        line = line.strip()
        if not line:
            continue
        on_lines(line)
