"""DjÊ Backend – FastAPI entry point."""
from fastapi import FastAPI

from app.routes import whatsapp as whatsapp_router

app = FastAPI(
    title="DjÊ Backend",
    description="WhatsApp-based AI financial assistant API",
    version="1.0.0",
)

app.include_router(whatsapp_router.router)


@app.get("/")
async def root():
    return {"service": "DjÊ", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
