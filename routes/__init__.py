from fastapi import APIRouter
from .embedding_routes import router as embedding_router
from .chat_routes import router as chat_router

# Combine all routers
router = APIRouter()
router.include_router(embedding_router)
router.include_router(chat_router)

__all__ = ["router"]

