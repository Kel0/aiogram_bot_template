from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy.orm import Session

from agbot.models.orm import Orm


class DatabaseSessionMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    async def pre_process(self, obj, data, *args):
        try:
            self.session.connection()
            data["session"] = self.session
            data.update({"orm": Orm})

        except Exception as e:
            print(e)
            self.session.rollback()
            self.session.refresh(self.session)
            await self.pre_process(obj, data, *args)

    async def post_process(self, obj, data, *args):
        del data["orm"]
        session: Session = data.get("session")

        if session:
            session.close()
