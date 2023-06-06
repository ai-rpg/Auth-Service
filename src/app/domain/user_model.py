
import uuid
from dataclasses import dataclass, field

@dataclass
class UserModel:
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
