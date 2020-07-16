import uuid
import hashlib


def gen_uuid_str() -> str:
    return str(uuid.uuid1())


def plain2md5(s: str, encoding='utf8') -> str:
    if isinstance(s, str):
        s = s.encode(encoding)
    elif not isinstance(s, bytes):
        raise TypeError("Unsupported type %r" % type(s))
    return hashlib.md5(s).hexdigest()
