from typing import Dict

from core.models.component import ComponentType


def make_new_sch(src: Dict, new_items: Dict) -> Dict:
    r = {}
    r.update(**src, **new_items)
    return r


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
        "empty": False,
        "excludes": ["page", "per_page", "type", "first"]
    },
    "page": make_new_sch(PAGINATE_SCH["page"], {"excludes": "name"}),
    "per_page":  make_new_sch(PAGINATE_SCH["per_page"], {"excludes": "name"}),
    "type": {
        "type": "string",
        "regex": COMPONENT_TYPE_REGEX,
        "excludes": "name"
    },
    "first": {
        "type": "string",
        "regex": COMPONENT_FIRST_REGEX,
        "excludes": "name"
    }
}
