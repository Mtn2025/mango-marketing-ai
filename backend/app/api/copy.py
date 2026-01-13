from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from app.services.copy_generator import CopyGeneratorService

router = APIRouter()
copy_service = CopyGeneratorService()


class GenerateCopyRequest(BaseModel):
    """Request para generar copy"""
    # Producto
    product_name: str = Field(..., description="Nombre del producto/servicio")
    description: str = Field(..., description="Descripción del producto")
    
    # Configuración
    platform: str = Field(..., description="Plataforma: facebook, instagram, tiktok, linkedin, whatsapp")
    language: str = Field(default="es-MX", description="Idioma: es-MX, en")
    quality_level: str = Field(default="rapido", description="Nivel de calidad: rapido, profesional, elite")
    
    # Provider (temporal - luego vendrá de config de usuario)
    api_key: str = Field(..., description="API key del provider (temporal)")
    llm_provider: str = Field(default="groq", description="Provider: groq, google, azure")
    llm_model: str = Field(default="llama-4-scout", description="Modelo a usar")
    
    # Copy config
    tone: str = Field(default="casual", description="Tono: casual, formal, juvenil, profesional")
    length: str = Field(default="medio", description="Longitud: corto, medio, largo")
    use_emojis: bool = Field(default=False, description="Incluir emojis")
    cta: Optional[str] = Field(None, description="Call to action personalizado")
    benefits: Optional[List[str]] = Field(None, description="Beneficios clave (máx 3)")
    keywords: Optional[List[str]] = Field(None, description="Palabras clave (máx 5)")
    
    # Generation params
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Creatividad del modelo")


class GenerateCopyResponse(BaseModel):
    """Response con el copy generado"""
    copy_text: str
    metadata: dict


@router.post("/generate/copy", response_model=GenerateCopyResponse)
async def generate_copy(request: GenerateCopyRequest):
    """
    Genera copy de marketing para una plataforma específica
    
    ## Ejemplo de uso:
    ```json
    {
      "product_name": "Café Artesanal Oaxaqueño",
      "description": "Café de altura cultivado en las montañas de Oaxaca",
      "platform": "instagram",
      "language": "es-MX",
      "api_key": "tu_groq_api_key",
      "tone": "casual",
      "use_emojis": true,
      "benefits": ["100% orgánico", "Sabor único", "Apoya a productores locales"]
    }
    ```
    """
    try:
        result = await copy_service.generate_copy(
            # Producto
            product_name=request.product_name,
            description=request.description,
            # Config
            platform=request.platform,
            language=request.language,
            quality_level=request.quality_level,
            # Provider
            llm_provider=request.llm_provider,
            llm_model=request.llm_model,
            api_key=request.api_key,
            # Copy config
            tone=request.tone,
            length=request.length,
            use_emojis=request.use_emojis,
            cta=request.cta,
            benefits=request.benefits,
            keywords=request.keywords,
            # Generation
            temperature=request.temperature
        )
        
        return GenerateCopyResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check del servicio de generación"""
    return {
        "status": "healthy",
        "service": "copy_generator",
        "providers": ["groq", "google"]
    }
