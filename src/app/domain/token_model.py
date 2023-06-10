from dataclasses import dataclass


@dataclass
class TokenModel:
    access_token: str
    token_type: str
