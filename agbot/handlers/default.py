from aiogram import Dispatcher
from aiogram.types import Message

from agbot.services.orm import User


async def default_start(msg: Message):
    user, _ = User.get_or_add_from_tg_message(data=msg)
    await msg.reply(f"Hello, {user.username}")


def register_default(dp: Dispatcher):
    dp.register_message_handler(
        default_start,
        commands=["start"],
        state="*",
    )
