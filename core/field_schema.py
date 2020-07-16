from typing import Dict

from core.models.component import ComponentType


def make_new_sch(src: Dict, new_items: Dict) -> Dict:
    r = {}
    r.update(**src, **new_items)
    return r


APISIGN_SCH = {
    "sign": {
        "type": "string",
        "empty": False,
        "required": True
    },
    "ts": {
        "type": "string",
        "empty": False,
        "required": True
    }
}
COMPONENT_TYPE_REGEX = "^(%s)$" % "|".join(ComponentType.all_kinds())
COMPONENT_FIRST_REGEX = "^[a-z]{1}$"
PAGINATE_SCH = {
    "page": {
        "type": "string",
        "regex": "^[0-9]+$"

    },
    "per_page": {
        "type": "string",
        "regex": "^[0-9]{1,3}$",
    }
}
COMPONENTS_GET_SCHEMA = {
    "name": {
        "type": "string",
        "empty": False
    },
    "page": PAGINATE_SCH["page"],
    "per_page": PAGINATE_SCH["per_page"],
    "type": {
        "type": "string",
        "regex": COMPONENT_TYPE_REGEX
    },
    "first": {
        "type": "string",
        "regex": COMPONENT_FIRST_REGEX
    },
    "ts": APISIGN_SCH["ts"],
    "sign": APISIGN_SCH["sign"]
}
