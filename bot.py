import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from agbot.config import load_config
from agbot.filters.role import RoleFilter, AdminFilter
from agbot.handlers.default import register_default
from agbot.handlers.admin import register_admin
from agbot.middlewares.database import DatabaseSessionMiddleware
from agbot.middlewares.role import RoleMiddleware
from agbot.services.db_conn import session, engine, base
from agbot.services.orm import BaseModel

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config()

    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)

    base.metadata.create_all(engine)
    BaseModel.set_session(session)

    dp.middleware.setup(DatabaseSessionMiddleware(session))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_default(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
