from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.services.history import HistoryService

router = APIRouter()
history_service = HistoryService()


class GenerationSummary(BaseModel):
    """Resumen de una generación"""
    id: str
    product_id: Optional[str]
    platforms: Optional[List[str]]
    quality_level: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class HistoryEntry(BaseModel):
    """Entrada de historial"""
    id: str
    action: str
    metadata: Optional[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/history", response_model=List[GenerationSummary])
async def get_recent_history(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Obtiene las generaciones más recientes
    
    Retorna un resumen de las últimas generaciones para mostrar en el historial.
    """
    try:
        generations = history_service.get_recent_generations(db, limit)
        
        return [
            GenerationSummary(
                id=str(g.id),
                product_id=str(g.product_id) if g.product_id else None,
                platforms=g.platforms,
                quality_level=g.quality_level.value if g.quality_level else None,
                created_at=g.created_at,
            )
            for g in generations
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{generation_id}", response_model=List[HistoryEntry])
async def get_generation_history(
    generation_id: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial completo de una generación específica
    
    Muestra todas las acciones realizadas sobre una generación
    (generada, editada, regenerada, exportada, etc.)
    """
    try:
        # Verificar que la generación existe
        generation = history_service.get_generation(db, generation_id)
        if not generation:
            raise HTTPException(status_code=404, detail="Generación no encontrada")
        
        history = history_service.get_generation_history(db, generation_id)
        
        return [
            HistoryEntry(
                id=str(h.id),
                action=h.action,
                metadata=h.metadata,
                created_at=h.created_at,
            )
            for h in history
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history/{generation_id}/regenerate")
async def regenerate_content(
    generation_id: str,
    db: Session = Depends(get_db)
):
    """
    Regenera el contenido de una generación
    
    Crea una nueva generación basada en los parámetros de una anterior.
    """
    try:
        # Obtener generación original
        original = history_service.get_generation(db, generation_id)
        if not original:
            raise HTTPException(status_code=404, detail="Generación no encontrada")
        
        # TODO: Implementar lógica de regeneración
        # Por ahora solo registramos la acción
        history_service.create_history_entry(
            db=db,
            generation_id=generation_id,
            action="regenerate_requested",
            metadata={"timestamp": datetime.utcnow().isoformat()}
        )
        
        return {
            "message": "Regeneración solicitada",
            "original_id": str(generation_id),
            "note": "Funcionalidad completa pendiente de implementación"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
