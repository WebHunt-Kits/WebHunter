import uuid

from pypinyin import Style, pinyin


def gen_uuid_str() -> str:
    return str(uuid.uuid1())


def get_pinyin_first_letter(name: str) -> str:
    try:
        # https://github.com/mozillazg/python-pinyin
        return pinyin(name, style=Style.INITIALS, strict=False)[0][0][0].lower()
    # pylint: disable=bare-except
    except:
        return 'z'
