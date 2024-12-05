from fastapi import APIRouter

from app.internal.auth.presentation.routers import router as auth_router
from app.internal.benefits.presentation.routers import router as benefits_router
from app.internal.categories.presentation.routers import router as categories_router
from app.internal.orders.presentation.routers import router as orders_router
from app.internal.statistics.presentation.routers import router as statistics_router
from app.internal.users.presentation.routers import router as users_router

api_router = APIRouter(
    prefix='/api',
)

api_router.include_router(auth_router)
api_router.include_router(benefits_router)
api_router.include_router(categories_router)
api_router.include_router(orders_router)
api_router.include_router(statistics_router)
api_router.include_router(users_router)
