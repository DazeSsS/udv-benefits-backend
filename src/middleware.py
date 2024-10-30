from jwt import InvalidTokenError
from fastapi import Request, HTTPException, status
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings

from app.internal.auth.domain.services import AuthService


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if settings.PUBLIC_API:
            response = await call_next(request)
            return response

        if request.url.path not in ["/docs", "/redoc", "/openapi.json"]:
            auth_header = request.headers.get("Authorization")
            if auth_header:
                try:
                    token = auth_header.split()[1]
                    payload = AuthService.get_payload(token)
                    request.state.user_id = payload.get('id')
                    request.state.role = payload.get('role')
                except InvalidTokenError:
                    return Response(content="Invalid or expired token", status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(content="Authorization header missing", status_code=status.HTTP_401_UNAUTHORIZED)

        response = await call_next(request)
        return response