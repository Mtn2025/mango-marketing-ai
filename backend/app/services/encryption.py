from cryptography.fernet import Fernet
from app.core.config import settings


class EncryptionService:
    """
    Servicio para encriptar/desencriptar API keys de usuarios
    Usa Fernet (symmetric encryption) de cryptography
    """
    
    def __init__(self):
        # La clave debe ser de 32 bytes en base64
        # En producción viene de settings.ENCRYPTION_KEY
        self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())
    
    def encrypt(self, text: str) -> str:
        """
        Encripta un texto (API key)
        
        Args:
            text: Texto plano a encriptar
            
        Returns:
            str: Texto encriptado en base64
        """
        if not text:
            return None
        
        encrypted_bytes = self.cipher.encrypt(text.encode())
        return encrypted_bytes.decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Desencripta un texto
        
        Args:
            encrypted_text: Texto encriptado
            
        Returns:
            str: Texto desencriptado
        """
        if not encrypted_text:
            return None
        
        decrypted_bytes = self.cipher.decrypt(encrypted_text.encode())
        return decrypted_bytes.decode()
    
    @staticmethod
    def generate_key() -> str:
        """
        Genera una nueva clave de encriptación
        Útil para setup inicial
        
        Returns:
            str: Clave de encriptación en base64
        """
        return Fernet.generate_key().decode()


# Instancia global del servicio
encryption_service = EncryptionService()
