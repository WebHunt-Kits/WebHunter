from typing import Dict, Tuple

from flask_mico.error import AppError
from sqlalchemy import exc as sqlalchemy_exc

from core.errors import APIErrorStausCode

from .base import BaseModel, db


class User(BaseModel):
    """user
    """
    __tablename__ = "user"

    username = db.Column(db.String(32), unique=True,
                         nullable=False, comment="用户名")
    avatar_url = db.Column(db.String(255), comment="头像")
    email = db.Column(db.String(128))

    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def get_user(cls, name: str):
        try:
            return cls.query.filter_by(
                username=name, deleted_at=None).first()
        except sqlalchemy_exc.SQLAlchemyError:
            raise AppError(APIErrorStausCode.DATABASE_ERR)

    @classmethod
    def create_gh_user(cls, info: Dict) -> Tuple[str, str]:
        username = info["login"]
        avatar_url = info["avatar_url"]
        email = info["email"]
        user = cls.get_user(username)
        if not user:
            user = cls(username=username, avatar_url=avatar_url, email=email)
            db.session.add(user)
            db.session.commit()
        return username, avatar_url
