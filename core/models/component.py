import enum
from typing import List

from sqlalchemy import exc as sqlalchemy_exc

from .base import BaseModel, db


@enum.unique
class ComponentType(enum.Enum):
    others = 0
    cms = 1
    os = 2
    middleware = 3
    database = 4
    device = 5
    service = 6
    service_provider = 7
    general = 8

    @classmethod
    def all_kinds(cls) -> List:
        return [c.name for c in cls]


class Component(BaseModel):
    __tablename__ = "component"

    c_id = db.Column(db.String(40), unique=True, nullable=False)
    c_name = db.Column(db.String(64), unique=True, nullable=False)
    c_first = db.Column(db.String(10), nullable=False)
    c_type = db.Column(db.String(40), nullable=False)

    author = db.Column(db.String(64))
    version = db.Column(db.String(10))
    website = db.Column(db.String(255))
    desc = db.Column(db.Text)
    producer = db.Column(db.String(100))
    properties = db.Column(db.Text)

    condition = db.Column(db.String(255))
    matches = db.Column(db.Text, nullable=False)
    implies = db.Column(db.Text)
    excludes = db.Column(db.Text)

    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Component %r>' % self.c_name
