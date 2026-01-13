from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from io import BytesIO

from app.services.export import ExportService

router = APIRouter()
export_service = ExportService()


class ExportRequest(BaseModel):
    """Request para exportar contenido"""
    copy_data: Dict[str, str] = Field(..., description="Copy por plataforma")
    product_name: str = Field(..., description="Nombre del producto")
    platforms: List[str] = Field(..., description="Plataformas incluidas")
    include_hashtags: bool = Field(default=True, description="Incluir hashtags")
    hashtags: Optional[List[str]] = Field(None, description="Lista de hashtags")


class ShareURLsResponse(BaseModel):
    """Response con URLs para compartir"""
    urls: Dict[str, str]


@router.post("/export/zip")
async def export_zip_package(request: ExportRequest):
    """
    Exporta todo el contenido en un archivo ZIP
    
    Del implementation_plan.md línea 613:
    "Exportar ZIP con imágenes + copy"
    
    ## Ejemplo de request:
    ```json
    {
      "copy_data": {
        "instagram": "Copy para Instagram...",
        "facebook": "Copy para Facebook..."
      },
      "product_name": "Café Artesanal",
      "platforms": ["instagram", "facebook"],
      "include_hashtags": true,
      "hashtags": ["cafe", "artesanal", "organico"]
    }
    ```
    
    Returns: Archivo ZIP descargable
    """
    try:
        # Por ahora solo exportamos copy (imágenes en fase 2)
        zip_bytes = await export_service.create_export_package(
            copy_data=request.copy_data,
            images={},  # TODO: Agregar imágenes cuando estén funcionando
            product_name=request.product_name,
            metadata={
                "platforms": request.platforms,
                "hashtags": request.hashtags
            }
        )
        
        # Retornar como descarga
        return StreamingResponse(
            BytesIO(zip_bytes),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename={request.product_name.replace(' ', '_')}_export.zip"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/share-urls", response_model=ShareURLsResponse)
async def generate_share_urls(
    platform: str,
    copy_text: str
):
    """
    Genera URLs para compartir directo en redes sociales
    
    Pre-pobladas con el copy generado para facilitar compartir.
    
    ## Plataformas soportadas:
    - facebook
    - twitter (X)
    - linkedin
    - whatsapp
    """
    try:
        urls = export_service.generate_share_urls(copy_text, platform)
        
        if not urls:
            raise HTTPException(
                status_code=400,
                detail=f"Plataforma '{platform}' no soportada para share URLs"
            )
        
        return ShareURLsResponse(urls=urls)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/clipboard-format")
async def format_for_clipboard(
    copy_text: str,
    include_hashtags: bool = True,
    hashtags: Optional[List[str]] = None
):
    """
    Formatea copy para copiar al portapapeles
    
    Del implementation_plan.md línea 614:
    "Copiar copy al portapapeles"
    """
    try:
        formatted = export_service.format_for_clipboard(
            copy_text=copy_text,
            include_hashtags=include_hashtags,
            hashtags=hashtags or []
        )
        
        return {
            "formatted_text": formatted,
            "length": len(formatted),
            "note": "Texto listo para copiar al portapapeles"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
