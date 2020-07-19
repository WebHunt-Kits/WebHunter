from enum import Enum


class APIErrorStausCode(Enum):
    # start with 1000
    DATABASE_ERR = {
        "status": 400,
        "code": 1001,
        "message": "database error"
    }
    EXCLUDED_DOMAIN = {
        "status": 400,
        "code": 1002,
        "message": "excluded domain"
    }
    NOT_URL = {
        "status": 400,
        "code": 1003,
        "message": "not url"
    }
