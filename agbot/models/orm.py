from dataclasses import dataclass

from agbot.services.orm import User


@dataclass
class Orm:
    user: User = User
