from datetime import datetime

from app.schema import BaseSchema


class TokenSchemaAdd(BaseSchema):
    jti: str
    user_id: int


class TokenSchemaUpdate(BaseSchema):
    revoked: bool


class TokenSchema(TokenSchemaAdd):
    created_at: datetime
    revoked: bool


class TokenPairSchema(BaseSchema):
    access_token: str
    refresh_token: str
