from dataclasses import dataclass
from typing import TYPE_CHECKING

@dataclass
class UserModel:
    Username: str = ""
    password: str = ""
    email: str = ""