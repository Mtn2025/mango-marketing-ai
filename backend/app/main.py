from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import copy, config, products, history, images, export

app = FastAPI(
    title="Mango Marketing AI",
    description="Sistema de automatización de marketing con IA",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mango.ubrokers.mx"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(copy.router, prefix="/api", tags=["copy"])
app.include_router(config.router, prefix="/api", tags=["config"])
app.include_router(products.router, prefix="/api", tags=["products"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(images.router, prefix="/api", tags=["images"])
app.include_router(export.router, prefix="/api", tags=["export"])

@app.get("/")
async def root():
    return {
        "message": "Mango Marketing AI API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "save_config": "/api/config",
            "generate_copy": "/api/generate/copy",
            "generate_image": "/api/generate/image",
            "products": "/api/products",
            "history": "/api/history",
            "export_zip": "/api/export/zip",
            "share_urls": "/api/export/share-urls"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
