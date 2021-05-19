from decouple import config


TELEGRAM_BOT_API_TOKEN = config("TELEGRAM_BOT_API_TOKEN", cast=str)
DATABASE_URL = config("DATABASE_URL", cast=str)
ADMIN_IDS = config("ADMIN_IDS", cast=str).split(",")
USE_REDIS = config("USE_REDIS", cast=str)
