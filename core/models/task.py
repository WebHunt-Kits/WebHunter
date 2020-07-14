from sqlalchemy import exc as sqlalchemy_exc

from .base import BaseModel, db


class Task(BaseModel):
    __tablename__ = "task"

    t_id = db.Column(db.String(64), unique=True, nullable=False)
    owner = db.Column(db.String(32), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    result = db.Column(db.JSON)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Task %r>' % self.t_id
