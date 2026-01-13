from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="Mango Marketing AI",
    description="Sistema de automatización de marketing con IA",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Mango Marketing AI API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# TODO: Import and include routers
# from app.api.endpoints import config, copy, images
# app.include_router(config.router, prefix="/api/config", tags=["config"])
# app.include_router(copy.router, prefix="/api/copy", tags=["copy"])
# app.include_router(images.router, prefix="/api/images", tags=["images"])
