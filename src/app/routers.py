from app.internal.categories.presentation.routers import router as categories_router
from app.internal.benefits.presentation.routers import router as benefits_router
from app.internal.users.presentation.routers import router as users_router

all_routers = [
    categories_router,
    benefits_router,
    users_router,
]
