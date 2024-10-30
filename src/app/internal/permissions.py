from fastapi import Depends, HTTPException, Request

from config import settings

from app.internal.users.db.models import Position


def admin_permission(request: Request):
    if not settings.PUBLIC_API:
        if request.state.role != Position.hr.value:
            raise HTTPException(status_code=403, detail='Admin permissions required')
