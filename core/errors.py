from enum import Enum


class APIErrorStausCode(Enum):
    # start with 1000
    DATABASE_ERR = {
        "status": 400,
        "code": 1001,
        "message": "database error"
    }
