from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import Configuration, QualityLevel
from app.services.encryption import encryption_service
import uuid


class ConfigurationService:
    """
    Servicio para manejar configuraciones de usuario
    """
    
    def create_or_update_config(
        self,
        db: Session,
        user_id: Optional[str] = None,  # Para futuras versiones con auth
        language: str = "es-MX",
        quality_level: str = "rapido",
        # LLM config
        llm_provider: Optional[str] = None,
        llm_model: Optional[str] = None,
        llm_api_key: Optional[str] = None,
        # Image config
        image_provider: Optional[str] = None,
        image_model: Optional[str] = None,
        image_api_key: Optional[str] = None,
    ) -> Configuration:
        """
        Crea o actualiza configuración
        
        Por ahora creamos una nueva cada vez (sin auth)
        En el futuro, con auth, actualizaremos la del usuario
        """
        
        # Encriptar API keys si existen
        llm_api_key_encrypted = None
        if llm_api_key:
            llm_api_key_encrypted = encryption_service.encrypt(llm_api_key)
        
        image_api_key_encrypted = None
        if image_api_key:
            image_api_key_encrypted = encryption_service.encrypt(image_api_key)
        
        # Crear nueva configuración
        config = Configuration(
            id=uuid.uuid4(),
            language=language,
            quality_level=QualityLevel[quality_level.upper()],
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_api_key_encrypted=llm_api_key_encrypted,
            image_provider=image_provider,
            image_model=image_model,
            image_api_key_encrypted=image_api_key_encrypted,
        )
        
        db.add(config)
        db.commit()
        db.refresh(config)
        
        return config
    
    def get_config(self, db: Session, config_id: str) -> Optional[Configuration]:
        """
        Obtiene una configuración por ID
        """
        return db.query(Configuration).filter(Configuration.id == config_id).first()
    
    def get_decrypted_api_key(self, config: Configuration, key_type: str) -> Optional[str]:
        """
        Obtiene API key desencriptada
        
        Args:
            config: Configuración
            key_type: 'llm' o 'image'
            
        Returns:
            str: API key desencriptada o None
        """
        if key_type == 'llm' and config.llm_api_key_encrypted:
            return encryption_service.decrypt(config.llm_api_key_encrypted)
        elif key_type == 'image' and config.image_api_key_encrypted:
            return encryption_service.decrypt(config.image_api_key_encrypted)
        
        return None
