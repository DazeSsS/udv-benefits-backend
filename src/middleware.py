from jwt import InvalidTokenError
from fastapi import Request, HTTPException, status
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings

from app.internal.auth.domain.services import AuthService


class BearerTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.token = None

        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split()[1]
                request.state.token = token
            except Exception:
                pass

        response = await call_next(request)
        return response