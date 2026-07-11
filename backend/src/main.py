from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.item.routers import router as item_router
from config import settings


app = FastAPI(
    root_path="/api",
    docs_url=settings.DOCS_URL_ENABLED,
    redoc_url=settings.REDOC_URL_ENABLED,
    openapi_url=settings.OPENAPI_URL_ENABLED,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["OPTIONS", "POST", "GET", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(item_router)
