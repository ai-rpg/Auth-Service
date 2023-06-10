import uuid
from dataclasses import dataclass, field


@dataclass
class CreateUserModel:
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False
