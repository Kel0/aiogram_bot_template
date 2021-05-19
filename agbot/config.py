from dataclasses import dataclass

from settings import ADMIN_IDS, DATABASE_URL, TELEGRAM_BOT_API_TOKEN, USE_REDIS


@dataclass
class DbConfig:
    link: str


@dataclass
class TgBot:
    token: str
    admin_id: list
    use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config():
    return Config(
        tg_bot=TgBot(
            token=TELEGRAM_BOT_API_TOKEN,
            admin_id=[int(_id) for _id in ADMIN_IDS],
            use_redis=cast_bool(USE_REDIS),
        ),
        db=DbConfig(DATABASE_URL),
    )
