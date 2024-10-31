from datetime import datetime
from pydantic import BaseModel


class TokenSchemaAdd(BaseModel):
    jti: str
    user_id: int


class TokenSchemaUpdate(BaseModel):
    revoked: bool


class TokenSchema(TokenSchemaAdd):
    created_at: datetime
    revoked: bool


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str
