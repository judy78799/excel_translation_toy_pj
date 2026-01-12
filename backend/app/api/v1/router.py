from fastapi import APIRouter
from app.api.v1.endpoints import upload, translation

# FASTAPI 구조
# Create API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    upload.router,
    prefix="/upload",
    tags=["File Upload"]
)

api_router.include_router(
    translation.router,
    prefix="/translate",
    tags=["Translation"]
)

from app.api.v1.endpoints import dataset
api_router.include_router(
    dataset.router,
    prefix="/dataset",
    tags=["Dataset Generation"]
)
