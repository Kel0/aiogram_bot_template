from typing import Optional, Tuple

from aiogram.types import Message
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin

from agbot.models.role import UserRole

from .db_conn import base


class BaseModel(base, AllFeaturesMixin, TimestampsMixin):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)

    def __init__(self, *args, **kwargs):
        pass


class User(BaseModel):
    __tablename__ = "users"

    telegram_id = Column(Integer, unique=True)
    username = Column(String(length=255))
    role = Column(String(length=30), default=UserRole.DEFAULT.value)
    active = Column(Boolean, default=True)

    @classmethod
    def add_from_tg_message(
        cls, data: Message, role: Optional[UserRole] = UserRole.DEFAULT
    ) -> "User":
        instance = cls.create(
            telegram_id=data.chat.id, username=data.chat.username, role=role.value
        )
        return instance

    @classmethod
    def get_or_add_from_tg_message(
        cls, data: Message, role: Optional[UserRole] = UserRole.DEFAULT
    ) -> Tuple["User", bool]:
        is_created = False
        instance = cls.where(telegram_id=data.from_user.id).all()

        if not len(instance):
            instance = cls.create(
                telegram_id=data.from_user.id,
                username=data.from_user.username,
                role=role.value,
            )
            is_created = True

        return instance if isinstance(instance, User) else instance[0], is_created
