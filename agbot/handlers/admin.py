from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from agbot.models.role import UserRole
from agbot.services.orm import User
from agbot.models.states import UseState


async def admin_start(msg: Message):
    data = ctx_data.get()
    user, _ = User.get_or_add_from_tg_message(data=msg)
    await msg.reply(f"Hello, {user.username}, your role is {data['role'].value}!")


async def use_state(msg: Message):
    await UseState.who.set()
    await msg.reply("GO")


async def use_state_step(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data["who"] = msg.text
        await msg.reply(data["who"])

    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, commands=["start"], state="*", role=UserRole.ADMIN
    )
    dp.register_message_handler(
        use_state, commands=["state1"], state="*", role=UserRole.ADMIN
    )
    dp.register_message_handler(
        use_state_step, state=UseState.who, role=UserRole.ADMIN
    )

