from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models import History, Generation
import uuid


class HistoryService:
    """
    Servicio para manejar historial de generaciones
    """
    
    def create_history_entry(
        self,
        db: Session,
        generation_id: str,
        action: str,
        metadata: Optional[dict] = None,
    ) -> History:
        """
        Crea una entrada en el historial
        
        Args:
            generation_id: ID de la generación
            action: Tipo de acción (generated, edited, regenerated, exported)
            metadata: Metadata adicional
        """
        history = History(
            id=uuid.uuid4(),
            generation_id=generation_id,
            action=action,
            metadata=metadata,
        )
        
        db.add(history)
        db.commit()
        db.refresh(history)
        
        return history
    
    def get_generation_history(
        self,
        db: Session,
        generation_id: str
    ) -> List[History]:
        """
        Obtiene todo el historial de una generación
        """
        return db.query(History)\
            .filter(History.generation_id == generation_id)\
            .order_by(History.created_at.asc())\
            .all()
    
    def get_recent_generations(
        self,
        db: Session,
        limit: int = 20
    ) -> List[Generation]:
        """
        Obtiene las generaciones más recientes
        """
        return db.query(Generation)\
            .order_by(Generation.created_at.desc())\
            .limit(limit)\
            .all()
    
    def get_generation(
        self,
        db: Session,
        generation_id: str
    ) -> Optional[Generation]:
        """
        Obtiene una generación por ID
        """
        return db.query(Generation)\
            .filter(Generation.id == generation_id)\
            .first()
