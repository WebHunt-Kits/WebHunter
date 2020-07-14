from datetime import datetime
from typing import Tuple

from core.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    _id = db.Column('_id', db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self, ignore_cols: Tuple[str]):
        r = {}
        for column in self.__table__.columns:
            if column.name in ignore_cols:
                continue
            val = getattr(self, column.name)
            if isinstance(val, datetime):
                val = val.strftime("%Y-%m-%d %H:%M:%S")
            r[column.name] = val
        return r
