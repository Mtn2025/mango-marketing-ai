from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.configuration import ConfigurationService

router = APIRouter()
config_service = ConfigurationService()


class SaveConfigRequest(BaseModel):
    """Request para guardar configuración"""
    language: str = Field(default="es-MX", description="Idioma: es-MX, en")
    quality_level: str = Field(default="rapido", description="Nivel: rapido, profesional, elite")
    
    # LLM Provider
    llm_provider: Optional[str] = Field(None, description="Provider LLM: groq, google, azure")
    llm_model: Optional[str] = Field(None, description="Modelo LLM")
    llm_api_key: Optional[str] = Field(None, description="API key LLM (será encriptada)")
    
    # Image Provider
    image_provider: Optional[str] = Field(None, description="Provider imagen: google, azure")
    image_model: Optional[str] = Field(None, description="Modelo de imagen")
    image_api_key: Optional[str] = Field(None, description="API key imagen (será encriptada)")


class SaveConfigResponse(BaseModel):
    """Response con configuración guardada"""
    config_id: str
    message: str
    
    class Config:
        from_attributes = True


@router.post("/config", response_model=SaveConfigResponse)
async def save_configuration(
    request: SaveConfigRequest,
    db: Session = Depends(get_db)
):
    """
    Guarda configuración del usuario
    
    Las API keys son encriptadas antes de guardarse en la base de datos.
    
    ## Modo Simple (3 botones):
    ```json
    {
      "quality_level": "rapido",  // o "profesional", "elite"
      "llm_api_key": "tu_groq_key",
      "image_api_key": "tu_google_key"
    }
    ```
    
    ## Modo Avanzado (12 combinaciones):
    ```json
    {
      "llm_provider": "groq",
      "llm_model": "llama-4-scout",
      "llm_api_key": "tu_groq_key",
      "image_provider": "google",
      "image_model": "imagen-4-fast",
      "image_api_key": "tu_google_key"
    }
    ```
    """
    try:
        config = config_service.create_or_update_config(
            db=db,
            language=request.language,
            quality_level=request.quality_level,
            llm_provider=request.llm_provider,
            llm_model=request.llm_model,
            llm_api_key=request.llm_api_key,
            image_provider=request.image_provider,
            image_model=request.image_model,
            image_api_key=request.image_api_key,
        )
        
        return SaveConfigResponse(
            config_id=str(config.id),
            message="Configuración guardada exitosamente"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando configuración: {str(e)}")


@router.get("/config/{config_id}")
async def get_configuration(
    config_id: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene configuración por ID
    
    Nota: Las API keys NO son retornadas por seguridad
    """
    try:
        config = config_service.get_config(db, config_id)
        
        if not config:
            raise HTTPException(status_code=404, detail="Configuración no encontrada")
        
        # Retornar config sin API keys
        return {
            "config_id": str(config.id),
            "language": config.language,
            "quality_level": config.quality_level.value,
            "llm_provider": config.llm_provider,
            "llm_model": config.llm_model,
            "image_provider": config.image_provider,
            "image_model": config.image_model,
            "created_at": config.created_at,
            "updated_at": config.updated_at,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
