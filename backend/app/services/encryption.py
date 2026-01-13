"""
Servicio de encriptación DESHABILITADO temporalmente
Para evitar problemas de deployment, simplemente retorna el texto sin encriptar
TODO: Re-habilitar cuando ENCRYPTION_KEY esté configurada correctamente
"""

class EncryptionService:
    """
    Servicio de encriptación (DESHABILITADO - modo pass-through)
    """
    
    def __init__(self):
        # NO inicializar cipher - modo pass-through
        pass
    
    def encrypt(self, text: str) -> str:
        """
        DESHABILITADO: Retorna el texto sin encriptar
        """
        return text if text else None
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        DESHABILITADO: Retorna el texto sin modificar
        """
        return encrypted_text if encrypted_text else None
    
    @staticmethod
    def generate_key() -> str:
        """
        Genera una clave (no se usa en modo pass-through)
        """
        return "ENCRYPTION_DISABLED"


# Instancia global del servicio
encryption_service = EncryptionService()

